# Start here: What is my Gainsight tenant configured to do?

Use this first. It gives you a readable tenant overview and leaves instructions for future AI sessions.

[See an example of what the output looks like](../examples/tenant-overview.md).

Copy the prompt below into an AI coding agent opened in your working folder.

```text
Help me understand what this Gainsight tenant is configured to do.

USE THE ADMIN CLI:
- Run the locally installed `gs-admin` command in the terminal.
- Do not use or silently fall back to another Gainsight MCP server or generic MCP tools.
- First run `gs-admin --help`, then `gs-admin whoami`.
- Confirm the expected tenant URL and a valid Token line. If either is wrong, stop and tell me what to fix.
- Ignore the `Auth mode:` line — it says `not configured — run 'gs-admin login'` even when the token is
  valid. Only the `Token:` line matters. Do not stop because of that line.

SAFETY:
- Read-only. Use only whoami, list, describe, query execute, and report schema.
- Never create, update, edit, publish, run, save, or delete tenant configuration.
- Save local output under `./intent/`. Do not send tenant data elsewhere.
- If the token expires, stop and ask me to run `gs-admin login`, then resume.

1. CREATE CONTEXT FOR FUTURE AGENTS
Create `./AGENTS.md` at the root of this working folder, and `./intent/README.md`.
`AGENTS.md` must be at the root — agent clients look for it there, not inside subfolders.

`AGENTS.md` must be short and say:
- read `./intent/README.md` before answering tenant questions,
- use local `gs-admin` terminal commands, never silently substitute MCP,
- run `gs-admin whoami` first and verify tenant + token,
- remain read-only unless I explicitly request and approve a write.

`./intent/README.md` must record the tenant URL and give future agents this command guide:
- For all rules, run `gs-admin rules-engine rules list --limit 200 --page <N> --json` and paginate
  until the collected count equals `data.pageInfo.totalRecords`.
- Present readable names/statuses instead of dumping raw JSON.
- Reuse files under `./intent/` when useful, but say when cached evidence may be stale.

2. CONFIRM ACCESS AND SIZE THE TENANT
Report these counts using their actual JSON locations:
- reports: `data.pageInfo.totalRecords` from `gs-admin report list --limit 1 --json`
- rules: `data.pageInfo.totalRecords` from `gs-admin rules-engine rules list --limit 1 --json`
- Journey programs: `data.totalRecords` from `gs-admin journey programs list --limit 1 --json`
- objects: `data.totalNumberOfObjects` from `gs-admin data-management objects list --json`
- scorecards: length of `data` from `gs-admin scorecard list --json`
- scorecard measures: length of `data` from `gs-admin scorecard measure list --limit 500 --json`

Always pass an explicit `--limit` on list commands. Some default to 20 records and report no total, so a
default call silently under-reports — measures is the one that bites.

3. PULL THE PROCESS SPINE
Run:
`gs-admin query execute --object da_picklist --select "GSID,Name,Category,IsActive,Deleted,EntityType,DisplayOrder,CtaType,SpType" --limit 2000 --json`

If the returned record count equals the limit, paginate for the rest. Do not assume 2000 covered everything.

Treat an item as live only when IsActive=true and Deleted=false. Summarize active/total counts for CTA
types, reasons, statuses, Success Plan types, objective categories, priorities, goal types, and task types.

4. IDENTIFY THE TENANT'S CS PROCESSES
Use the live taxonomy as the starting point. Confirm it with active rule names, measures used by at least
one scorecard, and Journey program names. Pull names/statuses only; do not describe every asset.

Anchor the result to these common processes: Segment, Risk & Churn, Onboarding, Adoption & Usage,
Renewal & Retention, Expansion & Sales, EBR / Executive Engagement, Advocacy & Reference,
Voice of Customer, Success Planning / Objectives, Stakeholder / Persona, and Lifecycle / Ops.
Add tenant-specific processes only when the evidence supports them. Leave opaque names unexplained.

Use date-free liveness. Dates and Journey on/off status are unreliable in refreshed sandboxes.
For rules, exclude obvious DNU, "do not use", "copy of", test, POC, old, and deprecated names.
Do not treat the substring "mig" as dead; Migration may be a real business process.

5. WRITE THE RESULT
Create:
- `./intent/reports/process_inventory.md`
- `./intent/reports/process_footprint.md`

Lead with a short answer: what the tenant appears to do, its three strongest CS motions, up to three
tenant-specific extensions, and the most useful concern if evidence supports one. Do not invent drift.
Cite exact asset names behind claims and separate observed evidence from interpretation.
```

Next, try [finding where a concept is defined](where-is.md) or [mapping one process](map-a-process.md).

