#!/usr/bin/env python3
"""
Tenant snapshot helper for the CS Admin CLI Advanced Kit.

Pulls your Gainsight tenant's configuration through the `gs-admin` CLI and turns
it into small, searchable index files that Claude can use. Python standard library only.

READ-ONLY BY CONSTRUCTION: every CLI call goes through `gs()`, which refuses
any command not listed in READ_COMMANDS below. Read that list before you run this.

Usage (from the kit folder):
  python3 scripts/snapshot.py pull  [all|objects|bi|picklists|rules|reports|scorecards|journey|integrations]
  python3 scripts/snapshot.py index
  python3 scripts/snapshot.py report-candidates
  python3 scripts/snapshot.py exemplar <reportId> [<reportId> ...]
  python3 scripts/snapshot.py status

Output goes to ./tenants/<tenant>/  (tenant = first part of your base URL host).
"""
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The ONLY commands this script will ever run. All are reads.
READ_COMMANDS = {
    ("whoami",),
    ("data-management", "objects", "list"),
    ("data-management", "objects", "describe"),
    ("data-management", "dropdowns", "list"),
    ("data-management", "dropdowns", "describe"),
    ("report", "list"),
    ("report", "list-objects"),
    ("report", "describe"),
    ("report", "run"),          # ad-hoc execution: returns rows, saves nothing
    ("query", "execute"),
    ("journey", "cta", "options"),
    ("journey", "programs", "list"),
    ("journey", "email", "templates"),
    ("journey", "surveys", "list"),
    ("rules-engine", "rules", "list"),
    ("rules-engine", "rules", "list-external-actions"),
    ("rules-engine", "chains", "list"),
    ("scorecard", "list"),
    ("scorecard", "measure", "list"),
    ("scorecard", "measure-group", "list"),
    ("scorecard", "scheme", "list"),
    ("connectors", "list"),
    ("data-designer", "templates", "list"),
}

DEAD_NAME = re.compile(r"\b(dnu|do not use|copy of|test|poc|old|deprecated|mig|backup|temp)\b", re.I)


class AuthExpired(Exception):
    pass


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gs(*args, json_out=True):
    """Run an allow-listed gs-admin read command and return parsed JSON (or text)."""
    if not any(tuple(args[: len(c)]) == c for c in READ_COMMANDS):
        raise SystemExit(f"REFUSED (not a read command in the allow-list): gs-admin {' '.join(args)}")
    cmd = ["gs-admin", *args] + (["--json"] if json_out else [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    if re.search(r"token.*(expired|invalid)|unauthori[sz]ed|run 'gs-admin login'", out, re.I) and args[0] != "whoami":
        raise AuthExpired(out.strip()[:300])
    if not json_out:
        return out
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"_error": out.strip()[:1000], "_cmd": " ".join(cmd)}


# ---------- paths / manifest ----------

def tenant_dir():
    who = gs("whoami", json_out=False)
    m = re.search(r"Base URL:\s*(\S+)", who)
    if not m:
        raise SystemExit("Could not read Base URL from `gs-admin whoami`. Run `gs-admin login` first.")
    if not re.search(r"Token:\s*valid", who):
        raise SystemExit("`gs-admin whoami` does not show a valid token. Run `gs-admin login` and retry.")
    url = m.group(1).rstrip("/")
    slug = re.sub(r"^https?://", "", url).split(".")[0]
    d = os.path.join(KIT_ROOT, "tenants", slug)
    os.makedirs(os.path.join(d, "raw"), exist_ok=True)
    return d, url


def load_manifest(d):
    p = os.path.join(d, "manifest.json")
    return json.load(open(p)) if os.path.exists(p) else {"sections": {}}


def save_manifest(d, m):
    json.dump(m, open(os.path.join(d, "manifest.json"), "w"), indent=2)


def mark(d, section, **info):
    m = load_manifest(d)
    m["sections"][section] = {"pulled_at": now(), **info}
    save_manifest(d, m)


def save(d, rel, obj):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, "w"), indent=1, default=str)
    return p


