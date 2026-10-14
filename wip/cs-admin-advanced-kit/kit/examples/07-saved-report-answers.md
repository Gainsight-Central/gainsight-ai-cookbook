# Answer from a saved report

**Pain.** You need a number that already has a report: rows loaded, email log, activity, attendees, renewals. Rebuilding that report in the agent re-describes the schema and still cannot express "this week" or an OR filter. The saved report already has those filters.

**What you can say**

```text
Answer this from a saved report. Read-only. Follow CLAUDE.md and examples/07-saved-report-answers.md.

Question: <what you want to know>.

1. Search config/reports.tsv and raw/reports.json for a report that already answers it.
   If several match, show me the names and ask which one. Do not create a report.
2. Run `gs-admin rp describe --name "<exact name>" --json` only if the filters are not already in the snapshot.
3. Take the report id from that row. Run `gs-admin report run-saved --id <id> --json`.
   Do not use `rp run --name` for a saved report. On CLI 1.0.10 that flag is a temporary name for an ad-hoc run and `--object` is required, which drops the saved filters.
   If the result is large, write it to tenants/<slug>/raw/report-runs/<slug>.json and summarize. Do not paste the whole payload into chat.
4. Give me the number, the report name, the filter the report used, and the command.
   If no saved report fits, say so. An ad-hoc report is a different job (prompts/build-report.md) and
   cannot express relative dates or OR filters. Do not pretend an ad-hoc run is the saved report.
```

**What the agent does**

It finds the report you already trust and runs it. One run. The rows stay in the tenant folder.

**Example output** (illustrative)

Report: "Email log — last 7 days" on object `email_log`.

Filter already on the saved report: `CreatedDate` in the current week, status Sent.

`gs-admin report run-saved --id <id> --json` returned 1,204 rows. 38 failed. Top failure reason in the payload: "bounced". The saved filter (current week, status Sent) is still the one that ran.

**Why the CLI.** The report builder is the wrong place to re-ask a question a saved report already answers. Running it from the agent is the path that does not rebuild filters the CLI would drop.

**Limits.** This overlaps what a CSM can ask through Gainsight CS MCP. Use this when you are checking a load, a log, or a config outcome. It does not fix two surfaces that return different counts for the same filter, and it does not add inline edit. If `report run-saved` is rejected, run `gs-admin report run-saved --help` once and stop. Do not fall back to `rp run --name`.
