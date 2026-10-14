# Answer from a saved report

**When you need this.** You need a number that already has a report: rows loaded, email log, activity, attendees, renewals. Rebuilding that report makes the agent read the schema again, and it still cannot express "this week" or an OR filter. The saved report already has those filters.

**What you can say**

```text
Answer this from a saved report. Read-only. Follow CLAUDE.md and examples/07-saved-report-answers.md.

Question: <what you want to know>.

1. Search config/reports.tsv and raw/reports.json for a report that already answers it.
   If several match, show me the names and ask which one. Do not create a report.
2. Run `gs-admin rp describe --name "<exact name>" --json` only if the filters are not already in the local tenant brain.
3. Take the report id from that row. Run `gs-admin report run-saved --id <id> --json`.
   Do not use `rp run --name` for a saved report. On CLI 1.0.10 that flag is a temporary name for a test run that is not saved, and `--object` is required, which drops the saved filters.
   If the result is large, write it to tenants/<slug>/raw/report-runs/<slug>.json and summarize. Do not paste the whole payload into chat.
4. Give me the number, the report name, the filter the report used, and the command.
   If no saved report fits, say so. Building a new report is a different job (prompts/build-report.md) and
   cannot express "this week" or an OR filter. Do not present a test run as if it were the saved report.
```

**What you get back**

The number from a report you already saved, plus the report name and the filter that report used. One run. The rows stay in the tenant folder.

**Example output** (illustrative)

Report: "Email log — last 7 days" on object `email_log`.

Filter already on the saved report: `CreatedDate` in the current week, status Sent.

`gs-admin report run-saved --id <id> --json` returned 1,204 rows. 38 failed. Top failure reason in the payload: "bounced". The saved filter (current week, status Sent) is still the one that ran.

**Why this is easier than the screens.** Report Builder is the wrong place to re-ask a question a saved report already answers. Running it from the agent keeps the filters the report already has, including "this week" and OR filters that a new report command would drop.

**What this will not tell you.** A CSM can ask some of these questions in the product as well. Use this when you are checking a load, a log, or a configuration outcome. It does not make two screens agree on a count, and it does not add inline edit. If the saved-report command is rejected, run `gs-admin report run-saved --help` once and stop. Do not rebuild the report.