def write_tsv(d, rel, header, rows):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    clean = lambda v: "" if v is None else str(v).replace("\t", " ").replace("\n", " ")
    with open(p, "w") as f:
        f.write("\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(clean(v) for v in r) + "\n")
    return len(rows)


# ---------- response parsing (CLI output shapes are NOT uniform) ----------

def records_and_total(resp):
    """Find the record list and total count in any of the CLI's envelope shapes."""
    if isinstance(resp, list):
        return resp, None
    if not isinstance(resp, dict):
        return [], None
    data = resp.get("data", resp)
    if isinstance(data, list):
        return data, None
    if not isinstance(data, dict):
        return [], None
    total = (data.get("pageInfo") or {}).get("totalRecords")
    for k in ("totalRecords", "totalNumberOfObjects", "totalSize", "total"):
        total = total if total is not None else data.get(k)
    for k in ("data", "liteObjects", "picklistList", "records", "content", "programs", "items"):
        if isinstance(data.get(k), list):
            return data[k], total
    for v in data.values():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v, total
    return [], total


def paged(args, limit=200, page_flag="--page", limit_flag="--limit", max_pages=200):
    """Page through a list command until we have `total` records (or a page comes back empty)."""
    out, total, page = [], None, 1
    while page <= max_pages:
        resp = gs(*args, limit_flag, str(limit), page_flag, str(page))
        recs, t = records_and_total(resp)
        if isinstance(resp, dict) and resp.get("_error") and not recs:
            if page == 1:
                return out, None, resp["_error"]
            break
        total = t if t is not None else total
        if not recs:
            break
        out.extend(recs)
        if total is not None and len(out) >= int(total):
            break
        if total is None and len(recs) < limit:
            break
        page += 1
    return out, total, None


# ---------- pull sections ----------

def pull_objects(d):
    objs, total, err = paged(["data-management", "objects", "list"], limit=200, limit_flag="--size")
    if err:
        print("  objects list failed:", err[:200]); return
    save(d, "raw/objects_list.json", objs)
    names = [o["name"] for o in objs]
    print(f"  {len(names)} objects listed (total reported {total}); describing each (parallel)...")
    os.makedirs(os.path.join(d, "raw", "objects"), exist_ok=True)

    def one(n):
        r = gs("data-management", "objects", "describe", "--name", n)
        if isinstance(r, dict) and r.get("data"):
            save(d, f"raw/objects/{safe(n)}.json", r["data"])
            return n, None
        return n, (r.get("_error") if isinstance(r, dict) else "unknown")[:200]

    fails = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for i, (n, e) in enumerate(ex.map(one, names), 1):
            if e:
                fails.append((n, e))
            if i % 50 == 0:
                print(f"    described {i}/{len(names)}")
    mark(d, "objects", count=len(names), described=len(names) - len(fails), failed=[f[0] for f in fails][:50],
         command="gs-admin data-management objects list --size 200 --page N; data-management objects describe --name <obj>")
    print(f"  done. {len(fails)} describe failures." if fails else "  done.")


def pull_bi(d):
    r = gs("report", "list-objects")
    recs, _ = records_and_total(r)
    save(d, "raw/bi_objects.json", recs)
    mark(d, "bi", count=len(recs), command="gs-admin report list-objects")
    print(f"  {len(recs)} BI (report) objects")


def pull_picklists(d):
    sel = "Name,Category,IsActive,Deleted,EntityType,DisplayOrder,CtaType,SpType"
    r = gs("query", "execute", "--object", "da_picklist", "--select", sel, "--limit", "5000")
    recs, _ = records_and_total(r)
    save(d, "raw/da_picklist.json", recs)
    cats, total, err = paged(["data-management", "dropdowns", "list"], limit=100)

    def values(cat):  # the list call returns categories only; values need a describe per category
        r = gs("data-management", "dropdowns", "describe", "--id", g(cat, "categoryDetails", "gsid", default=""))
        cat["childItems"] = g(r, "data", "childItems", default=[]) if isinstance(r, dict) else []
        return cat

    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        dd = list(ex.map(values, cats))
    save(d, "raw/dropdowns.json", dd)
    cta = gs("journey", "cta", "options")
    save(d, "raw/cta_options.json", cta)
    mark(d, "picklists", da_picklist=len(recs), dropdown_categories=len(dd),
         command=f"query execute --object da_picklist --select {sel}; data-management dropdowns list; journey cta options")
    print(f"  da_picklist {len(recs)} items, {len(dd)} dropdown categories, cta options saved")


def pull_rules(d):
    rules, total, err = paged(["rules-engine", "rules", "list"], limit=200)
    save(d, "raw/rules.json", rules)
    chains, _, _ = paged(["rules-engine", "chains", "list"], limit=100)
    save(d, "raw/rule_chains.json", chains)
    mark(d, "rules", count=len(rules), total_reported=total, chains=len(chains),
         command="rules-engine rules list --limit 200 --page N; rules-engine chains list")
    flag = "" if total is None or len(rules) == int(total) else f"  WARNING: got {len(rules)} of {total}"
    print(f"  {len(rules)} rules (reported {total}), {len(chains)} chains{flag}")


def pull_reports(d):
    reps, total, err = paged(["report", "list"], limit=200)
    save(d, "raw/reports.json", reps)
    mark(d, "reports", count=len(reps), total_reported=total, command="report list --limit 200 --page N")
    print(f"  {len(reps)} reports (reported {total})")


def pull_scorecards(d):
    out = {}
    for key, args in [("scorecards", ["scorecard", "list"]), ("measures", ["scorecard", "measure", "list"]),
                      ("measure_groups", ["scorecard", "measure-group", "list"])]:
        recs, _, _ = paged(args, limit=200)
        out[key] = recs
    out["schemes"] = records_and_total(gs("scorecard", "scheme", "list"))[0]
    save(d, "raw/scorecards.json", out)
    mark(d, "scorecards", **{k: len(v) for k, v in out.items()}, command="scorecard list / measure list / measure-group list / scheme list")
    print("  " + ", ".join(f"{len(v)} {k}" for k, v in out.items()))


def pull_journey(d):
    progs, total, _ = paged(["journey", "programs", "list"], limit=100)
    save(d, "raw/jo_programs.json", progs)
    tpl = records_and_total(gs("journey", "email", "templates", "--limit", "1000"))[0]
    save(d, "raw/email_templates.json", tpl)
    sv = records_and_total(gs("journey", "surveys", "list"))[0]
    save(d, "raw/surveys.json", sv)
    mark(d, "journey", programs=len(progs), email_templates=len(tpl), surveys=len(sv),
         command="journey programs list; journey email templates; journey surveys list")
    print(f"  {len(progs)} JO programs, {len(tpl)} email templates, {len(sv)} surveys")


def pull_integrations(d):
    con, _, _ = paged(["connectors", "list"], limit=100)
    dd = records_and_total(gs("data-designer", "templates", "list", "--limit", "1000"))[0]
    ext = records_and_total(gs("rules-engine", "rules", "list-external-actions", "--limit", "1000"))[0]
    save(d, "raw/integrations.json", {"connectors": con, "data_designer_templates": dd, "external_actions": ext})
    mark(d, "integrations", connectors=len(con), data_designer_templates=len(dd), external_actions=len(ext),
         command="connectors list; data-designer templates list; rules-engine rules list-external-actions")
    print(f"  {len(con)} connectors, {len(dd)} data designer templates, {len(ext)} external actions")


SECTIONS = {
    "objects": pull_objects, "bi": pull_bi, "picklists": pull_picklists, "rules": pull_rules,
    "reports": pull_reports, "scorecards": pull_scorecards, "journey": pull_journey, "integrations": pull_integrations,
}


# ---------- index: raw -> small searchable files ----------

def safe(name):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)


