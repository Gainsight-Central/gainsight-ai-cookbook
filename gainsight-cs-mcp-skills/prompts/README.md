# Prompts for Gainsight Copilot

Paste these into Gainsight Copilot. There is nothing to install.

Copilot reads Gainsight. When Staircase is connected, these prompts also use conversation intelligence (sentiment and what the customer said). When it is not connected, the prompt tells Copilot to say so.

You never paste an id. Where a prompt names an account, replace `[customer name]` with the customer.

The pack follows the Agentic / Headless use cases in the enablement hub. Where the hub and an older prompt covered the same job, the hub version replaced it. The rest line up with the [Customer Success prompts](https://www.gainsight.com/mcp/library/?_mcp-type=prompt&_products=customer-success) on the Gainsight CS MCP library. The wording here is the cookbook's: short, approval before any write, and unwilling to invent a number.

## On one account

| Prompt | Use it for | Lines up with |
|---|---|---|
| [Prep for a call](prep-for-a-call.md) | Before a customer call | Meeting prep in 60 seconds |
| [How is this account doing?](how-is-this-account.md) | A quick health check | Current health status |
| [Catch me up](catch-me-up.md) | The last 30 days | Last 30 days of activity |
| [Customer story and business review](customer-story.md) | One narrative across the connected products, an exec briefing, and the QBR or EBR deck outline | Hub: Customer Story and Business Review |
| [Renewal conversation](renewal-conversation.md) | One renewal meeting, including value and competitor mentions | Renewal risk assessment and value documentation |
| [Who matters here](who-matters-here.md) | Stakeholders, including who has gone quiet | Stakeholder mapping |
| [Success plan check](success-plan-check.md) | The plan, or a proposal if there is none | Success plan builder |
| [Taking over this account](taking-over-this-account.md) | The first 30 days on an account inherited from another CSM | Seamless account handoffs |
| [Draft a follow-up](draft-a-follow-up.md) | An email after the call. It is not sent | Contextual email drafting |
| [Exec meeting prep](exec-meeting-prep.md) | A one-screen brief for an exec walking into the meeting | Hub: Exec Meeting Prep |
| [Escalation and save plan](save-plan.md) | Why a red account is at risk, and the drafts to hold until you approve | Hub: CSM Command Center and Save Plan |
| [90-day handoff readout](handoff-readout.md) | A one-page briefing and a proposed success plan from post-sales notes | Hub: 90-Day Handoff Success Plan |

## Across the book

| Prompt | Use it for | Lines up with |
|---|---|---|
| [My command center](command-center.md) | Today's actions, the churn radar, and the top account | Hub: CSM Command Center |
| [Expansion signals](expansion-signals.md) | Signals side by side, and the next step for each account | Hub: Growth, Expansion and Handoff |
| [Open CTAs to clean up](open-ctas-to-clean-up.md) | Stale or already-done CTAs. Nothing is closed | CTA triage and cleanup |

## For a CS leader

| Prompt | Use it for | Lines up with |
|---|---|---|
| [Risk and expansion radar](risk-and-expansion-radar.md) | ARR that is safe, at risk, and still on the table | Hub: Risk & Expansion Radar |
| [CS capacity plan](cs-capacity-plan.md) | Where the work is, CSMs needed, and balanced books | Hub: CS Capacity Planning |

## Replaced by the hub

- **QBR outline** is now part of [Customer story and business review](customer-story.md).
- **Draft a VP call note** is now [Exec meeting prep](exec-meeting-prep.md).
- **What needs me this week** and **Renewals coming up** are now [My command center](command-center.md). Its churn radar lists renewals in the next 90 days.
- **Risks across my book** is now the [Risk and expansion radar](risk-and-expansion-radar.md).

## Left out on purpose

- **Writes without approval.** Prompts that draft a CTA, a timeline entry, a CSQL, or an email stop and wait for you. The [skills](../skills/) write, and each card says where.
- **Hardcoded health bands and ARR cutoffs.** A score of 40, or ARR above $500K, means different things in different tenants. These prompts use the labels and scores Copilot finds.
- **Assumed capacity numbers.** The [CS capacity plan](cs-capacity-plan.md) asks for hours, buffer, and segment hours. It does not guess them.
- **Slack canvases and Cowork dashboards.** The hub demos them, but they need a scheduled job or Claude Cowork. These prompts return the same content in the chat.
- **The Agentforce expansion brief.** The structured brief for Agentforce still lives in the [expansion analysis](../../agentforce-cs-agent/templates/expansion-analysis.md) template.
- **Admin reports, GSIDs, and rules.** Those belong in the CS Ops kits.

> Part of the [Gainsight AI Cookbook](../../). Sample prompts, not a supported Gainsight product.
