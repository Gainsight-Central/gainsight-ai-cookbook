# Step: review (funnel, drill-down, approve, dashboard)

Stages and badges come from the use case (`funnel_stages`, `status_badges`). This file defines how they render and behave.

## Rendering

Read `reference/design.md` before the first widget of a run. It holds the tokens, colors, icons, component styles, and the render flow. This file sets layout and sequence only. Where the two conflict on styling, `design.md` wins. Where they conflict on layout or sequence, this file wins, including the text fallbacks below.

If `show_widget` is available, render the funnel, review queue, and single-draft card as widgets. Style them with `reference/design.md`. If `show_widget` is not available, use the text fallback named in each section.

Horizon rules:
- Card outline: `border: 1px solid var(--border-strong)`, `border-radius: 12px`.
- Status chips: leading filled-circle icon (check, cross, triangle), light tint background, dark `#181F26` label. Success `#D5F5DB`, danger `#FDDFDC`, warning `#FFECB8`.
- Gauge or dot color: from the account's own score band if the source returns one. Never a hardcoded cutoff.
- KPI tiles: muted 13px label, 24-26px value at weight 500, same outline.
- Buttons that call `sendPrompt`: accent pill (`color: var(--text-accent); background: var(--bg-accent); border: none`).
- Icons: inline SVG only, per `reference/design.md`. No icon font.
- Sentence case, weights 400 and 500, and an `<h2 class="sr-only">` summary line.

## No dialog for a draft

A draft is decided on its card, with the card's Approve, Edit and Reject buttons. Never use `AskUserQuestion` for a per-draft decision, and never ask "What do you want to do?" about a draft. A dialog can hide the text above it, and a draft the CSM cannot see cannot be approved.

If the card does not render (two failed attempts, or no `show_widget`):

1. Print the draft in full in the message: the Why this account headline first, then To, subject, body, and the "Why this contact" line. Do not rely on a card.
2. End with one plain line: "Reply approve, edit, reject, or skip." No dialog.
3. When the CSM wants to move faster, offer the batch review question from `reference/questions.md`, with the list of drafts inside the question text.

Say the render failed in one line, once.

## Sequence (strict)

1. Finish drafting the cohort.
2. In one message, in this order: the counts strip (see Funnel) and the paginated review widget with the first draft open. Use `reference/widgets/paginated-review.html`. The CSM does not click to reach the first email. Add one summary line under the widget: `<n> drafts ready. <k> skipped: <account> (<reason in plain words>). Nothing was sent.` Name each skipped account when there are 3 or fewer. Above that, give the count and point to the Skipped group. Never drop a skipped account silently, a churned account included.
3. Order: the queue's own order. Ready drafts first, then Needs a look.
4. The CSM decides in the widget and presses Send decisions. Then show the result and the next widget (see After Send decisions). Show the full funnel only when no drafts are left.

A typed reply always works as well: "approve all ready", "reject 4, 9", "edit 7", "open 12". Take it as if the buttons had been pressed.

## Funnel

At the start of review, show the counts as one row of compact KPI tiles (`design.md`): the same stages and skipped, each a boxed tile with the label on one line and the value large. The strip tiles are not clickable. Put a muted line under the row: "3 drafts ready". Show the full funnel only at the end of the run, on the dashboard, and when the CSM asks for it. The tiles in the full funnel are clickable through `sendPrompt` and looks it: a trailing chevron (the SVG in `design.md`, `var(--text-muted)`), `cursor: pointer`, and `border-color: var(--border-strong)` on hover.

