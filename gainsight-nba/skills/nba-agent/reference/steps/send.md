# Step: send (mail drafts and sends)

Capability used: `mail`, and `ledger` to record. The adapter file for the configured mail tool names the exact calls.

## Default: Approve, then create drafts in one batch

Approving a draft in review writes nothing. Mail drafts and ledger rows are written at the batch step.

### Batch step

Run it when the queue is empty and at least one draft is approved, or when the CSM says "create drafts now".

1. Ask one question (`questions.md`, Create drafts) that lists each approved recipient with account and subject, and the cap check result. If the earlier agent threads could not be read, say so here, once, and that the per-person frequency cap was not checked.
2. "Create N <mail> drafts": create each draft through the adapter. Do not send. Write a ledger row per draft: run id, recipient, account, use case, subject, `edited`, `accepted_unedited`, `approved_in_bulk`, draft id, timestamp, `status: drafted`. Then give one confirmation that lists each draft as recipient, subject, and "in <mail> drafts", says nothing was sent, and names the folder or label to look in.
3. "Show copyable list": show each approved email as its own block (To, subject, body) for the CSM to copy. Write the ledger row as `status: shown`. Say no mail draft was created.
4. "Not now": write nothing. Say N approved drafts are not in the mail tool, and that "create drafts now" runs this step again in this chat.
5. If `mail` is `none`, skip the question and go to the copyable list.
6. If a draft fails to create, stop, say which one failed and which were created, and offer the copyable list for the rest. Never report a draft as created without a returned draft id.

Rejected drafts get a ledger row `status: rejected` when the CSM rejects them. After the batch, go to the dashboard.

## Test send

The CSM may send one draft to their own address (`csm_email` in config) for QA. Subject prefixed `[TEST] `. Needs the CSM's explicit confirmation of that specific draft. Never a batch. Never to anyone else. This is allowed with `send_enabled: false`, only for a mail adapter the guard covers (today, the Gmail adapter) on a surface where the guard is active. Pass the CSM address in `to` on the call. Do not send by draft id, the guard blocks a call that names no recipient.

The guard hook covers Gmail `send_message`, `reply`, and `forward`. For any other mail tool (Outlook, for example, through `adapters/mail-generic.md`) there is no guard, so allow no sends at all, test-send included. Create drafts only.

What the hook enforces: the `send_enabled` flag, and CSM-only recipients for a test-send. Caps, quiet hours, suppression, and the batch confirmation are instructions you follow. Say this when the user asks how safe sending is.

## Approve & send (off by default)

Available only when all of these hold:

1. `send_enabled: true` in config.
2. The send guard is active: the skill loaded from the plugin install path, the mail tool is Gmail, and the surface runs hooks (see preflight in SKILL.md). Otherwise refuse and say why.
3. `compliance.opt_out_source` is set and was read this run.

Before any send, show one confirmation for the batch:

- Recipient count and the list (name, email, account).
- If `allowed_basis` is not set, ask for it now: "Sending: what is your basis for emailing these contacts?" Options: `Existing customer relationship (Recommended)`, `Other basis (name it)`. Save it. The agent does not say it is legally sufficient.
- If `region` is not set, ask for it now: "Sending: which regions are the recipients in? The agent saves this and does not check regional email law." Options: `US`, `EU or UK`, `More than one region`, `Other region`. For the last two, ask one open follow-up to name the regions. Save a list. Nothing in the skill changes by region. If the answer is not a single US, add the line: "Regional email rules are not checked. Confirm the basis with your compliance team."
- If `timezone_source` is not set, ask for it now (one question: a contact field, an account field, or one fixed timezone) and save it. Then each recipient's local time against `quiet_hours`. Move any that fall outside to a later batch.
- The cap check: `draft_cap_per_run` and the per-person frequency from the ledger.
- Suppression and opt-out result: how many were removed.

Send only after the CSM answers yes to that confirmation. A general "looks good" earlier does not count. Then send each message through the adapter, write a ledger row with `status: sent`, and report the result per recipient. If any send fails, stop the batch and report where it stopped.

## Never

- Send to a recipient who was not in the confirmed list.
- Send during quiet hours.
- Send to an opted-out or suppressed contact.
- Retry a failed send without telling the CSM.
