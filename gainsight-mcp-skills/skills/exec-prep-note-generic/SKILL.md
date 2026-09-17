---
name: exec-prep-note-generic
description: >
  Produces a structured Executive Prep Note for a VP or C-suite joining a client
  call. Synthesizes Gainsight CS + Staircase AI data. Six sections: Executive Summary,
  Why We're Having This Call (1–2 bullets), How They Make Money (1–2 bullets),
  Key Strategic Objectives (O2), Key Contacts, Risk Overview (combined), Client Maturity Index.
  Posts to Gainsight Timeline automatically.

  ALWAYS trigger for: "exec prep note for [Account]", "prepare my exec for [Account]",
  "exec brief for [Account]", "executive prep for [Account]", "get [exec] ready for
  [Account]", "executive briefing for [Account]", "prep note for exec call", "prepare
  executive for [Account] call", "exec joining my call with [Account]", or any request
  to brief an executive before a client meeting. Also trigger when an account
  name appears alongside "exec", "executive", "VP", "C-suite", "briefing", or "prep note".
---

# Executive Prep Note Skill

Produces a structured Executive Prep Note for a single client account, grounded in real data
from Gainsight CS and Staircase AI, plus live web research on the client's business model and
(if publicly traded) recent earnings call intelligence. Designed to be read by a VP or C-suite
executive joining the CSM's client call.

> **Scope constraint:** Accounts with **Status = Active** only. Abort with an error if Status ≠ Active.

---

## Trigger Parsing

Extract the account name from the user's request. Examples:
- "exec prep note for Spring Health" → account = "Spring Health"
- "prepare my exec for Bill.com" → account = "Bill.com"
- "executive briefing for GE Healthcare" → account = "GE Healthcare"

If no account name is present, ask: *"Which account should I generate the executive prep note for?"*

If an exec name is mentioned (e.g. "get [exec name] ready for [account name]"), capture it for use in the
note header. If no exec name is given, use "Executive" as the placeholder.

---

## Phase 0 — Resolve Account Identity in Gainsight

Before querying anything else, resolve the account's Gainsight Company GSID:

```
Gainsight-CSMCP:search_company(search_name="[account name]")
```

Capture:
- `Gsid` (Company GSID — used in all subsequent queries)
- `Name` (canonical account name)
- `Status` — **must equal "Active"**; abort with error if Status ≠ Active
- `CsmName` / `CsmEmail` — capture for reference

Also resolve the requesting CSM's User GSID (use the authenticated user's name):
```
Gainsight-CSMCP:run_query(
  object_name="gsuser",
  select=["Gsid", "Name", "Email"],
  where=[{"name": "Name", "operator": "CONTAINS", "value": ["[CSM last name]"]}]
)
```

### Relationship-Level Resolution

After resolving the Company GSID, find the associated Relationship record:

```
Gainsight-CSMCP:search_relationship(companyId="[Company GSID]")
```

Capture:
- `RelationshipId` (Gsid of the Relationship record) — preferred posting target
- `RelationshipName` — for display in the note header

**Posting logic (hard rule):**
- If a Relationship record is found → use `relationshipId` in `create_timeline_activity`
- If no Relationship record is found → fall back to `companyId` (company-level post)
- Record which level was used; surface it in the Phase 5 confirmation line only

---

## Phase 1 — Data Collection (Run in Parallel Where Possible)

### 1A — Gainsight: Success Plan Objectives (O2 Framework)

```
Gainsight-CSMCP:fetch_success_plan_list(companyId="[Company GSID]")
```

For each active Success Plan, extract:
- Plan name, status, start/end date
- All Objectives: name, value driver, outcome, status, progress notes, due date

**O2 Value Drivers:**
| Value Driver | Slide |
|---|---|
| Improve Retention | 6 |
| Improve User Experience & Product Adoption | 7 |
| Increase Scale & Efficiency | 8 |
| Increase Expansion | 9 |

**16 Valid Outcomes (use exact names):**
| Value Driver | Outcomes |
|---|---|
| Improve Retention | Improve Health Score Predictiveness · Reduce Risk + Churn · Improve Customer ROI · Increase Renewal Forecast Accuracy |
| Improve User Experience & Product Adoption | Optimize Customer Journey · Improve Adoption Depth + Breadth · Improve User Engagement + Experience · Increase Advocates |
| Increase Scale & Efficiency | Increase Customer Facing Teams Impact · Increase Lifecycle Automation · Increase Self-Service Engagement · Prioritize R&D Effectively |
| Increase Expansion | Increase Growth Through Advocacy · Reduce Revenue Leakage · Improve Expansion Velocity · Improve Expansion Pipeline |