def rd(d, rel, default=None):
    p = os.path.join(d, rel)
    return json.load(open(p)) if os.path.exists(p) else default


def g(o, *path, default=None):
    for k in path:
        if not isinstance(o, dict):
            return default
        o = o.get(k)
    return default if o is None else o


def index(d):
    counts = {}
    # BI names (used by `report run/create --object`) joined to data-management names via dbName
    bi = rd(d, "raw/bi_objects.json", [])
    bi_by_db = {b.get("dbName"): b.get("objectName") for b in bi}

    # Objects + fields + lookups
    lite = rd(d, "raw/objects_list.json", [])
    obj_rows, field_rows, lookup_rows = [], [], []
    os.makedirs(os.path.join(d, "schema", "objects"), exist_ok=True)
    for o in lite:
        name = o["name"]
        desc = rd(d, f"raw/objects/{safe(name)}.json")
        cols = (desc or {}).get("columns") or []
        bi_name = bi_by_db.get(o.get("dbCollectionName")) or bi_by_db.get((desc or {}).get("dbName")) or ""
        dead = "dead-name" if DEAD_NAME.search(name + " " + (o.get("label") or "")) else ""
        obj_rows.append([name, o.get("label"), o.get("group"), bi_name, o.get("recordCount"), len(cols), dead])
        md = [f"# {o.get('label')} (`{name}`)", "",
              f"- group: {o.get('group')} | report/BI name: `{bi_name or '?'}` | records: {o.get('recordCount')}",
              f"- source: `gs-admin data-management objects describe --name {name}` (raw: raw/objects/{safe(name)}.json)", "",
              "| field | label | type | picklist category | lookup → | flags |", "|---|---|---|---|---|---|"]
        for c in cols:
            lk = ""
            if c.get("lookupDetails"):
                l0 = c["lookupDetails"][0]
                lk = f"{l0.get('objectName')}.{l0.get('columnName')}"
                lookup_rows.append([name, c["name"], c.get("label"), l0.get("objectName"), l0.get("columnName"),
                                    g(l0, "namedField", "columnName")])
            flags = ",".join(f for f, on in [("hidden", c.get("hidden")), ("formula", c.get("gdmFormulaColumn")),
                                             ("required", c.get("required")), ("custom", c.get("group") == "CUSTOM"),
                                             ("readonly", c.get("updateable") is False)] if on)
            pk = c.get("_dropdownCategory") or g(c, "properties", "PICKLIST_CATEGORY", default="")
            field_rows.append([name, c["name"], c.get("label"), c.get("type"), pk, lk, flags])
            md.append(f"| `{c['name']}` | {c.get('label')} | {c.get('type')} | {pk} | {lk} | {flags} |")
        if desc:
            open(os.path.join(d, "schema", "objects", f"{safe(name)}.md"), "w").write("\n".join(md) + "\n")
    counts["objects"] = write_tsv(d, "schema/_object_index.tsv",
                                  ["object", "label", "group", "bi_name", "records", "fields", "dead_signal"], obj_rows)
    counts["fields"] = write_tsv(d, "schema/_field_index.tsv",
                                 ["object", "field", "label", "type", "picklist_category", "lookup_to", "flags"], field_rows)
    counts["lookups"] = write_tsv(d, "schema/_lookup_index.tsv",
                                  ["object", "lookup_field", "label", "to_object", "to_key", "to_named_field"], lookup_rows)

    # Picklists
    dap = rd(d, "raw/da_picklist.json", [])
    counts["da_picklist"] = write_tsv(d, "config/da_picklist.tsv",
        ["category", "name", "live", "entity_type", "cta_type", "sp_type", "display_order"],
        [[p.get("Category"), p.get("Name"), bool(p.get("IsActive")) and not p.get("Deleted"), p.get("EntityType"),
          p.get("CtaType"), p.get("SpType"), p.get("DisplayOrder")] for p in dap])
    dd_rows = []
    for cat in rd(d, "raw/dropdowns.json", []):
        cd = cat.get("categoryDetails") or {}
        for it in cat.get("childItems") or [{}]:
            dd_rows.append([cd.get("name"), cd.get("gsid"), it.get("name"), it.get("systemName"), it.get("gsid"),
                            it.get("active"), it.get("deleted")])
    counts["dropdown_values"] = write_tsv(d, "config/dropdowns.tsv",
        ["category", "category_gsid", "value", "value_system_name", "value_gsid", "active", "deleted"], dd_rows)

    # Rules
    rules = rd(d, "raw/rules.json", [])
    counts["rules"] = write_tsv(d, "config/rules.tsv",
        ["rule_id", "name", "active", "live", "entity_type", "rule_type", "source_type", "folder_id", "entities",
         "last_run_result", "description"],
        [[r.get("ruleId") or r.get("id"), r.get("ruleName"), r.get("active"),
          bool(r.get("active")) and not DEAD_NAME.search(r.get("ruleName") or ""), r.get("entityType"), r.get("ruleType"),
          r.get("sourceType"), r.get("folderId"), json.dumps(r.get("entities"))[:200] if r.get("entities") else "",
          r.get("lastRunResult"), (r.get("description") or "")[:200]] for r in rules])

    # Reports (+ a "pattern" signature used to pick exemplars)
    reps = rd(d, "raw/reports.json", [])
    rrows = []
    for r in reps:
        sf, gb = r.get("showFields") or [], r.get("groupByFields") or []
        lookups = sum(1 for f in sf + gb if isinstance(f, dict) and f.get("fieldPath"))
        aggs = sorted({g(f, "expressionDetails", "expression", "key") for f in sf if g(f, "expressionDetails", "expression", "key")})
        pivot = any(f.get("pivoted") for f in gb if isinstance(f, dict))
        sig = f"{r.get('reportDisplayType')}|gb{min(len(gb), 2)}|{'lookup' if lookups else 'nolookup'}|{'pivot' if pivot else ''}"
        rrows.append([r.get("reportId"), r.get("reportName"), r.get("objectName"), r.get("reportDisplayType"), len(sf),
                      len(gb), lookups, ",".join(aggs), pivot, sig,
                      "dead-name" if DEAD_NAME.search(r.get("reportName") or "") else ""])
    counts["reports"] = write_tsv(d, "config/reports.tsv",
        ["report_id", "name", "object", "display_type", "n_show", "n_groupby", "n_lookup_fields", "aggregations",
         "pivot", "pattern", "dead_signal"], rrows)

    # Scorecards
    sc = rd(d, "raw/scorecards.json", {})
    counts["scorecards"] = write_tsv(d, "config/scorecards.tsv", ["id", "name", "active", "entity_type", "scheme_id"],
        [[s.get("id"), s.get("name"), s.get("active"), s.get("entityType"), s.get("schemeId")]
         for s in sc.get("scorecards", [])])
    counts["measures"] = write_tsv(d, "config/measures.tsv",
        ["id", "name", "level", "input_type", "scorecards_count", "live", "scorecards_used"],
        [[m.get("id"), m.get("name"), m.get("levelType"), m.get("inputType"), m.get("scorecardsCount"),
          (m.get("scorecardsCount") or 0) > 0 and not DEAD_NAME.search(m.get("name") or ""),
          m.get("_scorecardsUsed") or ""] for m in sc.get("measures", []) + sc.get("measure_groups", [])])

    # Journey
    jo = rd(d, "raw/jo_programs.json", [])
    counts["jo_programs"] = write_tsv(d, "config/jo_programs.tsv",
        ["id", "name", "status", "type", "model", "participant_source", "dead_signal"],
        [[p.get("advancedOutreachId") or p.get("gsid"), p.get("advancedOutreachName"), p.get("advancedOutreachStatus"),
          p.get("advancedOutreachType"), p.get("advancedOutreachModelName") or p.get("advancedOutreachModel"),
          p.get("participantSourceType"),
          "dead-name" if DEAD_NAME.search(p.get("advancedOutreachName") or "") else ""] for p in jo])

    m = load_manifest(d)
    m["indexed_at"] = now()
    m["index_counts"] = counts
    save_manifest(d, m)
    print("indexed:", ", ".join(f"{k}={v}" for k, v in counts.items()))


