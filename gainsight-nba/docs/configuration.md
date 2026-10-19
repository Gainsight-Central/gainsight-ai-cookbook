# Configuration

NBA Agent keeps your setup in a `.nba-agent/` folder in your working directory. The agent creates it the first time you run it, asks for anything missing, and shows you each file before saving. You can edit the files by hand at any time.

This page explains every file and setting.

## Plugin options

Two settings belong to the plugin itself, not to `.nba-agent/`. Claude asks for them when you install, and they live in your Claude settings.

| Option | Meaning | Required |
| --- | --- | --- |
| `cs_server_url` | The address of your Gainsight CS MCP server. Each tenant has its own. | Yes |
| `staircase_server_url` | The address of the Staircase AI MCP server. Defaults to `https://mcp.staircase.ai/mcp`. | No |

To change them, open `/plugin`, choose manage, pick `gainsight-nba`, and choose Configure options. If you set a capability to `file` or `none` and don't use one of these servers, its address can stay as is, and the agent doesn't call that server.

If you also added the same server as a connector in Claude, both appear. The agent asks once which to use and saves your answer under Servers in `config.md`.

## Files

| File | What it holds | Required |
| --- | --- | --- |
| `config.md` | Who you are, which tool answers which question, compliance, send limits | Yes |
| `style.md` | Your customer's email tone | Yes |
| `knowledge.md` | The features or actions the agent may recommend | Yes |
| `rules.md` | Rules every email must follow | No |
| `ledger.jsonl` | A log of drafts and sends | No |

The agent stops and asks if `config.md`, `style.md`, or `knowledge.md` is missing. It never borrows another customer's tone, rules, or product knowledge.

If you use Claude on the web or in the desktop chat, which can't write files, the agent gives you each file as an artifact. Save them to your project knowledge. On later runs it reads them from there, or asks you to paste them.

## config.md

```markdown
---
schema_version: 1
---
# Config: Acme

## Identity
customer: Acme
products: Acme Platform
csm_email: you@yourcompany.com
csm_name: Your Name

## Capabilities
identity: gainsight-cs
book: gainsight-cs
contacts: gainsight-cs
goals: gainsight-cs
signal: gainsight-cs
context: staircase
knowledge: file
mail: gmail
ledger: file

## File maps
(only for capabilities set to `file`)

## Servers
(only if more than one connected server matches)

## Compliance
region: US
opt_out_source: contacts field unsubscribed
allowed_basis: existing customer relationship
language: en
timezone_source: contacts field timezone

## Guardrails
draft_cap_per_run: 25
ground_top_n: 25
frequency_cap: 1 per 14 days
quiet_hours: 08:00-18:00 recipient local time
suppress: unsubscribed, open support escalation, contacted in last 7 days
send_enabled: false
```

Keep `csm_email` and `send_enabled` on their own lines as `key: value`. The send check reads those two lines.

### Identity

| Setting | Meaning |
| --- | --- |
| `customer` | The customer the emails are for |
| `products` | The products in scope |
| `csm_email` | Your email address. Test sends go here and only here. |
| `csm_name` | The name the emails are signed with |

### Capabilities

A capability is a question the agent needs answered. You choose which tool answers each one. Set a capability to `none` if you have no source for it.

| Capability | What it answers | If it's `none` |
| --- | --- | --- |
| `identity` | Who are you, as a CSM | Required. The agent can't run. |
| `book` | Which accounts are yours | Required. The agent can't run. |
| `contacts` | Who to email at each account, with opt-out status | Required. The agent can't run. |
| `signal` | The metric you're tracking, for example last login | Required. The agent can't run. |
| `knowledge` | What it may recommend | Required. The agent can't run. |
| `goals` | Goals and success plans customers have recorded | Discovery runs on the signal alone. Rows say "no recorded goal". |
| `context` | Account health, sentiment, and recent conversation themes | Drafts rely on usage and your product docs only. Rows say "context not available". |
| `mail` | Where approved drafts go | No approve buttons. Drafts show in chat for you to copy. |
| `ledger` | A record of what was drafted and sent | Frequency caps and edit rate show as unavailable. |

Values you can use:

| Value | What it uses |
| --- | --- |
| `gainsight-cs` | The Gainsight CS tools: `identity`, `book`, `contacts`, `goals`, `signal`, and the timeline part of `context` |
| `staircase` | Staircase AI for `context` |
| `gmail` | Gmail for `mail`, and Gmail labels as the `ledger` on surfaces with no files |
| `file` | A file. For `knowledge` and `ledger` it's the file in `.nba-agent/`. For `signal`, `book`, `contacts`, and `goals` it's a CSV or similar file you name under File maps. For `identity` it reads your details from the Identity section. |
| `none` | Nothing |

### File maps

Only needed when a capability is set to `file` and points at your own data. Add one line per capability, with the file and which column means what:

```
## File maps
signal: file=signal.csv; account=account; user=user_email; metric=last_login_days; blank_means=never
contacts: file=contacts.csv; user=user_email; name=name; account=account; role=role; opt_out=opted_out; timezone=timezone
book: derived from signal.csv column account
```