Only surface objectives updated or active in the **last 180 days**.

---

### 1B — Gainsight: Risk CTAs

```
Gainsight-CSMCP:fetch_cta_list(companyId="[Company GSID]", status="Open")
```

Filter for `Type = "Risk"` entries. For each, capture:
- CTA name, reason, status, priority, due date
- Any associated timeline notes

---

### 1C — Gainsight: Activity Timeline (Contacts + Call History)

Pull the last 180 days of timeline entries:

```
Gainsight-CSMCP:run_query(
  object_name="activity_timeline",
  select=[
    "Gsid", "Subject", "ActivityDate", "ActivitySubtype",
    "ExternalAttendees", "InternalAttendees", "NotesPlainText",
    "ActivitySentiment", "Ant__Meeting_Type__c",
    "WasAnExecPresentAtThisMeeting", "UserName", "DurationInMins"
  ],
  where=[
    {"name": "GsCompanyId", "operator": "EQ", "value": ["[Company GSID]"], "alias": "A"},
    {"name": "ActivityDate", "operator": "GTE",
     "value": ["[TODAY minus 180 days as ISO string]"], "alias": "B"}
  ],
  where_filter_expression="A AND B",
  sort_by=[{"sortField": "ActivityDate", "sortOrder": "desc"}],
  limit=100
)
```

Extract:
- Unique external contacts: name, title, email, last interaction date
- Engagement frequency per contact
- Whether execs were present at prior meetings (`WasAnExecPresentAtThisMeeting`)

---

### 1D — Staircase AI: Company Summary, Transcripts, Risk Analysis

Run three Staircase queries in parallel:

**Query 1 — Company AI Summary:**
```
staircase_query(query="company overview and health summary for [account name]")
```

**Query 2 — Recent Call Transcripts (last 180 days):**
```
staircase_query(query="strategic and operational call transcripts for [account name] last 180 days")
```

**Query 3 — Risk and Churn Signals:**
```
staircase_query(query="risk signals churn indicators escalation language for [account name]")
```

**Fetch all evidence IDs returned from each query:**
```
staircase_fetch_evidence(id="[evidence_id]")
```
Do this for every evidence ID returned. Do not skip.

---

### 1E — Staircase AI: Email Engagement

```
staircase_query(query="email engagement contacts outreach [account name] last 180 days")
```

Extract:
- Client contacts engaged via email (name, role, frequency)
- Key topics raised in email threads
- Any escalation or dissatisfaction signals

---

### 1F — Business Intelligence: Web Research (Run in Parallel with 1A–1E)

This phase powers **Section 3: How This Client Makes Money**. Run lightweight — you need the
sharpest 1–2 signals, not a full business case.

**Step 1 — Business Model Research (all companies):**
```
web_search("[account name] business model revenue how they make money")
web_search("[account name] company overview customers market position")
```

Capture: revenue model, customer type, any notable market dynamic.

**Step 2 — Public Company Check:**
```
web_search("[account name] stock ticker earnings")
```

If publicly traded, run one targeted earnings search for signals that directly implicate the vendor relationship:
```
web_search("[account name] earnings 2025 customer success retention AI budget headcount")
```

Use `web_fetch` on the most relevant result if a specific vendor-relevant signal appears in the snippet.

**Hard rules:**
- For Section 3, surface at most 2 bullets from all of this — the most call-relevant signals only
- Earnings intelligence only surfaces in Section 3 if it directly implicates the vendor partnership (tech stack consolidation, AI replacing manual work, budget freezes affecting software spend)
- Do not fabricate — if nothing directly relevant is found, omit earnings from Section 3 entirely

---

## Phase 2 — Synthesize the Seven Sections

### Section 1: Executive Summary (4–5 sentences max)

Written for an executive who has never met this client. Tone: peer-to-peer, confident,
business-outcome focused. No internal jargon.

Synthesize from Staircase company summary + Gainsight success plan status + health signals:
- Relationship tenure and current partnership stage
- Primary use case / product footprint
- Current health trajectory (improving / stable / at-risk)
- The single most important strategic theme heading into this call
- One sentence on what the executive should know before entering the room

**Hard rules:**
- Max 5 sentences. No bullet points. Narrative prose only.
- Lead with the relationship, not the product.
- Assume the exec has zero prior context — make it self-contained.

