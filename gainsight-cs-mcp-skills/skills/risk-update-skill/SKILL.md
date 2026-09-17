---
name: risk-update-skill
description: >
  Generates and posts Risk Timeline Updates in a Customer Success Platform (CSP)
  for accounts where the operating CSM owns an active Risk task. Combines
  conversation intelligence (CCI) data (sentiment, churn signals, risk scores,
  suggested playbooks) with the most recent call transcripts to write a
  structured entry, including executive summary, key risk signals, call
  context, and Recommended Next Steps. Posts the update onto the Risk task's
  Timeline.

  **Always trigger for:** "risk update", "update my risk tasks", "post risk
  updates", "update at-risk accounts", "log risk notes", "write risk timeline
  entries", "sync risk analysis to CSP", "update risk tasks from calls",
  "generate risk updates", "post risk notes", or any request to log, write, or
  sync risk-related account updates into CSP timeline entries.
---

# Risk Update Skill

Identifies all active Risk tasks across the operating CSM's portfolio,
enriches each account with conversation intelligence Risk Analysis plus the
most recent call context, then posts a structured Risk Update Timeline entry
directly onto the Risk task in the Customer Success Platform.

> **Scope constraint:** This skill operates exclusively on accounts where the
> CSM is the operating user. Every data pull and every write must be verified
> against the operating user's book of business. Do not touch accounts owned
> by other CSMs.

---

## Integration Points

This skill assumes two data integrations:

| Integration | Role |
|---|---|
| Customer Conversation Intelligence (CCI) | Source of call transcripts, sentiment, risk signals, suggested playbooks |
| Customer Success Platform (CSP) | Source of account ownership, Risk tasks, timeline entries; destination for the posted Risk Update |

Substitute the CCI tool, the CSP tool, and their specific MCP/API methods as
applicable to the active environment. The workflow below is platform-agnostic
but assumes both integrations are connected and authenticated.

---

## Step 0 — Resolve the Operating User's ID

Before any other step, resolve the operating CSM's user ID in the CSP. Store
as `OPERATING_USER_ID`. This is required for all CSP queries and writes.

If the operating user is not specified by the caller, ask before proceeding.
Do not default to "self" or any hardcoded user.

---

## Step 1 — Pull All Active Risk Tasks for the Operating User's Portfolio

Query the CSP's task / call-to-action object with:

```
Filters:
  - Owner = OPERATING_USER_ID
  - Type = "Risk"  (or equivalent risk classification)
  - IsClosed = false  (or equivalent open status)
```

Retrieve per task:
- Task ID (required for Timeline write)
- Task name / title
- Company ID
- Company name
- Relationship ID (if relationship-level)
- Risk reason / category
- Priority
- Due date
- Owner name (confirm = operating user)

**Ownership check:** If the owner is not the operating user, skip that task
entirely. Add to the "Skipped" list in the final report.

Store all verified tasks as a list: `riskTasks[]`

---

## Step 2 — Pull CCI Risk Analysis + Recent Transcripts for Each Account

For each company in `riskTasks[]`, run **all three queries** against the
conversation intelligence source. These are required, do not skip any:

```
Query 1: "Risk analysis, churn signals, and suggested playbooks for [Company Name]"
Query 2: "Most recent call transcript or call summary for [Company Name]"
Query 3: "Account health and risk summary for [Company Name]"
```

**Always fetch full evidence** for every result ID returned across all three
queries. The summary snippets alone are insufficient. Full evidence content is
required to produce an accurate Executive Summary. Do not draft the Risk
Update until evidence has been fetched and reviewed.

For each account, extract and store:
- **Risk Score / Sentiment** — overall risk level (High / Medium / Low) and
  sentiment trend (Declining / Flat / Improving)
- **Key Risk Signals** — top 3 to 5 specific signals (e.g., low engagement,
  competitor mentions, low NPS, usage drop, stakeholder departure, support
  escalations)
- **Risk Summary** — 2 to 3 sentence narrative of why this account is at
  risk, grounded in the fetched evidence (transcripts, call summaries,
  CCI signals, not generic filler)