def report_candidates(d):
    """Print one or two candidate reports per pattern, so Claude can pick exemplars."""
    p = os.path.join(d, "config", "reports.tsv")
    if not os.path.exists(p):
        raise SystemExit("Run `pull reports` and `index` first.")
    rows = [l.rstrip("\n").split("\t") for l in open(p)][1:]
    by_pat = defaultdict(list)
    obj_freq = Counter(r[2] for r in rows)
    for r in rows:
        if not r[10]:  # skip dead-by-name
            by_pat[r[9]].append(r)
    print("pattern\tcount\tcandidate_report_id\tobject\tname")
    weak = re.compile(r"\b(demo|sample|example)\b", re.I)  # usable, but real reports teach conventions better
    for pat, rs in sorted(by_pat.items(), key=lambda kv: -len(kv[1])):
        rs.sort(key=lambda r: (bool(weak.search(r[1])), -obj_freq[r[2]], -int(r[4] or 0)))
        seen_obj = set()
        picks = []
        for r in rs:
            if r[2] not in seen_obj:
                picks.append(r); seen_obj.add(r[2])
            if len(picks) == 2:
                break
        for r in picks:
            print(f"{pat}\t{len(rs)}\t{r[0]}\t{r[2]}\t{r[1]}")
    print("\nmost-reported objects:", ", ".join(f"{o}({n})" for o, n in obj_freq.most_common(12)))


