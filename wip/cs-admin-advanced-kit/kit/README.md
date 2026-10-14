# CS Admin CLI Advanced Kit

**Teach Claude your Gainsight tenant once. Then ask it anything, and have it build reports and configuration the way your tenant already does them.**

The Starter Kit is read-only and answers "what does my tenant do?". This kit is for admins who want to **work** through the CLI, reading and writing. It starts with a one-time initialization that gives Claude a working knowledge of your tenant:

- **Every object and field**, every lookup path between objects, and every picklist value (with the internal IDs that filters need).
- **Your rules, reports, scorecards, Journey programs and integrations**, indexed and searchable.
- **Verified report exemplars.** Real reports from your tenant, translated into working CLI commands and proven with a test run. Gainsight report JSON is hard to guess; with these, Claude doesn't have to.
- **Your conventions.** Naming, folders, which CTA types and reasons you actually use, so new work looks like your team built it.
- **Where your core concepts live** (ARR, renewal date, health, CSM, stage…), including where they're duplicated.

> Built and maintained by Gainsight. Everything here is plain text you can read: `CLAUDE.md` (how Claude behaves), `prompts/` (what it does), and `scripts/snapshot.py` (the only code, read-only by construction).

---

## Start in 3 steps

**1. Install and log in to the Gainsight Admin CLI** (one time, ~10 minutes. Full guide: [Configure the Gainsight Admin CLI](https://support.gainsight.com/gainsight_nxt/AI_Assistants/Admin_CLI/Configure_Admin_CLI))
```
npm install -g @gainsight/gs-admin-cli@latest
gs-admin login --base-url https://YOUR_TENANT.gainsightcloud.com
gs-admin whoami          # look for "Token: valid"
```
You need a **super-admin** login and one OAuth app in your tenant (Scopes: Read, Write · PKCE: enabled · Callback: `http://localhost:19876/callback`).

**2. Open this folder in Claude Code** (or Claude cowork). Download the folder, then:
```
cd "CS Admin CLI Advanced Kit"
claude
```
Claude reads `CLAUDE.md` automatically, checks your login, and sees whether your tenant has been initialized.

**3. Say "initialize my tenant."** Claude runs `prompts/initialize.md`. It's read-only, takes about 10–20 minutes, and asks you two questions first (is this sandbox or production, and is it OK to start). When it's done you'll have `tenants/<your-tenant>/TENANT.md` and a short self-test showing it works.

Requirements: Node.js, Python 3 (preinstalled on macOS; used for the snapshot script), and an approved Claude model.

---

## Then just ask

| You say | What happens |
|---|---|
| *"Where is ARR defined, and which one is canonical?"* | Answered from the snapshot, with the evidence |
| *"Which rules create Risk CTAs, and what triggers them?"* | Rules index → live `describe` of the matches |
| *"How many customers renew next quarter, by CSM?"* | Ad-hoc `report run` (nothing saved) → a table |
| *"Build a report of ARR by stage as a stacked column, and save it to the CS Ops folder."* | `prompts/build-report.md`: closest exemplar → test run → shows you → saves **only on your yes** |
| *"Add a 'Budget cut' value to the churn reason dropdown."* | `prompts/change-config.md`: checks dependencies → plan → your yes → verify → changelog |
| *"What would break if I retire the Segment field?"* | Dependency check plus rule/report references |
| *"Refresh my snapshot."* | `prompts/refresh.md`: re-pull, diff, re-verify exemplars |

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
