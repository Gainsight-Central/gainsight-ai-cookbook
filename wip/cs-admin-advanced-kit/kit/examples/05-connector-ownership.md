# Which connector writes this, and what else writes it too

**Pain.** A Company field is null after sync. Permissions on the integration user look fine. A rule is also loading that object, and the two overwrite each other. The connector job and the rule do not appear on the same screen.

**What you can say**

```text
For the Company object, show which connector jobs map fields and which rules also write those fields.
Read-only. Follow CLAUDE.md and examples/05-connector-ownership.md.

1. Page `gs-admin cn list --limit 20 --page N --json` until a short page. For each connection,
   `gs-admin cn jobs --id <connectionId> --limit 20 --json` (or `--name` for the first match).
   Do not pass `--connector-id` or `--describe`. Save under tenants/<slug>/raw/connectors/.
   If a job payload has no field mappings, say so. Do not invent a flag to go get them.
2. For the connector that syncs Company (or the one I name), also run
   `gs-admin cn activity --name "<connection>" --limit 20 --json` and
   `gs-admin cn audit --id <connectionId> --limit 20 --json`.
   `--id` on activity is for realtime connections only. Use `--name` for a batch connection.
3. From raw/rules-described.json (page `re r list-and-describe --limit 20` if older than 14 days),
   keep `rd._flatMappings` whose target is Company or which name a Company field.
4. Write tenants/<slug>/intent/company-writers.md:
   field, connector job and source field, rule that also writes it, last activity status, last audit change.
   If activity says success and the mapping exists, you may still not claim the row was non-null.
```

**What the agent does**

It joins three read models the UI keeps apart: job mappings, job activity, and rule load actions.

**Example output** (illustrative)

| Company field | Connector | Also written by | Last activity | Last config change |
|---|---|---|---|---|
| `Arr` | Company Sync ← `Account.AnnualRevenue` | Rule "Load ARR from warehouse" (UPSERT) | Success, 02:10 UTC | Mapping edited 12 days ago |
| `Csm` | User Sync ← `Account.OwnerId` | Rule "CSM from owner" | Success | None in the audit payload |
| `Segment` | Company Sync ← `Account.Segment__c` | — | Partial | — |

`Arr` has two writers. A success status does not mean the value landed. Partial on Segment is the one to open in the connector activity screen.

**Why the CLI.** Admins already compare a connector mapping to a rule by hand when a field comes through empty. This writes the comparison down and keeps it next to the rest of the snapshot.

**Limits.** This does not fix a null, a picklist mismatch, a Salesforce merge, or a user that was deleted in Salesforce and is still active here. Activity is whatever the connector API returns. Warehouse scale failures and Timeline association rules are outside these commands.
