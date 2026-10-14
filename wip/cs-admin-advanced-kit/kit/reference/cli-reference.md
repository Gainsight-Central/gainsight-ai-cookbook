# gs-admin CLI reference (verified)

Everything here was checked against a live tenant with `@gainsight/gs-admin-cli` 1.0.10 (Oct 2026). If the CLI version you have is newer and something disagrees, trust `gs-admin <command> --help` and tell the user what changed.

Always pass `--json` when you parse output.

---

## 1. Output shapes (they are NOT uniform)

| Command | Records are at | Total count is at | Paging |
|---|---|---|---|
| `report list` | `data.data[]` | `data.pageInfo.totalRecords` | `--limit 200 --page N` |
| `rules-engine rules list` | `data.data[]` | `data.pageInfo.totalRecords` | page size is capped at ~200 no matter what `--limit` says. Stop when you have `totalRecords` rules |
| `rules-engine chains list` | `data.data[]` | `data.pageInfo.totalRecords` | `--limit/--page` |
| `data-management objects list` | `data.liteObjects[]` | `data.totalNumberOfObjects` | `--size 200 --page N` (**`--size`**, not `--limit`) |
| `data-management dropdowns list` | `data.picklistList[].categoryDetails` | `data.totalSize` | `--limit/--page`. **Values are not included.** Run `dropdowns describe --id <category gsid>` and read `data.childItems[]` |
| `journey programs list` | list inside `data` | `data.totalRecords` | `--limit/--page`. Record keys are `advancedOutreachId/Name/Status/Type/Model` |
| `scorecard list`, `scorecard measure list` | list inside `data` | length of the list | `--limit/--page` |
| `query execute` | **bare array** (no envelope) | array length | `--limit N --page N` |
| `report run` | **bare array of rows** (see §3) | n/a | `--limit` (cap 2000) |
| `report list-objects` | **bare array** | array length | none |
| `report describe` | `data` = full saved definition (server shape, §4) | n/a | n/a |
| `data-management objects describe` | `data.columns[]` (fields) | n/a | n/a |

Known problems:
- `data-management objects list-and-describe` returned **zero objects** in testing. Use `objects list` and then `objects describe --name` for each object.
- `query execute` has **no WHERE clause** (only `--select`, `--limit`, `--page`, `--order-by`). For filtered data, use `report run --where-filters`.
- The login token lasts about **1 hour**. On an auth error, stop, ask the user to run `gs-admin login`, then resume.

## 2. Object names: data-management vs. reports

- Data-management commands use names like `Company` and `GsUser`.
- Report commands (`report run/create/schema --object`) use the **BI name**, e.g. `company`, `gsuser`, `call_to_action`. Find it in the `bi_name` column of `schema/_object_index.tsv`, or run `report list-objects`.
- Object names inside `fieldPath.hops[].to` are case-insensitive. Both `gsuser` and `GsUser` worked.

## 3. Building reports: the CLI input shape (verified)

The CLI takes a **simplified** field spec. It is NOT the JSON you get back from `report describe`.

### Plain fields
```
gs-admin report run --object company \
  --show-fields '[{"name":"Name"},{"name":"Arr"},{"name":"Stage"}]' --limit 5 --json
```

### Aggregation and group-by
```
gs-admin report run --object company \
  --show-fields '[{"name":"Arr","aggregation":"SUM"}]' \
  --group-by '[{"name":"Stage"}]' --display-type GRID --json
```
- If group-by is set and a show-field has no aggregation, the CLI picks a default based on the data type.
- Date buckets: add `"summarize":"Day|Week|Month|Quarter|Year"` to a date group-by entry. The value is **case-sensitive** (`"WEEK"` is rejected, even though saved reports store it that way).
  Example: `{"name":"RenewalDate","summarize":"Month"}` produces a column called `summarize_month_of_company_RenewalDate`.
- Pivot: GRID with at least 2 group-by entries and **exactly one** marked `"pivoted":true`.
  Example: `--group-by '[{"name":"ReasonId"},{"name":"TypeId","pivoted":true}]'`.
  **Pivot is GRID-only.** For STACKED_* charts, just give 2 group-by entries; the second becomes the series. Saved stacked reports mark it `pivoted`, but the CLI rejects that with `PIVOT_CHART_NOT_SUPPORTED`.
- `--order-by` entries take the same shape plus `"order":"ASC|DESC"` and `"nulls":"FIRST|LAST"`. Each one **must also appear** in show-fields or group-by.

### Lookup fields (one or more hops)
```
{"fieldPath":{"hops":[{"through":"Csm","to":"gsuser"}],"leaf":"Name"}}
```
- `through` is the lookup field on the current object.
- `to` is the object it points to.
- `leaf` is the field you want on that target.

Add more hop objects for multi-hop paths. Get `through` and `to` from `schema/_lookup_index.tsv`. A dotted string like `"Csm.Name"` is rejected. So is the server-style `{left,right}` object.

