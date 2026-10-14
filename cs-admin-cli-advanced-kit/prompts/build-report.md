# Build a report

**What you get.** A Gainsight report that matches the way this tenant already builds reports. The agent starts from a key definition (a real report from your tenant, already written as a working command), runs it as a test, shows you the rows, and saves the report only after you say yes.

**How to run.** Ask in plain English, for example: *"Build a report of ARR by CSM for customers renewing in the next 6 months, as a bar chart."* You can also paste the box below.

---

```
Build the report I describe. Follow CLAUDE.md and reference/cli-reference.md.

1. Restate the report in one sentence: which object, which numbers, how it is grouped, which filters,
   and which chart or grid. If a choice would change the answer (which ARR field, or whether "renewing"
   means the renewal date or an open renewal CTA), ask me. Otherwise pick the field this tenant uses
   and say which one you picked.

2. Look up names in the local tenant brain. Do not guess them.
   - The report object name is the BI name in schema/_object_index.tsv.
   - Each field name and type is in schema/_field_index.tsv. Prefer the field named in TENANT.md.
   - A lookup (for example CSM name on the user record) comes from schema/_lookup_index.tsv.
   - A dropdown filter must use the value's ID from config/dropdowns.tsv, not the label.
     A label returns zero rows and no error.
   - "Next 6 months" and other relative dates must become real dates (yyyy-MM-dd) from today.
     The CLI cannot store a rolling date.

3. Start from a key definition. Open exemplars/reports/_index.tsv and pick the closest report
   (same chart type, or the same object) whose copy column is exact. Copy its command and change it.
   If the closest one is partial, tell me what was left out and do not treat its row count as the saved report.
   Those files are key definitions. Do not call them exemplars when you talk to me.
   If none are close, use the command shapes in reference/cli-reference.md.

4. Prove it before you save anything. Run `gs-admin report run … --limit 5 --json`.
   Run it once more as a grid so the rows are visible. Check that the row count and totals make sense.
   If a dropdown filter returns zero rows, you used the label instead of the ID. Fix it and run again.

5. Show me the rows, the test command, and the save command you would run.
   Name the report the way conventions.md names reports, and put it in the folder where similar reports live.
   If the CLI cannot express part of the request (an OR filter, or a rolling date), say what I would finish
   in Report Builder.

6. Save only after I say yes to this specific report. Then:
   - Read the saved report back and compare it with what I asked for.
   - Run the saved report and confirm the rows match the test.
   - Add a line to tenants/<slug>/changelog.md.
   - Offer to save this report as a new key definition: `python3 scripts/snapshot.py exemplar <new report id>`.

If I only wanted the number, and not a saved report, stop after step 5.
```
