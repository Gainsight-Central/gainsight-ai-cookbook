---
name: weekly-call-briefs
description: >
  Weekly Call Brief dashboard — a full-week interactive HTML widget of external client
  calls (Mon–Fri), pulled from your calendar and enriched with CRM and conversation
  intelligence data. Each call card expands to show an account brief, prioritized
  talking points, a draft pre-call agenda email, three executive ghost email variants,
  and a one-click "Update Success Plan" / "Generate Risk Update" action panel.
  Defaults to the current Mon–Fri week; accepts overrides like "next week" or
  "week of Apr 14". Always trigger this skill for: "weekly brief", "weekly call brief",
  "prep my week", "calls this week", "calls next week", "week of [date]",
  "show me my week", "weekly prep". NOT for daily/today queries — those should use
  a daily brief skill instead.
---

# Weekly Call Briefs

A generic, shareable version of the weekly call brief dashboard. **Before first use,
edit `config.md` in this skill folder** to fill in your CSM name, CRM user ID, timezone,
calendar filters, and CRM/conversation-intel MCP names.

When this SKILL.md references `{{CONFIG.X}}`, read the value from `config.md`. If a
required config value is missing, surface a clear error in the closing message and
do not fabricate.

---

## SILENT EXECUTION — HARD RULE

Run ALL phases (calendar fetch, conversation intel queries, CRM queries, synthesis,
widget render) completely silently. Output ONLY:

1. A single short loading message before data gathering
2. The widget itself
3. A short closing summary line

Zero narration, zero tool-call commentary, zero raw data, zero intermediate status
messages at any step.

---

## Step 0 — Read Config

Read `config.md` from this skill's folder. Parse out:

- `CSM_NAME`, `CSM_USER_ID`, `TIMEZONE`, `EMAIL_SIGNATURE`
- `INTERNAL_EMAIL_DOMAIN`, `CALENDAR_EXCLUDE_KEYWORDS`
- `CRM_MCP_NAME`, `CONVERSATION_INTEL_MCP_NAME`
- Branding colors (use defaults if absent)

If `CSM_USER_ID` or `CSM_NAME` is still a placeholder ("PASTE_..." or "Your Full Name"),
abort and tell the user to edit `config.md` first.

---

## Step 1 — Calendar Fetch

Use the user's connected Google Calendar MCP (or equivalent). Call `list_events` for
the date range:

- **Default range:** Monday 00:00 → Friday 23:59 of the current week, in `{{CONFIG.TIMEZONE}}`
- **Override range:** If user said "next week", "week of [date]", etc., compute from that

**Filter rules** (keep an event only if ALL apply):
- At least one attendee email does NOT contain `{{CONFIG.INTERNAL_EMAIL_DOMAIN}}`
- `allDay` is `false`
- `status` is `confirmed`
- Event title (lowercased) does NOT contain any substring from `{{CONFIG.CALENDAR_EXCLUDE_KEYWORDS}}`

For each kept event, extract:
`client` (best guess from external attendee company or event title),
`meetingDay`, `meetingDate`, `meetingTime`, `meetingType` (from title keywords:
QBR, EBR, Strategic, Operational, Config, Discovery, Onboarding, etc. — fall back
to "Sync"), `durationMins`, `attendees[]`, `attendeeEmails[]`, `calendarEventId`.

Sort the final list chronologically.

---

## Step 2 — Per-Client Data Gathering (run in parallel where possible)

For each unique client across the week, gather two parallel data pulls.

### 2A — Conversation Intelligence (Staircase / Gong / Chorus / etc.)

Skip this section entirely if `CONVERSATION_INTEL_MCP_NAME` is empty in config.

Run two queries against your conversation intel MCP for each client:

1. **Recent calls + themes:**
   `"<client name> recent strategic operational call transcript themes sentiment last 60 days"`
2. **Support / friction signals:**
   `"<client name> support ticket issue bug complaint escalation"`

For every evidence ID returned, fetch the full content (most conversation intel MCPs
expose a `fetch_evidence` or equivalent tool — use whatever your MCP provides).