### Where filters (pre-aggregation)
```
--where-filters '{"conditions":[
  {"leftOperand":{"fieldName":"Arr"},"operator":"BTW","rightOperand":{"value":[100000,300000]}},
  {"leftOperand":{"fieldPath":{"hops":[{"through":"Csm","to":"gsuser"}],"leaf":"Name"}},"operator":"IS_NOT_NULL"}
]}'
```
- Conditions are joined with **AND**. Do not pass `alias` or `expression`; the CLI assigns them. For OR or nested logic, save the report, run `report update --where-filters`, then use `report run-saved`.
- Dates: absolute values work, e.g. `"operator":"BTW","rightOperand":{"value":["2026-10-01","2027-03-31"]}` or `"GTE"` with `"2026-10-01"`.
- ⚠️ **Relative dates (THIS_QUARTER, NEXT_N_QUARTERS, LAST_N_WEEKS…) failed in every form tried through `report run`.** Work out absolute dates from today instead, and tell the user that a saved report will then be fixed to those dates rather than rolling. For a rolling filter, the user can set it in the report builder UI after you create the report.
- ⚠️ **Picklist values must be the value's GSID, not its label.** Filtering `Stage EQ "2. Implementation"` silently returns **0 rows**. Filtering on the value's GSID (e.g. `1I00…`) works. Look up GSIDs in `config/dropdowns.tsv` (`value_gsid`). A 0-row result on a picklist filter almost always means this mistake.

### Having filters (post-aggregation)
Same shape as where filters, except `leftOperand.key` is the aggregated `fieldAlias` (e.g. `sum_of_company_Arr`) and each condition needs `aggregateFunction`.

### Display types
`GRID` (use this when you want rows back), `KPI`, `BAR`, `COLUMN`, `STACKED_BAR`, `STACKED_COLUMN`, `LINE`, `AREA`, `PIE`, `DONUT`, `COLUMN_LINE`, `HEATMAP`, `FUNNEL`, `GAUGE`, `SCATTER`, `BUBBLE`, … Chart types return a chart `configuration` payload, so run as `GRID` when you only need numbers. The CLI checks that the show-field and group-by counts are valid for the chart type you pick.

### Reading `report run` results
A bare array of rows. Each key is a column alias and each cell is `{k, v, fv}`:
```
{"company_Stage": {"k":"1I00…","v":"2. Implementation","fv":"2. Implementation"},
 "sum_of_company_Arr": {"k":1250000,"v":1250000,"p":"USD","fv":"USD 1,250,000"}}
```
- `v` is the raw value, `fv` is formatted, and `k` is the key/GSID (for picklists, it is the GSID you filter on).
- Alias patterns: `<object>_<field>`, `<agg>_of_<object>_<field>`, and for lookups `<targetobject>_<lookup>__gr_<leaf>` (e.g. `gsuser_Csm__gr_Name`).

### Saving
`report create` takes the same flags as `report run`, plus `--name` (must be unique in the tenant), `--display-type` (required), and `--folder-id` (default 2; system folders are not allowed). **It is a write**, so follow the write gate in `CLAUDE.md`. Always get the same flags working with `report run` first.

## 4. Translating a saved report (`report describe`) into CLI flags

| Server shape (from `describe`) | CLI input |
|---|---|
| `showFields[].fieldName` | `{"name": fieldName}` |
| `showFields[].expressionDetails.expression.key` = `SUM`/`COUNT`/`AVG`/… | add `"aggregation": key` |
| `expression.key = "summarize"` with value `WEEK` | add `"summarize": "Week"` (title case) |
| `groupByFields[].pivoted = true` on a non-GRID chart | drop `pivoted`; the 2nd group-by is the series |
| `fieldPath: {left:{fieldName:K, objectName:T}, right:{fieldName:L, objectName:S}}` + `fieldName: F` | `{"fieldPath":{"hops":[{"through":L,"to":T}],"leaf":F}}` |
| `groupByFields[]` (with `pivoted`, `rowGrouped`) | `--group-by` entries, same rule |
| `orderByFields[].orderByInfo: {order, nulls}` | `--order-by` entry plus `"order"`, `"nulls"` |
| `whereFilters.conditions[]`: `leftOperand.fieldName`, `comparisonOperator`, `filterValue.value` | `{"leftOperand":{"fieldName":…},"operator":…,"rightOperand":{"value":…}}` |
| `whereFilters.expression` with OR | can't be passed to `run`/`create`. Save first, then `report update` |
| `reportDisplayType` | `--display-type` |
| `sourceDetails.objectName` | `--object` |

`python3 scripts/snapshot.py exemplar <reportId>` does this translation for you and proves it with a `report run` (nothing is saved). Each exemplar in `tenants/<tenant>/exemplars/reports/` contains the translated command, whether it ran, and anything that could not be carried over.

## 5. Other read commands worth knowing

| Need | Command |
|---|---|
| What depends on an object (reports, rules, JO, scorecards, C360…) | `data-management dependencies check --name <Object>` |
| Full rule definition (source, criteria, actions) | `rules-engine rules describe --id <ruleId>` |
| Fields a rule's source makes available | `rules-engine rules list-task-outputs --rule-id <id>` |
| Rule run history | `rules-engine rules executions --id <ruleId>` |
| JO program step structure | `journey programs describe --id <id>` |
| Pre-publish checks (read-only) | `journey programs validate --id <id>` |
| CTA types/reasons/statuses/priorities as IDs | `journey cta options` |
| Email template tokens | `journey email template --id <id>` |
| BI field metadata incl. lookups for one object | `report schema --object <bi_name>` (large; extract what you need) |
| Run a saved report | `report run-saved --id <id>` (read-only) |
