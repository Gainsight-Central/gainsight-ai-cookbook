# Weekly Call Briefs — User Configuration

Edit the values below to personalize this skill. SKILL.md reads from this file as `{{CONFIG.X}}`.
Save your changes and the skill will use them on the next run.

---

## Identity

- **CSM_NAME**: `Your Full Name`
  Your full display name as it appears in your CRM (e.g. "Jane Smith").

- **CSM_USER_ID**: `PASTE_YOUR_CRM_USER_ID_HERE`
  Your unique user GUID/GSID in your CRM. In Gainsight you can find this by running
  `search_user(name="Your Name")` once and pasting the GSID returned. Other CRMs use
  similar lookup patterns.

- **TIMEZONE**: `America/New_York`
  IANA timezone identifier (e.g. `America/Phoenix`, `Europe/London`, `Asia/Tokyo`).
  Used for week boundary calculations.

- **EMAIL_SIGNATURE**: `Your Name | Your Title | Your Company`
  Used at the bottom of agenda email drafts.

---

## Calendar Filtering

- **INTERNAL_EMAIL_DOMAIN**: `@yourcompany.com`
  Calendar events are kept ONLY if at least one attendee email does NOT match this domain
  (i.e. the event has at least one external/client attendee).

- **CALENDAR_EXCLUDE_KEYWORDS**: `do not book, dnb, busy, head down, focus time, working location, internal sync, 1:1`
  Comma-separated list of substrings (case-insensitive) that exclude a calendar event from
  the brief if found in the event title. Customize freely — add personal events, recurring
  internal meetings, etc.

---

## CRM Connection

This skill is CRM-agnostic. It expects you to have an MCP connector configured for your
customer data platform (Gainsight, HubSpot, Salesforce, custom, etc.).

- **CRM_MCP_NAME**: `your-crm-mcp`
  The display name of your CRM MCP server as it appears in your connected MCPs.

- **CONVERSATION_INTEL_MCP_NAME**: `your-conversation-mcp`
  The display name of your conversation intelligence MCP (Staircase AI, Gong, Chorus, etc.).
  Leave blank if you don't have one — the skill will fall back to CRM data only.

The skill calls these by their MCP tool names — no URLs needed in this config. Just make
sure both MCPs are connected in your Claude settings before running.

---

## CRM Field Mapping

Map your CRM's terminology to the skill's generic concepts. Defaults shown match Gainsight;
adjust if you use a different CRM.

- **ACCOUNT_OBJECT**: `company`
- **OBJECTIVE_OBJECT**: `success_plan` (the parent) + `cta` of type "Objective" (the children)
- **RISK_OBJECT**: `cta` of type "Risk"
- **TIMELINE_OBJECT**: `activity_timeline`
- **OWNER_FIELD**: `OwnerId` (or `account_owner`, `csm_id`, etc. depending on CRM)
- **EXTERNAL_ID_FIELD**: `Gsid` (or `Id`, `_id`, depending on CRM)

If your CRM uses different terminology, the skill's tool calls will need to use whatever
search/query/fetch tools your MCP exposes. The logic in SKILL.md is generic — it asks you
to "fetch the active objectives for this account" rather than hardcoding a specific tool
name.

---

## Optional: Risk Trigger Rules

The "Generate Risk Update" button only appears when an account has an active risk signal.
Define what constitutes a risk for your setup:

- **RISK_TRIGGER_FIELDS**: `is_important=true OR risk_status=Red OR status=Red Account Call`
  Plain-English description of the field conditions that should trigger the risk button.
  The skill will look for these signals on whatever risk record type your CRM uses.

---

## Branding (Optional)

Default colors are neutral. Override if you want brand-aligned widgets.

- **PRIMARY_COLOR**: `#378ADD` (blue — main accent)
- **WARNING_COLOR**: `#FDAB3D` (orange — actions panel)
- **DANGER_COLOR**: `#E24B4A` (red — overdue/risk)
- **ACCENT_COLOR**: `#8B5CF6` (purple — exec email)
- **WARNING_TEXT_COLOR**: `#633806` (dark amber — button text on warning panel)
- **WARNING_BG_COLOR**: `#FAEEDA` (light amber — button bg on warning panel)
- **WARNING_BORDER_COLOR**: `#BA7517` (amber — button border on warning panel)

---

## Notes for Editors

- All `{{CONFIG.X}}` placeholders in SKILL.md resolve to the values above.
- If a value is missing or empty, the skill will skip that feature gracefully and warn you in the closing message.
- You can edit this file at any time — changes apply on the next run.
