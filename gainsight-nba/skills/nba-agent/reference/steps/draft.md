# Step: draft

Inputs: `style.md`, `rules.md`, the use case's `draft_intent`, the grounded facts and recommended item from `ground.md`.

## Rules

- Write one email per unit the use case names, to the recipient the `recipient_rule` selects.
- Follow `style.md`. Apply every item in `rules.md` as a hard constraint.
- Follow `draft_intent` for purpose, length, the one ask, and what the email anchors on.
- Reference only facts from the data and ground steps. The email body states only `sourced` facts. An `inferred` point may shape which item you pick and never appears in the body as a statement about the recipient or their account. Drop it, or turn it into a plain question to the recipient only if the CSM asks for that.
- The one ask is the item's link or a next step the CSM's rules allow. Do not offer a meeting, call, demo, deadline, discount, or any commitment of the CSM's time unless `rules.md` allows it.
- Do not state the customer's product, plan, license, role, segment, or usage history unless a `sourced` fact says so.
- Open with the thread from `ground.md` when one exists: one line, in the customer's terms, citing nothing the recipient was not part of. Then the value of the recommended item for their gap. Then one ask. With `thread: none`, write no acknowledgement and imply no history.
- Name people by name. Never use a gendered pronoun for the recipient or anyone else unless a source states it.
- Do not state that something is done, scheduled, or promised unless a fetched source says so.
- Write in the language set in `compliance.language`.
- Subject line: specific, names the value or the item. No "Quick question."
- Sign as the CSM from `identity`. If the CSM name is missing, leave a placeholder for the CSM to fill.
- Keep the writing rules in `style.md`. If the customer has none, use plain sentences, active voice, no em dashes.

## Test first (large cohorts only)

- Cohort of 5 recipients or fewer: no sample step. Draft all of them, then go to the funnel in `review.md`. The review is the only time the CSM sees the drafts.
- Cohort of more than 5: write 3 of the drafts first as a tone check, then ask one question. Call it the **tone check** everywhere. Never call it "samples" in one place and "previews" in another, and never state a count twice in different words.
- The previews go **inside the question**, not in chat text above it. A question dialog can hide the text above it, and a CSM who sees only the dialog must still see the previews. Put each preview on its own short line in the question: number, recipient and account, subject, and the first sentence (at most 120 characters). Three lines, nothing else. Follow the Tone check template in `reference/questions.md`.
- If there is no dialog tool, print the same three lines and the question in one message, as one block.
- Do not show a full draft card, and do not repeat the previews as chat text before or after the question.
- Say once, in the question, that these drafts will appear again in the review queue. Mark them `Sample reviewed` there. Do not ask for tone again.
- Draft the rest only after the user says yes. If they ask for changes, redo the three first and ask again once.
- Never show the full drafts of the whole cohort before the funnel.

## Fact check (before showing any draft)

Read the finished body one sentence at a time. For every sentence that says something about the recipient, their account, their usage, their history, or the product they have:

1. Find the matching bullet in the draft's Grounded on list, with its source.
2. If there is none, the sentence is unsupported. Remove it or rewrite it as a statement about the feature only (what the item lets anyone do).
3. If the email no longer works without it, set `Grounding incomplete`, say what is missing, and do not show it as a ready draft.
   If what is left is only a follow-up on the thread, first try one rewrite around a single sourced item from `knowledge` that fits the gap and the account's products. If none fits, show it with the label "Thread follow-up only, no feature". That label is never shown with `High confidence`.
4. Check the recommended item's product against the account's products (`ground.md`, Product fit). Config's `products` is the vendor's list, not the account's.
5. Check the ask. A meeting, call, demo, or deadline in the body is unsupported unless `rules.md` allows it.

Record what you removed, as a count. The card shows "Left out: N unsupported points". Do not paraphrase an inferred point into the body to get around this.

## Each draft carries

- To (name, role), subject, body, sign-off.
- A **Personalization** line: the thread acknowledged, with date and source, or "thin" when there was none.
- A **Grounded on** list: every fact, tagged `sourced` or `inferred`, matching the body exactly.
- The status badge the use case defines.

## Caps

Stop at `draft_cap_per_run`. If more recipients qualify, say how many were left out and offer a second run. At most one email per person per run.