---

### Section 2: Why Are We Having This Exec Connect?

One or two bullets — max. The exec usually already knows why they're on the call. This section
surfaces the single sharpest signal that makes the context unambiguous.

Scan these sources quickly and pick the 1–2 highest-signal reasons:
- Open Risk CTAs (renewal risk, active RFP, competitive displacement)
- Gainsight Timeline — exec presence history, stalled objectives
- Staircase transcripts — escalation language, exec sponsor changes, strategic drift
- Maturity divergence flags (if a product score is way below the composite)

Each bullet follows this pattern:
> **[Signal type]:** [What the data shows] → [What the exec can specifically unlock]

**Hard rules:**
- 1 bullet minimum, 2 bullets maximum
- Every bullet must be grounded in a specific data signal — no generic framing
- If no clear exec-level signal exists, say: "Proactive relationship investment — no active escalation signals found." Do not fabricate urgency.

---

### Section 3: How This Client Makes Money

1–2 bullets only. Just enough to make the exec dangerous in conversation — not a business school
case study. Prioritize what's most relevant to the vendor relationship or the call's context.

Pull from the 1F web research. Surface whichever of these is most useful:
- How the company actually makes money (revenue model, customer type, key metric)
- A market or competitive signal that's relevant to the call (e.g., under budget pressure, AI-driven transformation, consolidating vendors)
- For public companies: one earnings signal if it directly implicates the vendor relationship (budget freeze, headcount reduction, AI replacing manual work)

**Hard rules:**
- Maximum 2 bullets — pick the sharpest signals, not all of them
- Earnings call detail belongs here only if it's directly relevant to the vendor relationship; skip otherwise
- Do not reproduce the full business model writeup — that's for sales strategy and expansion conversations, not exec prep

---

### Section 4: Key Strategic Objectives (Last 180 Days)

Group all O2 objectives by Value Driver. For each objective:
- Status (Active / Completed / At Risk / Stalled)
- Progress summary in 1–2 sentences
- Call/transcript evidence from Staircase

If an objective appears in Staircase transcripts but is NOT in Gainsight, flag it as:
> ⚠️ *Observed in calls — not yet formalized in Success Plan*

**Hard rule:** Do NOT include an "Active Success Plans" sub-section listing plan names, owners, and due dates. Success Plan metadata (names, statuses, owners) is background research only — surface it through objectives grouped by Value Driver, not as a standalone plan inventory block.

---

### Section 5: Key Contacts

Build the contact map from Gainsight `ExternalAttendees` + Staircase email engagement.

For each unique contact, include:
- Name, Title
- Engagement method(s): Call / Email / Both
- Last interaction date
- Engagement depth: High (5+ touchpoints) / Medium (2–4) / Low (1)
- Executive sponsor flag: note if `WasAnExecPresentAtThisMeeting = true` in any call
- Any notable signal (champion, detractor, silent stakeholder, new contact)

Sort by engagement depth (High → Low). Flag the primary exec sponsor prominently.

---

### Section 6: Risk Overview

Combine formal Risk CTAs and observed signals into a single unified list — the exec doesn't need
the distinction; they need to know what's real.

For each item, include:
- What the risk is (plain language, not CTA field names)
- Whether it's a formal CTA or an observed pattern
- For public companies: flag any earnings-linked dimension if relevant (budget, headcount, AI displacement)
- Risk Trajectory: **Improving / Stable / Escalating** at the bottom

Max 3–5 items total. Use `color:#c0392b` for risk items in HTML output.
State plainly if nothing is real: "No active risk signals identified."

**Hard rules:**
- **No adoption risk CTAs:** Do NOT include auto-generated adoption risk CTAs (e.g., "HAUs dropped X%", "Active Users dropped X%"). These are system-generated signals and not meaningful exec-level risk items. If adoption risk is a genuine strategic concern, surface it as an observed signal in plain business language (e.g., "CDM adoption stalled pending executive mandate") — not as a raw CTA citation.
- **No cross-sell closed-lost:** Do NOT include failed or declined cross-sell/upsell opportunities as risk items. A product a customer chose not to buy is not a risk to the existing relationship.

**Tone guidance:** Business context, not CRM language.
Example: "Active RFP underway — renewal at risk in Q2" not "Risk CTA: Open"

---

### Section 7: Client Maturity Index

Score maturity **per active product first**, then roll up to a composite index.

**Step A — Identify Active Products**

