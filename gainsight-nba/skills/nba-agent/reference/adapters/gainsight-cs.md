# Adapter: gainsight-cs

Maps capabilities to the Gainsight CS MCP. Tool names are suffixes. Preflight matches them to whatever connected server exposes them.

| Capability | Tools (suffix) | Notes |
| --- | --- | --- |
| `identity` | `resolve_user` | Look up by email, then by name. If neither resolves, ask which CSM to run for. The result may carry the user's id (GSID) and no email. Say when the email match could not be verified. `resolve_user` needs a person's name (never "me"). `get_portfolio_filters` returned no user identity on 2026-10-08. The signed-in user cannot be read from this server, so setup uses a name or email from the chat or asks once. |
| `book` | `run_query`, `get_records` | Query `company` where a CSM field equals the resolved CSM's id and the account is active (see Book rules below). Do not use `get_portfolio_filters` to find another CSM's book: it returns the signed-in user's filters, not the named CSM's. Ranking in one `run_query`, not per account. |
| `contacts` | `resolve_customer`, `run_query`, `get_records` | Resolve the account, then query `company_person` (see Contacts below). `fetch_customer_contacts` failed on every call on the test tenant. Do not rely on it. |
| `goals` | `fetch_success_plan_list`, `fetch_cta_list`, `get_records`, `run_query` | Success plan objectives and open adoption-type CTAs. If the Customer Goals object is not known, find it with `get_object_metadata` or ask the CSM which object holds it. Do not guess. Keep goal text verbatim. |
| `signal` | `ask_scorecard`, `run_query`, `fetch_report_data`, `report_search_tool`, `get_records` | Scorecard measures first. Then a custom adoption object or report named in config. Use `report_search_tool` to find an existing adoption report. |
| `context` (timeline part) | `fetch_timeline_activity_list` | Notes and activities that mention the goal topic. |

## Scope fields (declared, not probed)

The goal check may offer these scopes on this adapter. Field names are tenant-specific: find them from the `company` object's metadata, and say which you used. Do not write a field name from another tenant.

- Renewal window: the renewal date on the `company` object.
- Health band ("red", "at risk"): the scorecard's overall label and color for the account, read through `ask_scorecard`, one company at a time. Use the tenant's own band names.

Not yet verified on a real tenant. If the metadata does not show a renewal date, say so at the goal check.

## Catalog probe (setup step 1, item 4)

Not yet verified on a real tenant. Run it and say what each call returned. Do not fill a gap from this list.

- Metrics: look first at scorecard measures (`ask_scorecard`, one company at a time), then at numeric usage fields on `company` (read the field list from a small `run_query`, or grep the saved `get_object_metadata` file), then at any adoption report `report_search_tool` returns by name. A field earns a catalog entry only if a query returned a value for it. Sample up to 5 accounts from the CSM's book, one `ask_scorecard` call per account. Say how many of the sampled accounts had a value, and whether the field carries a timestamp.
- Segments: from the same `company` field list, pick fields that group accounts (picklists first). Read values with `get_picklist_values` and count accounts per value with one `run_query` per field, filtered to the CSM's active book.
- Do not read `get_object_metadata` on `company` into the chat. It is about 85,000 characters. Save it and search it.
- If a call fails (see the errors below), record the capability as not probed and say so. Do not record it as not found.

## Behavior seen on a real tenant (2026-10-07)

- Every tool requires `originating_user_query`. Pass the user's latest message verbatim.
- `get_object_metadata` on `company` returned about 85,000 characters, over the output limit, and was saved to a file. To find the CSM field, grep that file, or use `run_query` with a small select list. Do not read the whole response into the conversation.
- `fetch_success_plan_list` returned 57,000 characters for one page of 50, with `has_more: true` (131 plans across 3 pages). Read the saved file with a script or grep. Page until `has_more` is false, or say how many pages you read.
- `ask_scorecard` (170,000 characters for 10 companies), `report_search_tool` (280,000), and `fetch_cta_list` (90,000) also exceeded the limit. Ask for one company at a time, filter by name or date, and handle saved files with grep or a script.
- `report_search_tool` returns report names and descriptions but no report ids, so a found report cannot be run with `fetch_report_data` without another lookup. Say so and fall back to the company fields or the scorecard.
- `fetch_timeline_activity_list` failed with `P_5068 Invalid Lookup name` when filtered on `CompanyId__gr.Csm`. Filtering on `CompanyId` IN a list of resolved account ids worked. It returned subjects only, so it carries little goal evidence.
- `fetch_customer_contacts` failed with the same internal error on 9 of 9 calls (4 argument shapes, 4 accounts). The cause is unknown. Use the `company_person` query below.
- The `goals` capability read only success plans in that run. Open adoption-type CTAs and timeline notes were not read. Say which sources a scan covered.

## Contacts (verified on a real tenant, 2026-10-07)

Query `company_person` with `run_query`, filtered on `Company_ID` equal to the account's id. A `select` that names fields the object does not have fails with `P_5068`, so use these:

