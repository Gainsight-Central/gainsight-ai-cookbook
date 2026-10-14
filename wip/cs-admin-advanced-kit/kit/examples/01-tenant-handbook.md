# Where the tenant actually lives

**Pain.** One admin holds the map. A field called ARR exists in more than one place, and nobody can say which one the connector writes, which one a rule overwrites, and which one the scorecard reads. A new admin, or an agent, starts by describing the same objects again.

**What you can say**

```text
Build the tenant handbook. Read-only. Follow CLAUDE.md and examples/01-tenant-handbook.md.

Use the snapshot under tenants/<slug>/. If TENANT.md is missing, stop and offer prompts/initialize.md.
Do not describe an object that already has a file in schema/objects/ or raw/objects/.

From the indexes, answer:
1. For ARR, renewal date, health, CSM, stage, segment, and churn: every object.field that looks like it,
   which reports and rules name it, and which one is used most. Say when two candidates are both plausible.
2. Which of those fields a connector job maps, and which a rule loads. Page `gs-admin cn list --limit 20 --page N --json` until a short page. For each connection, `gs-admin cn jobs --id <connectionId> --limit 20 --json` (or `--name` for the first match). Do not pass `--connector-id` or `--describe`.
   Page `gs-admin re r list-and-describe --limit 20 --page N --json` until the collected count equals `totalRules`. Read `rd._flatMappings` and `rd._sourceObject`. Do not describe rules one by one.
3. Write tenants/<slug>/TENANT.md (at most 120 lines) and tenants/<slug>/intent/field-ownership.md.
   Keep "found in this file" separate from "this looks canonical".
```

**What the agent does**

1. Reads `schema/_field_index.tsv`, `config/rules.tsv`, and `config/reports.tsv`. It greps. It does not reload raw JSON.
2. Pages `cn list`, then `cn jobs --id` (or `--name`) per connection.
3. Pages `re r list-and-describe --limit 20`. If that command is missing, it runs `gs-admin re r --help` once and stops. It does not describe every rule.
4. Writes the handbook. Canonical means "most reports and live rules use this field," and the file says so.

**Example output** (illustrative — not a real tenant)

| Concept | Field | Written by | Read by |
|---|---|---|---|
| ARR | `Company.Arr` | Salesforce connector job "Company Sync", mapped from `Account.AnnualRevenue` | 14 reports, scorecard measure "ARR band" |
| ARR | `Company.Arr__gc` | Rule "Load ARR from warehouse" (load to Company) | 2 reports |
| CSM | `Company.Csm` | Rule "CSM from owner" | Cockpit owner on 6 CTA rules |

`Company.Arr` is the one reports use. `Company.Arr__gc` is a second write. They are not the same number until someone checks a row.

**Why the CLI.** The UI shows one connector mapping, or one rule, at a time. The handbook is the list you would otherwise rebuild in a spreadsheet after someone leaves.

**Limits.** The connector command shows the mapping. It does not show whether the last run wrote nulls. Picklist mismatches and Salesforce merges are not in this job. Object dependency checks do not list every dashboard filter or playbook.
