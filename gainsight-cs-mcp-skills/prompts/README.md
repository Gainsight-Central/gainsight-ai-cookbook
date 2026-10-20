# Prompts for Gainsight Copilot

Paste these into Gainsight Copilot. There is nothing to install.

Copilot reads Gainsight. When Staircase is connected, these prompts also use conversation intelligence (sentiment and what the customer said). When it is not connected, the prompt tells Copilot to say so.

You never paste an id. Where a prompt names an account, replace `[customer name]` with the customer.

These are the jobs CSMs actually ask for, matched to the [Customer Success prompts](https://www.gainsight.com/mcp/library/?_mcp-type=prompt&_products=customer-success) on the Gainsight CS MCP library. The wording here is the cookbook's: short, read-only, and unwilling to invent a number.

## On one account

| Prompt | Use it for | Library job it lines up with |
|---|---|---|
| [Prep for a call](prep-for-a-call.md) | Before a customer call | Meeting prep in 60 seconds |
| [How is this account doing?](how-is-this-account.md) | A quick health check | Current health status |
| [Catch me up](catch-me-up.md) | The last 30 days | Last 30 days of activity |
| [QBR outline](qbr-outline.md) | The last 90 days, as a QBR | QBR outline builder |
| [Renewal conversation](renewal-conversation.md) | One renewal meeting, including value and competitor mentions | Renewal risk assessment and value documentation |
| [Who matters here](who-matters-here.md) | Stakeholders, including who has gone quiet | Stakeholder mapping |
| [Success plan check](success-plan-check.md) | The plan, or a proposal if there is none | Success plan builder |
| [Taking over this account](taking-over-this-account.md) | The first 30 days on an inherited account | Seamless account handoffs |
| [Draft a follow-up](draft-a-follow-up.md) | An email after the call. It is not sent | Contextual email drafting |
| [Draft a VP call note](draft-a-vp-call-note.md) | A chat-only note when an exec is joining | Executive briefing |

## Across the book

| Prompt | Use it for | Library job it lines up with |
|---|---|---|
| [What needs me this week](what-needs-me-this-week.md) | A ranked Monday list | Weekly portfolio triage |
| [Renewals coming up](renewals-coming-up.md) | Renewals in the next 90 days | Portfolio renewal calendar |
| [Risks across my book](risks-across-my-book.md) | Open risk CTAs, most urgent first | Portfolio health report |
| [Open CTAs to clean up](open-ctas-to-clean-up.md) | Stale or already-done CTAs. Nothing is closed | CTA triage and cleanup |

## Left out on purpose

- **Writes.** Closing a CTA, posting Timeline, and assigning an owner are not in this folder. The prompts recommend or draft. The [skills](../skills/) write, and each card says where.
- **Hardcoded health bands and ARR cutoffs.** A score of 40, or ARR above $500K, means different things in different tenants. These prompts use the scores Copilot finds.
- **A 120-day renewal window.** The library uses 120 days. This pack uses 90, which matches a Monday pass. Use [Renewal conversation](renewal-conversation.md) for one account.
- **Competitor-only and cross-customer feature research.** Competitor mentions sit inside the renewal conversation. A topic search across every customer is a different job.
- **Expansion as its own prompt.** The output contract already lives in the Agentforce [expansion analysis](../../agentforce-cs-agent/templates/expansion-analysis.md) template. Expansion signals are included in the QBR and renewal prompts.
- **Admin reports, GSIDs, and rules.** Those belong in the CS Ops kits.

These prompts do not post to Timeline or send email. The [skills](../skills/) do more of the job when calendar, email, or other tools are connected, and the cards on the cookbook site say what each one writes.

> Part of the [Gainsight AI Cookbook](../../). Sample prompts, not a supported Gainsight product.
