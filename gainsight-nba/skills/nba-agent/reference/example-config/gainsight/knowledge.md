# Knowledge (example: Gainsight CS)

Use this to (a) pick the right feature to nudge a low-adoption user toward and (b) describe it the way the docs do. Every feature name, capability, or benefit in a draft must trace to a URL here or to a release-notes page you fetched. Do not invent feature names or capabilities.

Scope: Gainsight CS (NXT) only. Every item below belongs to the product Gainsight CS. Sources are support.gainsight.com pages fetched directly (2026-07-30).

## How to use in the loop

1. Take the account's adoption gap from the data and ground steps (the signal, CS scorecard, Staircase grounding).
2. Match it to a feature in the gap map below.
3. Check entitlement: features marked (add-on) are paid. Do not nudge a feature the account may not own without flagging it as `[verify entitlement]`.
4. For currency, fetch the latest release notes (Part 2) and prefer a newly shipped, relevant feature when one fits.
5. Name the feature in the draft exactly as the docs name it, with a one-line value grounded in the source.

## Part 1. Adoption-relevant CS features

| Feature (doc name) | What it does | Adoption gap it addresses | Source |
| --- | --- | --- | --- |
| CTAs, Tasks, and Playbooks (Cockpit) | Cockpit is the CSM day-to-day workspace. CTAs are data- or lifecycle-driven alerts, "the backbone of the Cockpit"; each carries a Playbook of best-practice tasks. | Open risks/opportunities with no structured follow-up. | https://support.gainsight.com/gainsight_nxt/04Cockpit_and_Playbooks/00Cockpit_Horizon_Experience/About/CTAs%2C_Tasks%2C_and_Playbooks_Overview |
| Success Plans | Define, track, and communicate a customer's strategic goals in a shared workspace; track progress via CTAs and tasks. Admins can build templates. | User has never opened a Success Plan; no shared, tracked goals. | https://support.gainsight.com/gainsight_nxt/Success_Plans/About/Success_Plan_Overview |
| Scorecards | Track multiple dimensions of customer health (each dimension is a Measure, e.g. product usage, support, renewal chances) and report on them. | No health visibility; risk not tracked or scored. | https://support.gainsight.com/gainsight_nxt/05Scorecards/01About/Scorecards_Overview |
| Timeline | "The official record of your customers." Log and view interactions over the lifecycle; reachable from C360 and CTA detail. | No logged record of interactions; activity not captured. | https://support.gainsight.com/gainsight_nxt/Timeline/01About/Timeline_Overview |
| Adoption Explorer | Manages customer usage data (Company and Person level, daily/weekly) plus entitlements; derives metrics without Rules Engine. | No usage visibility; can't see who under-adopts or track entitlement vs. use. | https://support.gainsight.com/gainsight_nxt/Adoption_Explorer/About/Adoption_Explorer_Overview |
| Customer 360 / Relationship 360 | Central hub synthesizing a customer's business data into one view; cuts meeting-prep time. | No single account view before customer meetings. | https://support.gainsight.com/gainsight_nxt/07360/User_Guides/Overview_of_C360%2F%2FR360_Sections_and_Widgets |
| Gainsight Home | One-stop CSM workspace showing insights and action items across the full portfolio. | Not working from a prioritized cross-book view. | https://support.gainsight.com/gainsight_nxt/Gainsight_Home/About/Gainsight_Home_Overview |
| Surveys | Design and distribute surveys (CSAT, NPS, etc.), integrated to JO/CTAs, with follow-ups triggered from responses. | No voice-of-customer or sentiment signal captured. | https://support.gainsight.com/gainsight_nxt/06Surveys/01About/Surveys_Overview |
| Copilot | AI conversational assistant inside CS; answers context questions from structured records plus unstructured interaction data. | CSM manually digging sources instead of using AI. | https://support.gainsight.com/gainsight_nxt/AI_Assistants/Copilot/About/Copilot_Overview |
| Reports and Dashboards (Horizon) | Turns disparate customer data into a single source of truth and surfaces insights to deploy actions. | Data not turned into shared insight. | https://support.gainsight.com/gainsight_nxt/Reports_and_Dashboards/About/Horizon_Reports_and_Dashboards_Overview |
| Renewal Center (add-on) | Analyze and forecast renewals; enriches CRM with a predictive health score to spot risk earlier. | Renewals not forecast; at-risk accounts caught late. | https://support.gainsight.com/gainsight_nxt/Renewal_Center/01About/Renewal_Center_Overview |
| Journey Orchestrator and Automated Email (add-on) | "Your center for automated communications". automate customer communications at scale. This is the agent's own delivery surface. | No automated or scaled touchpoints. | https://support.gainsight.com/gainsight_nxt/Journey_Orchestrator_and_Email_Templates/About/Journey_Orchestrator_and_Automated_Email_Overview |
| Sally (Gainsight Bot) | Brings Gainsight data, health, risks, and record updates into Slack/Teams via chat. | Insights not reachable where the CSM already works. | https://support.gainsight.com/gainsight_nxt/AI_Assistants/Sally/Sally_for_Slack/About/Sally_-_The_Gainsight_Bot_Overview |

Naming notes: the doc calls it "Scorecards" (not "Scorecards 2.0"); Cockpit, CTAs, and Playbooks live under one "CTAs, Tasks, and Playbooks" doc; the CS email-send surfaces are Email Assist and Group Send under Journey Orchestrator and Automated Email.

## Part 2. Latest CS features (fetch at runtime for currency)

Canonical URLs (fetch the raw page, not a summarizer):
- Release notes hub: https://support.gainsight.com/gainsight_nxt/Release_Notes
- Current-year index: https://support.gainsight.com/gainsight_nxt/Release_Notes/Current_Release_Notes_-_2026

Most recent found at build time: **Q2, July 2026** (https://support.gainsight.com/gainsight_nxt/Release_Notes/Current_Release_Notes_-_2026/Gainsight_CS_Release_Notes_Q2_July_2026). Refresh this section by re-fetching the hub. Release notes are labeled by month/quarter, not per-feature dates. Per-feature dates are not published.

Top features shipped in Q2 July 2026:
- JO: Create Programs with AI Assistant ("Build with AI") from a natural-language prompt.
- JO: Track Program Outcomes with Program Goals (health-score, lifecycle-stage, renewal-date change), beyond opens/clicks.
- JO: Generate AI-powered subject lines and preheaders from the email body in the Template Builder.
- JO: Branch journeys based on email responses (Responded / Not Responded paths).
- JO: Translate email templates in one action, preserving HTML/CSS and merge tokens.
- Email Assist / Group Send: track email responses ("Email Responded" metric for unique repliers).
- Data Management: view Staircase AI Insights directly in Gainsight CS (near real-time sync into C360 Summary and Home).
- Copilot / AI Agent in Slack: query Relationships and create records (Timeline, CTAs, Success Plans, Tasks) from chat.
- Cockpit: group CTAs by Owner to spot unassigned CTAs.
- Timeline: associate Timeline activities with Success Plans.

Relevance to this agent: the JO AI features (Build with AI, AI subject lines, Program Goals, response branching) and Group Send response tracking are the same surface the design doc scopes for delivery; "Staircase AI Insights in CS" is the grounding layer this agent already uses.
