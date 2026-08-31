# Where is a concept defined and used?

Use this for ARR, Risk, Health, Segment, Renewal Date, or another concept your team discusses differently.

Replace `<CONCEPT>` before running. [See an example ARR output](../examples/where-is-arr.md).

```text
Find where "<CONCEPT>" is defined and used in my Gainsight tenant.

USE THE ADMIN CLI:
- Run the local `gs-admin` executable in the terminal. Do not silently substitute another MCP integration.
- Run `gs-admin whoami` first and verify the tenant URL and valid token.

SAFETY:
- Read-only: whoami, list, describe, query execute, and report schema only.
- Never create, update, edit, publish, run, save, or delete configuration.
- Reuse relevant `./intent/` files when present and say when cached evidence may be stale.

1. PLAN THE SEARCH
Separate search terms into:
- exact definition terms,
- plausible variants or abbreviations,
- related concepts that are not automatically equivalent.

Match field and asset names as case-insensitive substrings, but reject accidental matches—for example,
ARR inside "Arrays". Show me the terms before searching.

2. SEARCH THE VISIBLE SURFACES
- Taxonomy: query da_picklist with GSID, Name, Category, IsActive, Deleted, CtaType, and SpType.
- Rules: search names, then describe strong matches to capture exact criteria, fields, and actions.
- Reports: page through report definitions and locally extract matching fields and whereFilters. Record
  the exact object, field, operator, and value. Do not paste raw report JSON into chat.
- Scorecards: search measure names/descriptions. Used means scorecardsCount > 0.
- Journey programs: page/list and filter names locally. Do not assume `--search` filtered correctly;
  sandbox program status is not reliable liveness evidence.
- Objects and fields: do not use `data-management objects list --search` because it may fail. Describe
  Company, Relationship, and relevant custom objects. Enumerate object names without --search if needed.

Keep observed facts separate from interpretation. Similar names are not proof of duplication.

3. WRITE THE RESULT
Create `./intent/reports/where_is_<concept>.md` with:
- Short answer
- What the concept appears to mean here (interpretation)
- Compact evidence table with exact loci and confidence
- Canonical-looking definition, if one exists (interpretation)
- Variants and why they differ
- Contradictions only when proven
- Related concepts
- Unknowns / surfaces not checked
- Five concrete checks for the admin

Also create `./intent/model/concepts/<concept>.json` with the complete evidence list. Keep the Markdown
report readable; put exhaustive matches in JSON. Finish by telling me the canonical candidate, strongest
evidence, top concern if any, and what you could not verify.
```

