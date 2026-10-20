# Questions the agent asks during a run

Every question must make sense to someone who sees only the question and its options. Start it with the step name. Put the facts that matter inside the question. Options say what will happen. The first option is the recommended one.

## Banned

- Open questions about unnamed things: "What should I do with the 3 Acme recipients?". Name each person and role in the question, and give options that are actions.
- Announcing the next step and then asking about the previous one ("Grounding next. ... What should I do with the recipients?"). Settle the open decision first. Narrate the next step only after the answer, in the same message that starts it.
- Menus with no decision in them: "How do you want to continue?", "What would you like to do next?", "How do you want it said?".
- Bare confirms: "Looks good?", "Use these, or change something?", "Save this?".
- Options that are examples, not choices: "Change the goal (for example low logins)". An option is an action.
- A question the agent can answer from the config, the data, or an earlier answer.
- Asking when nothing is undecided. If the next step is obvious and safe, run it and say what you did in one line.

- A per-draft dialog: "Review draft 1 of 4: <draft>. What do you want to do?". Drafts are decided on the card. See `steps/review.md`, No dialog for a draft.

## Templates

| Decision point | Question | Options |
| --- | --- | --- |
| Book (first run) | `Book: you are CSM on <N> active accounts through <field label>, and on <M> through <other field label>. <K> churned or inactive accounts are left out. Examples: <5 names>. Use these accounts?` | `Use the <N> (Recommended)` / `Include the <M> too` / `Only accounts I name` |
| Goal check, metric missing | `Goal check: <what the goal needs, in the CSM's words> is not in <source>. These adoption metrics are: <metric 1>, <metric 2>, <metric 3>. Which one should I track?` | Nearest metrics first (first is Recommended), then the ladder options that apply from `reference/steps/goal-check.md`, then `Stop`. A question has at most 4 options: drop the lowest-ranked ones, and list every metric in the question text |
| Goal check, scope missing | `Goal check: no <group the CSM named> found in <field>. Its values are: <value (count)>, <value (count)>, <value (count)>. Which scope should I use?` | The 2 largest real values (first is Recommended) / `Whole book` / `Accounts I name`. Every value stays listed in the question text |
| No adoption metric (fallback ladder) | `Goal: <source> holds no adoption metric I can measure. Next best options for <N> accounts in your book:` | The ladder options that apply, in the order in `reference/steps/goal-check.md`, first applicable is Recommended, `Stop` last. At most 4 options: drop the lowest-ranked middle ones and say in the question text what else is possible |
| Close | `Close: <n> drafts are in <mail tool>, unsent. <a> approved, <r> rejected, <s> skipped. What next?` | `Run the same goal again (Recommended)` / `Run a new goal` / `Stop` |
| Review, text fallback (card did not render) | `Review: <n> drafts are ready. 1. <name>, <account>: "<subject>" 2. <name>, <account>: "<subject>" ... How do you want to review them?` | `Show them one by one (Recommended)` / `Approve all <n> without a flag` / `Stop` |
| Goal confirm | `Goal: <metric> <threshold> over <window>, scope <scope>, from <source>. Track this?` | `Track this goal` / `Change the threshold or window` / `Pick a different goal` |
| After discovery | `Discovery: <N> of <M> accounts raised this goal. Look at the usage signal for these <N>?` | `Yes, these <N>` / `Use my whole book instead` / `Stop here` |
| No match (first time) | `Discovery: no account in <scope> mentions this goal. Run the signal on the whole book anyway?` | `Run on the whole book (Recommended)` / `Type a different goal` / `Stop` |
| No signal (first time) | `Signal: <source> returned nothing for <metric>. What should I do?` | `Use <other source found>` / `Type a different goal` / `Stop` |
| Loop exit (second miss in a row) | `Goal: I tried <goal 1> and <goal 2>. <source> holds these measurable metrics: <metric list from the source>. Which one should I track?` | One option per metric found (up to 3) / `Scan my book for themes` (only if `goals` or `context` is mapped) / `Stop` |
| Recipients | `Recipients for <account>: <name, role> (primary), <name, role>, <name, role>. Draft for these?` | `Draft for these` / `Only the primary` / `Choose someone else` |
| Customer's own CSM | `<name> looks like <customer>'s own CSM. Send the nudge to them too?` | `Leave them out` / `Include them` |
| Tone check (cohort over 5) | `Tone check: <n> drafts to write. These 3 go first.\n1. <recipient>, <account>: "<subject>" <first sentence>\n2. ...\n3. ...\nThey show again in review. Do they sound right?` | `Yes, draft the rest (Recommended)` / `Change the tone` / `Change what they recommend` |
| Create drafts | `Create drafts: <n> approved. <name, account, subject> for each. Create them as <mail tool> drafts? Nothing is sent.` | `Create <n> <mail tool> drafts (Recommended)` / `Show copyable list` / `Not now` |
| Timezone at first send | `Sending: where do I find each recipient's timezone?` | `A contact field` / `An account field` / `One timezone for all` |

If a decision point is not in the table, write the question the same way: step name, the facts, then options that are actions.

## After an approve, edit, or reject

Never ask "review the next draft?". Give the result bar, the running counts, and the next draft, as `review.md` says.

## After an answer

Do the thing. Do not ask a follow-up "anything else?" or "how do you want to continue?". When a step ends, say what happened in one line and what comes next, then start the next step.

## After a miss

- `Type a different goal` is offered only when the catalog gives no options to show. It asks one open question: "Goal: what should the agent track?". It does not show the ready banner or the example cards again. The banner shows once per run.
- The loop-exit question lists metrics the source returned, not examples. If the source returned none, say so and stop. Do not ask again.

## Tone check

- The three previews are part of the question text. They are not chat text above it.
- Use one word for the step: tone check. State the count once: "<n> drafts to write. These 3 go first."
- Each preview is one line, 120 characters of body at most. No sign-off, no grounding list.