Text fallback, one line: `Book: 42 | With goal: 17 | Flagged: 11 | Contacts: 24 | Drafts: 14 | Skipped: 3` (use the use case's stage names).

Right after the funnel, add a plain-text note: one line per stage, naming the actual capability, tool, and filter used this run. If a stage count did not change from the one before, say so instead of restating the filter. Say when a stage was capped or when an optional capability was `none`.

## Paginated review widget

One widget holds up to 10 drafts, one per page. It is the main review surface. Use the fragment in `reference/widgets/paginated-review.html` and the component spec in `reference/design.md`, Paginated review card.

**Groups.** Ready: every fact passed the fact check and is sourced (the `High confidence` badge). Needs a look: `Thread follow-up only`, `Flagged risk`, `Grounding incomplete`, any inferred claim, or any risk note on the card. Order Ready first.

**Controls**

- Prev, Next, and a dot per draft, colored by status. These run in the page and make no model turn.
- **All drafts:** a list view in the same widget. One row per draft: status dot, number, recipient, account, subject, its group, and the Why this account headline on a second muted line. A row opens that draft's page.
- **Approve all ready:** marks every Ready draft that has no risk note. A draft with any risk note, and any draft in Needs a look, is never marked by it. The CSM opens those.
- Approve, Edit and Reject mark the page and move to the next one. Nothing is recorded until **Send decisions**.
- **Send decisions** calls `sendPrompt` once with plain text that names every decision: "Review decisions. Approve: 1 Jordan Lee (Acme), 2 ... Approved in bulk: 2, 3. Reject: 4 ... Edit: 7 ... Not reviewed: 3." It does nothing when nothing is marked.
- More than 10 drafts: a **Next 10** button that calls `sendPrompt('Show the next 10 drafts for review')`.
- No dialog for any of it. See No dialog for a draft.

**State.** Decisions live in the widget until Send decisions. If the widget re-renders or the chat reloads, they are lost. The count line says "Nothing is recorded until you press Send decisions."

**Skipped.** Under the widget, a short "Skipped, no draft" group. Each skipped account is a card with the name and status chip on the first row, the sub-line on one line with an ellipsis, and the reason on its own row beneath. Rows never overlap. In chat text, call these accounts "skipped", never "flagged". For a skipped account with `Flagged risk`, add a short read-only brief under its row, never a bare "skip": what flagged it, the sourced usage fact, who is already writing to the customer (from the thread and timeline items), and one suggested next step in plain words for the CSM. If the data names the account's renewal owner or account owner, offer one draft note to that person as a mail draft, written for the CSM to review. Never create a CTA or write to Gainsight. Never send. "Flagged" is the funnel stage name, and a CSM reads it as a warning.

**Footer.** If `ground_top_n` or another cap left flagged accounts out, one line: "N more flagged accounts not yet grounded: A, B, C." with a **Ground remaining accounts** button.

**Text fallback** (no widget, or the render failed twice): the one-draft-at-a-time print from No dialog for a draft. The CSM can say "approve all ready".

## Single-draft card

Top to bottom, in this order, as one card layout. It follows the layout the CSMs already know from the earlier skill.

1. **Header row.** The heading is always the **account name**, even for a user-level draft. Under it, one sub-line: the goal in a short phrase and the segment if known. The sub-line may wrap to two lines. Never let the chips overlap it: the chips sit on their own row beneath it, with a gap. Top right: the **account's health** as a gauge, as `design.md` defines it, with the score inside, colored by the band, and the band label beneath it.
   - Band: when the card opens, read the scorecard for this one account through the `signal` adapter and take the label and color from it (`overall_label`, `score_color`, or the range). Bands are tenant-configured. Show the label verbatim. The gauge is always the half-circle arc from `design.md`, never a ring.
   - Only a bare number came back (for example from a context source): color the gauge with the standard scale in `design.md` and write "standard scale" beneath it, not a band name. Never write Healthy or At risk.
   - Nothing came back: the empty track with a dash and "health not available".
   - **Two health numbers.** The gauge is the scorecard value. If a context source also returned a health value and it differs, label the gauge "Scorecard" and put the other value in the grounding box with its source (for example "Health 29, sourced, <context source>"). If they match, show it once.
   There is no checkbox on the card.
2. **Status chip.** The badge from the use case (`Approved`, `Drafted in mail`, `Sent`). In the paginated widget the chip also shows the local mark before Send decisions: "Not reviewed", "Marked to approve", "Marked to reject", "Marked to edit". After the agent records an approval the chip reads "Approved, not yet in <mail tool> drafts". Never write "simulated".
   - **Why this badge.** Under the chips, one muted line for `High confidence`, built only from this run's checks: "Fact check passed, 5 of 5 facts sourced, product fit checked" or "...product fit not checked, single product". Add "thread acknowledged" or "no recent customer-visible thread" so the CSM sees how personal it is. If the badge is not earned, name the first check that failed instead ("1 fact inferred", "fact check removed 2 points", "product not confirmed"). Never write a score or a percentage.
2b. **Why this account.** A block directly under the header and the status chip, above the tiles. It has a muted label "Why this account", one plain headline at 16px weight 500, and up to 3 short bullets under it. Left border in the accent color, surface-2 background.
   - The headline is built only from facts retrieved in this run: what flagged the account (the signal, with its number or direction) and one context fact when there is one, such as the renewal date, the health band, or the last thread. Example form: "Usage down over 90 days. Renews in 60 days."
   - Each bullet ends with `sourced` or `inferred` and the source name. The headline names nothing that is not in a bullet. Use the source's own words. Coin no label.
   - When nothing supports a headline, the block reads "No usage signal, drafted from account context." and has no bullets. Never invent a reason.
   - It is for the CSM. Nothing from it goes into the email unless `draft.md` already allows it.
3. **Four tiles in a row,** each a KPI tile from `design.md`: a label and one large value, and nothing else. No sub-lines, no sources, no dates inside a tile. Sources go in the grounding box.
   - ARR: the account's ARR, or "(illustrative)" in the label if it came from no source.
   - Signal: the number or date that flagged this recipient, with its own label. For a login goal: "Last seen" and the date (for example "2 Sep 2026"). For an account-level signal: the ratio or change. This is the per-user fact, so it is the one tile that differs between users of the same account.
   - Grounding facts: "n sourced", and "n sourced, n inferred" only if any are inferred.
   - Active risk: the risk level in the source's words (for example High), or a dash. Never set your own level.
4. **Banner,** in chip colors with dark text (see `design.md`), only when grounding found something that should change the send: a warning chip for risk that does not block (for example contract friction, noted, not treated as blocking), danger colors for a blocking risk, success colors for a supporting goal. Omit it otherwise.
4b. **Why this contact.** A compact box between the banner and the email, so the CSM sees why this person, in two parts:
   - Chips on one row, only for fields that exist: role as mapped to the use case's recipient roles (for example "Adoption champion"), title as recorded, license type, last seen date, and "primary" or "backup".
   - One line starting "Chosen because": the fields that decided it, for example "Admin role, full license, last seen 6 Oct 2026". Add anything odd the use case says to flag (duplicate record, name that does not match the email, no opt-out value). Leave out fields that were not recorded. If the signal itself names the person (a per-user signal), say that instead.
5. **Recommended action box.** A first row that names the recipient: name, role, and email in muted text. Leave out any field that was not recorded. Do not print "role not recorded" in this row. Say it once in the grounding box if it matters. Then subject, body, sign-off. The same draft as the draft step. If the draft does not address the signal that flagged the user (for example it recommends a different feature because the signal is old), say so in one line above the box: what flagged the user, and why the email is about something else.
6. **Evidence box.** The full grounding list, titled "Evidence". First bullet: the acknowledged thread with its date and source (`sourced`), or "Personalization: thin, no recent customer-visible thread". A last line, only when something was dropped: "Left out: N unsupported points". Then one bullet per fact, ending with `sourced` or `inferred` and the source name, matching the draft exactly.
7. **Action buttons,** accent pills, each through `sendPrompt`. No button calls a tool directly. In the paginated widget, Prev, Next and All drafts replace Back to review queue.
   - **Approve to <mail tool> draft**, **Edit**, **Reject**, **Approve & send**. In the paginated widget they mark the page, see Paginated review widget.
   - Name the approve buttons for the configured mail tool (for example "Approve to Outlook draft").
   - If `mail` is `none`: no approve buttons. Show the draft for copying, plus Edit and Reject.
   - Name people by name. Never use a gendered pronoun for a contact or the CSM unless a source states it, in the card text and in the email.
   - If `send_enabled` is false, or the surface has no send guard: render **Approve & send** disabled, with the reason.
   - A test send to the CSM's own address is not a button. The CSM asks for it in chat, and the agent confirms first.

## Approve and edit tracking

- **Viewing writes nothing.** Opening, showing, or re-showing a draft is not a ledger event. Write a row only when the CSM acts: approve, edit then save, reject, send, or test send. The frequency cap reads the ledger, so a row written on view would block a contact the CSM never approved.
- Approve: marks the draft approved for this run and writes nothing to mail or the ledger. Show the chip "Approved, not yet in <mail tool>" (name the configured mail tool) and count it under Approved. The mail drafts are created in one batch, see `reference/steps/send.md`, Batch step. Read it before you write any ledger row.
- Edit: let the CSM change the draft, then show it again. Record `edited: true` in the ledger when the draft is created.
- Reject: record the reason if the CSM gives one. Do not draft again for that recipient this run.
- Record `accepted_unedited: true` when a draft is approved with no edit. This is the quality signal behind the edit rate.
- Record `approved_in_bulk: true` for a draft marked by Approve all ready and not opened. Report bulk approvals apart from the edit rate on the dashboard, so unedited acceptance is not inflated.

## After Send decisions: result, then the next step

When the decisions text arrives (or a typed reply), do not ask "review the next draft?" or any other menu question. Do this:

1. One result bar with chips: Approved n, Rejected n, Edit n. Name any draft the CSM must act on (a sender mismatch, a high-risk account reminder). Say "Approved drafts are not in <mail tool> yet."
2. One muted line of counts: "Approved 8, Rejected 1, Edit 1, Left to review 3".
3. If any draft is marked Edit, ask one plain-text question for the first one: "What should change in the draft for <name>?" Show the draft again with the change, then the next edit. This is plain text, not a dialog.
4. If drafts are left (Not reviewed, or the next 10), show the next widget with those drafts. Do not ask first.
5. When Left to review reaches 0, run the batch step in `send.md` if any draft is approved, then show the cumulative dashboard with the full funnel.

In the text fallback, the old one-draft flow applies: a result line, the running counts, and the next draft in full.

## Cumulative dashboard (end of run)

Render as a widget, or a text table in the fallback. Show:

- **Funnel outcomes.** Each funnel stage, then approved, drafted in mail, sent.
- **Edit rate.** Unedited acceptance as a share of approved drafts. Label it "edits made in the agent only". The agent does not see edits the CSM makes later in the mail tool. If `ledger` is `none`, say "unavailable".
- **Skipped and why.** Suppressed, opted out, rejected, grounding incomplete, flagged for risk, capped. One count per reason.
- Add the use case's `outcome_metric`.

If the ledger holds earlier runs, say the dashboard is for this run only unless the user asks for history.

## Close (after the dashboard)

1. **Save the run.** Write a `## Last run` section to `config.md`: date, the confirmed goal in the CSM's words, scope, and counts (flagged, drafted in mail or shown, approved, rejected, skipped). Replace the old section. With no filesystem, update the config artifact and tell the CSM once to save it to project knowledge again. This is the only config write at close.
2. **Say where things stand,** in one line: how many drafts sit in <mail tool> unsent, or that the list was copied. The agent cannot see later sends or edits in the mail tool. Say so once.
3. **Ask the close question** from `reference/questions.md`. Do not show the banner.
