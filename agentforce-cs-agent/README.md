# Gainsight CS Agent — Agentforce Subagent & Response Templates

> Part of the [Gainsight AI Cookbook](../).

A Salesforce Agentforce subagent that answers Customer Success questions from Gainsight data, plus a library of response templates that control how it answers.

The subagent handles account summaries, transitions and handoffs, renewal risk, expansion, health, stakeholders, Timeline, Success Plans, and CTAs. The templates are what keep its answers consistent, evidence-backed, and free of invented detail.

## How the two pieces fit together

[`agentforce-subagent.md`](agentforce-subagent.md) holds the three fields you paste into Agentforce: the subagent **name**, **description** (Agentforce uses this to decide when to route to the subagent), and **reasoning** (the standing instructions).

The reasoning ends with a marker:

```text
< copy-paste the suggested structure for each use-case here from the Gainsight template library >
```

Replace that line with the contents of whichever files from [`templates/`](templates/) you want the agent to support. You do not need all four — take only the use cases you're deploying.

## Setup

1. Create a new subagent in Agentforce.
2. Copy the **name** and **description** from [`agentforce-subagent.md`](agentforce-subagent.md).
3. Copy the **reasoning** into the instructions field.
4. Replace the `< copy-paste … >` marker with one or more templates from [`templates/`](templates/).
5. Wire up the Gainsight actions the templates depend on (Company/Relationship lookup, Timeline, Success Plans, CTAs, scorecards).
6. Test with a named customer and confirm the output follows the template's section order.

## Prerequisites

- **Gainsight CS**, with the actions above exposed to Agentforce.
- **Salesforce Agentforce**, with permission to create subagents.
- ***Staircase AI — optional.*** *The reasoning instructs the agent to use Staircase when it is available, and a few template fields read from it directly (marked inline). Without Staircase AI the agent should fall back to Gainsight data and say so, rather than leaving those fields blank.*

Field names differ between tenants. `ARR`, `Health Score`, `Customer Tier`, and `Renewal Date` are labels in these templates, not API names — point your Agentforce actions at whatever the equivalent fields are called in your org. The reasoning deliberately forbids the agent from surfacing internal field names to end users.

## Templates

| Template | Use it for |
|---|---|
| [Account Summary](templates/account-summary.md) | Current state of an account — health, sentiment, risks, wins, next steps |
| [Account Transition](templates/account-transition.md) | Onboarding brief for an incoming CSM, with a stakeholder map and 30-day plan |
| [Renewal Risk](templates/renewal-risk.md) | Renewal posture, risk drivers, protective factors, 30-day renewal plan |
| [Expansion Analysis](templates/expansion-analysis.md) | Expansion signals, best plays, blockers, recommended motion |

See [`templates/README.md`](templates/README.md) for what each one produces and how they differ.

## Reusing the templates outside Agentforce

The templates are platform-agnostic — they specify output structure, not tool calls. The same file can back a Slack skill, an MCP-connected assistant, or any other agent surface with access to Gainsight data. Only [`agentforce-subagent.md`](agentforce-subagent.md) is Agentforce-specific.

## A note on placeholders

Template text is reproduced verbatim from the source template library, including its placeholder tokens and empty table cells. Some format specifications are terse — for example `- — .` — because the token that named each part is absent in the source. Treat those as "one bullet per item, in the order shown" and fill in your own convention.
