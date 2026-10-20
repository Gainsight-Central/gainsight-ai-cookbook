# Use-case contract

A use case is a folder under `reference/use-cases/<id>/` with a `usecase.md` that fills in every field below. The shared steps read these fields. They hold no use-case logic of their own.

To add a use case (onboarding, renewal, churn risk, expansion): copy this contract, fill every field, add the folder, add a row to the table in SKILL.md. Change nothing else. If a use case needs something this contract cannot express, extend the contract here first.

## Fields

| Field | What to declare |
| --- | --- |
| `id`, `version`, `requires_schema` | Folder name, use-case version, minimum config `schema_version` |
| `trigger` | `threshold` (a signal crosses a value), `event` (a date or milestone such as a renewal date or go-live), or `manual` (a list the user gives) |
| `unit` | `user` or `account`. One draft per unit. |
| `recipient_rule` | Who gets the email. For example low-usage users, the economic buyer, the champion. |
| `goal_schema` | The fields a goal has (metric, threshold, window, scope), how "not sure" is handled, and how each part is checked against the config `Catalog` before the confirm (see `steps/goal-check.md`) |
| `capabilities` | Each capability from `capabilities.md` marked required or optional for this use case, with the fallback |
| `discovery` | Where to look for discussions of the goal, in capability terms (for example `goals`, `context`), and what counts as a match |
| `signal` | What to measure, how to rank the cohort in one query, how to cap it |
| `grounding_questions` | What to ask `context` per account. Include exclusion rules (for example, skip accounts with an open escalation). |
| `actions_allowed` | Any of: `email_draft`, `sequence_step`, `cta_proposal`, `internal_note`. Anything other than `email_draft` is a proposal shown to the CSM. The agent never writes it to a system of record. |
| `draft_intent` | Purpose, length, the one ask, what the email anchors on (a feature, a renewal date, a value recap) |
| `funnel_stages` | Ordered stage names. Each maps to the step that produces its count. |
| `status_badges` | Badge names and the retrieved fact that earns each one |
| `cadence` | `one_shot` or `sequence`. A sequence needs the `ledger` capability. |
| `outcome_metric` | What the final dashboard reports as the result for this use case |
| `evals` | Path to this use case's eval fixtures |

## Checks before a use case is accepted

- Every field is filled. A field that does not apply says `n/a` with a reason.
- No tool names appear. Capabilities only.
- Every status badge names the retrieved fact that earns it.
- If `actions_allowed` has no `email_draft`, the draft step and the mail buttons are skipped. The review step shows the proposals instead.
