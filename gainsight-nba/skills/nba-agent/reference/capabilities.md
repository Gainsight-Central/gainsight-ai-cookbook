# Capabilities

Steps never name a tool. They call a capability. `.nba-agent/config.md` maps each capability to an adapter, a file, or `none`. An adapter file in `adapters/` says which tool does the work.

Adapters are written by tool suffix (the last part of the tool name), not by full tool name. The full name depends on how the server is connected: a claude.ai connector looks like `mcp__claude_ai_<server>__<suffix>`, a plugin server looks like `mcp__plugin_<plugin>_<server>__<suffix>`. Preflight lists the connected tools and matches by suffix.

## The nine capabilities

| Capability | Purpose | Returns | Default |
| --- | --- | --- | --- |
| `identity` | Resolve the current user to a CSM record | CSM id, name, email, role | required |
| `book` | List the CSM's accounts | account id, name, owner, ARR if available, products owned if available | required |
| `contacts` | Contacts for an account | name, email, title or role, opt-out flags, license or user type and last login if available, timezone if available | required |
| `goals` | Recorded customer goals and plans | goal text verbatim, account, source, date, status | optional |
| `signal` | The metric the use case tracks | per account (or per user) value, threshold flag, source | required |
| `context` | Account context for grounding | health, sentiment, recent communication themes, risk flags, each with a source id | optional |
| `knowledge` | What can be recommended, in the customer's own words | feature or offer name, one-line value, gap it addresses, source URL | required |
| `mail` | Create drafts, and send when allowed | draft id, send result | optional |
| `ledger` | Record of what the agent drafted, sent, edited | rows read and appended | optional |

## Required and optional

- A required capability set to `none` blocks the run. Preflight says which one and asks the user to map it.
- An optional capability set to `none` degrades the run. Each degradation is stated on screen, never hidden.

| If this is `none` | The run does this |
| --- | --- |
| `goals` | Skip goal-scoped discovery. Run discovery against the `signal` instead and label rows "no recorded goal". |
| `context` | Ground each draft on `signal` and `knowledge` only. Label every row "context not available". |
| `mail` | Show each draft in chat for the CSM to copy. No mail buttons. |
| `ledger` | Frequency caps and edit rate are marked "unavailable". The dashboard covers this run only. |

## Capability rules

- Every returned fact carries a source (tool, record id, or URL). Grounding depends on it.
- `contacts` must return an opt-out flag or the run treats the opt-out source in `compliance` as the only filter.
- `signal` must be ranked by one query where the source allows it. Do not call a tool per account across a large book.
- `mail` and `ledger` are the only capabilities that write. Nothing else writes anywhere.