Paths are relative to your working directory. The agent reads the files as given. It doesn't fix or fill in columns, and it reports the file's modified time so you know how old the signal is.

### Servers

Needed only when more than one connected server could answer a capability, for example two Gainsight tenants. The agent asks once which to use and saves your answer:

```
## Servers
identity_server: <server name as connected>
signal_server: <server name as connected>
```

It never picks one silently.

### Compliance

| Setting | Meaning |
| --- | --- |
| `region` | Where your recipients are, for example `US` or `EU` |
| `opt_out_source` | Where opt-outs are recorded: a contact field, a file column, or a list |
| `allowed_basis` | The lawful basis your company uses for these emails |
| `language` | The language drafts are written in |
| `timezone_source` | How the agent finds each recipient's local time: a contact or account field, or one fixed timezone |

If `opt_out_source` is empty, the agent can still draft emails. It won't send any until you set it.

### Guardrails

| Setting | Default if blank | Meaning |
| --- | --- | --- |
| `draft_cap_per_run` | 25 | The most drafts in one run. The agent tells you how many were left out and offers a second run. |
| `ground_top_n` | 25 | How many top-ranked accounts get the deeper look. The rest are counted, not drafted. |
| `frequency_cap` | 1 per 14 days | How often one person can be emailed. Needs a ledger to check. |
| `quiet_hours` | 08:00 to 18:00 recipient local time | When emails may go out |
| `suppress` | unsubscribed, open support escalation, contacted in last 7 days | Contacts to skip. The agent reports who was skipped and why. |
| `send_enabled` | `false` | Whether Approve & send is available |

The agent also always skips contacts with no email address or marked opted out or do-not-contact, and sends at most one email per person per run.

When a default applies, the agent says so.

#### How these limits are enforced

- `send_enabled` is enforced by a check that runs before a Gmail send, reply, or forward. While it's `false`, that check blocks any recipient except you.
- The other limits (caps, quiet hours, suppression, the recipient list you confirm before a send) are rules the agent follows. Nothing technical stops it from ignoring them, so check the recipient list before you confirm a send.

#### Turning sending on

Open `.nba-agent/config.md` and change `send_enabled: false` to `send_enabled: true`. Do this yourself. The agent never writes `true`, and if you ask it to, it tells you to edit the file.

Approve & send also needs:
- the plugin installed from the marketplace (the check comes with the plugin),
- Gmail as the mail tool,
- `opt_out_source` set.

With any other mail tool, the agent creates drafts only.

## style.md

Your customer's tone, written from the sample emails you provided. It holds the greeting and sign-off patterns, sentence length and formality, and any do's and don'ts the samples show. If the samples don't show something, the file doesn't claim it.

To change the tone, edit the file, or give the agent new sample emails and ask it to rewrite `style.md`.

## rules.md

Hard rules every email must follow, kept in your words. Examples: "always name the CSM", "never mention pricing", "link only to the academy". The agent treats each as a constraint. Leave the file out if you have none.

## knowledge.md

The list of features or actions the agent may recommend. For each one:

| Column | Meaning |
| --- | --- |
| Feature | The name, as your docs name it |
| One-line value | What it does for the user |
| Adoption gap it addresses | The situation it fits |
| Source URL | The doc page it came from |

Every feature named in a draft has to trace to this file. Items you mark as paid get a `[verify entitlement]` flag unless the account's entitlement is known.

To add or update an item, edit the file or give the agent a doc link and ask it to add the entry. The agent fetches the page directly, so what it records matches what the page says.

## ledger.jsonl

One line per drafted, sent, or edited email, saved on your machine. Fields:

| Field | Meaning |
| --- | --- |
| `run_id`, `timestamp` | Which run, and when |
| `use_case` | For example `adoption` |
| `account`, `recipient`, `subject` | Who and what |
| `status` | `drafted`, `shown`, `sent`, `test_sent`, or `rejected` |
| `edited`, `accepted_unedited` | Whether you changed the draft in the agent before approving |
| `draft_id` | The draft in your mail tool |

The agent only adds lines. It never edits or deletes them. The ledger is what lets the agent check the frequency cap across runs and report your edit rate. The edit rate counts changes made in the agent only, not edits you make later in your mail tool.

On surfaces with no files, Gmail labels (`gainsight-nba`, and `gainsight-nba/<use case>`) do the same job.

## Changing your setup

- **Edit a file directly.** The agent reads the files at the start of every run.
- **Ask the agent.** For example, "set up the NBA agent for Acme" to redo a section, or "change the quiet hours to 9 to 5." It shows you the change and asks you to confirm before saving.
- **Start fresh.** Delete the `.nba-agent/` folder. The agent asks for everything again.

Run `/gainsight-nba:status` to see which files exist, the config version, and which capabilities are ready.

## Updating from an older version

`config.md` starts with `schema_version`. If a plugin update adds settings, the agent lists the new ones, asks you for values, and rewrites the file. It never changes your file silently.

| Version | Change |
| --- | --- |
| 1 | First release |
