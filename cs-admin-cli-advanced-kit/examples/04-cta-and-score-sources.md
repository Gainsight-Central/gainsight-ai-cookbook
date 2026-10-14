# What creates CTAs, and what writes each measure

**When you need this.** Cockpit fills up, and the rule that created the CTAs is not obvious. Two rules set the same scorecard measure, and the later one wins. A health score is quoted in a meeting, and half of it is a manual sentiment measure nobody has re-weighted.

**What you can say**

```text
Show what creates CTAs and what writes each scorecard measure. Read-only.
Follow CLAUDE.md and examples/04-cta-and-score-sources.md.

1. Run `gs-admin sc list --json`. For each scorecard, run `gs-admin sc measures --name "<scorecard>" --json`.
   `sc measures list` is not a command on CLI 1.0.10. Save both under tenants/<slug>/raw/.
2. Use tenants/<slug>/raw/rules-described.json if it is under 14 days old. Otherwise page
   `gs-admin re r list-and-describe --limit <rule count> --json` once and save the `rules` array. Do not pass `--page`.
3. From that payload, list every action that creates or closes a CTA, and every action that sets a score.
   For a measure with two writers, run `gs-admin re r describe --name "<rule>" --action-id <id> --json`
   only for those actions, so the field mappings are exact.
   If `--action-id` is rejected, stop and use the `rd` payload from list-and-describe.
4. Write tenants/<slug>/intent/cta-and-scores.md with two tables:
   - CTA actions: rule, active, CTA type, reason, priority, schedule or chain.
   - Measures: measure, how many scorecards use it, every rule that sets it, in chain order when you know it.
5. If the measure list has no weight, say weights were not in the payload. Do not invent a percentage.
```

**What you get back**

Two tables: which rules create or close CTAs, and which rules set each scorecard measure. The agent reads the scorecard list and the rules already saved on your machine. It opens a single rule only when two rules write the same measure.

**Example output** (illustrative)

CTA actions

| Rule | Active | Action | Type | Reason |
|---|---|---|---|---|
| Usage drop | yes | Create CTA | Risk | Usage Drop |
| Renewal in 90 days | yes | Create CTA | Lifecycle | Upcoming Renewal |
| Close stale risks | yes | Close CTA | Risk | — |

Measures

| Measure | Scorecards | Set by |
|---|---|---|
| Sentiment | 1 | "NPS to sentiment", then "CSM override" (later in chain "Nightly scores") |
| Product usage | 1 | "Usage to score" |

Sentiment has two writers. The chain order is the precedence. Weights are included only when `sc measures --name` returns them.

**Why this is easier than the screens.** Gainsight lets you open one rule or one measure. It does not list every CTA-creating action next to every measure writer. That list is how you decide which rule to tighten before you ask CSMs to live in Cockpit.

**What this will not tell you.** This does not forecast how many CTAs the next run will create, and it does not close any. Turning a rule off is a change, and the agent asks you first. Measure weights are included only when the scorecard command actually returns them.
