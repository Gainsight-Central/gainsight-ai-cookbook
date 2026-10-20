# Step: data (signal, book, contacts)

Capabilities used: `book`, `signal`, `contacts`. The use case supplies the signal definition and the unit.

## 1. Scope

The default scope is the CSM's `book`. If the discovery step narrowed it to accounts that raised the goal, use that list. If the user names an account or segment, use that.

**Build the book from three rules, and say them.**

1. **Owner.** An account belongs to the CSM through the fields that name a CSM. A tenant can have more than one (a main CSM and product-specific CSM fields). Find them from the object's metadata, not from a list in this file, and count the CSM's accounts under each. Use `book.owner_fields` from config when it is set.
2. **Active only.** Leave out accounts that are churned, inactive, ex-customers, or at a churned or debooked stage. Use the fields the metadata offers (a status, a managed-as value, a stage) and say which you used. `book.active_filter` holds the answer once confirmed. Say how many you left out.
3. **Level.** Accounts first. Relationships (a product or business unit under an account) only if the tenant has relationship records with a CSM and the user asks for them, or `book.include_relationships` is true.

**Confirm once.** On the first run, before ranking, ask the book question from `reference/questions.md` with the counts and five account names inside it. The CSM is the only one who knows which accounts are really theirs. Save the answer to `book` in config. Skip the question on later runs and state the rule in one line instead.

**A named segment.** If the user names a segment (for example Scale), filter on the segment field the metadata offers and say which field.

**Say it in the funnel.** The Book tile carries the number of active accounts. The line under the funnel says the owner field and how many were left out as churned or inactive.

**Never page through an unchecked list.** If the book is over 100 accounts, say so and ask for a segment, a named customer, or the goal's accounts first.

## 2. Signal

Run the `signal` definition from the use case.

- Rank the whole scoped cohort with one query or report where the source allows it. Do not call a tool per account across a large book.
- Keep the top `ground_top_n` accounts (config, default 25) for the later steps. Report how many were ranked and how many were cut.
- Record for each account or user: the value, the threshold it crossed, and the source.
- If the source returns nothing for this signal, say so and ask the no-signal question from `reference/questions.md`. Do not make up a signal.

## 3. Contacts

For each kept account, get `contacts`. Apply the use case's `recipient_rule`.

- Reconcile the signal's user list with the contact list. Report mismatches.
- For an account-level signal, follow Choosing recipients in the use case. Ask the recipients question from `reference/questions.md`, with each candidate's name and role inside the question, before drafting. Do not start the next step until it is answered.
- Drop contacts with no email, an opt-out flag, or a match in the suppression list.
- Drop contacts that break the frequency cap. Read the ledger. If `ledger` is `none`, say the frequency cap is unavailable.
- On a re-run of the same goal, say how many flagged contacts are new since the `## Last run` date and how many were left out because the ledger shows them handled inside the cap. With no ledger, say you cannot tell which are new, and do not claim any are.
- Keep the opt-out and timezone fields. The send step needs them.
- Note who was skipped and why. Show this the first time the counts appear, not on every draft.

## Output

Matched recipients with real email addresses, the signal value that flagged each, its source, and the skipped list with reasons.
