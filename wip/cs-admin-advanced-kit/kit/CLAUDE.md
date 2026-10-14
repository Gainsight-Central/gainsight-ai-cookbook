# Gainsight tenant workspace (CS Admin CLI Advanced Kit)

You are working with a Gainsight CS admin through the `gs-admin` CLI, which is installed and logged in on this machine. This folder is your workspace. It holds a local snapshot of their tenant, so you can answer questions about it accurately and build configuration (reports, rules, programs, fields) that matches how their tenant is actually set up.

Do not use any other Gainsight MCP server or integration in place of `gs-admin`. They expose less, so answers would be incomplete. If `gs-admin` is unavailable, say so.

## Start of every session

1. Run `gs-admin whoami`. The `Token:` line must say `valid` (ignore "Auth mode: not configured"). If it doesn't, ask the user to run `gs-admin login --base-url https://<tenant>.gainsightcloud.com` and wait.
2. The tenant slug is the first part of the Base URL host (`https://acme.gainsightcloud.com` → `acme`). The workspace is `tenants/<slug>/`.
3. **If `tenants/<slug>/TENANT.md` does not exist**, the tenant isn't initialized. Tell the user, and offer to run `prompts/initialize.md`: it's read-only, takes about 10–20 minutes, and you'll ask before anything big. You can still answer simple one-off questions live, but don't build configuration without a snapshot.
4. **If it exists**, read `tenants/<slug>/TENANT.md` and nothing else yet. Check `tenants/<slug>/manifest.json`. If a section you need was pulled more than 14 days ago, say so and offer `prompts/refresh.md` for just that section.
5. Note the environment recorded in TENANT.md (**sandbox** or **production**). It changes how carefully you treat writes.

If the user has more than one tenant (e.g. sandbox and production), each has its own `tenants/<slug>/` folder. Always work in the one that matches `whoami`, and never apply knowledge from one tenant's snapshot to another without saying so.

## How to behave on the CLI

These rules come from how the CLI is actually called. Break one and you will throttle the tenant or loop on a bad id.

- **Search the snapshot before you call.** If `schema/objects/`, `raw/`, or a `config/*.tsv` already has the object, rule, or report, read that. Do not describe it again in this session.
- **One inventory call, then drill in.** For rules, `gs-admin re r list-and-describe --limit 20 --page N --json` until `totalRules` is covered. Never omit `--limit` (the default is every rule). Never describe every rule in a loop.
- **Stop on a repeated failure.** If a command fails, read the error. Do not run that same command with the same arguments again. Run `gs-admin <command> --help` once if the error is an unknown flag or the wrong id kind, then stop and tell the user. Journey program fetches take the id the list command returned. Do not send a GSID to a command that returned a UUID, or the reverse.
- **Stop on HTTP 429.** Wait. Do not raise parallelism and do not continue the fan-out.
- **Saved reports answer data questions.** Find the report with `rp list` or `rp describe --id`, then run `report run-saved --id`. `rp run --name` is an ad-hoc run: `--name` is a temporary label and `--object` is required. It is not how you run a saved report. Ad-hoc JSON cannot express relative dates or OR filters.
- **Commands move between CLI versions.** `reference/cli-reference.md` §§1–6 match CLI 1.0.10. If a command is not there, run `--help` once and treat the syntax as unverified.

## Jobs

| The admin is asking | Follow |
|---|---|
| Where a concept lives, or which field is canonical | `examples/01-tenant-handbook.md` |
| What uses a field, or what breaks if it changes | `examples/02-what-uses-this-field.md` |
| Which rules failed, or which look healthy and are not | `examples/03-rule-health.md` |
| What creates CTAs, or what writes a measure | `examples/04-cta-and-score-sources.md` |
| Which connector and which rule write a Company field | `examples/05-connector-ownership.md` |
| How sandbox and production differ | `examples/06-sandbox-prod-diff.md` |
| A number a saved report already computes | `examples/07-saved-report-answers.md` |
| Build a new report | `prompts/build-report.md` |
| Change a rule, program, field, or dropdown | `prompts/change-config.md` |

## Where to look

All paths are under `tenants/<slug>/`. The `.tsv` index files can be large: **search them with `grep`/`awk`/`python`, don't read them whole.** Never print a `raw/` file. Extract only the part you need with `python3` or `jq` (one object describe can be 170 KB+).

| Question / task | Look here first |
|---|---|
| Tenant overview, key objects, where core concepts live (ARR, health, CSM, stage, renewal) | `TENANT.md` |
| Does field X exist / which object has it / its type | `schema/_field_index.tsv` (object, field, label, type, picklist category, lookup, flags) |
| All fields of one object | `schema/objects/<Object>.md` |
| How to join A → B (lookups) | `schema/_lookup_index.tsv` |
| Object names: data-management vs. report (BI) | `schema/_object_index.tsv` (`bi_name` column) |
| Picklist values **and their GSIDs** (needed for filters) | `config/dropdowns.tsv` |
| CTA types/reasons/statuses, Success Plan types, objective categories | `config/da_picklist.tsv`, `raw/cta_options.json` |
| Rules | `config/rules.tsv`, then `gs-admin rules-engine rules describe --id` for detail |
| Reports and their patterns | `config/reports.tsv` |
| **How to build a report like the ones they already have** | `exemplars/reports/_index.tsv` → `exemplars/reports/<name>.md` |
| Scorecards / measures | `config/scorecards.tsv`, `config/measures.tsv` |
| Journey programs | `config/jo_programs.tsv` |
| Naming, folders, and other conventions | `conventions.md` |
| CS processes the tenant runs (standard vs bespoke) | `intent/process_inventory.md` |
| What has been changed through the AI agent | `changelog.md` |
| CLI syntax, output shapes, known bugs | `reference/cli-reference.md` (kit root) |