Confirm which products the client actively uses (confirmed in transcripts, timeline, or Gainsight).
List each contracted product line and mark whether it is evidenced in calls/timeline data.

Only score products confirmed active. Mark contracted but unevidenced products as
"Contracted — not evidenced" and exclude from scoring.

**Step B — Per-Product Maturity Score**

For each active product, score 5 dimensions on a 1–4 scale:

| Dimension | Signals | Score (1–4) |
|---|---|---|
| **Strategic Engagement** | Business outcomes, ROI, exec-level strategy discussions | 1 = transactional / 4 = consultative |
| **Self-Sufficiency** | Self-serve, references docs, runs product independently | 1 = high-touch dependent / 4 = autonomous |
| **Stakeholder Maturity** | Seniority and breadth of contacts for this product | 1 = single end-user / 4 = C-suite + cross-functional |
| **Adoption Depth** | Advanced features, new use cases, expansion conversations | 1 = basic / 4 = power user / evangelist |
| **Partnership Quality** | Proactive and mutual vs. reactive and transactional | 1 = reactive / 4 = strategic co-creator |

**Per-Product Score = Sum of 5 dimensions / 20 → normalize to 1–10 scale**

**Step C — Product Breadth Multiplier**

| Active Products | Multiplier |
|---|---|
| 1 product | × 0.80 |
| 2 products | × 0.90 |
| 3 products | × 0.95 |
| 4+ products | × 1.00 |

**Step D — Composite Maturity Index**

```
Raw Average = Equal-weighted average of all per-product scores
Composite Maturity Index = Raw Average × Product Breadth Multiplier
```

Express on a 1–10 scale. Round to one decimal. Label as:
- 1–3: **Foundational** — Limited adoption, reactive engagement
- 4–6: **Developing** — Growing adoption, emerging strategic conversations
- 7–8: **Advanced** — Multi-product, consultative, exec-aligned
- 9–10: **Champion** — Deep adoption, co-innovating, high expansion potential

**Flag divergence:** If any product score deviates more than 2 points from the Raw Average,
call it out explicitly.

**Scoring guardrails:**
- 7+ requires direct transcript evidence of strategic engagement for that product
- "Has exec sponsor" alone does not justify high Stakeholder Maturity
- "Renews on time" does not count as strategic engagement
- If evidence is thin, default to the lower bound, not the midpoint

---

## Phase 3 — Render Output

### Hard Rules: HTML Formatting for Timeline Posting

The exec prep note MUST be rendered as clean, structured HTML. These rules are non-negotiable —
the HTML is what gets posted to Gainsight Timeline and must render correctly and be easy to consume.

**Structural rules:**
- Inline styles ONLY — no `<style>` tags, no external CSS (Gainsight strips them)
- No `<html>`, `<head>`, or `<body>` wrappers — output the `<div>` block only
- Every section MUST use the exact `<h3>` header format defined below — no plain text headers
- All body text MUST be wrapped in `<p>` tags — no naked text nodes
- All lists MUST use `<ul>/<li>` — no hyphens, asterisks, or dashes as bullet substitutes
- All tables MUST include `border-collapse:collapse`, explicit `padding` on every `<th>` and `<td>`, and alternating row backgrounds (`#fff` / `#f5f7fa`)
- No `<br>` tags to fake spacing — use `margin-top` on block elements instead
- No emoji in headers or section titles — clean text only
- Risk items MUST use `color:#c0392b` — never plain black text for open risks
- Earnings call ⚠️ Vendor Relevance callouts MUST use the orange callout box format — never inline text

**Whitespace and readability rules:**
- Sections separated by `margin-top: 24px` on each `<h3>`
- Table cells: minimum `padding: 8px` on all sides
- Font size: `13px` for tables and metadata lines; `inherit` (default) for body prose
- Line height: `1.6` on the outer wrapper — do not override inside sections
- Max width: `900px` on the outer wrapper — do not exceed

**Prohibited patterns (will cause poor Timeline rendering):**
- No raw HTML entities used as decorative bullets (e.g., `&bull;`, `&#8226;`)
- No `<div>` used as a paragraph substitute — use `<p>` for prose
- No nested tables
- No hardcoded pixel widths on table columns — use percentages or `width:100%` on the table only
- No `<font>` tags — use inline `style` on the appropriate element instead

