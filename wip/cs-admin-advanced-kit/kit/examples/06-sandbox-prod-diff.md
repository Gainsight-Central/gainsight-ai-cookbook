# What is different between sandbox and production

**Pain.** A sandbox promotion fails partway, or a sandbox refresh quietly drops programs and resets dates. You need the list of what differs. You do not need another full click-through.

**What you can say**

```text
Diff sandbox and production. Read-only. Follow CLAUDE.md and examples/06-sandbox-prod-diff.md.

I have two snapshots: tenants/<sandbox-slug>/ and tenants/<prod-slug>/.
If either TENANT.md is missing, stop and tell me to initialize that tenant. Do not copy files from one tenant into the other.

Diff only the indexes, with a short Python script, not by reading the files whole:
- schema/_field_index.tsv (object, field, type)
- config/rules.tsv (name, active)
- config/reports.tsv (name, object, display type)
- config/scorecards.tsv and config/measures.tsv
- config/jo_programs.tsv (name, status)
- config/dropdowns.tsv (category, value)

Write tenants/<prod-slug>/intent/diff-vs-<sandbox-slug>.md with three lists:
only in sandbox, only in production, in both but different (type, active flag, status, picklist values).
Ignore created/modified dates. On a sandbox, Journey "off" after a refresh is not proof the program was retired.
Do not replay any change. If I want to copy something later, that is a separate write and I will say which rows.
```

**What the agent does**

It compares two local snapshots. It does not log into the second tenant unless you ask it to refresh one of them, and it never applies a row from one side to the other inside this job.

**Example output** (illustrative)

| | Sandbox only | Production only | Different |
|---|---|---|---|
| Rules | "CLI - test risk" (inactive) | "Legacy load" (inactive) | "Set sentiment" active in prod, inactive in sandbox |
| Fields | `Company.Budget_Note__gc` | — | `Company.Segment` picklist has "Strategic" only in sandbox |
| Journey | — | "QBR invite" | — |

**Why the CLI.** X-Org tells you a promotion failed. It does not hand you a field-and-rule diff you can read. Two snapshots do.

**Limits.** A diff is not a promotion. Connector configs, permission bundles, and PX connections are not in these indexes. Dates and Journey on/off status are the wrong signal after a sandbox refresh. Copying a change across is a write, on the target tenant, through the write gate, one approved list at a time.
