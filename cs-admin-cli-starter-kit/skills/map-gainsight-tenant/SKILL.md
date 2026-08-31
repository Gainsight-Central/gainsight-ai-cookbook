---
name: map-gainsight-tenant
description: Use the locally installed gs-admin CLI to explain a Gainsight CS tenant read-only. Use when an admin asks what the tenant is configured to do, where a concept such as ARR, Risk, Health, or Segment is defined, how a CS process works end to end, what rules exist, or which configuration may be duplicated, unclear, or stale.
---

# Map a Gainsight tenant

Use the local `gs-admin` executable in the terminal. Never silently substitute another Gainsight MCP integration.

## Safety boundary

- Run `gs-admin whoami` first. Verify the expected tenant URL and a valid token. Ignore the `Auth mode:` line — it reads `not configured` even when the token is valid; only the `Token:` line matters.
- Use read operations only: `whoami`, `list`, `describe`, `query execute`, and `report schema`.
- Never create, update, edit, publish, run, save, add an action, or delete configuration.
- Stop on an invalid/expired token and ask the user to run `gs-admin login`.
- Save tenant artifacts under `./intent/`; do not send them elsewhere.
- Show the user large planned pulls before running them.

## Choose the workflow

- For a tenant overview, follow **Tenant overview**.
- For “where is X?”, follow **Concept map**.
- For Risk, Renewal, Onboarding, Adoption, or another process, follow **Process map**.
- For “list all rules,” follow **Rule inventory**.

## Establish durable context

On the first run, create `./AGENTS.md` at the working-folder root and `./intent/README.md`.

`AGENTS.md` belongs at the root, not inside `intent/` — agent clients discover it there. Keep it short: require future agents to read `./intent/README.md`, use local `gs-admin`, verify `whoami`, stay read-only, and never silently fall back to MCP.

In `./intent/README.md`, record the tenant URL, safe command policy, cache freshness note, and the rule-pagination command. This makes later sessions usable without reinstalling the skill.

## Read CLI output correctly

- Reports and rules: count at `data.pageInfo.totalRecords`.
- Journey programs: count at `data.totalRecords`.
- Objects: count at `data.totalNumberOfObjects`.
- Scorecards and measures: `data` is an array.
- `query execute` returns a bare array.
- Always pass an explicit `--limit` on list commands. Several default to a small page and report no total — `scorecard measure list --json` returns 20 records on a tenant that has 103 — so a default call silently under-reports. Where a total *is* reported, check the returned count against it.
- Rules cap pages near 200; paginate until collected records equal the reported total.
- Do not use `data-management objects list --search`; enumerate names without search and describe candidate objects.
- Verify Journey search results locally rather than assuming `--search` filtered them.

## Tenant overview

1. Report counts for reports, rules, Journey programs, objects, and scorecards.
2. Query `da_picklist` for `GSID,Name,Category,IsActive,Deleted,EntityType,DisplayOrder,CtaType,SpType` with limit 2000. If the returned count equals the limit, paginate for the rest.
3. Treat taxonomy as live only when `IsActive=true` and `Deleted=false`.
4. Use the taxonomy as the process spine; confirm with active rule names, used scorecard measures, and Journey names.
5. Anchor to Segment, Risk, Onboarding, Adoption, Renewal, Expansion, EBR, Advocacy, Voice of Customer, Success Planning, Stakeholder, and Lifecycle/Ops. Add bespoke processes only with evidence.
6. Write `./intent/reports/process_inventory.md` and `process_footprint.md`.

Use date-free liveness. For rules, exclude clear DNU, “do not use,” “copy of,” test, POC, old, and deprecated names. Do not use the substring `mig` as a dead signal because Migration may be a real process. Measures are used when `scorecardsCount>0`. Treat Journey status as unknown in refreshed sandboxes.

## Concept map

1. Split terms into exact definitions, plausible variants, and related concepts.
2. Search taxonomy, rules, report fields/whereFilters, measures, Journey names, and candidate object fields.
3. Describe strong rule matches to capture exact criteria and actions.
4. Reject accidental substring matches and do not label similar fields duplicates without semantic evidence.
5. Write `./intent/reports/where_is_<concept>.md` and the exhaustive evidence list to `./intent/model/concepts/<concept>.json`.

## Process map

1. **Detect:** find exact fields, used measures, and active rules; describe the strongest rules.
2. **Respond:** map CTA types/reasons/statuses, plans, playbooks, and Journey programs.
3. Resolve rule action IDs by matching them to `da_picklist.GSID`.
4. **Extend:** identify tenant-specific behavior.
5. **Check:** flag overlapping automation, unused measures, obvious dead/test/copy assets, and taxonomy-to-action mismatches.
6. Write `./intent/reports/<process>_process.md`.

## Rule inventory

Run `gs-admin rules-engine rules list --limit 200 --page <N> --json`, paging until the collected count equals `data.pageInfo.totalRecords`. Return a readable table with rule name and active status. Do not paste raw JSON unless requested.

## Output standard

- Lead with the answer, not the harvest procedure.
- Cite exact asset names, fields, filters, thresholds, and actions.
- Separate observed evidence from interpretation.
- Use “at least” for incomplete dependency or usage counts.
- Do not manufacture a drift narrative for a clean tenant.
- End with a short admin validation checklist and any surfaces not checked.