**Color palette:**
- `#0a2f5e` — dark blue headers
- `#1a1a1a` — body text
- `#f5f7fa` — alternate row background
- `#c0392b` — open Risk CTAs
- `#e67e22` — ⚠️ Vendor Relevance callout background (`#fff8f0`)
- Maturity label colors: Foundational=`#e74c3c`, Developing=`#f39c12`, Advanced=`#27ae60`, Champion=`#1a6b3a`

**HTML structure:**
```html
<div style="font-family: Arial, sans-serif; max-width: 900px; line-height: 1.6; color: #1a1a1a;">

  <h2 style="color: #0a2f5e; border-bottom: 2px solid #0a2f5e; padding-bottom: 6px;">
    Executive Prep Note — [Account Name]
  </h2>
  <p style="color: #666; font-size: 13px; margin-top: -8px;">
    Prepared by [CSM Name] · [Date] · For: [Exec Name or "Executive"]
  </p>

  <!-- Section 1: Executive Summary -->
  <h3 style="color: #0a2f5e; margin-top: 24px;">1. Executive Summary</h3>
  <p>[Narrative prose — 4-5 sentences, exec audience]</p>

  <!-- Section 2: Why Are We Having This Exec Connect? -->
  <h3 style="color: #0a2f5e; margin-top: 24px;">2. Why Are We Having This Exec Connect?</h3>
  <ul>
    <li><strong>[Signal type]:</strong> [What the data shows] → [What the exec can specifically unlock]</li>
    <!-- 1–2 bullets max. Grounded in a specific data signal. -->
  </ul>

  <!-- Section 3: How This Client Makes Money -->
  <h3 style="color: #0a2f5e; margin-top: 24px;">3. How This Client Makes Money</h3>
  <ul>
    <li>[Revenue model / market signal most relevant to this call]</li>
    <!-- 1–2 bullets only. Sharpest signals. Include a vendor-relevant earnings flag here if applicable. -->
  </ul>
  <!-- If a public company earnings signal directly implicates the vendor: -->
  <div style="background:#fff8f0; border-left:4px solid #e67e22; padding:10px 14px; margin:12px 0; font-size:13px;">
    <strong>⚠️ Vendor Relevance:</strong> [Direct implication for vendor relationship]
  </div>

  <!-- Section 3: Key Strategic Objectives -->
  <h3 style="color: #0a2f5e; margin-top: 24px;">4. Key Strategic Objectives (Last 180 Days)</h3>
  [Grouped by Value Driver — use <strong> for driver headers, <ul>/<li> for objectives]

  <!-- Section 4: Key Contacts -->
  <h3 style="color: #0a2f5e; margin-top: 24px;">5. Key Contacts</h3>
  <table style="width:100%; border-collapse:collapse; font-size:13px;">
    <thead>
      <tr style="background:#0a2f5e; color:#fff;">
        <th style="padding:8px; text-align:left;">Name</th>
        <th style="padding:8px; text-align:left;">Title</th>
        <th style="padding:8px; text-align:left;">Engagement</th>
        <th style="padding:8px; text-align:left;">Last Touch</th>
        <th style="padding:8px; text-align:left;">Depth</th>
        <th style="padding:8px; text-align:left;">Signal</th>
      </tr>
    </thead>
    <tbody>[rows — alternating #fff / #f5f7fa background]</tbody>
  </table>

  <!-- Section 6: Risk Overview -->
  <h3 style="color: #0a2f5e; margin-top: 24px;">6. Risk Overview</h3>
  <ul>
    <li style="color:#c0392b;">[Risk item — plain language, business context. Note if formal CTA or observed signal.]</li>
    <!-- Max 3–5 items. Formal CTAs and observed signals combined. Earnings-linked risks included inline if applicable. -->
  </ul>
  <p><strong>Risk Trajectory:</strong> [Improving / Stable / Escalating]</p>

  <!-- Section 7: Client Maturity Index -->
  <h3 style="color: #0a2f5e; margin-top: 24px;">7. Client Maturity Index</h3>
  <p><strong>Composite Maturity Index: [X.X] / 10 — <span style="color:[label-color];">[Label]</span></strong></p>
  <p style="color:#666; font-size:13px;">Product Breadth Multiplier: ×[multiplier] ([N] active products)</p>

  <table style="width:100%; border-collapse:collapse; font-size:13px; margin-top:8px;">
    <thead>
      <tr style="background:#0a2f5e; color:#fff;">
        <th style="padding:8px; text-align:left;">Product</th>
        <th style="padding:8px; text-align:center;">Strategic Engagement</th>
        <th style="padding:8px; text-align:center;">Self-Sufficiency</th>
        <th style="padding:8px; text-align:center;">Stakeholder Maturity</th>
        <th style="padding:8px; text-align:center;">Adoption Depth</th>
        <th style="padding:8px; text-align:center;">Partnership Quality</th>
        <th style="padding:8px; text-align:center;"><strong>Score /10</strong></th>
      </tr>
    </thead>
    <tbody>[rows per active product]</tbody>
  </table>

  <p style="margin-top:10px;">[Divergence flag if any product deviates ≥2 points]</p>
  <p>[2–3 sentence narrative anchored to evidence]</p>

</div>
```

