# Adapter: mail-generic

Maps `mail` for any connected mail tool that has no adapter of its own (Outlook, Microsoft 365, or another mail connector). It was written from the capability contract, not from a tested tool. Its tool names are unknown until a tool is matched, so the first run on a new tool is a test. Say so.

## What a tool must offer

| Need | Required | What to look for in the tool's schema |
| --- | --- | --- |
| Create a draft | yes | A tool that creates an email draft and does not send it. Inputs: to, subject, body. Returns a draft id or link. |
| Edit a draft | no | A tool that updates a draft by id. |
| Tag or label | no | A tool that adds a label, category, or folder to a draft. Needed only to use the mail tool as the ledger. |
| Send | never used | Do not call a send, reply, or forward tool. |

Match by what the tool does, read from its description and input schema, not by its name. A tool whose description says it sends and cannot save a draft does not qualify.

## Detection and confirm

1. At preflight, if the `mail` capability has no adapter match, look through the connected tools for one that creates an email draft.
2. If exactly one qualifies, ask one question: "Mail: I matched <tool>. Use it to create drafts? Nothing is sent." with options "Use <tool> (Recommended)" and "No mail tool, show drafts to copy". Save the answer as `mail: generic` and `mail_server: <server>` in config.
3. If more than one qualifies, ask which one in that question, with the candidates as options.
4. If none qualifies, set `mail` to `none` and say so. Drafts show in chat for copying.

## Rules

- Drafts only. No send, no test send, no reply, no forward. There is no send guard for this adapter, so `send_enabled` has no effect on it. Approve & send is shown disabled, with the reason: "No send guard for <tool>".
- Create each draft at the batch step in `steps/send.md`, with the recipient, subject, and body exactly as approved. Never report a draft as created without an id or link returned by the tool.
- Tag drafts with `gainsight-nba` only if the tool supports tags. Without tags, the mail tool cannot be the ledger: use the file ledger, or say the frequency cap was not checked. Do not claim it was.
- Do not delete, move, or edit any message the agent did not create.
- Recipient timezone is not a mail field. Take it from `compliance.timezone_source`.
- If a call fails, stop, say which draft failed and which were created, and offer the copyable list for the rest.