# ---------- exemplars: saved report (server JSON) -> verified CLI command ----------

def _path_to_hops(fp):
    """Server fieldPath {left: target, right: source lookup} (possibly nested) -> CLI hops, source first."""
    hops = []
    while isinstance(fp, dict) and fp.get("left") and fp.get("right"):
        hops.insert(0, {"through": fp["right"]["fieldName"], "to": fp["left"]["objectName"]})
        fp = fp["right"].get("fieldPath")
    return hops


def _field_spec(f, notes):
    spec = {}
    if f.get("fieldPath"):
        spec["fieldPath"] = {"hops": _path_to_hops(f["fieldPath"]), "leaf": f["fieldName"]}
    else:
        spec["name"] = f["fieldName"]
    ex = f.get("expressionDetails") or {}
    key = g(ex, "expression", "key")
    if ex.get("expressionType") == "aggregationFunction" and key:
        spec["aggregation"] = key
    elif key == "summarize":
        args = g(ex, "expression", "arguments", default=[])
        val = next((a.get("value") for a in args if a.get("tokenType") == "value"), None)
        if val:
            spec["summarize"] = str(val).capitalize()  # server may say WEEK; CLI accepts Day|Week|Month|Quarter|Year
    elif ex:
        notes.append(f"field `{f.get('fieldName')}` uses a {ex.get('expressionType')} expression (`{key}`) that was not translated")
    return spec


