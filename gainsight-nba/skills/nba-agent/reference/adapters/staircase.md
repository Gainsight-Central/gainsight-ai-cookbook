# Adapter: staircase

Maps the `context` capability to the Staircase AI MCP. Tool names are suffixes.

| Need | Tools (suffix) |
| --- | --- |
| Resolve the account | `staircase_account_lookup` (pass the account name as `name`) |
| Stored fields: summary, health, sentiment, churn, renewal, risk, expansion, owner, tier, revenue | `staircase_account_info` |
| What the account said about a topic, from emails, calls, tickets, meetings | `staircase_analyze_account` |
| Full text of one evidence item you plan to use | `staircase_fetch_evidence` |
| Recent threads for one account (last 90 days, then 180) | `staircase_analyze_account` with a date-bounded question, then `staircase_fetch_evidence` on each item you will use |
| A topic across accounts (theme scan for the "not sure" path) | `staircase_semantic_search`, `staircase_query` |

## Behavior seen on a real tenant (2026-10-07)

- `staircase_semantic_search` returned about 117,000 characters, over the output limit, and was saved to a file. It cannot filter by CSM or book. An unscoped topic search over 100 rows returned only 3 from one CSM's 30-account book.
- To scope to a book, resolve each account with `staircase_account_lookup` and search within those accounts. That costs one lookup per account, so apply it to the top `ground_top_n` accounts, not the whole book.
- Scoped search works. Passing the resolved `account_ids` of a 30-account book (28 resolved) with a 12-month range returned 300 rows over 3 calls, all inside the book, and 25 of the 28 accounts had at least one hit. The unscoped search found 3 of 100.
- Each call returned 100 rows and overflowed the output limit (about 105,000 characters). Use a smaller `limit`, split the account list, or narrow the date range, and handle saved files with a script or a subagent. A subagent's hand tally is a lower bound: check its counts against the file.
- `per_account_limit` of 5 did not cap rows per account (one account returned 17). Cap per account yourself.
- Topic terms matched nothing in these calls (every row matched on text only, with an empty topic). Rely on text terms, and do not report a topic match.
- The search returns no total, so report "N rows scanned", not a share of all rows.
- Lookup can return several high-confidence matches (one account returned four). Use the exact-name match and say you did. Two accounts returned `no_data` even with a shorter name. List them as not resolved and do not search them.
- Fetched video evidence carries no date. Take the date from the search row and say so.
- Search rows carried no topic labels. Do not invent theme names. See the adoption use case.
- `staircase_query` returned no data for an open question about adoption themes. Prefer account-scoped tools.

## Rules

- Ground a claim on `staircase_account_info` fields or on evidence you fetched. A summary is not quotable. Fetch the evidence before you rely on its wording.
- Apply the tied-to-recipient rule in SKILL.md guardrail 4. Evidence from another contact informs the action. It never appears in the email.
- Write tools do not exist here. Do not look for any.
- `staircase_account_lookup` resolves by name only. It does not find accounts by topic.
- Scoped topic search: put text terms and topic terms in the same call. A scoped topic search alone often returns nothing.
