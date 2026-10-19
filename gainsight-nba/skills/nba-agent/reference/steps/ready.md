# Step: ready (banner and goal prompt)

Runs after setup finishes, and at the start of every later run once preflight passes. Show it once per run. Do not show it again after a no-match, a no-signal, or a "Type a different goal" answer: those use a single open question from `reference/questions.md`. When the chat already has a confirmed goal, resume instead of showing it. Show visuals, not paragraphs. One short line of narration at most. Do not repeat the widget's content as text.

Read `reference/design.md` first. Render the banner and the goal prompt as one widget if `show_widget` is available.

## Banner

1. **Headline.** First run after setup: "Your adoption agent is ready, <first name>". Later runs: "Welcome back, <first name>". Under it, one sub-line: the use case name and "Drafts for your approval". Use the success chip's check icon beside the headline.
2. **Connected chips,** one per source the capability map uses, in a row:
   - the source's name and its state: `Gainsight CS on`, `Staircase on`, `<mail tool> on`, `Files on`.
   - a capability mapped to `none`, or a tool not connected: a neutral chip, `Mail: none`.
   - Chips never wrap. Name only sources you actually matched in preflight.
3. **Send chip.** `Drafts only, sending off` when `send_enabled` is false or the send guard is not active. `Sending on` only when the flag is true and the guard is active. Never infer it.
4. **Save notice,** only when config is not persisted (no filesystem): a warning bar in chip colors: "Download your N setup files and add them to project knowledge, or setup runs again next time." Omit it when files are written to `.nba-agent/`.
5. **What's next.** A row of four steps with the current one marked: Goal, Find accounts, Draft emails, Review.

## Goal prompt

Under the banner: the heading "What should the agent track?", then cards the CSM can click, then one line: "Or describe your own goal below." Name the metrics that have values in the sub-line, for example "Your data can measure: Engagement, ROI." Show only what the CSM can pick. Never list hidden cards, missing metrics, or empty samples on the banner. A limit is shown later, only when the CSM's choice runs into it.

- Cards: up to 3. First the use case's `goal_examples` whose metric is in the `## Catalog` in `config.md` and whose capability is mapped. Fill the remaining slots with the use case's `catalog_cards`, built from the metrics and segments the catalog holds. The banner is never left with only the scan card when the catalog holds a metric with values. Then **Not sure: scan my book for adoption themes**.
- When `config.md` has a `## Last run` section, the first card is **Re-run: <last goal>**, with its date and counts underneath (for example "last run 12 Oct, 8 drafted"). It calls `sendPrompt` with that goal in plain words. The goal check and confirm still run. Skip the catalog probe and the book question. A re-run is a new run, so it reads the ledger as in `reference/steps/data.md`.
- If the catalog holds no adoption metric, show the fallback ladder cards that apply from `reference/steps/goal-check.md` (theme scan, load a usage export, accounts I name) and no metric cards. Add no sentence explaining why.
- Clicking an example card calls `sendPrompt` with that example as the goal in plain words. The goal still goes through the use case's confirm. Nothing runs before it.
- Clicking the scan card calls `sendPrompt('I am not sure. Scan my book for adoption themes.')`, which starts the theme scan.
- A metric card is shown only when the catalog holds that metric. A goal typed in the box goes through the goal check in `reference/steps/goal-check.md` before the confirm.

## Text fallback

No widget tool: print five lines at most.

```
Your adoption agent is ready, <name>.
Connected: Gainsight CS, Staircase, <mail tool>. Sending off, drafts only.
<Save notice, if needed>
Next: goal, find accounts, draft emails, review.
What should the agent track? Describe it, or say "not sure" and I will scan your book.
```