def translate_report(r):
    notes, flags = [], {"--object": g(r, "sourceDetails", "objectName"), "--display-type": r.get("reportDisplayType")}
    flags["--show-fields"] = [_field_spec(f, notes) for f in r.get("showFields") or []]
    gb = []
    for f in r.get("groupByFields") or []:
        s = _field_spec(f, notes)
        if f.get("pivoted") and r.get("reportDisplayType") == "GRID":  # CLI allows pivot only on GRID;
            s["pivoted"] = True                                         # stacked charts use the 2nd group-by as series
        gb.append(s)
    if gb:
        flags["--group-by"] = gb
    ob = []
    for f in r.get("orderByFields") or []:
        s = _field_spec(f, notes)
        s.update({k: v for k, v in (f.get("orderByInfo") or {}).items() if k in ("order", "nulls") and v})
        ob.append(s)
    if ob:
        flags["--order-by"] = ob
    wf = r.get("whereFilters") or {}
    expr = (wf.get("expression") or "").upper()
    if wf.get("conditions"):
        if " OR " in f" {expr} " or "(" in expr:
            notes.append(f"where filter uses OR/nesting (`{wf.get('expression')}`): not passable to run/create; save then `report update --where-filters`")
        else:
            conds = []
            for c in wf["conditions"]:
                lo = c.get("leftOperand") or {}
                left = ({"fieldPath": {"hops": _path_to_hops(lo["fieldPath"]), "leaf": lo["fieldName"]}}
                        if lo.get("fieldPath") else {"fieldName": lo.get("fieldName")})
                fv = c.get("filterValue") or {}
                if fv.get("dateLiteral"):
                    notes.append(f"filter on `{lo.get('fieldName')}` uses relative date `{fv['dateLiteral']}` "
                                 f"{fv.get('value')}: relative dates failed via `report run` in testing, so it was dropped; use absolute dates (BTW yyyy-MM-dd)")
                    continue
                cond = {"leftOperand": left, "operator": c.get("comparisonOperator")}
                if "value" in fv:
                    cond["rightOperand"] = {"value": fv["value"]}
                conds.append(cond)
            if conds:
                flags["--where-filters"] = {"conditions": conds}
    if (r.get("havingFilters") or {}).get("conditions"):
        notes.append("having filters present: not translated (see reference §3, Having filters)")
    return flags, notes


