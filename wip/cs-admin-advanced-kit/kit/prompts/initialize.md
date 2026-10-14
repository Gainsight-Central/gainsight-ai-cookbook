# Initialize: build the tenant snapshot

**What this does:** reads your tenant's configuration (read-only) and builds a local tenant brain under `tenants/<your-tenant>/`. It covers every object and field, picklist values, rules, reports, scorecards, Journey Orchestrator programs, connectors, and report examples taken from your own tenant. After this, your AI agent can answer questions about your tenant and draft new configuration in your tenant's own shape.

**Time:** about 10–20 minutes, depending on tenant size. **Writes to your tenant:** none.

**How to run:** point your AI agent at this folder and say **"Initialize my tenant."** You can also paste everything in the box below. Claude, Cursor, and ChatGPT can all use this folder.

---

```
Initialize my Gainsight tenant workspace. Follow CLAUDE.md. This whole task is READ-ONLY: the only
gs-admin commands allowed are list / describe / schema / list-objects / query execute / journey cta options /
dependencies check / report run (ad-hoc, saves nothing). Never run a write command.

PHASE 0: PREFLIGHT (then pause for me)
1. Run `gs-admin whoami`. Confirm the token is valid and note the Base URL and tenant slug.
2. Get counts (one cheap call each, `--limit 1 --json`): reports, rules, objects, JO programs, scorecards.
   Use the count paths in reference/cli-reference.md §1.
3. Ask me two things, in one message:
   a) Is this tenant SANDBOX or PRODUCTION? (Recorded in TENANT.md; it governs future writes.)
   b) OK to start the snapshot? Show the counts and the rough size (e.g. "~550 objects → ~15 MB on disk,
      ~3–5 min of pulling").
   Wait for my answer.

PHASE 1: PULL + INDEX (scripted, read-only)
4. Run: `python3 scripts/snapshot.py pull all` then `python3 scripts/snapshot.py index`.
   - If it stops on token expiry, ask me to `gs-admin login`, then re-run only the sections that didn't finish
     (e.g. `pull reports rules`).
   - If it stops on HTTP 429, stop. Tell me to wait and re-run that section. Do not raise parallelism and do not
     describe the same object again.
   - If python3 isn't available, do the same pulls by hand with gs-admin --json and write the same files
     (schema/_object_index.tsv, schema/_field_index.tsv, schema/_lookup_index.tsv, config/*.tsv).
5. Sanity-check the result: rules and reports pulled must equal the reported totals (the script warns if not),
   and spot-check 3 objects in schema/objects/. Report anything missing.

PHASE 2: REPORT EXEMPLARS (the key step for building reports later)
6. Run `python3 scripts/snapshot.py report-candidates`. From its output, pick 10–15 reports that together cover:
   - the most common patterns (KPI, GRID, grouped BAR/COLUMN, STACKED, LINE/date trend, pivot GRID)
   - at least 3 with lookup fields (fieldPath), at least 3 with where-filters, one with a date bucket
   - the most-reported objects (company, call_to_action, plus whatever this tenant reports on most)
   - real production-looking reports rather than "Demo"/"Sample"/"Test" ones where possible
7. Run `python3 scripts/snapshot.py exemplar <id1> <id2> …`. Each one is described, translated to CLI flags,
   and verified with `report run` (nothing saved). For any FAILED exemplar, read the error, fix the flags using
   reference/cli-reference.md, re-run the corrected command with `gs-admin report run … --limit 3 --json`, and update that
   exemplar's .md with the working command. If you can't fix it, leave it marked failed and say why.
8. In each exemplar .md, fill in "What this exemplar teaches" (2–4 bullets: the pattern, conventions it shows,
   when to copy it).

PHASE 3: RULE + PROGRAM EXEMPLARS (lighter)
9. From config/rules.tsv, pick up to 8 LIVE rules covering different action types (create CTA, close CTA,
   set score, load to object/company, success plan, external action, if present). Run
   `gs-admin rules-engine rules describe --id <ruleId> --json` for each. Save to exemplars/rules/<slug>.json
   and write exemplars/rules/<slug>.md: source object, criteria pattern, actions + key parameters (CTA type,
   reason, priority, playbook, owner field), schedule type. Keep it short.
10. From config/jo_programs.tsv, describe 2–3 representative programs (`journey programs describe --id`).
    Save them and write a short .md each (participant source, steps, emails/CTAs created).

PHASE 4: CONVENTIONS + CONCEPTS
11. Write tenants/<slug>/conventions.md from evidence in the indexes:
    - naming patterns/prefixes for reports, rules, programs, custom fields (e.g. "CSMPF:", "(JO)", "__gc")
    - report folders and rule folders in use
    - CTA types/reasons/priorities actually used by live rules (vs. merely configured)
    - dead/legacy signals (DNU, "copy of", test…) and how common they are
    Cite counts. Don't invent conventions that the data doesn't show.
12. Find where the core CS concepts live. For each of ARR, renewal date, health score, CSM/owner, customer
    stage/lifecycle, segment/tier, churn/risk, NPS: grep schema/_field_index.tsv. List the candidate fields
    and pick the likely canonical one, with evidence: it's on Company, it's used by the most reports, rules
    write to it. Flag ambiguity explicitly (e.g. "ARR exists on 8 objects; Company.Arr is used by N reports").

PHASE 5: PROCESS INVENTORY
13. Using config/da_picklist.tsv (live = active and not deleted) and reference/cs_ontology.seed.json, classify
    the live CTA reasons/types and Success Plan types into CS processes (standard vs bespoke). Size each with
    live rules and live measures (by name match). Write tenants/<slug>/intent/process_inventory.md.
    On a clean/demo tenant it's fine to report "clean"; don't manufacture drift.

PHASE 6: TENANT.md + SELF-TEST
14. Write tenants/<slug>/TENANT.md, at most ~120 lines. It's what you'll read at the start of every future session:
    - tenant URL, slug, SANDBOX/PRODUCTION, snapshot date, CLI version (`gs-admin --version`)
    - counts table (objects, fields, rules live/total, reports, scorecards, JO programs)
    - top 15 objects by report usage, with their BI names
    - core concepts table from step 12 (concept → canonical object.field → alternates)
    - the processes from step 13 in one line each
    - pointers: exemplars index, conventions.md, changelog.md
    - any gaps (sections that failed or were skipped)
15. Create tenants/<slug>/changelog.md with just a header (no writes have been made).
16. SELF-TEST, then tell me the results:
    a) Answer from the snapshot: "Where is ARR defined and which one is canonical?"
    b) Answer from the snapshot: "Which live rules create CTAs, and with which types/reasons?"
    c) Build and RUN (not save) one new report using an exemplar: "ARR by customer stage, GRID", with
       `report run --limit 5`. Show the command and the result.

FINISH: summarize in chat (counts, the exemplars that verified vs failed, the 3 most useful things you learned
about this tenant, any gaps) and point me to TENANT.md. Remind me I can now ask anything about the tenant
or ask you to build a report.
```

---

**Next:** ask your question in plain English. To build a report, describe it (the AI agent follows `prompts/build-report.md`). To bring the local tenant brain up to date, use `prompts/refresh.md`.
