# Config schema

Customer configuration lives in `.nba-agent/`. Nothing customer-specific lives in the skill.

## Where it lives

- Claude Code, or the Desktop Code tab: files in `.nba-agent/` in the working directory.
- Claude Desktop chat or claude.ai (no filesystem): the same files as artifacts. The user saves them to project knowledge. On later runs, read them from project knowledge, or ask the user to paste them. Preflight states which path is in use.

## Files

| File | Holds | Required |
| --- | --- | --- |
| `config.md` | identity, capability map, compliance, guardrails | yes |
| `style.md` | tone, derived from 2-3 sample emails | yes |
| `rules.md` | hard rules the emails must follow, verbatim | no |
| `knowledge.md` | features or offers the agent may recommend | yes |
| `ledger.jsonl` | one JSON row per drafted, sent, or edited email | no (Code only) |

## config.md

```markdown
---
schema_version: 2
---
# Config: <customer name>

## Identity
customer: <name>
products: <list>
csm_email: <email of the user running the agent>
csm_name: <name>

## Capabilities
identity: gainsight-cs
book: gainsight-cs
contacts: gainsight-cs
goals: gainsight-cs
signal: gainsight-cs
context: staircase
knowledge: file
mail: gmail   # or generic (any tool that creates drafts), or none
ledger: file

## Book
# Saved after the first run confirms it. See steps/data.md, Scope.
owner_fields: <the account fields that name the CSM, for example the main CSM field>
active_filter: <how active accounts are told apart, for example status is Active>
include_relationships: <true | false>

## Catalog
# Written by setup step 1 (Connect). What the configured sources returned when probed. See steps/setup.md.
checked: <date of the probe>
metrics:
  - <metric name as the source names it> | level: <user | account> | timestamp: <yes | no> | coverage: <n of m sampled accounts had a value> | source: <where it came from>
segments:
  - <field name> | object: <account | contact> | values: <value (count), value (count), ...>
not_found: <what the probe looked for and did not find, for example: feature-level usage>

## Last run
# Written at the close of a run. Optional. Replaced each run.
date: <date of the run>
goal: <the confirmed goal in the CSM's words>
scope: <book, segment, or named accounts>
counts: flagged <n>, drafted or shown <n>, approved <n>, rejected <n>, skipped <n>

## File maps
# Only for capabilities mapped to `file`. Format in adapters/file.md.

## Servers
# Needed only when more than one connected server matches an adapter.
# Preflight asks once and saves the answer. Use the server name as connected.
identity_server: <server name>
signal_server: <server name>

## Compliance
region: <list of regions, for example US, EU. Recorded only. No step changes behavior by region.>
opt_out_source: <capability, field, or file that lists opted-out contacts>
allowed_basis: <for example: existing customer relationship>
language: <for example: en>
timezone_source: <contact field, account field, or a single fixed timezone>

## Guardrails
draft_cap_per_run: 25
ground_top_n: 25
frequency_cap: 1 per 14 days
quiet_hours: 08:00-18:00 recipient local time
suppress: unsubscribed, open support escalation, contacted in last 7 days
send_enabled: false
```

The send guard hook reads `csm_email` and `send_enabled` with a line match. Keep those two keys on their own lines, as `key: value`.

## Rules

- `send_enabled` is edited by the user by hand. The agent never writes `true`. This is an instruction, not a lock: the file is writable. The send guard hook reads it.
- `schema_version` is required. If the file is older than the skill's version, preflight lists the new fields, asks for them, and rewrites the file. It never edits silently.
- Blockers (the run stops until they exist): `identity` section, `style.md`, `knowledge.md`, and a capability map with every required capability set.
- `style.md` may be a short neutral style marked `source: default, no samples` when the user skips the sample email. Setup says so. `products` may stay unset when the knowledge doc names none.
- Guardrails fall back to the values above if the section is empty. The user is told.
- `book` is confirmed once, on the first run, by the book question in `reference/questions.md`. Later runs reuse it and state it in the funnel.
- `compliance.opt_out_source` is a blocker for any send. Drafting can run without it, sending cannot.
- `Last run` is optional. A missing section is fine, and it never blocks a run. It holds only what the run's own counts showed. In chat the CSM must save the updated artifact again for it to persist.
- `Catalog` holds only what a tool or file returned during the probe. Never fill an entry from memory or from an example. An empty `metrics` list is valid and means the source holds no adoption metric. The goal check reads it. See `steps/setup.md` and `steps/goal-check.md`.
- No config value is silently guessed. A missing value means ask, or propose a default the user confirms. Setup states every default it applies.
- `compliance.region`, `compliance.allowed_basis`, `compliance.timezone_source` and `quiet_hours` stay unset until the first send. The send step asks for them. Drafting does not read them. (`timezone_source` and `quiet_hours` already worked this way.)
- `compliance.timezone_source` and `quiet_hours` may stay unset until the first send. Drafting does not need them. The send step asks for them then.

## Versioning

| Version | Change |
| --- | --- |
| 1 | First release. |
| 2 | Adds the `Catalog` section. A version 1 config is upgraded by running the catalog probe once and saving the result. No other value changes. |
