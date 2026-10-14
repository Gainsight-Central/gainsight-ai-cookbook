# Where the tenant actually lives

**When you need this.** One admin holds the map. A field called ARR exists in more than one place, and nobody can say which one the connector writes, which one a rule overwrites, and which one the scorecard reads. A new admin, or an agent, starts by describing the same objects again.

**What you can say**

```text
Build the tenant handbook. Read-only. Follow CLAUDE.md and examples/01-tenant-handbook.md.

Use the local tenant brain under tenants/<slug>/. If TENANT.md is missing, stop and offer prompts/initialize.md.
Do not describe an object that already has a file in schema/objects/ or raw/objects/.

From the indexes, answer:
1. For ARR, renewal date, health, CSM, stage, segment, and churn: every object.field that looks like it,
   which reports and rules name it, and which one is used most. Say when two candidates are both plausible.
2. Which of those fields a connector job maps, and which a rule loads. Page `gs-admin cn list --limit 20 --page N --json` until a short page. For each connection, `gs-admin cn jobs --id <connectionId> --limit 20 --json` (or `--name` for the first match). Do not pass `--connector-id` or `--describe`.
   One call: `gs-admin re r list-and-describe --limit <rule count> --json`. Do not pass `--page` (on CLI 1.0.10 every page is the same first page). Read `rd._flatMappings` and `rd._sourceObject`. The schedule is not in that payload. For a rule you write up, run `gs-admin re r schedules --id <id> --json`. Do not describe rules one by one.
3. Write tenants/<slug>/TENANT.md (at most 120 lines) and tenants/<slug>/intent/field-ownership.md.
   Keep "found in this file" separate from "this looks canonical".
```

**What you get back**

A short handbook of the fields your team actually uses. The agent searches the indexes already on disk. It does not describe every object again. For connectors and rules it reads one page at a time. "The field this tenant uses" means the one most reports and live rules already use, and the file says so.

**Example output** (illustrative — not a real tenant)

| Concept | Field | Written by | Read by |
|---|---|---|---|
| ARR | `Company.Arr` | Salesforce connector job "Company Sync", mapped from `Account.AnnualRevenue` | 14 reports, scorecard measure "ARR band" |
| ARR | `Company.Arr__gc` | Rule "Load ARR from warehouse" (load to Company) | 2 reports |
| CSM | `Company.Csm` | Rule "CSM from owner" | Cockpit owner on 6 CTA rules |

`Company.Arr` is the one reports use. `Company.Arr__gc` is a second write. They are not the same number until someone checks a row.

**Why this is easier than the screens.** Gainsight shows one connector mapping, or one rule, at a time. The handbook is the list you would otherwise rebuild in a spreadsheet after someone leaves.

**What this will not tell you.** The connector command shows the mapping. It does not show whether the last run wrote blanks. Dropdown mismatches and Salesforce merges are not in this job. A dependency check does not list every dashboard filter or playbook.
