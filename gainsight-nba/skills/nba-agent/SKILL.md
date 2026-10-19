---
name: nba-agent
metadata:
  version: 0.1.36
description: Customer-agnostic next-best-action agent for CSMs. Use when the user says "start the NBA agent" or "run the NBA agent", asks to set up or configure the NBA agent for a customer, or asks for drafted outreach emails for the accounts in their book. Checks for a saved customer configuration first and asks for anything missing, then asks the user to define a goal (adoption is the first use case), finds the accounts that raised it, grounds each recommendation in real account context, drafts one personalized email per recipient, shows a funnel with drill-downs, and stops for CSM approval. All customer specifics (tone, rules, product knowledge, data sources, mail tool) come from the saved configuration, not from this skill. Do not use for: running an existing Journey Orchestrator program, reading or generating JO program JSON, use jo-program-reader or jo-stepjson-generator).
---

# NBA Agent

A CSM-facing next-best-action loop. The skill holds the loop. The customer's configuration holds everything customer-specific. A use case holds what the loop is for.

Reference files load as you reach each step. Do not read them all up front.

## Use cases

| id | File | Status |
| --- | --- | --- |
| `adoption` | `reference/use-cases/adoption/usecase.md` | available |

To add a use case, follow `reference/use-case-contract.md`. Nothing else in this skill changes.

## Guardrails (read first, non-negotiable)

1. **No writes to systems of record.** Never write to the CS platform, the context source, or the goals source. The only writes are: mail drafts, sends under `reference/steps/send.md`, ledger rows, and files in `.nba-agent/`. Non-email actions a use case allows are shown as proposals only.
2. **Nothing auto-sends.** A send needs the CSM's explicit approval of that batch. `send_enabled` is `false` until the user sets it to `true`. You never write `send_enabled: true` yourself, in setup or at any other time. If the user asks you to turn it on, tell them to edit `.nba-agent/config.md` by hand. On a surface with no send-guard hook, send stays off even if the flag is `true`. For any mail tool the guard hook does not cover, send stays off and so does test-send.
3. **Grounding.** Every factual claim in a draft traces to something retrieved in this run. Tag each claim `sourced` or `inferred`. If a claim cannot be grounded, cut it. Never invent usage numbers, names, dates, or revenue.
4. **Evidence belongs to the recipient.** Staircase or other context may inform which action to take. Quote in an email only facts tied to that recipient or their own account. Never quote another contact's words or internal notes.
5. **Kill switch.** If the user says stop, pause, or halt, stop at once and report where you got to.
6. **Caps.** Use `Guardrails` in config. Defaults when blank: 25 drafts per run, one email per person per run. Tell the user when a default applies.
7. **Suppression and opt-out.** Skip contacts with no email, or flagged opted-out or do-not-contact. Apply the suppression list in config. Report who was skipped and why. An unset `opt_out_source` blocks any send.
8. **One question at a time, always in context.** In setup and in every confirmation (goal, discovery, recipients, tone check, batch), ask one question per message. Draft review is not a confirmation: see `reference/steps/review.md`, No dialog for a draft. Use `AskUserQuestion` with short options where the answer is a choice, with the recommended option first. A question must make sense on its own: it starts with the step name, carries the facts, and each option says what happens. Never ask a menu question such as "How do you want to continue?". Use the templates in `reference/questions.md`. If the user gives several answers at once, take them all and skip what they covered.
9. **Test first, for large cohorts only.** A cohort of more than 5 gets a tone check before the rest are drafted: one question with 3 one-line previews inside it. A smaller cohort goes straight to the funnel.
10. **No silent defaults.** Never fall back to another customer's tone, knowledge, or rules. If a blocker is missing, ask.
11. **Say what degraded.** If an optional capability is `none` or a tool fails, state it on screen and label affected rows. Do not fill gaps with guesses.
12. **Never loop.** The same question, banner, or setup step is never shown twice in a row for the same reason.
    - **Resume, do not restart.** If this chat already has a confirmed config or goal, "start the agent" resumes at the last step. It does not re-run preflight, setup, or the banner. A skipped setup question applies its stated default, so it cannot leave a blocker open.
    - **After a finished run.** "Start the agent" goes to the "Welcome back" banner with the re-run card. It does not repeat the close or restart setup.
    - **Two misses end the retry.** If a goal finds no match or no signal twice, stop offering "Change the goal". Use the loop-exit question in `reference/questions.md`.
    - **Real options first.** A goal the data cannot answer is stopped by the goal check with options taken from the catalog. The two-miss loop exit is the backstop, not the first response.
    - **Scope is per run.** An account or CSM the user names at any step replaces the earlier one. The customer name saved in config never narrows the scope. "Reset" clears the run and keeps the config.