---

## Phase 4 — Post to Gainsight Timeline

Post silently — do NOT stream progress or intermediate results to chat.

**If Relationship record was found (preferred):**
```
Gainsight-CSMCP:create_timeline_activity(
  relationshipId="[Relationship GSID]",
  subject="Executive Prep Note — [Account Name]",
  activityDate="[Today ISO date]",
  typeName="Update",
  notes="[Full HTML block]",
  custom_field_values={"Status": "N/A - Internal Update", "Update Type": "Internal notes"}
)
```

**If no Relationship record (company-level fallback):**
```
Gainsight-CSMCP:create_timeline_activity(
  companyId="[Company GSID]",
  subject="Executive Prep Note — [Account Name]",
  activityDate="[Today ISO date]",
  typeName="Update",
  notes="[Full HTML block]",
  custom_field_values={"Status": "N/A - Internal Update", "Update Type": "Internal notes"}
)
```

**Hard rules:**
- `typeName` MUST be `"Update"` — no exceptions
- `custom_field_values` MUST include BOTH keys on every post — omitting either causes an error:
  - `"Status": "N/A - Internal Update"`
  - `"Update Type": "Internal notes"` ← case-sensitive: lowercase 'n' — "Internal Notes" will fail
- Never post with only one of the two `custom_field_values` keys — both are required every time
- Never alter the case of these values — Gainsight picklist matching is case-sensitive
- `notes` receives the full HTML block from Phase 3

---

## Phase 5 — Silent Completion Confirmation

**HARD RULE — FULLY SILENT EXECUTION:**
- Do NOT stream any intermediate steps, tool calls, data pull progress, status messages,
  or partial results to chat at any point during Phases 0–4.
- Do NOT narrate what you are doing (e.g., no "Now pulling Gainsight data…", "Querying Staircase…",
  "Resolving account identity…").
- Do NOT output the HTML block to chat under any circumstances.
- The ONLY chat output from this skill is the compact confirmation block below, after the
  Timeline post succeeds. Everything else is silent.

**On success, output a single confirmation block (no more than 8 lines):**

```
✅ Executive Prep Note posted for [Account Name]
   For: [Exec Name or "Executive"]
   Posted at: [Relationship level — "[RelationshipName]"] OR [Company level (no relationship found)]
   Data window: [Start date] → [Today]
   Contacts: [N] · Objectives: [N] · Open Risks: [N]
   Maturity: [X.X]/10 ([Label]) — [per-product breakdown]
   Business Intel: [Public — [Ticker] · Q[X] [YYYY] earnings reviewed] OR [Private — no earnings data]
   Vendor Relevance flags: [N found] OR [None]
```

If the Timeline post fails, surface the error message and provide the HTML block for manual posting.
Do NOT silently swallow failures.

---

## Error Handling

- **Account not found in Gainsight:** Prompt user to check spelling. Do not proceed.
- **Account Status ≠ Active:** Surface: "[Account Name] has a status of [Status] — exec prep notes are only generated for Active accounts."
- **No Relationship record found:** Fall back to company-level post. Note in confirmation line.
- **No Success Plan found:** Note in Section 3: "No active Success Plan on file. Strategic objectives were inferred from call transcripts and Staircase AI only."
- **No Staircase data found:** Proceed with Gainsight + web data only. Note the gap explicitly in each affected section.
- **No earnings call data found (public company):** Note "No relevant earnings call signals found for this period" in each earnings category.
- **Web search returns no business model data:** Note "Business model research returned limited results — manual review recommended" and proceed with available data.
- **No activity in last 180 days:** Flag in Executive Summary and reduce scope to available data range.
- **Timeline post fails:** Surface error and output full HTML block with instructions for manual posting.
- **Missing `custom_field_values` error from Gainsight:** Retry with both keys explicitly set: `{"Status": "N/A - Internal Update", "Update Type": "Internal notes"}`
