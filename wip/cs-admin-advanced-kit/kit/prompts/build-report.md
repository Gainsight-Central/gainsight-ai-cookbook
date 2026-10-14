# Build a report

**What this does:** turns a plain-English report request into a working Gainsight report. The AI agent starts from your tenant's own reports, checks the report with a test run (nothing saved), and saves it only after you say yes.

**How to run:** ask, for example, *"Build a report of ARR by CSM for customers renewing in the next 6 months, as a bar chart."* The AI agent follows the steps below. You can also paste the box.

---

```
Build the report I describe. Follow CLAUDE.md and reference/cli-reference.md.

1. UNDERSTAND. Restate the report in one line: object, measures, grouping, filters, display type. If a choice
   really changes the result (e.g. which ARR field, or whether "renewing" means the renewal date or an open
   renewal CTA), ask me. Otherwise pick the sensible default and say which.

2. RESOLVE FIELDS FROM THE SNAPSHOT (don't guess names):
   - object → BI name from schema/_object_index.tsv
   - each field → exact name and type from schema/_field_index.tsv (prefer the canonical field in TENANT.md)
   - each lookup → `through`/`to` from schema/_lookup_index.tsv
   - each picklist filter value → its GSID from config/dropdowns.tsv (labels silently return 0 rows)
   - relative dates ("next 6 months") → absolute yyyy-MM-dd from today's date

3. START FROM AN EXEMPLAR. Pick the closest one in exemplars/reports/_index.tsv (same display type and/or same
   object and pattern). Copy its working command and change it. If none are close, use the verified syntax in
   reference/cli-reference.md §3.

4. PROVE IT (read-only): run `gs-admin report run … --limit 5 --json` with the final display type, then once more
   as `--display-type GRID` so you can see actual rows. Check the numbers make sense: row count, totals, no
   unexpected empties. If a picklist filter returns 0 rows, check you used the GSID. Fix and re-run until it's right.

5. SHOW ME: the rows (formatted table), the exact `report run` command, and the `report create` command you
   would run, with a name that follows conventions.md and a folder (`--folder-id`) that matches where similar
   reports live. Mention anything the CLI can't express (OR filters, rolling date ranges) and how to finish
   it in the UI.

6. SAVE ONLY ON MY EXPLICIT YES (write gate in CLAUDE.md). Then:
   - `gs-admin report describe --id <newId> --json`: compare with what was intended
   - `gs-admin report run-saved --id <newId> --limit 5 --json`: confirm it returns the same rows
   - append to tenants/<slug>/changelog.md
   - offer to add it as a new exemplar: `python3 scripts/snapshot.py exemplar <newId>`

If I only wanted the answer (data, not a saved report), stop after step 5 and just give me the numbers.
```
