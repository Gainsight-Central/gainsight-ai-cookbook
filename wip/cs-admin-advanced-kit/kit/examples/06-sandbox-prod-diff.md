# What is different between sandbox and production

**When you need this.** A sandbox promotion fails partway, or a sandbox refresh quietly drops programs and resets dates. You need the list of what differs. You do not need another full click-through.

**What you can say**

```text
Compare sandbox and production. Read-only. Follow CLAUDE.md and examples/06-sandbox-prod-diff.md.

I have two local tenant brains: tenants/<sandbox-slug>/ and tenants/<prod-slug>/.
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

**What you get back**

Three lists: only in sandbox, only in production, and in both but not the same. The agent compares the two folders on your machine. It does not log into the second tenant unless you ask it to refresh one of them, and it does not copy a change from one side to the other.

**Example output** (illustrative)

| | Sandbox only | Production only | Different |
|---|---|---|---|
| Rules | "CLI - test risk" (inactive) | "Legacy load" (inactive) | "Set sentiment" active in prod, inactive in sandbox |
| Fields | `Company.Budget_Note__gc` | — | `Company.Segment` picklist has "Strategic" only in sandbox |
| Journey | — | "QBR invite" | — |

**Why this is easier than the screens.** X-Org tells you a promotion failed. It does not hand you a list of fields and rules you can read. The two local copies do.

**What this will not tell you.** A comparison is not a promotion. Connector settings, permission bundles, and PX connections are not in these indexes. Dates, and whether a Journey Orchestrator program is on, are the wrong signal after a sandbox refresh. Copying a change across is a change in the target tenant. The agent asks you before it does that, one list at a time.
