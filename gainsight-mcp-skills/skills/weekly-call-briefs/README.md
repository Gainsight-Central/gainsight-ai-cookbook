# Weekly Call Briefs — Generic / Shareable

A shareable, CRM-agnostic version of the Weekly Call Briefs skill. Generates an
interactive Mon-Fri dashboard of your client calls with auto-drafted agendas, exec
emails, talking points, and one-click CRM update actions.

## What it does

For every external client call on your calendar this week, it produces:
- A 2-3 sentence account brief grounded in conversation intelligence + CRM data
- 3-4 prioritized talking points
- A pre-call agenda email draft (one-click to Gmail)
- 3 ghost exec email variants (one-click to Gmail)
- A "Update Success Plan" / "Generate Risk Update" action panel

Everything renders in a single interactive HTML widget. Gmail drafts and CRM timeline
posts fire silently with one click; success plan and risk updates open a draft in
chat for your review.

## Install

1. Drop this skill folder into your skills directory (or upload the `.skill` package
   to Claude.ai).
2. **Edit `config.md`** — fill in your name, CRM user ID, timezone, calendar filters,
   and MCP names. The skill will refuse to run until placeholders are replaced.
3. Make sure your CRM MCP and (optionally) conversation intelligence MCP are connected
   in your Claude settings.

## First run

Once `config.md` is filled in, just say one of:
- "weekly brief"
- "weekly call brief"
- "prep my week"
- "calls this week"
- "calls next week"
- "week of Apr 14"

## Customization

Most behavior is config-driven, but if you want to change deeper logic:
- Calendar filtering rules → Step 1 of `SKILL.md`
- Account brief synthesis rules → Step 3
- Talking point priority stack → Step 4
- Agenda email format → Step 6
- Ghost exec email structure → Step 7
- Widget layout / styling → Step 10

## Notes

- The skill is CRM-agnostic — it describes data needs in generic terms (account,
  objectives, risk records, timeline) rather than hardcoded tool names. The
  underlying Claude session uses whatever search/fetch tools your connected CRM
  MCP exposes.
- Conversation intelligence is optional. If you don't have a Staircase / Gong /
  Chorus MCP connected, leave `CONVERSATION_INTEL_MCP_NAME` blank and the skill
  falls back to CRM-only data.
- No em-dashes are used anywhere in output by design — replace with hyphens,
  commas, or restructured sentences.
