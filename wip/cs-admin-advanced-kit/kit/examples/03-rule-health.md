# Which rules failed, and which only look healthy

**When you need this.** A rule says success, or partial success, and the execution history is empty or only a few weeks deep. Scorecard chains sit unscheduled. You find out because a CSM asks why the score did not move.

**What you can say**

```text
Audit rule and chain health. Read-only. Follow CLAUDE.md and examples/03-rule-health.md.

1. From config/rules.tsv, list rules whose last run is not success, plus rules that are active and have
   no schedule you can see. Confirm schedule with `gs-admin re r schedules --id <id> --json`
   only for that short list, one at a time. Stop on the first 429.
2. For each rule on that short list, run `gs-admin re r debug --name "<name>" --recent 5 --json` once.
   `re r list-executions` is not a command on CLI 1.0.10. Do not try it. Save under tenants/<slug>/raw/rule-health/.
3. For chains, run `gs-admin re chains list --json`. Debug only chains with a failed or partial task:
   `gs-admin re chains debug --name "<name>" --json`.
4. Write tenants/<slug>/intent/rule-health.md:
   rule, last status, last time, scheduled or not, chain parent, and the failure text the API returned.
   If the API returns no history, write "no history returned" — do not infer that the rule is fine.
```

**What you get back**

A list of rules that failed, finished only in part, or have no history. The agent starts from the index and looks up history only for those rules. A successful last run with an empty history stays on the list.

**Example output** (illustrative)

| Rule | Last status | History returned | Schedule |
|---|---|---|---|
| Set sentiment score | Partial success | None in the payload | Daily 02:00, chain "Nightly scores" step 2 |
| Load usage | Failed | "Source row count 0" | Daily 01:00 |
| Onboarding CTAs | Success | 3 runs | Unscheduled — chain says the chain owns the schedule |

**Why this is easier than the screens.** Rules Engine shows one rule's last run. This is the list you can take to the Monday ops review: failed, partial, and not scheduled.

**What this will not tell you.** Gainsight keeps a short history. This job cannot recover an older run, and it cannot show the row that a partial success skipped. A partial success with no history is still something to open in Rules Engine.
