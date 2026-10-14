# CS Admin CLI Advanced Kit

**Seven jobs admins already do by hand, run through the Gainsight Admin CLI, with the answers saved on your machine so the next question does not start over.**

The [Starter Kit](../../cs-admin-cli-starter-kit/) answers "what is this tenant configured to do?". This kit is the next set of questions: who writes a field, what uses it, which rules failed, what creates CTAs, what sets a measure, and what differs between sandbox and production.

A one-time snapshot (`prompts/initialize.md`) is how the agent remembers the tenant. Refresh it when the tenant changes (`prompts/refresh.md`). The jobs below are the reason to take the snapshot. They use the CLI you already have (`@gainsight/gs-admin-cli`). They do not require a new command.

| You are dealing with | Say this | Example |
|---|---|---|
| Nobody can say which ARR is real, or a new admin is taking over | "Build the tenant handbook." | [01](examples/01-tenant-handbook.md) |
| You are about to change or retire a field | "What uses Company.Segment?" | [02](examples/02-what-uses-this-field.md) |
| A rule says success and the score did not move | "Audit rule and chain health." | [03](examples/03-rule-health.md) |
| Cockpit is full, or two things write the same measure | "What creates CTAs, and what writes each measure?" | [04](examples/04-cta-and-score-sources.md) |
| A connector sync and a rule both write Company | "Who writes Company fields?" | [05](examples/05-connector-ownership.md) |
| Sandbox and production have drifted | "Diff sandbox and production." | [06](examples/06-sandbox-prod-diff.md) |
| A saved report already answers the question | "Run the saved report. Do not rebuild it." | [07](examples/07-saved-report-answers.md) |

What this kit does not claim is listed in [DOES-NOT-COVER.md](DOES-NOT-COVER.md). Null Salesforce fields, license counts, X-Org promotion, and Journey sends that never leave are product gaps. The CLI can show the configuration around them. It cannot repair them.

The snapshot also holds:

- **Every object and field**, every lookup path between objects, and every picklist value (with the internal IDs that filters need).
- **Your rules, reports, scorecards, Journey programs and integrations**, indexed and searchable.
- **Verified report exemplars.** Real reports from your tenant, translated into working CLI commands and proven with a test run. Gainsight report JSON is hard to guess; with these, Claude doesn't have to.
- **Your conventions.** Naming, folders, which CTA types and reasons you actually use, so new work looks like your team built it.
- **Where your core concepts live** (ARR, renewal date, health, CSM, stage…), including where they're duplicated.

> Built and maintained by Gainsight. Everything here is plain text you can read: `CLAUDE.md` (how Claude behaves), `examples/` (the jobs), `prompts/` (initialize, refresh, and the write paths), and `scripts/snapshot.py` (the only code, read-only by construction).

---

## Start in 3 steps

**1. Install and log in to the Gainsight Admin CLI** (one time, ~10 minutes. Full guide: [Configure the Gainsight Admin CLI](https://support.gainsight.com/gainsight_nxt/AI_Assistants/Admin_CLI/Configure_Admin_CLI))
```
npm install -g @gainsight/gs-admin-cli@latest
gs-admin login --base-url https://YOUR_TENANT.gainsightcloud.com
gs-admin whoami          # look for "Token: valid"
```
You need a **super-admin** login and one OAuth app in your tenant (Scopes: Read, Write · PKCE: enabled · Callback: `http://localhost:19876/callback`).

**2. Open this folder in Cursor** (or Claude Code). Use a copy of this folder as the workspace, outside the cookbook repo, so the tenant export is never committed.
```
cd "CS Admin CLI Advanced Kit"
```
Cursor reads `AGENTS.md`.

**3. Say "initialize my tenant."** Claude runs `prompts/initialize.md`. It's read-only, takes about 10–20 minutes, and asks you two questions first (is this sandbox or production, and is it OK to start). When it's done you'll have `tenants/<your-tenant>/TENANT.md` and a short self-test showing it works.

Requirements: Node.js, Python 3 (preinstalled on macOS; used for the snapshot script), and an approved Claude model.

---

## Then ask for a job

Use the table at the top. A few more that sit on the same snapshot:

| You say | What happens |
|---|---|
| *"Build a report of ARR by stage as a stacked column, and save it to the CS Ops folder."* | `prompts/build-report.md`: closest exemplar → test run → shows you → saves **only on your yes**. Relative dates and OR filters cannot be set this way. |
| *"Add a 'Budget cut' value to the churn reason dropdown."* | `prompts/change-config.md`: plan → your yes → verify → changelog |
| *"Refresh my snapshot."* | `prompts/refresh.md`: re-pull, diff, re-verify exemplars |

Building a new report is a separate job from running one you already have. If a saved report answers the question, use [example 07](examples/07-saved-report-answers.md).

## How writes work

Claude can create and change configuration, but only through the **write gate** in `CLAUDE.md`, every time:
1. A plain-English plan, the exact commands, what else it touches, and any real-world effects (emails, CTAs, data overwrites).
2. Your explicit **yes** for that specific write. In production, Claude recommends trying it in sandbox first.
3. Read-back verification, and an entry in `tenants/<your-tenant>/changelog.md`.

New rules are left inactive and Journey programs unpublished unless you ask otherwise. See `GUARDRAILS.md`.

## What's in the folder

```
CLAUDE.md            how Claude works in this folder (loaded automatically): routing, write gate, CLI facts
GUARDRAILS.md        the safety model, in 1 minute
DOES-NOT-COVER.md    admin pains this CLI cannot close
examples/            the seven jobs: what to say, what runs, what it will not claim
prompts/
  initialize.md      one-time snapshot of your tenant (start here)
  build-report.md    plain English → verified report
  change-config.md   rules, Journey, scorecards, fields, dropdowns, behind the write gate
  refresh.md         keep the snapshot current
reference/
  cli-reference.md   verified CLI syntax, output shapes, known gaps
  cs_ontology.seed.json  standard CS processes, used to classify yours
scripts/snapshot.py  read-only puller + indexer (stdlib Python; allow-listed read commands only)
tenants/             created by initialize: one folder per tenant (sandbox and prod side by side)
```

After initialization, `tenants/<your-tenant>/` contains:
```
TENANT.md            the overview Claude reads every session
manifest.json        what was pulled, when, with which command
schema/              _object_index.tsv, _field_index.tsv, _lookup_index.tsv, objects/<Object>.md
config/              rules, reports, dropdowns (with GSIDs), da_picklist, scorecards, measures, jo_programs
exemplars/           reports/ (verified CLI commands), rules/, jo/
conventions.md       how your team names and organizes things
intent/              process inventory (standard vs bespoke)
changelog.md         every write made through Claude
raw/                 full JSON pulls (large; Claude extracts from these, never loads them whole)
```

## Good to know
- **Your data stays local.** The snapshot is written to this folder on your machine. Treat `tenants/` like a config export: don't commit it to a public repo.
- **Sandbox vs production.** Initialize each one separately; they get separate folders. Claude always works in the one `gs-admin whoami` points to.
- **The token lasts about an hour.** If it expires mid-task, Claude will ask you to run `gs-admin login` and pick up where it left off.
- **Known CLI gaps** (documented in `reference/cli-reference.md`): relative-date filters and OR filters can't be set through `report run/create`. Claude uses absolute dates, or tells you what to finish in the report builder.