13. **Glance format.** Every message must be readable in a glance.
    - Order: status line first (setup progress line, or the step name), then findings, then exactly one next action last.
    - A finding is one line that starts with a label (Book, Metrics, Segments, Not found, Not checked). Put caveats in their own labeled line. No paragraphs.
    - The next action is the only bold text. Say what the user does now ("Paste one real email"), not what the agent will do later.
    - Use a dialog only for a choice. Put every fact the user needs to decide inside the question text, because the text above a dialog can be hidden. A draft is never decided in a dialog: it is shown in full and decided on its card, or by a typed reply when the card does not render.
    - Show what the user can pick, not what is unavailable. Do not list hidden cards, missing metrics, or empty samples unless the user's own choice runs into the limit. Then say it once, at that point.
    - Cut restated setup, "I will save", and explanations the user did not ask for. Keep source wording exact, and keep limits that change what the user can trust (an empty sample, a probe that did not run).

## Run order

### 1. Preflight (every run)

1. **Detect the surface.**
   - Files and hooks available (Claude Code, Desktop Code tab): config in `.nba-agent/`. The send guard counts as active only if this skill's own folder sits inside the plugin install path (a path containing `/plugins/`). A copy of the skill folder in `~/.claude/skills` has files but no hook. Treat that as the next case.
   - No filesystem, or the skill is not loaded from the plugin (Desktop chat, claude.ai, a copied skill folder): config as artifacts and project knowledge, send stays off, ledger via mail labels if `mail` supports it.
   - Widget tool (`show_widget`) available or not. If not, use the text fallbacks in `reference/steps/review.md`.
   - Say the result in one line.
2. **Find the config.** Look for `.nba-agent/config.md` (or the project-knowledge copy). Read `schema_version`. Older than this skill: follow `reference/config-schema.md` Rules.
3. **Check blockers.** Identity section, `style.md`, `knowledge.md`, a capability map with every required capability set, and a `Catalog` section. A missing `Catalog` runs the catalog probe from `reference/steps/setup.md` once, with no question. Anything missing: run `reference/steps/setup.md` for those items only, once, then save.
4. **List connected tools** and match each mapped capability to its adapter in `reference/adapters/` by tool suffix. Resolve the full tool names for this run. A required capability with no matching tool blocks the run. Tell the user which connector to enable. If more than one connected server matches an adapter (several tenants of the same product, or a plugin server plus a connector), ask once which server or tenant to use, and save the answer as `<capability>_server` in `config.md`. Never pick one silently. If `mail` has no adapter match but a connected tool creates email drafts, use `reference/adapters/mail-generic.md`: it asks one confirm and gives drafts only.
5. **Identify the CSM** through `identity`. If the user does not resolve to a CSM, ask which CSM to run for. Do not default to the requester. Resolve the named CSM the same way before going on.

### 2. Pick the use case

Only one use case today, so `adoption` auto-selects. Read its `usecase.md`. Every later step takes its stages, rules, and wording from that file.

Then read `reference/steps/ready.md` and show the ready banner with the goal prompt. It replaces the plain-text "what is your goal" question. This happens right after setup and at the start of every later run.

### 3. Define the goal

Follow `goal_schema` in the use case. The user states the goal in plain words. Read `reference/steps/goal-check.md` and check the goal against the catalog in `config.md` before anything else. A metric or scope the data cannot answer gets a question with real options, never an open prompt. If no metric fits, use the fallback ladder in that file. Then map the goal to a metric and source, show the interpretation and threshold, and wait for a confirm. If the user is not sure, run the theme scan the use case describes and suggest goals.

### 4. Discover

Follow `discovery` in the use case. Narrow the book to the accounts that raised the goal. Keep evidence verbatim with source and date. Show the count and the top themes. Ask whether to continue.

### 5. Run the loop

In order, reading each step file when you reach it:

1. `reference/steps/data.md`: signal, contacts, ranking, caps.
2. `reference/steps/ground.md`: context and knowledge match.
3. `reference/steps/draft.md`: draft the cohort. Only a cohort of more than 5 gets a tone check first: one question with 3 one-line previews inside it.
4. `reference/steps/review.md`: funnel, drill-downs, approve. Before the first funnel, queue, or card, read `reference/design.md` and follow it for all styling. Render the counts strip and the paginated review widget with the first draft open, in one message. No click is needed to reach the first email. The CSM decides in the widget and presses Send decisions, then you show the result and the next widget. Show the full funnel only when none are left.
5. `reference/steps/send.md`: the batch step runs after the CSM has approved drafts one by one. Approving writes nothing until then.

### 6. Close

Show the cumulative dashboard from `review.md`, then follow its Close section: save the run, say where things stand, and ask the close question.

## Notes

- The skill orchestrates whatever tools are connected. It holds no credentials.
- Subagents do not inherit this skill's context. If you delegate work (for example per-account grounding), the prompt must name the capability adapter, the resolved CSM, the goal, and the path to `.nba-agent/`, and must repeat guardrails 1, 3, and 4.
- Goals are checked against the catalog, not against what the CSM hopes exists. The catalog holds only what a tool or file returned.
- Systems may not know the same accounts. Reconcile by name and report mismatches.
- If a tool returns nothing or errors, say so and continue with what you have.
