# Step: goal check and fallback ladder

Runs after the CSM states a goal and before the goal confirm in `reference/questions.md`. It reads the `## Catalog` section of `config.md`. It never calls a tool to guess at a metric. Show a question only when something fails.

## 1. Parse

Split the goal the CSM typed into metric, threshold, window, and scope. If a part is missing, the use case's goal schema says how to treat it. Do not invent a part.

## 2. Check each part against the catalog

Check in this order and stop at the first miss. One question per message.

1. **Metric.** The goal's metric must match a `metrics` entry, by the source's own name or an obvious equivalent. Say which entry you matched.
   - If the metric is in the catalog but had no values on the sampled accounts, treat it as a miss and say so in the question: "<metric> had no values on the <m> sampled accounts."
   - Miss: ask the metric-missing question. Name what is missing in the CSM's words and offer the nearest `metrics` entries as options (up to 3), then the ladder options that apply.
2. **Window.** If the matched metric has no timestamp, say the window cannot be checked. Continue, and carry the note into the interpretation.
3. **Scope.** A scope of the CSM's book, a single account, or named accounts needs no check. Other scopes:
   - **Renewal window** or **health band** ("red", "at risk"): valid when the adapter declares that field (see the adapter's Scope fields), or the file's column map names it. Say which field you will use. If the tenant has no such field, ask the scope-missing question and say that field was not found.
   - **A group** (a segment, tier, region): must match a value in a `segments` entry.
   - Miss: ask the scope-missing question. Say the field you looked in, list its real values (up to 5, with counts) as options, and add "Whole book". For a missing renewal or health field, offer "Whole book" and "Accounts I name".
   - If no segment field exists at all, say so and offer "Whole book" and "Accounts I name".

All parts pass: go to the goal confirm. Put the matched metric and source in the interpretation.

If the CSM says the data exists, offer "Refresh the catalog" once. After a refresh, check again. If it still misses, use the ladder.

## 3. Fallback ladder (no usable metric)

Use this when `metrics` is empty, when no entry is near the goal, or at the loop exit. Offer only the options that apply, in this order, with the first one that applies marked as the recommended option. Always end with Stop.

| Order | Option | Applies when | What it is, and what it is not |
| --- | --- | --- | --- |
| 1 | Nearest proxy signal | The catalog or the `contacts` and `signal` adapters hold something related, such as a scorecard measure, or last-seen and license fields on contacts | A weaker signal. Say what it measures and what it does not. Example: last seen shows who has gone quiet, not what they use. A draft never claims usage the data does not show. |
| 2 | Scan my book for themes | `goals` or `context` is mapped | The theme scan in the use case. Works with no usage data. Rows are labeled "no usage signal". |
| 3 | Load a usage export | Always | The CSM provides a file. The `file` adapter maps it, and the catalog is rebuilt from it. |
| 4 | Accounts I name | Always | The CSM names the accounts. The agent drafts from `context` and `knowledge` with no threshold signal. Every row and draft card is labeled "no usage signal". The email makes no claim about usage. |
| 5 | Stop | Always | Say what would unlock the run: which source to connect or which file to load. |

Rules:

- State the reason for the ladder in one line before the question: "Your source holds no adoption metric I can measure."
- Option 4 follows the same recipients, grounding, fact check, and approval steps as any other run. Only the signal is missing.
- The ladder is shown once for the same reason. If the CSM picks an option and it also fails, use the loop-exit rule in `SKILL.md` guardrail 12.