- **Most Recent Transcript / Call Summary** — verbatim key quotes or close
  paraphrase of what was discussed; this directly populates the Executive
  Summary and Call Context sections
- **Suggested Playbooks** — any playbook names or recommended actions the CCI
  surfaces. These feed the "Recommended Next Steps" section.

Store as: `cciData[companyName]`

---

## Step 3 — Pull Recent Timeline Entries from the CSP (Calls + Notes)

For each account, fetch the **two most recent** timeline entries of any
strategic, operational, or update type. This ensures the Executive Summary
reflects both the latest call and any interim notes posted since.

```
Filters:
  - CompanyId = [company ID]
  - CreatedByUser = OPERATING_USER_ID
  - TypeName IN ("Strategic Call", "Operational Call", "QBR", "EBR",
                 "Monthly Strategic", "Check-in", "Call", "Update", "Note")
Sort: ActivityDate DESC
Limit: 2
```

Retrieve for each entry:
- Subject
- Activity date
- Type
- Notes (plain text or rendered text body)

**Use both entries** when composing the Executive Summary and Call Context
section. If the most recent entry is an "Update" or "Note" (not a call), it
may contain important interim context, include it. The call entry provides
call context; the note entry may provide updated risk framing.

If no CSP timeline entry exists, note "No recent call on record" and rely on
CCI call summaries instead (query: `"Most recent call summary for [Company Name]"`).

Store as: `recentTimeline[companyName]` (array of up to 2 entries)

---

## Step 4 — Cross-Reference CCI Transcripts Against CSP Timeline Notes

For each account, compare the CCI call transcript / summary (from Step 2)
against the CSP Timeline entries (from Step 3):

- If the CCI source has a **more recent** call than the CSP Timeline, prefer
  the CCI source as primary for Call Context
- If the CSP has a more recent entry, use it as primary and the CCI source as
  supplement
- **Always use both sources** together when drafting the Executive Summary.
  The combination produces the most accurate and complete picture of account
  health
- Never fabricate or merge incompatible details. If the two sources conflict,
  note the discrepancy explicitly in the Risk Update entry

The Executive Summary (RISK SUMMARY section) **must reflect both sources**,
not just the CCI risk score. Ground every sentence in concrete data from
transcripts or Timeline notes.

---

## Step 5 — Draft the Risk Update Timeline Entry (HTML)

For each account with a verified Risk task, compose a structured risk update
note **as HTML**. CSP Timelines typically render HTML, and Risk Update entries
must always be posted as HTML, not plain text with ASCII separators.

> ⚠️ **HTML formatting hard rule:** Risk Update Timeline entries MUST be
> posted as HTML. Use `<h2>` for the title, `<p>` for the metadata line,
> `<h3>` for section headers (RISK SUMMARY, KEY RISK SIGNALS, RECENT CALL
> CONTEXT, RECOMMENDED NEXT STEPS), `<ul>`/`<li>` for signal and next-step
> lists, `<p>` for narrative paragraphs, and `<strong>` for inline labels.
> **No ASCII line separators** (no `─────`, no `===`, no dashes-as-dividers).
> No plain-text formatting.

Use this exact HTML template:

