# Response Templates

Each file is a self-contained output contract. Paste one or more into the `< copy-paste … >` marker in [`../agentforce-subagent.md`](../agentforce-subagent.md), or use them with any other agent surface that can read Gainsight data.

You do not need all four. Take only the use cases you're deploying.

| Template | Answers the question | Output shape |
|---|---|---|
| [account-summary.md](account-summary.md) | "What's going on with this account?" | Exec summary, snapshot table, sentiment verdict, risks, expansion signals, wins, recent activity, next steps |
| [account-transition.md](account-transition.md) | "I'm inheriting this account — what do I need to know?" | Onboarding brief, snapshot, stakeholder map, relationship history, 30-day plan, discovery questions |
| [renewal-risk.md](renewal-risk.md) | "Is this renewal at risk?" | Verdict, at-a-glance table, risk drivers, protective factors, open commitments, 30-day renewal plan |
| [expansion-analysis.md](expansion-analysis.md) | "Is there room to grow this account?" | Expansion thesis, signals split by intent vs. readiness, best plays, blockers, recommended motion |

## What these templates enforce

The value is less in the section lists than in the guardrails every template repeats:

- **No invented detail.** *"Do not manufacture risks from a low Health Score alone."* *"Never fabricate missing activities."* *"Do not invent protective factors."*
- **Explicit empty states.** Every section has a defined fallback string, so a quiet account produces "No risks identified in recent activity." instead of speculation.
- **Evidence with every claim.** Risks, opportunities, and signals each carry a source, and several templates close with an overall confidence rating plus named data gaps.
- **Omit rather than pad.** *"Omit an empty subgroup rather than padding it."*
- **Fixed vocabularies.** Status values are constrained sets (`HAPPY / NEUTRAL / AT RISK`, `HIGH / MEDIUM / LOW / INSUFFICIENT DATA`) so downstream readers and automations can rely on them.

Keep these rules when you adapt a template. They are what make the output trustworthy enough to act on.

## Staircase AI

A few fields read from Staircase AI and are marked inline where they appear. Without Staircase AI, the agent should fall back to Gainsight data and state the gap rather than leaving the field blank. Only [account-transition.md](account-transition.md) names Staircase directly.

## Placeholders are verbatim

Template text matches the source template library exactly, including placeholder tokens and empty table cells. Where a format spec looks incomplete — `- — .` — the naming token is absent in the source; read it as "one bullet per item, in the order described above."