| Need | Field |
| --- | --- |
| Name, email | `Person_ID__gr.Name`, `Person_ID__gr.Email` (a lookup to `person`. Email is not on `company_person`.) |
| Title, role | `Title`, `Role`, `role0__gc` (post-sales role), `secondary_role__gc` |
| Can they log in | `License_Type__gc` (values seen: Viewer, Full, Internal_Collaborator, External, Viewer_Analytics), `CS_Super_Admin__gc`, `Likely_Admin__gc` |
| Last login (likely) | `Last_Seen__gc`. Treat as a likely login date, not confirmed. |
| Opt-out and contactability | `hasoptedoutofemail__gc`, `copilot_unsubscribed__gc` (labeled Do Not Contact), `outreach_opt_out__gc`, `isemailbounced__gc`, `no_longer_at_account__gc`, `Active` |
| Relationship | `Relationship_Contact__gc`, `Products_Currently_Used__gc` |

- Picklists return ids plus a `_PicklistLabel` field in the response. You cannot select the label field. Selecting `Role_PicklistLabel` failed with `P_5005`.
- One account had 468 rows. The `run_query` result already holds the first 50, so start `get_records` at page 2 (starting at page 1 repeats those rows). The page size is capped at 50 even if you ask for 100. Each page of 50 is about 54,000 characters and exceeds the output limit, so it is saved to a file. Filter in the query (`Role IS_NOT_NULL`, `License_Type__gc IS_NOT_NULL`) when you can, and say how many rows you read and how many exist.
- `Last_Seen__gc` is an empty string, not null, when the person was never seen. `IS_NOT_NULL` does not select seen people. Test for a non-empty value.
- Role values seen on one tenant: Gainsight Admin, Adoption Champion, Decision Maker, Sales Decision Maker, Customer Success, Community Manager, Unknown (Default), Not Licensed, No Longer at Company. The set is tenant-specific. Map them to the use case's recipient roles yourself and state the mapping. A "No Longer at Company" role and the `no_longer_at_account__gc` flag may disagree, so apply both.
- Whether Viewer, Viewer_Analytics, Internal_Collaborator, and External licenses can log in is not confirmed. One ticket says Internal_Collaborator cannot. Only treat Full as able to log in, and say that you did.
- Opt-out is mostly null, not false: 358 of 468 on one account. Treat null as unknown. Only true is a block, and the opt-out source in config decides the rest.
- The same query worked on a second account. That account's rows had no title or role.
- Duplicates and mismatches exist (two records for one person, a name that does not match its email, shared mailboxes such as an AP inbox, Gainsight staff, and people marked no longer at the company). Flag these. Do not pick them silently.

## Book rules (checked on metadata, 2026-10-08)

The `company` object on the test tenant has more than one CSM field and several active-state fields. The first book query read only the standard `Csm` field and no active state. A scale-segment CSM tester then saw 77 accounts, 61 of them under their name, when they said only 3 are theirs. The cause was not confirmed: `run_query` returned an internal error on every call that day, including a plain two-field query, so the counts could not be run.

| Need | Fields seen on the tenant |
| --- | --- |
| The CSM | `Csm` (standard lookup to `gsuser`), plus product CSM lookups: `CE_CSM__gc`, `IN_CSM__gc`, `ST_CSM__gc`. `Owner__gc` is the account owner, not the CSM. |
| Active state | `Status` (Active, Inactive, Churn), `ManagedAs` (Customer, Ex-Customer, Prospect, Partner), `Status_Detail__gc` (Active Customer, Churned Customer and others), and `Stage` (values include 8 Debooked and 9 Churned). |
| Segment | `CS_Segment__gc` and product segment fields (values include Scale, Enterprise, Strategic). |
| Products bought | `Purchased_Products_for_MP_O2_Process__gc`, a multiselect (CS, CC, CE, ST, Skilljar, and others). Use it, and the product type on relationships, for the product fit check. A blank value means unknown, not none. |
| Relationships | The `relationship` object, with a type (Product, Professional Services). |

These names are for this tenant. Find them from the metadata on any other. To count per field, run one query per CSM field and filter on active state. If the response is too large, read the saved file with a script. The signed-in user is named in `current_user_info` on a `resolve_user` response (seen once, 2026-10-08).

## Health band for the review card

The review card colors the health gauge with the tenant's own band. Call `ask_scorecard` with `company_ids` for one account at a time. Checked on a real tenant on 2026-10-08, one account:

- `scorecard.overall_score` and `scorecard.overall_label` hold the overall score and band label (38, "Orange").
- The band color and range are not on `scorecard`. Read them from the entry in `measures_flat` with `level_type` `ROLLUP` and no parent: `score_color` (a hex, `#ff8f00`), `score_range_from` and `score_range_to` (30 and 50), and its `score_modified_at` for the date.
- Bands seen on that tenant: Red 0-30, Orange 30-50, Yellow 50-75, Lime 75-85. The Yellow color was `#ffcc80`, a pale amber. Use the returned hex as is. This tenant's Lime band ends at 85, not 90, so do not assume the standard scale.
- `no_scorecard_assigned: true` means no score. Show the dash, not a gauge.
- The response for one account was about 25 KB because of `measures_flat`. Ask for one account per call. If it goes to a file, read only the ROLLUP entry.

If the tool returns no band, the card falls back to the standard scale in `design.md`.

## Rules

- Read tools only. Do not call `create_timeline_activity`, `update_timeline_activity`, `manage_cockpit_actions`, or `manage_success_plan_actions`.
- Score color: use the band the scorecard returns. Do not set your own cutoff.
- If a field the use case needs is not in the response, use `get_object_metadata` to find it, then `run_query` or `get_records`.
- Empty or demo tenants return little. Say so and continue.