def exemplar(d, ids):
    import shlex
    outdir = os.path.join(d, "exemplars", "reports")
    os.makedirs(outdir, exist_ok=True)
    idx_path = os.path.join(outdir, "_index.tsv")
    existing = {}
    if os.path.exists(idx_path):
        for l in list(open(idx_path))[1:]:
            parts = l.rstrip("\n").split("\t")
            existing[parts[0]] = parts
    for rid in ids:
        resp = gs("report", "describe", "--id", rid)
        r = resp.get("data") if isinstance(resp, dict) else None
        if not r:
            print(f"{rid}: describe failed: {(resp or {}).get('_error', '')[:200]}"); continue
        slug = safe(re.sub(r"\s+", "-", (r.get("reportName") or rid).strip().lower()))[:60]
        save(d, f"exemplars/reports/{slug}.server.json", r)
        flags, notes = translate_report(r)
        args = ["report", "run"]
        for k, v in flags.items():
            args += [k, v if isinstance(v, str) else json.dumps(v)]
        res = gs(*args, "--limit", "3")
        err = res.get("_error") if isinstance(res, dict) else None
        ok = res is not None and not err
        if isinstance(res, list):
            result = f"ran OK, {len(res)} row(s); columns: {', '.join(res[0].keys()) if res else '(no rows)'}"
        elif ok:  # chart display types return a chart payload rather than rows
            result = f"ran OK (chart payload; top-level keys: {', '.join(list(res.keys())[:6])})"
        else:
            result = f"FAILED: {(err or str(res))[:400]}"
        cmd = "gs-admin " + " ".join(shlex.quote(a) for a in args) + " --limit 3 --json"
        create = cmd.replace("gs-admin report run", "gs-admin report create --name '<NEW UNIQUE NAME>'", 1) \
                    .replace(" --limit 3 --json", " --json")
        md = [f"# Report exemplar: {r.get('reportName')}", "",
              f"- report id: `{rid}` | object: `{flags['--object']}` | display: `{flags['--display-type']}`",
              f"- server JSON: `{slug}.server.json` (from `gs-admin report describe --id {rid} --json`)",
              f"- verification (`report run`, nothing saved, {now()}): **{'✅ ' if ok else '❌ '}{result}**", "",
              "## Working CLI command (run, read-only)", "```", cmd, "```", "",
              "## Same report, saved (WRITE: follow the write gate)", "```", create, "```", ""]
        if notes:
            md += ["## Not carried over / watch-outs"] + [f"- {n}" for n in notes] + [""]
        md += ["## What this exemplar teaches", "_(Claude: add 2–4 bullets: the pattern, the tenant conventions it shows,"
               " and when to copy it.)_", ""]
        open(os.path.join(outdir, f"{slug}.md"), "w").write("\n".join(md))
        existing[rid] = [rid, slug, r.get("reportName"), flags["--object"], flags["--display-type"],
                         "verified" if ok else "failed", str(len(notes))]
        print(f"{'OK  ' if ok else 'FAIL'} {r.get('reportName')}  -> exemplars/reports/{slug}.md" + (f"  ({len(notes)} note(s))" if notes else ""))
    write_tsv(d, "exemplars/reports/_index.tsv", ["report_id", "file", "name", "object", "display_type", "status", "notes"],
              list(existing.values()))
    mark(d, "exemplars_reports", count=len(existing), verified=sum(1 for v in existing.values() if v[5] == "verified"))


def status(d):
    m = load_manifest(d)
    print(json.dumps(m, indent=2))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("pull", "index", "report-candidates", "exemplar", "status"):
        print(__doc__); sys.exit(1)
    d, url = tenant_dir()
    m = load_manifest(d)
    m.setdefault("tenant_url", url)
    m.setdefault("tenant_slug", os.path.basename(d))
    save_manifest(d, m)
    cmd = sys.argv[1]
    try:
        if cmd == "pull":
            which = sys.argv[2:] or ["all"]
            todo = list(SECTIONS) if "all" in which else which
            for s in todo:
                if s not in SECTIONS:
                    raise SystemExit(f"unknown section {s}; choose from {', '.join(SECTIONS)} or all")
                print(f"[{s}]"); t = time.time()
                SECTIONS[s](d)
                print(f"  ({time.time() - t:.0f}s)")
        elif cmd == "index":
            index(d)
        elif cmd == "report-candidates":
            report_candidates(d)
        elif cmd == "exemplar":
            if len(sys.argv) < 3:
                raise SystemExit("usage: snapshot.py exemplar <reportId> [<reportId> ...]")
            exemplar(d, sys.argv[2:])
        else:
            status(d)
    except AuthExpired as e:
        print("\nSTOPPED: your gs-admin login token expired or is unauthorized.\n"
              "Run `gs-admin login`, then re-run the same command (finished sections are kept).\n", e)
        sys.exit(2)
    print(f"\nTenant folder: {d}")


if __name__ == "__main__":
    main()
