# Build the local tenant brain

**What you get.** A folder on your machine that your AI agent reads before it calls Gainsight again. It holds your objects and fields, dropdown values, rules, reports, scorecards, Journey Orchestrator programs, and connectors.

It also holds **key definitions**: a short set of notes about how this tenant is set up. The agent uses them so the next report or rule looks like the ones your team already built.

**What a key definition is.** It is not a screen in Gainsight. It is a note the agent writes from your tenant:

- Which field is the ARR, renewal date, health score, CSM, stage, segment, or churn value your reports and rules actually use.
- How your team names things, and which folders you keep reports and rules in.
- A few real reports, rules, and Journey Orchestrator programs, written out as commands, so a new one can be copied from a real one.

Those sample reports and rules are saved under a folder named `exemplars/`. That is only the folder name. When you talk to the agent, ask for key definitions.

**Time.** About 10–20 minutes, depending on the size of the tenant.

**Does this change Gainsight?** No. This step only reads.

**How to run.** Point your AI agent at this folder and say **"Initialize my tenant."** You can also paste the box below. Claude, Cursor, and ChatGPT can all use this folder.

---

```
Initialize my Gainsight tenant. Follow CLAUDE.md.

This task only reads. You may list, describe, and run a report as a test.
A test run does not save a report. Do not create, edit, delete, schedule, or publish anything.

Before you start, stop and ask me two things in one message:
- Is this sandbox or production?
- May you build the local tenant brain?

With that question, show counts for objects, rules, reports, scorecards, and Journey Orchestrator programs.
One small call each is enough (`--limit 1 --json`). Use the count paths in reference/cli-reference.md.
Also say roughly how long it will take and how much disk it will use.
Wait for my answer. Run `gs-admin whoami` first and confirm the token is valid.

After I say yes, build the brain:

1. Run `python3 scripts/snapshot.py pull all`, then `python3 scripts/snapshot.py index`.
   If the login expires, ask me to run `gs-admin login`, then pull only the sections that did not finish.
   If the API returns HTTP 429, stop. Ask me to wait. Do not describe the same object again.
   If Python is missing, make the same reads with `gs-admin --json` and write the same index files.
2. Check the result. The number of rules and reports saved must match the totals the API reported.
   Open three object pages under schema/objects/ and tell me if something is missing.

Then write the key definitions. These are what you will copy later, so do not skip them.

3. Reports. Run `python3 scripts/snapshot.py report-candidates`.
   Choose 10 to 15 real reports that together show how this tenant builds reports:
   a single number, a grid, a chart grouped by one field, a stacked chart, a trend over time,
   at least three reports that look up a related object, at least three with filters, and one grouped by date.
   Prefer reports your team uses. Skip names that are Demo, Sample, or Test when you have a real one.
4. For each chosen report, run `python3 scripts/snapshot.py exemplar <report id>`.
   The script saves a file under exemplars/reports/. The file is a key definition.
   Read the copy line. exact means every filter was copied and the test command ran.
   partial means the command ran but a filter was left out (often a relative date, or OR). The row count
   is not the saved report's count. Do not call a partial copy verified.
   failed means the command did not run. Read the error, fix it using reference/cli-reference.md, and test
   with `gs-admin report run … --limit 3 --json`. If you cannot fix it, leave it failed and say why.
   In each file, add two to four sentences: what kind of report this is, what it shows about how this tenant
   builds reports, and when to copy it. When you talk to me, call these key definitions. Do not say "exemplar."
5. Rules. From config/rules.tsv, pick up to eight rules that are turned on and do different jobs
   (create a CTA, close a CTA, set a score, load data to Company, create a Success Plan, call an external action).
   Describe each one. That payload does not include the schedule. The snapshot stores it separately
   as `_schedule`, from `gs-admin re r schedules --id`. If `_schedule` is missing, run that command.
   Save the page under exemplars/rules/: source object, filters, what the action does, and the schedule.
   If nothing came back, write "no schedule returned." Do not guess a schedule from the describe payload.
6. Programs. Describe two or three Journey Orchestrator programs that represent how this tenant sends email
   or creates CTAs. Save a short page for each: who enters the program, and what the steps do.

Then write the pages a person can read:

7. conventions.md. Only what the indexes show: name prefixes, folders in use, CTA types and reasons that
   live rules actually use, and names that look retired (DNU, "copy of", test). Cite counts. Do not invent a standard.
8. Where the main fields live. For ARR, renewal date, health score, CSM, stage, segment, and churn,
   search schema/_field_index.tsv. List every field that might be it. Say which one the most reports and
   live rules use. If two are both plausible, say so.
9. intent/process_inventory.md. Using the live dropdown values and reference/cs_ontology.seed.json,
   group CTA reasons and Success Plan types into the Customer Success processes this tenant runs,
   and which of those look specific to this tenant. On a clean demo tenant, say it is clean.
10. TENANT.md, about 120 lines. This is the page you will read at the start of later sessions.
    Include: tenant URL, sandbox or production, date, CLI version, counts, the main fields from step 8,
    the processes from step 9, where the key definitions are (exemplars/), conventions.md, and changelog.md.
    Note any section that failed.
11. Create changelog.md with a heading only. Nothing has been changed in Gainsight yet.
12. Check your own work, then tell me the results:
    - Where is ARR, and which field looks like the one this tenant uses?
    - Which live rules create CTAs, and with which type and reason?
    - Using one key definition, run (do not save) a grid of ARR by customer stage, limit 5.
      Show the command and the rows.

When you finish, tell me the counts, which key definitions worked, which failed, and three things you
learned about this tenant. Point me to TENANT.md.
```

---

**Next.** Ask your question in plain English. To build a report, describe it. The agent follows `prompts/build-report.md` and starts from a key definition. To bring the local tenant brain up to date, use `prompts/refresh.md`.