```html
<h2>🔴 Risk Update — [Company Name]</h2>
<p><strong>Task:</strong> [Task Name] &nbsp;|&nbsp; <strong>Risk Reason:</strong> [Reason] &nbsp;|&nbsp; <strong>Priority:</strong> [Priority] &nbsp;|&nbsp; <strong>Updated:</strong> [Today's Date]</p>

<h3>Risk Summary</h3>
<p>[2 to 3 sentence executive summary of the account's current risk status. Lead with the most acute signal. Reference CCI risk score / sentiment. Be direct, this is an internal note for the CSM and leadership, not customer-facing.]</p>

<h3>Key Risk Signals</h3>
<ul>
  <li>[Signal 1, specific and factual, sourced from CCI risk analysis]</li>
  <li>[Signal 2]</li>
  <li>[Signal 3]</li>
  <li>[Signal 4, if applicable]</li>
  <li>[Signal 5, if applicable]</li>
</ul>

<h3>Recent Call Context</h3>
<p><strong>Call Type:</strong> [Strategic Call / Operational Call / QBR / etc.] &nbsp;|&nbsp; <strong>Date:</strong> [Call Date] &nbsp;|&nbsp; <strong>Source:</strong> [CSP Timeline / CCI Summary]</p>
<p>[3 to 5 sentence summary of what was discussed on the most recent call. Note any topics that directly relate to the risk signals above. If the client raised concerns, quote or closely paraphrase them. If sentiment on the call was misaligned with the risk signals, note the discrepancy.]</p>

<h3>Recommended Next Steps</h3>
<ol>
  <li>[Action item, e.g., "Schedule executive sponsor check-in within 7 days to address [specific concern raised on call]"]</li>
  <li>[Action item, e.g., "Initiate [Playbook Name] playbook: [brief description of playbook steps]"]</li>
  <li>[Action item]</li>
  <li>[Action item, if applicable]</li>
  <li>[Action item, if applicable]</li>
</ol>

<p><strong>Playbooks Referenced:</strong> [List playbook names from CCI source, comma-separated, or "None suggested" if none returned]</p>
```

**Drafting rules:**
- Output must be valid HTML, never plain text, never ASCII separators
- Risk Signals must be factual and sourced, never generic filler
- Call Context must reflect actual call notes / transcript, never invented
- Recommended Next Steps must reflect CCI-suggested playbooks where available;
  supplement with logical CS judgment if playbooks are sparse
- Total note length: 200 to 400 words of body content. Concise but complete.
- No customer-facing language, this is an internal CSM record
- If the CCI source returned no playbooks, add a `<p>` note above the `<ol>`
  reading "No playbooks returned by the CCI source, next steps based on risk
  signals and call context"
- No em dashes anywhere in the output, use commas, colons, hyphens, or
  restructured sentences

---

## Step 6 — Post Timeline Entry to the CSP Risk Task

For each completed draft, create a Timeline entry linked to the Risk task.
**The body must be posted as HTML**, pass the HTML content into the
HTML-body field (commonly `Notes`), not the plain-text body field.

```
Required fields:
  - CompanyId: [company ID]
  - RelationshipId: [relationship ID, if relationship-level task]
  - Subject: "Risk Update — [Company Name] — [Today's Date]"
  - TypeName: "Update"           ← ALWAYS "Update", no exceptions, no fallback
  - SubType: "Risk"              ← ALWAYS "Risk", hard required
  - Status: "Red"                ← ALWAYS "Red", hard required
  - Notes: [full HTML body from Step 5]   ← HTML, not plain text
  - custom_field_values: {
        "Status": "N/A - Internal Update",   ← required to avoid missing-field error
        "Update Type": "Risk"                ← ALWAYS "Risk", picklist value, hard required
    }
  - CreatedByUser: OPERATING_USER_ID
  - ActivityDate: [today's date]
  - TaskId: [Risk task ID]   ← links the timeline entry to the Risk task
```

> ⚠️ **Hard rules, no exceptions:**
> - **Body format:** Notes body must be **HTML** (passed in the HTML-body
>   field, not the plain-text body field). No ASCII separators, no
>   plain-text formatting.
> - `TypeName` must be **"Update"**. Never use "Call", "Note", or any other type.
> - `SubType` must be **"Risk"**. Always pass this field explicitly.
> - `Status` must be **"Red"**. Always pass this field explicitly.
> - `custom_field_values` must always include both:
>   - `"Status": "N/A - Internal Update"` (prevents CSP missing-required-fields errors)
>   - `"Update Type": "Risk"` (picklist value, required on every Risk Update write)
>
> If the CSP's activity-types config does not list "Update" as a valid type, or
> if "Risk" is not a valid picklist option for the "Update Type" field, report
> an error in the Needs Review section and output the drafted HTML in chat for
> manual entry. Do **not** substitute a different TypeName or Update Type value.

