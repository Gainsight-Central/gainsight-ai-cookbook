# Adapter: gmail

Maps `mail` and, on surfaces with no filesystem, `ledger`. Gmail is the user's own connector. This plugin does not bundle it.

| Need | Tools (suffix) |
| --- | --- |
| Create a draft | `create_draft` |
| Edit a draft | `update_draft`, `get_draft` |
| Send (guarded, see `steps/send.md`) | `send_message` |
| Tag drafts and sent mail for the ledger | `create_label`, `label_message`, `label_thread`, `list_labels` |
| Read the ledger back | `search_threads` on the label |

## Rules

- Default action is `create_draft`. Sending is a separate, guarded step.
- Test-send goes to `csm_email` only, subject prefixed `[TEST] `.
- Label every draft and sent message `gainsight-nba`, plus `gainsight-nba/<use case id>`. On a chat surface this label is the ledger. Edited drafts get `gainsight-nba/edited`.
- Earlier versions (up to 0.1.34) used `nba-agent`, `nba-agent/<use case id>` and `nba-agent/edited`. When reading the ledger back, search both the new and the old label. Write only the new one. If a draft carries the old label only, count it as handled for the frequency cap and do not relabel it.
- Keep label names lowercase with hyphens. Gmail rewrites spaces and capitals in a label search, and a search that returns nothing would turn the frequency cap off without a warning. If `create_label` fails, say so and mark the frequency cap unavailable.
- Do not delete, trash, forward, or reply to any message. This adapter does not need those tools.
- Recipient timezone is not a Gmail field. Take it from `compliance.timezone_source`.
