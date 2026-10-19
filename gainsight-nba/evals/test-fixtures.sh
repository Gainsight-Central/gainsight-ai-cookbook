#!/bin/sh
# Offline check of the file-adapter fixtures. Recomputes the expected cohort from the
# CSVs and the ledger, and compares it with fixtures/file-adapter/expected.json.
# This does not run the agent. It proves the fixtures hold the cases eval 2 relies on.
HERE=$(cd "$(dirname "$0")" && pwd)
python3 -I - "$HERE/fixtures/file-adapter" <<'PY'
import csv, json, sys, datetime
d = sys.argv[1]
exp = json.load(open(f"{d}/expected.json"))
as_of = datetime.date.fromisoformat(exp["as_of"])
thr = exp["threshold_days"]
sig = list(csv.DictReader(open(f"{d}/signal.csv")))
contacts = {r["user_email"]: r for r in csv.DictReader(open(f"{d}/contacts.csv"))}
ledger = [json.loads(l) for l in open(f"{d}/ledger.jsonl") if l.strip()]
recent = {r["recipient"] for r in ledger
          if (as_of - datetime.date.fromisoformat(r["timestamp"][:10])).days < 7 and r["status"] in ("sent", "drafted")}
flagged, drafts, skipped = [], [], {}
for r in sig:
    days = r["last_login_days"]
    if days == "" or int(days) > thr:
        e = r["user_email"]
        flagged.append(e)
        c = contacts.get(e)
        if c is None: skipped[e] = "no_contact_record"
        elif c["opted_out"].lower() == "true": skipped[e] = "opted_out"
        elif e in recent: skipped[e] = "contacted_in_last_7_days"
        else: drafts.append(e)
by_acct = {}
for r in sig:
    by_acct.setdefault(r["account"], []).append(r["last_login_days"])
adopting = sorted(a for a, v in by_acct.items() if all(x != "" and int(x) <= thr for x in v))
got = {"flagged": flagged, "drafts": drafts, "skipped": skipped, "already_adopting_accounts": adopting}
bad = 0
for k, v in got.items():
    if v != exp[k]:
        print(f"FAIL {k}: expected {exp[k]} got {v}"); bad = 1
    else:
        print(f"PASS {k}")
cfg = open(f"{d}/.nba-agent/config.md").read()
none = sorted(l.split(":")[0] for l in cfg.splitlines() if l.endswith(": none"))
if none != sorted(exp["capabilities_none"]):
    print(f"FAIL capabilities_none: {none}"); bad = 1
else:
    print("PASS capabilities_none")
sys.exit(bad)
PY