## Answering questions

- **Shape questions** ("which object holds ARR?", "what rules write to Company?", "which reports use CTA reason?"): answer from the snapshot and cite the file. When the same concept lives in several places (for example ARR on several objects), list them and say which looks canonical and why.
- **Data questions** ("how many customers renew next quarter?"): run them live with `gs-admin report run` (supports filters, grouping, and lookups), using `--display-type GRID`. `query execute` has no WHERE clause, so use it only for simple pulls.
- **Current state of config** ("is that rule still active?"): the snapshot is a hint. Confirm with one live `describe` before stating it as fact.
- Keep **what you found** (evidence: the field, rule, or filter, plus the command) separate from **what it seems to mean**. Say so plainly when the snapshot doesn't cover something.

## Building or changing configuration

- **Reports** → follow `prompts/build-report.md`. Never write report JSON from memory. Start from the closest exemplar and the verified syntax in `reference/cli-reference.md`, and get it working with `report run` before any `report create`.
- **Rules, Journey programs, scorecards, objects/fields, dropdowns** → follow `prompts/change-config.md`.
- Match the tenant's conventions (`conventions.md`): naming prefixes, folders, which CTA types and reasons to use. A new report or rule should look like the admin built it.

## WRITE GATE (applies to every write, every time)

A write is any command that creates, updates, edits, deletes, adds, assigns, uploads, schedules, publishes, saves, runs, pauses, resumes, or stops something. Examples: `report create/update`, `rules-engine rules create/edit/add-*/delete-*/schedule*/run-now`, `journey programs create/save/publish/resume/stop`, `scorecard create/update/measure assign`, `data-management objects create/add-field/update`, `dropdowns add-item/upload-csv`.

Before a write:
1. **Plan** in plain English: what changes, where, and why.
2. **Blast radius**: for object or field changes, run `data-management dependencies check --name <Object>`. Grep `config/rules.tsv` and `config/reports.tsv` for references.
3. **Real-world effects**: say whether it will email customers, create CTAs for CSMs, or overwrite data. `rules run-now`, JO `publish`/`resume`, and load-to-object actions all have real effects.
4. **Environment**: say whether this is sandbox or production. In production, recommend trying it in sandbox first.
5. Show the **exact command(s)**, then **wait for an explicit yes for this specific write**. Approval for one write doesn't cover the next.

After a write:
1. Read it back (`describe`) and compare it to what was intended. Report any differences.
2. Add an entry to `tenants/<slug>/changelog.md`: UTC time, what and why, the exact command, IDs created or changed, and the verification result.
3. Refresh the affected index (e.g. `python3 scripts/snapshot.py pull reports && python3 scripts/snapshot.py index`) or note that it is stale.

Never get around the gate by splitting a write into steps, using another tool, or calling the API directly.

## CLI facts you will need (verified; details in reference/cli-reference.md)

- Always pass `--json` when you parse output. Envelopes differ by command (`data.data`, `data.liteObjects`, bare arrays…).
- The token lasts about **1 hour**. On an auth error, stop, ask the user to `gs-admin login`, then resume where you left off.
- `rules-engine rules list` caps pages at about 200, so page until you have `data.pageInfo.totalRecords`. `objects list` pages with `--size`, not `--limit`.
- Report commands use **BI object names** (`company`, `call_to_action`, `gsuser`), not data-management names.
- Lookup fields in reports: `{"fieldPath":{"hops":[{"through":"Csm","to":"gsuser"}],"leaf":"Name"}}`.
- **Picklist filters need the value GSID, not the label.** A label returns 0 rows with no error.
- Date buckets: `"summarize":"Month"` (case-sensitive). Relative-date filters don't work via `report run`, so use absolute dates.
- Pivot is GRID-only. Stacked charts use the 2nd group-by as the series.
- `data-management objects list-and-describe` returns nothing, so use `list` and then `describe` per object.
- In sandboxes, created/modified dates are reset and Journey programs are deactivated. Don't infer "stale" from dates or JO status there.

## Helper script

`scripts/snapshot.py` (Python stdlib only) pulls and indexes the snapshot. It can only run the read commands listed in its `READ_COMMANDS` allow-list. Commands: `pull <section>`, `index`, `report-candidates`, `exemplar <reportId>…`, `status`. If Python isn't available, do the same steps by hand with `gs-admin … --json`, following `prompts/initialize.md`.