**Validating the "Update Type" picklist:** Before the first write of a run,
look up picklist values for the "Update Type" field on the Activity object to
confirm "Risk" is a valid option. If it is not, halt the run and surface the
available options in the Needs Review section.

**Do not modify** the Risk task's status, owner, reason, or priority. Only add
the Timeline entry, no other fields change.

---

## Step 7 — Summary Report

After all accounts are processed, present this summary in chat:

```
## Risk Task Update Run
Run Date: [Today's Date]
Operating User: [User Name]

✅ Successfully Updated: [N] accounts
─────────────────────────────────────
[Company Name]
  Task: [Task Name]
  Risk Level: [High/Medium/Low from CCI]
  Key Signal: [Top signal, one line]
  Playbooks Applied: [playbook name(s) or "None"]
  Timeline Entry: Posted ✓

[Repeat for each updated account]

─────────────────────────────────────
⚠️ Needs Review: [N] accounts
  • [Company Name]: [reason, e.g., "No CCI data found", "No recent call on
    record", "Could not resolve task ID"]

─────────────────────────────────────
⏭️ Skipped: [N] accounts
  • [Company Name]: Owner ≠ operating user, not in scope

─────────────────────────────────────
Total Risk Tasks Reviewed: [N]
```

---

## Fallback Handling

| Scenario | Action |
|---|---|
| No Risk tasks found for operating user | Report "No active Risk tasks found" and stop |
| CCI returns no data for account | Use CSP task reason + call context only; note "CCI data unavailable" in the Risk Summary section |
| No recent call in CSP or CCI | Write "No recent call on record" in Call Context section; proceed with risk signals |
| CSP timeline-write call fails | Log failure in Needs Review section; output the drafted note in chat so the user can paste manually |
| Activity Type "Update" not found in config | Report error in Needs Review, do NOT substitute another TypeName. Output HTML draft in chat for manual entry. |
| "Update Type" picklist does not include "Risk" | Halt the run, surface the available picklist options in Needs Review, and output HTML drafts in chat for manual entry. Do NOT substitute another Update Type value. |

---

## Non-Negotiable Rules

1. **Operating-user scope is absolute.** Only process tasks owned by the
   resolved operating user. Verify ownership on every task. No exceptions.
2. **Risk tasks only.** Only process tasks where the type is "Risk" and the
   task is open. Never touch closed tasks or non-risk task types.
3. **No task mutations.** Never change task status, priority, owner, or reason.
   Only add a Timeline entry.
4. **Signals must be real.** Risk signals and call context must come from CCI
   or CSP data. Never fabricate, infer generically, or pad with filler text.
5. **Playbooks from CCI only.** Recommended Next Steps must reference
   CCI-suggested playbooks where returned. Supplement with judgment, never
   invent playbook names.
6. **Post to the task, not just the company.** The Timeline entry must use
   the task ID to link to the specific Risk task, not just the company or
   relationship record.
7. **Flag, don't guess.** If account ownership, task identity, or data quality
   is uncertain, add to "Needs Review" and report it. Never assume.
8. **Activity Type = "Update", SubType = "Risk", Status = "Red", always.**
   These three fields are hard-required on every timeline-write call. Never
   use a substitute type, omit SubType, or change Status. `custom_field_values`
   must include both `"Status": "N/A - Internal Update"` AND
   `"Update Type": "Risk"` on every write.
9. **HTML body, always.** Risk Update entries must be posted as HTML in the
   HTML-body field. No plain text, no ASCII separators (no `─────`, no `===`).
   Use `<h2>`, `<h3>`, `<p>`, `<ul>`/`<li>`, `<ol>`/`<li>`, and `<strong>` only.
10. **Executive Summary must be grounded in transcripts and Timeline notes.**
    Always fetch full evidence from the CCI source and pull the two most recent
    CSP Timeline entries before drafting. The Risk Summary section must reflect
    actual call and transcript content, not generic risk score language.
