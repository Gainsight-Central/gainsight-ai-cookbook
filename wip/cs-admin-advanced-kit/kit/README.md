# CS Admin CLI Advanced Kit

Give your AI agent a local tenant brain.

This kit builds that brain on your machine from your Gainsight configuration. Your AI agent reads it before calling the tenant again. Answers come back faster, they match how your instance is actually set up, and the agent is not downloading the same objects, rules, and reports for every question.

An AI agent such as Claude, Cursor, or ChatGPT can use this folder. Point your AI agent at the folder, then describe what you want in plain English. The agent uses the [Gainsight Admin CLI](https://support.gainsight.com/gainsight_nxt/AI_Assistants/Admin_CLI/Configure_Admin_CLI) you already have. You do not need a new command.

The [Starter Kit](../../cs-admin-cli-starter-kit/) answers "what is this tenant configured to do?" This kit is for the questions that come after that.

## Questions you can ask

| You are dealing with | Say this | Example |
|---|---|---|
| Nobody can say which ARR is the one your team uses, or a new admin is taking over | "Build the tenant handbook." | [01](examples/01-tenant-handbook.md) |
| You are about to change or retire a field | "What uses Company.Segment?" | [02](examples/02-what-uses-this-field.md) |
| A rule says success and the score did not move | "Which rules failed, and which only look healthy?" | [03](examples/03-rule-health.md) |
| Cockpit is full, or two things write the same measure | "What creates CTAs, and what writes each measure?" | [04](examples/04-cta-and-score-sources.md) |
| A connector sync and a rule both write Company | "Who writes Company fields?" | [05](examples/05-connector-ownership.md) |
| Sandbox and production have drifted | "Compare sandbox and production." | [06](examples/06-sandbox-prod-diff.md) |
| A saved report already answers the question | "Run the saved report. Do not rebuild it." | [07](examples/07-saved-report-answers.md) |

## What the local tenant brain holds

A one-time setup (`prompts/initialize.md`) writes the brain under `tenants/<your-tenant>/`. When the tenant changes, refresh it (`prompts/refresh.md`).

- **Every object and field**, every lookup path between objects, and every picklist value, including the IDs that filters need.
- **Your rules, reports, scorecards, Journey Orchestrator programs, and connectors**, indexed so the agent can search them.
- **Report examples from your own tenant**, translated into CLI commands and checked with a test run. Gainsight report setup is hard to guess. These examples show the agent how your reports are built.
- **Your conventions.** Naming, folders, and the CTA types and reasons your team actually uses, so new work looks like your team built it.
- **Where your core fields live** (ARR, renewal date, health, CSM, stage), including where the same idea exists in more than one field.

> Part of the Gainsight AI Cookbook. The files in this folder are plain text you can read: how the agent behaves, the questions above, and `scripts/snapshot.py`, which only reads configuration.

---

## Get started

**1. Install and connect the Gainsight Admin CLI.** Full steps: [Configure the Gainsight Admin CLI](https://support.gainsight.com/gainsight_nxt/AI_Assistants/Admin_CLI/Configure_Admin_CLI).

```
npm install -g @gainsight/gs-admin-cli@latest
gs-admin login --base-url https://YOUR_TENANT.gainsightcloud.com
gs-admin whoami
```

You need a super admin login. Before you log in, register one OAuth application in your tenant:

| Setting | Value |
|---|---|
| Scopes | Read, Write |
| PKCE | Enabled |
| Callback URL | `http://localhost:19876/callback` |

`gs-admin whoami` should show `Token: valid`.

**2. Point your AI agent at this folder.** Use a copy of the folder as the working directory, outside any git repository, so the tenant export is never committed. Claude, Cursor, and ChatGPT can all use the same folder. The instructions in the folder tell the agent how to behave.

**3. Say "Initialize my tenant."** The agent follows `prompts/initialize.md`. This step is read-only. It asks two questions first: is this sandbox or production, and is it all right to start. On a typical tenant this takes about 10–20 minutes. When it finishes you have `tenants/<your-tenant>/TENANT.md` and a short check that the brain is usable.

You need Node.js, Python 3 (already on macOS; the snapshot script uses it), and an AI agent that can run commands in the terminal.

---

## Ask for a change

The same local brain supports a few tasks beyond the table above.

| You say | What happens |
|---|---|
| "Build a report of ARR by stage as a stacked column, and save it to the CS Ops folder." | The agent follows `prompts/build-report.md`: it starts from a similar report in your tenant, runs a test, shows you the result, and saves only after you say yes. Relative dates and OR filters cannot be set this way. |
| "Add a Budget cut value to the churn reason dropdown." | The agent follows `prompts/change-config.md`: it shows the plan, waits for your yes, checks the result, and writes a changelog entry. |
| "Refresh my tenant brain." | The agent follows `prompts/refresh.md`: it re-reads what is out of date, shows what changed, and checks the report examples again. |

If a saved report already answers the question, use [example 07](examples/07-saved-report-answers.md). Building a new report is a separate task.

## How changes are made

The agent can create and change configuration only through the write gate in `CLAUDE.md`:

1. A plain-English plan, the exact commands, what else the change touches, and any real-world effects (emails, CTAs, data overwrites).
2. Your explicit yes for that specific change. For a production change, the agent recommends trying it in sandbox first.
3. A read-back of the result, and an entry in `tenants/<your-tenant>/changelog.md`.

New rules are left inactive, and Journey Orchestrator programs are left unpublished, unless you ask otherwise. See `GUARDRAILS.md`.

## What's in the folder

```
CLAUDE.md            how the AI agent behaves in this folder: routing, write gate, CLI facts
AGENTS.md            the same instruction, for agents that read this file name
GUARDRAILS.md        the safety model
examples/            the questions in the table above: what to say, what runs, and the limit
prompts/
  initialize.md      build the local tenant brain (start here)
  build-report.md    plain English → a report checked against your tenant
  change-config.md   rules, Journey Orchestrator, scorecards, fields, dropdowns, behind the write gate
  refresh.md         bring the local tenant brain up to date
reference/
  cli-reference.md   CLI syntax, output shapes, and known limits
  cs_ontology.seed.json  standard Customer Success processes, used to classify yours
scripts/snapshot.py  reads configuration and writes the local indexes (Python standard library only)
tenants/             created when you initialize: one folder per tenant
```

After initialization, `tenants/<your-tenant>/` contains:

```
TENANT.md            the overview the AI agent reads each session
manifest.json        what was read, when, and with which command
schema/              object, field, and lookup indexes, plus one page per object
config/              rules, reports, dropdowns (with GSIDs), scorecards, measures, Journey Orchestrator programs
exemplars/           reports, rules, and programs translated into CLI commands
conventions.md       how your team names and organizes configuration
intent/              which standard processes you run, and which are specific to you
changelog.md         every change made through the AI agent
raw/                 full JSON reads (large; the agent searches these, it does not load them whole)
```

## Good to know

- **Your data stays on your machine.** The local tenant brain is written to this folder. Treat `tenants/` like a configuration export. Do not commit it to a shared or public repository.
- **Sandbox and production.** Initialize each one separately. Each gets its own folder. The agent works in the tenant that `gs-admin whoami` shows.
- **The login lasts about an hour.** If it expires mid-task, the agent asks you to run `gs-admin login`, then continues from the step that stopped.
- **Some report filters cannot be set from the CLI.** Relative dates and OR filters cannot be passed to `report run` or `report create`. The agent uses absolute dates, or tells you what to finish in Report Builder. Details are in `reference/cli-reference.md`.