**Failure handling:** If the MCP errors, retry once. On second failure, set a
`staircaseWarning = true` flag and use a fallback string ("No conversation data
available for this account") in the brief. Display a `⚠` pill on the source row.

### 2B — CRM Queries

For each client, in parallel:

1. **Find the account:** Search your CRM by client name → resolve a unique account ID.
   If multiple matches return, pick the one owned by `{{CONFIG.CSM_USER_ID}}`.
2. **Active objectives / success plan:** Fetch open objectives at the relationship level
   where the owner equals `{{CONFIG.CSM_USER_ID}}`. Capture:
   - Plan ID, plan name, plan modified date
   - Each objective's name, due date, status, ID
   - Flag any objective with `due_date < today` as overdue.
3. **Active risk records:** Fetch open Risk-type CTAs / records. For each, capture the
   fields described in `RISK_TRIGGER_FIELDS` in config so you can decide whether to
   show the "Generate Risk Update" button.
4. **Recent timeline (last 2 entries):** Fetch the 2 most recent timeline activities
   for the account.

Store the bundle as: `{accountId, planId, planName, planModified, relationshipId,
objectives[], riskRecord, recentTimeline[]}`

---

## Step 3 — Synthesize Account Brief (per client)

Inlined from the original `account-brief` sub-skill. For each client, produce:

```json
{
  "summary": "2-3 sentence narrative",
  "themes": [{"label": "≤4 words", "detail": "1-2 sentences"}],
  "momentum": ["positive signal", ...],
  "risks": ["risk signal", ...]
}
```

**Summary rules** (2-3 sentences):
- Sentence 1: Lead with conversation intel framing — engagement level, relationship tone, current focus.
- Sentence 2: Primary active workstream or tension heading into this call.
- Sentence 3: Health signal — sentiment trend, open risks, overdue items, or renewal proximity.
- If conversation intel unavailable, lead with CRM objective status and open risks.
- Never fabricate. If no data: `"No recent activity data — review manually."`

**Themes (3-5 items):**
- Pull from conversation intel topics, transcript themes, objective names, support patterns.
- Label ≤4 words, specific over generic ("HAU Adoption Drop" > "Adoption").
- Detail: 1-2 sentences describing what is actively happening.
- Order by recency/urgency.

**Momentum (0-3 items):**
- Positive client mentions of the product, milestone completions, exec engagement, forward progress.
- Format as short declaratives. Empty array if none — never fabricate.

**Risks (0-3 items):**
- Real signals only: open risk records, overdue objectives >30 days, negative sentiment, churn language, stalled objectives.
- ≤10 words each, prefixed with category: `"Adoption Risk:"`, `"Overdue:"`, `"Renewal:"`, `"Sentiment Drop:"`.

---

## Step 4 — Synthesize Talking Points (per call)

Inlined from the original `talking-points` sub-skill. Produce 3-4 talking points per call.

**Priority stack (apply in order):**

1. **Risk first.** If an active risk record exists OR conversation intel surfaces churn /
   negative sentiment / executive disengagement, the first TP must address it directly.
   Frame as an open question grounded in specific transcript or ticket language.
2. **Support / product friction.** If recurring support issues or unresolved bugs surface,
   include a TP. Frame: "Close the loop on X" / "Confirm resolution of Y."
3. **Overdue objectives.** Each objective overdue >30 days gets a TP framed as a triage
   decision (close, reset timeline, escalate) — not a status check.
4. **Active objective progress.** 1-2 TPs on the most important open objectives. Focus on
   what's blocked or what the next milestone is.
5. **Forward-looking.** One TP on what's next: renewal timing, expansion signal, upcoming
   milestone, positive theme to open the call on momentum.

**Hard rules:**
- Each TP is one sentence, action-oriented, **under 25 words**.
- Every TP must trace to a real signal (transcript, ticket, objective, risk record).
- No generic filler ("ask about their experience", "review the agenda").
- Max 4 TPs. 3 is fine if signals are sparse.
- For QBR/EBR meetings: lead with business outcomes / ROI / exec themes, not features.
- For Config Sessions: lead with the specific config task or related ticket.
- If conversation intel returned nothing, fall back to CRM-only TPs and note the gap
  in your internal sources block — never hallucinate transcript content.

---

## Step 5 — Synthesize O2 / Value Driver Recommendation (per call)

Inlined from the original `o2-success-plan-updater` sub-skill (the per-call inference part —
NOT the bulk write pass). For each call, decide what objective the recent activity supports.

If your CRM uses a Value Driver / Outcome framework, map each call's signals to:
- A `suggestedValueDriver` (one of your defined drivers)
- A `suggestedOutcome` (one of your defined outcome names — exact text, never invented)
- A `rationale` — one sentence grounded in real signals (no fabrication)
- An action: `update_existing_objective` (if a matching objective exists on the plan) or
  `create_new_objective`

If your CRM does NOT use a Value Driver / Outcome framework, simply produce a
`suggestedTopic` (3-6 words) and `rationale`. The widget will show this in the Actions
panel without forcing the framework structure.

If no clear mapping exists for this call, set `suggestedOutcome = null` and the widget
will show "No outcome match — review manually."

---

## Step 6 — Draft Pre-Call Agenda Email (per call)

Inlined from `agenda-drafter`. Producing a draftable email body for each upcoming call.

**Phase 0 — Continuity data:**
- Pull the most recent strategic call from conversation intel within the past 30-45 days.
- Pull the 1-2 most recent timeline entries (Call/Email/Update type) corresponding to or
  following that call.
- Extract Next Steps / Action Items from both, dedupe, keep 2 most actionable.
- Use the calendar invite's attendee list (already extracted in Step 1) for the To: field.

**Email format (under 200 words):**

```
Hey [First Name(s) or "[Client] team"],

Looking forward to our upcoming conversation! In preparation for our call, here is a brief agenda:

Picking up from last time:
- [Next Step #1]
- [Next Step #2]   <- only if 2 clear ones

Key topics from our last call:
- [Topic 1]
- [Topic 2]
- [Topic 3]

Are there any additional topics you would like to cover, or any questions that have come up since we last spoke?

Best,
{{CONFIG.EMAIL_SIGNATURE}}
```

**Rules:**
- Salutation: "Hey [First Name]," for one contact, "Hey [Client] team," for 2+.
- Plain ASCII apostrophes (`'`) only — no curly quotes.
- **No em-dashes** anywhere. Use hyphens, commas, or restructured sentences.
- Subject line: `Agenda: [Client] sync — [Day] [Mon DD]`
- If no previous call found, omit "Picking up from last time" gracefully.
- If calendar invite has no client attendees, leave `agendaTo` empty and flag it.

---

## Step 7 — Draft Three Ghost Exec Email Variants (per call)

Inlined from `ghost-exec-email`. 3 variants per call, all under 120 words each.

**Phase 0 — Gather:**
- Exec sponsor: query the CRM Person/Contact records for this account, filter where
  IsPrimary or Title contains "Chief|VP|SVP|EVP|President|Director". Pick top one.
  Fallback: `[Client] Executive`.
- 1 positive theme from conversation intel → P2 anchor.
- 1 strategic topic / objective from CRM → P3 anchor.

**Canonical 4-paragraph structure (every variant):**

```
[P1 — WARM OPENER]
One sentence. "I hope you're doing well." or equivalent. No agenda yet.

[P2 — ACCOUNT-SPECIFIC ACKNOWLEDGMENT]
2-3 sentences. Reference one real specific thing from conversation intel or CRM —
a momentum theme, an active initiative, a milestone. Show leadership is paying
attention. Genuine enthusiasm for what they're doing.

[P3 — THE ASK]
2-3 sentences. One clear, low-pressure CTA. Tie directly to the strategic topic
from CRM. Frame as alignment / support — not a check-in or review.

[P4 — SOFT CLOSE]
1-2 sentences. Defer to their schedule. Warm sign-off.
```

**Three variant strategies:**

1. **Momentum acknowledgment** — P2 anchors a specific positive theme; P3 asks to connect
   around measurement / alignment / ensuring product is supporting the initiative.
2. **Strategic partnership framing** — P2 anchors a named strategic objective from CRM;
   P3 frames the connection as exec-to-exec alignment on a shared goal.
3. **Simple low-friction outreach** — P2 keeps it brief and general; P3 is a casual,
   open-ended sync request. Best fallback when data is sparse.

**Rules:**
- Under 120 words per variant.
- Signature: `[Executive Name] | [Title] | [Company]` — placeholder, never hardcoded.
- NEVER mention: churn, risk, adoption drop, cancellation, escalation, competitors.
- NEVER promise specific outcomes.
- Plain ASCII apostrophes only. **No em-dashes.**
- Salutation: `Hi [Exec Sponsor Name],` or `Hi [Client] Executive,`.
- Subject lines conversational, not corporate.
  - Good: `"Acme x [Company] — hello from leadership"`
  - Bad: `"Executive Partnership Alignment Communication Q2"`

---

## Step 8 — Decide Which Buttons Show

For each call's Account Actions panel:

- **"Update Success Plan ↗"** — always show. Sends a chat-response prompt to the user
  for review (does NOT execute silently).
- **"Generate Risk Update ↗"** — show ONLY if the risk record matches the conditions
  defined in `{{CONFIG.RISK_TRIGGER_FIELDS}}`. Otherwise omit and show muted italic text:
  *"No active risk signal."*

---

## Step 9 — Compute Week Summary Stats

Before rendering the widget, compute:
- `totalCalls`
- `atRiskCount` — calls where the client has a triggering risk record
- `overdueObjCount` — sum of overdue objectives across all clients in the week
- `weekPatterns[]` — 2-3 sentence-level observations ("3 of 5 calls are with renewal-window accounts", etc.)
- `staircaseWarning` — true if conversation intel failed for any client

---

## Step 10 — Render via show_widget

**HARD RULES:**
- NEVER use `create_file`, `present_files`, or bash. Render via `show_widget` only.
- ALWAYS call `read_me(["interactive"])` first.
- Self-contained HTML in a single `show_widget` call.
- Use hex colors from `{{CONFIG.PRIMARY_COLOR}}`, etc. (defaults: blue `#378ADD`,
  orange `#FDAB3D`, red `#E24B4A`, purple `#8B5CF6`).

### Card Expand — Critical CSS

NEVER use `display:none/block`. Always use max-height transitions:

```css
.card-body { max-height: 0; overflow: hidden; transition: max-height 0.3s ease; }
.card-body.open { max-height: 6000px; }
```

```js
function toggle(i){
  document.getElementById('body'+i).classList.toggle('open');
  document.getElementById('chev'+i).classList.toggle('open');
}
```

### Widget Layout

**Header:** `Weekly Call Brief — [Mon DD MMM] → [Fri DD MMM YYYY]` + source pills (`✓` or `⚠`)

**Week Summary Banner:** N calls · N at-risk · N overdue objectives · `weekPatterns[]`
bullets · `⚠ Staircase` pill if `staircaseWarning`

**Collapsed card row:** `Day/Date · Time · Xm · Client · Contacts | Type · Sentiment dot ·
⚠ badge | ▼` — left border in `{{CONFIG.PRIMARY_COLOR}}`

**Expanded card — 5 sections:**

**① Three-column grid:**
- Col 1: Account brief — summary text + theme pills + momentum/risk lists. Overdue
  objective dates rendered in `{{CONFIG.DANGER_COLOR}}`.
- Col 2: Active objectives.
- Col 3: Talking points. First TP gets a `{{CONFIG.PRIMARY_COLOR}}` left border ONLY
  (no background fill).

**② Account Actions panel:**
- Border `{{CONFIG.WARNING_COLOR}}`, background `#FFF8EE`.
- Display: `[Value Driver]: [Outcome]` (or `Suggested topic: [Topic]`) + rationale.
- "Update Success Plan ↗" button (always shown).
- "Generate Risk Update ↗" button (conditional).
- **Button styling — HARD RULE:** Both button labels MUST use `color: {{CONFIG.WARNING_TEXT_COLOR}} !important`.
  Default: text `#633806`, bg `#FAEEDA`, border `#BA7517`, hover `#FAC775`.

**③ Agenda Email section:**
- Left border `{{CONFIG.PRIMARY_COLOR}}`. Render the agenda body. Single button:
  "Draft agenda in Gmail ↗" — fires silently.
- **HARD RULE:** Gmail draft body MUST wrap content in `<span style="color:#ffffff">...</span>`.

**④ Ghost Exec Email section:**
- Left border `{{CONFIG.ACCENT_COLOR}}`. Render 3 variants with dot-nav (JS-only swap, no
  separate buttons per variant).
- Single button: **"Draft exec note in Gmail ↗"** — never "Draft Variant 1 in Gmail" or
  similar. Sends the currently-selected variant to Gmail silently.
- **HARD RULE:** Gmail draft body MUST wrap content in `<span style="color:#ffffff">...</span>`.

**⑤ Footer:** "Send to CRM Timeline ↗" — HTML body only, fires silently.

### Silent Action Handling — CRITICAL

**⚠ NEVER use `fetch('https://api.anthropic.com/...')` from inside the widget JS** —
the iframe sandbox blocks it. ALL writes flow through `sendPrompt()` only.

**fireAction helper (use on every button):**

```js
function fireAction(btn, statusEl, prompt) {
  btn._o = btn._o || btn.textContent;
  btn.disabled = true;
  btn.textContent = 'Sending...';
  sendPrompt(prompt);
  statusEl.textContent = '✓ Sent';
  setTimeout(() => {
    btn.disabled = false;
    btn.textContent = btn._o;
    statusEl.textContent = '';
  }, 4500);
}
```

```html
<button onclick="fireAction(this, document.getElementById('s-ID'), PROMPT)">Label ↗</button>
<span id="s-ID" style="font-size:11px;color:#854F0B"></span>
```

**Silent buttons** (append `"Handle this silently — do NOT respond unless error."` to the prompt):
- Draft agenda in Gmail
- Draft exec note in Gmail
- Send to CRM Timeline

**Chat-response buttons** (omit the silent line — user wants to review the draft):
- Update Success Plan
- Generate Risk Update

**Gmail draft prompt format:**

```
Create a Gmail draft:
To: ${to}
Subject: ${subj}
Body:
<span style="color:#ffffff">${body}</span>

Handle this silently — do NOT respond unless error.
```

**CRM Timeline post format:**
- HTML body only (`<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`, `<hr>`).
- Whatever required custom field your CRM needs to mark this as an internal update —
  reference your CRM's docs (in Gainsight: `custom_field_values: {"Status": "N/A - Internal Update"}`).

---

## Step 11 — Fallbacks

| Failure | Behavior |
|---|---|
| Calendar unavailable | Error banner at top of widget; do not render cards |
| Conversation intel KI / error | `⚠` source pill + fallback summary text per affected card |
| CRM error | Warning text in objectives column for affected card |
| No outcome / value driver match | Show "No outcome match — review manually" in Actions panel |
| Empty week (zero calls survive filtering) | Render header + banner only with "No external calls this week." |

**Never guess. Never fabricate.**

---

## Step 12 — Closing Message

After the widget renders, output exactly one line:

```
Weekly Call Brief ready — [Mon DD] → [Fri DD MMM] · [N] calls · [source status]
```

Followed by a one-line-per-call list:

```
[Day, Time — Client · Type]
```

Then a final tip line:

```
Tip: Gmail and Timeline buttons fire silently (✓ in-card). Update Success Plan and Generate Risk Update open a draft in chat for review.
```

That's the entire output after the widget. No other narration.

---

## Universal Style Rules

- **No em-dashes** in any output (emails, widget text, closing message). Use hyphens,
  colons, commas, or restructured sentences.
- Plain ASCII apostrophes (`'`) — no curly quotes.
- HTML in CRM timeline writes only — no markdown, no plain-text separators.
