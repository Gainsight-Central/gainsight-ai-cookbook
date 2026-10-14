# What uses this field

**Pain.** You are about to retire a field, change a picklist, or delete a scorecard. Analyzer and Data Management dependencies miss dashboard filters, Data Designer, real-time rules, and playbooks. People find out when a rule fails the next morning.

**What you can say**

```text
What uses Company.Segment? Read-only. Follow CLAUDE.md and examples/02-what-uses-this-field.md.

1. Run `gs-admin dm dependencies check --name Company --json` and save it under
   tenants/<slug>/raw/dependencies-Company.json. This is object-level. Say that in the answer.
2. Search the snapshot for the field name. Reports: `showFields`, `groupByFields`, and `filterVariations` inside raw/reports.json (the list payload already has them).
   Rules: if tenants/<slug>/raw/rules-described.json is missing or older than 14 days, page
   `gs-admin re r list-and-describe --limit 20 --page N --json` until `totalRules` and save the `rules` array there. Never omit `--limit`. Do not describe each rule.
3. Data Designer: `gs-admin dd templates list --json`, then describe only templates whose name or
   list payload mentions the field or the object. Journey: search raw/jo_programs.json and
   raw/email_templates.json.
4. Write tenants/<slug>/intent/uses-Company.Segment.md with a table:
   asset, type, how it touches the field (filter, mapping, show field, write target, unknown).
5. End with a blind-spot list: anything the commands above did not return. Do not fill those rows
   with guesses. Playbooks, dashboard filters, and real-time rules belong on that list unless a
   command actually returned them.
```

**What the agent does**

One dependency call, one rule inventory call, a search of files already on disk, and a short table. A miss stays a miss.

**Example output** (illustrative)

| Asset | Type | How |
|---|---|---|
| Company Sync | Connector job | Maps `Account.Segment__c` → `Company.Segment` |
| Risk: segment drop | Rule | Filter `Segment` EQ `Enterprise`; creates a Risk CTA |
| Book of business | Report | Group-by `Segment` |
| ARR by segment | Data Designer template "CS Weekly" | Transform task output column `Segment` |

Not searched, so not cleared: playbooks, C360 dashboard filters, real-time rules.

**Why the CLI.** This is the bulk inventory admins already attempt by clicking. The kit does it once and writes it down, so the next question does not start over.

**Limits.** `dm dependencies check` names an object, not a field. A field can be unused while the object is busy. Deleting the field is a separate write and goes through the write gate. This job does not delete anything.
