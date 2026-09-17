---
name: gainsight-viz
description: >
  Render ANY Gainsight account, company, relationship, or portfolio answer as an inline
  visual dashboard via the Visualizer (show_widget), styled with Horizon Design System
  colors. USE THIS SKILL WHENEVER the user asks about a Gainsight
  customer/account/company/relationship or its data — even without the word "visualize."
  Covers: summary / status / "how is X doing," account summary, health score, scorecard,
  open CTAs, success plan, timeline / activity / QBR /
  "last quarter of activity," trends over time, portfolio / book of business, renewals, owner ("who
  owns X"), attributes / company details, contacts, a contact's email or phone — and any
  request reading Gainsight data. Fire AUTOMATICALLY; the user should never have to say "use
  the skill." If the answer would contain Gainsight account data, this skill applies. ALWAYS
  render inline via show_widget — NEVER a plain text/bullet/markdown summary, NEVER a file
  artifact. When unsure, prefer this skill.
---

# HOW TO RENDER — read this first

## Mandatory tool flow (every Gainsight visualization)

1. **Fetch the data** from the Gainsight MCP tools (resolve the entity first, then scorecard / CTAs / timeline / etc.).
2. **Call `mcp__visualize__read_me` once** with `modules: ["mockup"]` before your first `show_widget` call in the session (loads the live rendering contract). For a **trend / time-series** request (pattern 8), load `modules: ["chart"]` instead so you get the line-chart guidance. Do not narrate this call.
3. **Call `mcp__visualize__show_widget`** with an HTML fragment. This renders **inline in the conversation.**
4. In your text reply, add the short narrative + next steps. Do NOT repeat the widget's content as text.

NEVER return a plain bullet-point list for Gainsight data. NEVER write an `.html`/`.jsx`/`.tsx` file artifact — those open in a side panel, not inline. The Visualizer is the only inline path.

### If `show_widget` fails — recover, do NOT bail to text after one error
A single `show_widget` error is **not** evidence the Visualizer is down. But do NOT loop: **at most 2 render attempts total, then fall back fast.** A retry storm (split into parts → rebuild lighter → retry again…) can burn 10+ minutes and still fail — never do that.
1. **Keep the payload lean so it renders the first time — no row cap.** Pick the format by item count: **≤10 items → rich cards; 11+ items → one compact table** (lean markup, one text row each — no per-item cards, no gauges). Render the FULL set either way, in a **single widget** — **NEVER split one answer across multiple widgets**. A lean 50-row table is a small payload and renders fine; 50 heavy cards (or splitting + rebuilding) is what caused the 10-minute loop.
2. **If a render still fails, did you call `read_me` this session?** If not, call `mcp__visualize__read_me` (`modules: ["mockup"]`) once, then retry.
3. **Retry AT MOST ONCE, smaller and simpler** — drop to ≤10 rows, strip gradients/`<script>`/SVG paths, keep plain divs + host CSS vars, and verify the fragment is well-formed (balanced tags, no stray quotes/backticks, no external URLs). Do NOT attempt a 3rd render, do NOT split into parts, do NOT "rebuild as a lighter artifact" repeatedly.
4. **Then fall back FAST.** If the one capped retry still fails, immediately give a brief text summary — say plainly "the inline visual failed to render; here's the summary" — and stop. Never silently degrade to a bullet list as the intended output, and never keep retrying.

Empty data is NOT a render failure: if a fetch returns nothing (no scorecard, no CTAs, no success plans), still render the layout's **honest empty state** (`—` tiles / "No open CTAs" box), not a text sentence.

### Three data states — never conflate them
Distinguish **no data** from **source not connected**. They look tempting to render the same way, but they mean opposite things, and showing one as the other misleads the user ("No open CTAs" reads as *this account has none*, when really *the CTA source isn't connected*).

1. **Live data** — the tool returned data → render the populated dashboard.
2. **No data** — the tool succeeded but returned an empty set (0 CTAs, no plan, `Unscored`) → render the layout's **empty state** (`—`, "No open CTAs.", "Unscored"). Same layout, empty values.
3. **Source not connected / not configured** — the needed tool isn't available, or errors with a not-configured / permission / connector-missing signal → render a **distinct "not configured" panel**, NOT an empty state and NOT invented numbers. Name the connector required.

**Not-configured panel** (use this exact structure, host vars only):
```html
<div style="background:var(--surface-1);border:1px solid var(--border-strong);border-radius:12px;padding:28px 24px;text-align:center">
  <div style="display:inline-block;font-size:12px;font-weight:600;color:var(--text-warning);background:var(--bg-warning);border-radius:999px;padding:4px 12px;margin-bottom:12px">Not configured</div>
  <div style="font-size:16px;font-weight:600;color:var(--text-primary);margin-bottom:6px">Connect [connector] to see [dashboard]</div>
  <div style="font-size:14px;color:var(--text-secondary);max-width:540px;margin:0 auto;line-height:22px">This dashboard is powered by the <b>[connector]</b> connector, which isn't configured for this tenant — so there's no data to show yet. This is different from an account that simply has no data.</div>
</div>
```
Decision rule: only render an empty state when a tool **actually ran and returned empty**. If the required tool/connector is missing or a fetch fails with a configuration/permission error, render the not-configured panel instead — never a zeroed-out dashboard.

### Consistency & determinism rules (QA 2026-09-04)
- **ONE layout per request.** Pick the single best layout and render it once. Never stack a card view AND a table AND a gauge for the same answer. "Are there any open CTAs for X?" → the CTA pipeline, not card + table + gauge together.
- **Render ALL rows — no cap — but match format to size.** Show the full set (all 51). Format by item count: **≤10 items → rich cards; 11+ → one compact table** (lean rows, not per-item cards), one widget, sorted by the key — the table keeps the payload small enough to render reliably. Never split across multiple widgets. Only if a render genuinely fails after the one retry (see the failure section) do you fall back — and then give the **full list as text**, never a silently-dropped subset. If a header shows a total (e.g. "51 open"), the rows below it must be the full set, not a quiet partial.
- **Header pills clear of the top-right corner.** The host renders a `⋯` overflow menu in the top-right of every widget — keep header pills (ARR, renewal, overdue, %) out from under it: put them below the title, or leave right padding, so they never truncate ("Total ARR USD 11.3…"). Prefer a short pill label.
- **Stat/KPI grid never orphans a tile.** Set `grid-template-columns` to the *number* of tiles (up to 4, or 5 for wide) so 4 tiles are 4-up, not 3+1 with one tile alone on a second row.
- **Do NOT color a plain COUNT number.** KPI/stat values that are just counts ("High priority 15", "Overdue 12", "Total open 51") use `var(--text-primary)` — never a severity color. The AA-dark light-mode danger/warning hues (`#9A1C0B` dark-red, `#DA7309` olive-brown) look muddy as large numbers and imply a status the count doesn't have. Only color a value that is *inherently* a status: a health **score** (by its `score_color`), or a **trend delta** (`↑/↓`). Convey "high priority" via the label, not by painting the number.
- **Wide tables must not overlap.** Use `table-layout:fixed` + a `<colgroup>` and `nowrap`/ellipsis per cell so e.g. a "Due date" cell can't bleed into "Owner". If columns won't fit, drop a column rather than overlap.
- **Simple lookups still render a visual.** "Who is the account owner of X?", "list attributes for X", "what's the renewal date for X", **"get the email / phone of a contact"** → render a compact **card** (header + a small key/value `detail` block, or a contact card), NOT plain text/markdown. A one-line answer is still a card.
- **Task-style prompts that read Gainsight data still render.** A QBR outline, "what's on my plate this week," "prep for the Atlassian renewal," "last quarter of activity" — even when phrased as a task, not a question — pull Gainsight data, so they render as a dashboard (timeline/QBR cards, book-of-business, etc.), NOT a text write-up. The user should never have to add "use the skill" — fire on the data, not the phrasing.
- **Aggregate / one-number answers render as a stat card, not a sentence.** "What's my total book ARR," "how many accounts are at risk," "average health across my portfolio" → a **stat row** (1–3 KPI tiles), not a text reply. One number is still a card.
- **Analytical questions render the data + reason in text.** "Why is Acme at risk," "should I escalate Globex," "summarize the risks in my book" → render the supporting visual (risk cards / health / timeline — whatever the answer rests on) via `show_widget`, and put the judgement/recommendation in your text reply. Don't answer text-only when Gainsight data backs the point; don't bury the data in prose.
- **Genuinely prose deliverables stay text.** A drafted email, a written exec summary, open-ended advice with no underlying dataset → answer in text (optionally render the supporting data if the user also asked to see it). Don't force a dashboard around prose.

> Scope note: `show_widget` is a Claude-side tool (claude.ai and Claude Code). It renders inline **in Claude**. It is not part of the Gainsight MCP server, so other MCP clients (ChatGPT, Copilot, Gemini) do not have it and will not render this inline — there they get your text reply. Cross-client inline UI is a different mechanism (MCP Apps / UI resources served by the MCP server itself), not this skill.

## The Visualizer contract — obey it, it overrides Horizon where they conflict

The widget renders in a themed sandbox that provides CSS variables and Tabler icons. Follow these rules; they take priority over the Horizon design-system font-weight and casing conventions **inside the widget** (Horizon *colors*, all listed below, still apply for brand accents).

- Output an HTML **fragment only** — no `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`. Start with content.
- Outer container is transparent — **never** put a dark or colored background on the outermost element. The host provides the page background.
- First element is a visually-hidden summary: `<h2 class="sr-only">one-sentence summary…</h2>`.
- **Font weights: 400 and 500 only.** Never 600 or 700 (they look heavy against the host UI). This overrides Horizon's 600 headings.
- **Sentence case everywhere.** Never Title Case, never ALL CAPS — including table headers and section titles. This overrides Horizon's uppercase H7 table headers.
- Body text 16px / line-height 1.7; card corners `12px`; control corners `var(--radius)`.
- On a colored background (badge/pill), text uses the **darkest shade of that same color family** — never black or gray.
- On single-sided borders (`border-left` accents), set `border-radius: 0` on that element.
- Never `position: fixed` — it collapses the auto-sized iframe height.
- No emoji. Icons = Tabler outline webfont (already loaded): `<i class="ti ti-building"></i>`. Outline only, never `-filled`. See the icon map below.

## Canonical layouts — render EXACTLY the same every time

The output MUST be deterministic: the same request type produces the same structure every
time. Do NOT improvise, add, remove, reorder, split, or regroup sections. Pick the layout
for the matched pattern below and render its sections top-to-bottom, exactly.

**Rules that apply to every response:**
- One dashboard per response (never partial text + partial visual).
- Header always = `[icon] Title` + a subtitle meta line; optional right-side status (health gauge OR one pill).
- KPI tile = muted label (top) · big value · muted sub. A defined tile is NEVER omitted; missing value shows `—`; never invent a number.
- Trend indicator: the **arrow** shows direction (↑/↓); the **color** shows good/bad, NOT direction. Rising is green for good-when-up metrics (ARR, adoption, health, posts) but **red** for bad-when-up metrics (open CTAs, response time, churn). A drop in a good metric is red; a drop in a bad metric is green.
- A "table" section = ONE table sorted by the fixed key — never split one list into several tables, UNLESS the pattern explicitly says grouped (only Portfolio does).
- Missing data → the section's defined empty state, or collapse the section per its rule — never an ad-hoc alternative.

**The 9 layouts (render sections in this order):**
1. **Account summary** — ALWAYS these sections in this order, for EVERY account (never swap or substitute):
   - header `[building] name · segment` + right health gauge — label = the tenant's `overall_label` (e.g. "Yellow"), number colored by `score_color`; `—` + "Unscored" if no score. Never label it "Healthy" from a hardcoded cutoff.
   - alert banner — the "Scorecard not scored" notice when unscored (this is the ONLY conditional section)
   - KPI row (4, fixed): ARR · Renewal · Open CTAs · Stage — always present, `—` for any missing value
   - **Open CTAs** section — always present: CTA cards, or an empty state box ("No open CTAs.") when 0
   - **Recent timeline** section — always present: timeline rows, or an empty state box ("No timeline activity…") when none
   - Do NOT render scorecard measures here, and NEVER replace the KPI row with measures or the timeline with a CTA list. Scorecard-measure detail is a separate request, not part of the account summary.
2. **Portfolio health** — header `Portfolio health · N accounts`; summary KPI row (4): Total ARR · Healthy · Needs attention · At risk (each count + ARR); ARR-by-health stacked bar; a sort toggle (`Grouped by band` default · `Sorted by ARR`); then **one table/card per band, grouped by the tenant's OWN bands** (columns Account · Health · ARR · Renewal · CSM; rows sorted by ARR desc). Toggle → one flat table sorted by ARR. Never other groupings.
   - **Group by the system's bands — do NOT impose our own buckets.** Group the tables by the distinct `overall_label` values actually present (e.g. Red / Orange / Yellow / Lime / Green, or whatever the tenant configured), **ordered worst→best by `score_range_from`**. Empty bands don't render. The group header color and the account chip color are BOTH the band's `score_color` — so header color always equals chip color. Never map bands into a red/amber/green 3-bucket for the *tables* (that made an orange account sit under a red "At risk" header).
   - **The 3-bucket rollup (At risk / Needs attention / Healthy) is ONLY for the summary KPI row + the ARR-by-health bar** — a legitimate aggregate. It never colors the group headers or the chips.
   - **Each band header:** a colored square (11px, radius 3px) filled with the band's `score_color` + bold band label (16px `var(--text-primary)`) + muted `· N accounts · $X ARR`.
   - **Health cell:** the score rendered as a **status chip** colored by the band's `score_color` — a light tint of `score_color` as the pill background + a solid `score_color` dot + the score in dark text. The color is the tenant's, never invented from score cutoffs; Orange is its own color, never red.
   - **Column alignment (fixed):** all band tables use identical fixed column widths (`table-layout:fixed` + a shared `<colgroup>` — e.g. 26% / 13% / 14% / 15% / 32%) so every column, Health included, lines up across the groups. Each table is a card (`var(--surface-1)` + a `1px solid var(--border-strong)` outline, no shadow). Cells are single-line (`white-space:nowrap; text-overflow:ellipsis`).
3. **Success plan** — header `plan — account · dates` + right `%` pill; progress bar; objectives checklist (done / active / pending).
4. **CTA pipeline** — header `Open CTA pipeline · N` + right `overdue` pill; CTA cards (no colored left border; priority pill + due).
5. **KPI dashboard** — header `title · N accounts`; KPI row (4) with trends; health-split bar + legend.
6. **Timeline activity** — for any request about an account's activity/history/QBR/"last quarter" (standalone, not the account-summary section). Header `Recent activity — account · N activities` (the **account name is a click-through** → `sendPrompt('Show the account summary for <account>')`). Then a stack of **timeline cards** (NOT plain text) — one card per activity, newest first, each a **clickable card** that expands detail via `sendPrompt` (see the Timeline card template). For a QBR-style ask, use the two-column card layout (Wins & milestones / Challenges & response, + Upcoming priorities / Expansion) over the same timeline cards. NEVER return timeline/QBR data as a text/bullet answer — it renders as cards.
7. **Scorecard measures** — for "show the scorecard measures / breakdown / why is X unscored". Header `Scorecard — account` + the overall band gauge (same gauge as account summary, label/color from `overall_label`/`score_color`). Then **one measure card per measure** (see the Scorecard-measure card template): measure name (bold) + weight `%` (muted) on the left; a **status chip colored by that measure's own `score_color`** on the right, or `— · Unscored` when not scored; submeasures on a muted sub-line. Tag unweighted rows "informational". Never a bullet list.
8. **Trend / time-series** — for "health / ARR / adoption **over time**", "trend", "last N months/quarters". This is the ONE pattern that uses a **line chart**: call `mcp__visualize__read_me` with `modules: ["chart"]` (NOT "mockup") first to load chart guidance, then render a single inline **line chart** (Chart.js from the CDN allowlist). Header `<metric> trend — account/portfolio · <period>`; x-axis = time, y-axis = metric; one line per series (multiple lines only for an explicit compare); Horizon/CDS colors; one widget. If there's only a single data point (no history), fall back to the KPI tile with its ↑/↓ delta — do not draw a one-point chart.
9. **Comparison / ranking** — for "compare Acme vs Globex," "top 10 accounts by ARR," "which accounts renew this quarter." Two shapes: (a) **Compare** a few named entities → side-by-side **cards** (one per entity, the SAME fields in the SAME order so differences line up), or a compact table with entities as columns; (b) **Rank / filter** a list → a sorted **table** (or ranked horizontal **bars** when it's one metric), sorted by the metric, following the big-list rules (≤10 → cards/bars, 11+ → compact table). Health/score cells use the band chip colored by `score_color`. Never a prose comparison.

For the portfolio sort toggle, render both buttons and re-issue the query via `sendPrompt`
(e.g. `sendPrompt('Show my portfolio health sorted by ARR')`).

## Fallback — data outside the 9 patterns (the long tail)

Not every request maps to a dashboard above (contacts, custom reports, comparisons, ad-hoc
queries). Do NOT force a mismatched dashboard and NEVER fabricate. Instead pick the best-fit
**primitive** and build it from the shared components (same colors, fonts, chips):

1. **Stat row** — 2–4 big numbers (KPI tiles), for counts/summaries.
2. **Table** — columns + rows; first column bold; `table-layout:fixed` + `nowrap`; wrap the table in a card. **Header row must be visually distinct:** `<th>` = 600 weight, `var(--text-secondary)`, a `var(--surface-2)` background, and a `2px solid var(--border)` bottom border — never grey headers that read like data. Give each column enough width that cells don't collide (e.g. Due date must not overlap Owner); truncate with ellipsis rather than overflow. **Status cells are ALWAYS pilled consistently** — if one value in a column is a pill (e.g. "Churned"), every value in that column is a pill (e.g. "Active" too), same shape; never mix a pill with plain text in one column.
3. **Card list** — title + subtitle + optional status chip on the right, one per item.
4. **Bars** — label + value + bar; color by health band (green/amber/red) or a single accent blue.
5. **Detail** — a two-column key/value grid (muted label · value), for attribute lists.

Rule: dashboard if it fits → else the closest primitive → else clean text. Same header pattern
(`[icon] Title` + subtitle) and Horizon styling as the 9, so the long tail still looks consistent.

## CSS variables the host provides (auto light/dark) — use the exact names

These are the ONLY theme variables that exist. Do not invent others.

```
Surfaces:  var(--surface-2)  inset / white       var(--surface-1)  card bg
           var(--surface-0)  page bg
Tints:     var(--bg-accent)  var(--bg-success)  var(--bg-warning)  var(--bg-danger)
Text:      var(--text-primary)   var(--text-secondary)   var(--text-muted)
           var(--text-accent)  var(--text-success)  var(--text-warning)  var(--text-danger)
Borders:   var(--border)  var(--border-strong)   role: var(--border-accent) etc.
Layout:    var(--radius)   var(--pad-sm|md|lg|xl)   var(--gap-xs|sm|md|lg|xl)
```

There is **no** `--bg-pro`, `--text-pro`, `--sec`, `--text`, or `--muted` — earlier versions used those and they render as invisible/broken. For neutral and the four semantic roles (accent/success/warning/danger), always use the variables above.

## Where hardcoded Horizon hex is allowed

Use host variables for all neutral + accent/success/warning/danger. Use hardcoded Horizon hex ONLY for brand-specific colorful marks the theme can't express:

- Health gauge / score — use the TENANT'S OWN band from the `ask_scorecard` response, never hardcoded thresholds. Label = `overall_label`; color = `score_color` (or derive from `score_range_from`/`score_range_to`). Bands are tenant-configured, so a 72 may be **"Yellow"**, not "Healthy". Standard scheme (fallback ONLY if the response has no color): 0–30 Red `#DC3626` · 30–50 Orange `#E8833A` · 50–75 Yellow `#F4A702` · 75–90 Lime `#7DBB34` · 90–100 Green `#13AD68`. Show the number in that color and the `overall_label` verbatim — never invent "Healthy/At risk" text that contradicts Gainsight.
- CTA cards have **NO colored left border** — the accent was removed to avoid confusion (a type color next to a priority pill read as conflicting). CTA cards use only the standard card outline; the type is shown in the text sub-label. The distinct per-type palette below is used **only for the "by type" bar chart** (never leave half those bars grey): Risk `#F75D4F` · Opportunity/Expansion `#FD7CAB` · Objective `#6E32AE` · Lifecycle `#3084ED` · CSQL `#1A7381` · Activity `#43ADE5` · Exec sponsor `#A04406` · Product req/enh `#517723` · unknown `#5F6C7A`.
- Status chips (priority, overdue, severity, %, unanswered): dark label `#181F26` on tint — success `#D5F5DB` · warning `#FFECB8` · danger `#FDDFDC` · **orange `#FFE5D2`** (health Orange band), each with its leading filled icon (see Status chip pattern)
- **Priority pills NEVER use the green success chip.** Green (`✓`/`#D5F5DB`) means done/active only. Map priority: High / Priority 1 → danger (red) · Medium / Priority 2 / Yellow → warning (amber) · Low / Priority 3 → a **neutral** pill (grey `var(--surface-2)` bg, `var(--text-secondary)` text, no icon). A numbered priority like "Priority 3" in a green pill reads as "complete" — wrong.
- Expansion / "pro" purple (no host variable exists): `#6E32AE` text on `#F0E5FA` bg
- Alert banner: `rgba(255,187,0,0.12)` bg + `rgba(255,187,0,0.25)` border; title/icon `#FFBB00`, body `var(--text-secondary)`. (Works in both modes.)
- Distribution-bar segments: `#13C77F` / `#FFBB00` / `#F75D4F`
- **Semantic TEXT on the surface (contrast rule):** any green/amber/red text that sits directly on a dark card/page — percentages, legend labels, trend deltas (`↑/↓`), overdue counts — must use the host vars `var(--text-success)` / `var(--text-warning)` / `var(--text-danger)`, which the Visualizer tunes for AA contrast in both modes. Do NOT use the dark 90-stop hexes for on-surface text (`#9A1C0B` ≈2:1, `#0F8754` ≈3.4:1, and `#DC3626`/`#13AD68` are borderline on dark). Those dark hexes are for **dark text on a light chip/pill only** (see Status chips above). The gauge score number is the one exception — it's large-format, so `score_color` is acceptable there. Dim neutrals: date/sub-label text uses `var(--text-secondary)`, never `var(--text-muted)` on dark.
- **Card/box separation — REQUIRED, outline only (no shadow).** Every card/box container uses a visible **outline, not a shadow**. Use `border:1px solid var(--border-strong)` (NOT `var(--border)`, which is ~1.2:1 on white and disappears). `--border-strong` is more visible and adapts to both light and dark. Do **not** add a `box-shadow`. Apply the outline to every boxed element: KPI tiles, CTA cards, table containers, success-plan card, empty-state boxes, and the not-configured panel.
- **`var(--text-muted)` is for de-emphasized text only, never a section's primary label.** KPI-tile labels, table headers, and band sub-labels use `var(--text-secondary)` — `--text-muted` can fall below 4.5:1 on white.

## Icons — Tabler webfont, sized 16–24px, colored via `color`

```
account/company  ti-building         meeting     ti-calendar-event
CTA / target     ti-target           email       ti-mail
risk / warning   ti-alert-triangle   note        ti-file-text
success / check  ti-circle-check     call        ti-phone
clock / due      ti-clock            trend up    ti-trending-up
health / pulse   ti-activity         trend down  ti-trending-down
```

Example: `<i class="ti ti-building" style="font-size:22px;color:var(--text-accent)" aria-hidden="true"></i>`. Decorative icons get `aria-hidden="true"`; icon-only buttons get `aria-label`. Do not hand-draw icon SVG paths — the earlier inline-SVG icons used `stroke="var(--sec)"`, a variable that does not exist, so they rendered colorless.

## Reusable patterns (all use the corrected variables)

### KPI tile — ALWAYS a card (consistency rule)
Every KPI/stat number is a **carded tile with the outline** — the same on every render and in every layout (account summary, portfolio summary, KPI dashboard, book-of-business, generic stat row). **NEVER** render KPI numbers as borderless plain text; the same query must not come back carded one time and bare the next. If you show N stats, show N identical tiles in a `repeat(N,1fr)` grid (N≤4, or 5 wide).
```html
<div style="background:var(--surface-1);border:1px solid var(--border-strong);border-radius:12px;padding:14px">
  <div style="font-size:13px;color:var(--text-secondary);margin-bottom:6px">Open CTAs</div>
  <div style="font-size:26px;font-weight:500;color:var(--text-primary);line-height:1.2">0</div>
  <div style="font-size:13px;color:var(--text-secondary)">None in cockpit</div>
</div>
```

### Status chip — leading filled icon + light tint + dark label (use for ALL status pills)
Standard for priority, overdue, risk severity, success %, "unanswered", etc. Text is always `#181F26`.
Three variants — pick by meaning, not by which field it is:
- **success** (green): bg `#D5F5DB`, icon = green filled circle + white check
- **danger** (red): bg `#FDDFDC`, icon = red filled circle + white ✕
- **warning** (amber): bg `#FFECB8`, icon = amber triangle + white !

```html
<!-- success -->
<span style="display:inline-flex;align-items:center;gap:6px;padding:4px 12px 4px 7px;border-radius:10px;font-size:13px;font-weight:500;color:#181F26;background:#D5F5DB;line-height:1">
  <svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="#13AD68"/><path d="M4.6 8.3l2 2 4-4.6" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>Healthy</span>
<!-- danger: bg #FDDFDC, icon <circle r=8 fill=#DC3626/> + white ✕ path "M5.5 5.5l5 5M10.5 5.5l-5 5" -->
<!-- warning: bg #FFECB8, icon <path triangle fill=#F4A702/> + white "!" -->
```
Mapping: priority High→danger · Medium/Yellow→warning · Low→success. Overdue→danger. Success-plan %→success.

### CTA card — 2×2 grid, standard outline (no colored left border)
Grid keeps the sub-line and the due date on the same row (aligned), with a 4px row gap.
```html
<div style="display:grid;grid-template-columns:1fr auto;column-gap:16px;row-gap:4px;align-items:center;background:var(--surface-1);border:1px solid var(--border-strong);border-radius:8px;padding:16px 18px">
  <div style="font-size:15px;font-weight:500;color:var(--text-primary)">CTA name</div>
  <div style="justify-self:end"><!-- priority chip (danger/warning/success) --></div>
  <div style="font-size:13px;color:var(--text-secondary)">Type · account · owner</div>
  <div style="justify-self:end;font-size:13px;color:#F75D4F">Overdue · Apr 30, 2019</div>
</div>
```
No colored left border — CTA cards use only the standard outline; type is shown in the text sub-label.
**Right-side indicator is ALWAYS a pill — consistently.** Every CTA card shows a pill on the right (priority pill, or the overdue `✕ N overdue` pill). If a CTA has no priority, show a **neutral** pill (grey `var(--surface-2)` / `var(--text-secondary)`, no icon) with its type (e.g. "Objectives", "Lifecycle") — NEVER plain text for some cards and a pill for others. Priority pills never use the green ✓.

### Distribution / weighting bar — full width, no gaps, widths sum to 100%
```html
<div style="height:10px;border-radius:6px;overflow:hidden;background:var(--surface-2);display:flex">
  <div style="width:58%;background:#13C77F"></div>
  <div style="width:26%;background:#FFBB00"></div>
  <div style="width:16%;background:#F75D4F"></div>
</div>
```

### Health gauge — arc offset = 100.5 × (1 − score/100)
```html
<svg viewBox="0 0 84 52" width="72" aria-hidden="true">
  <path d="M10 44 A32 32 0 0 1 74 44" fill="none" stroke="var(--border)" stroke-width="6" stroke-linecap="round"/>
  <path d="M10 44 A32 32 0 0 1 74 44" fill="none" stroke="SCORE_COLOR" stroke-width="6" stroke-linecap="round" stroke-dasharray="100.5" stroke-dashoffset="28"/>
  <text x="42" y="44" text-anchor="middle" font-size="20" font-weight="500" fill="SCORE_COLOR">72</text>
</svg>
```
`SCORE_COLOR` = the tenant's `score_color` from `ask_scorecard` (see the health-color rule) — do NOT hardcode green. The number baseline sits at `y=44` so it's **bottom-aligned to the gauge arc**. Unscored: draw only the gray track and put `—` in `var(--text-muted)` at the same `y=44`.

### Timeline card — clickable card (icon circle + date + badge + description)
Each timeline entry is a **clickable card**, not a bare row — clicking it expands the detail via `sendPrompt`. Standalone timeline queries render a stack of these; the account-summary "Recent timeline" section uses the same card.
```html
<div onclick="sendPrompt('Show the full details of the 12 Jun meeting (QBR with exec sponsor) for Acme Inc.')" style="display:grid;grid-template-columns:36px 64px auto 1fr;column-gap:14px;align-items:center;background:var(--surface-1);border:1px solid var(--border-strong);border-radius:8px;padding:12px 14px;margin-bottom:8px;cursor:pointer">
  <div style="width:36px;height:36px;border-radius:50%;background:var(--bg-accent);display:flex;align-items:center;justify-content:center">
    <i class="ti ti-calendar-event" style="font-size:18px;color:var(--text-accent)" aria-hidden="true"></i>
  </div>
  <div style="font-size:14px;color:var(--text-secondary)">12 Jun</div>
  <span style="font-size:13px;font-weight:500;color:var(--text-accent);background:var(--bg-accent);padding:3px 12px;border-radius:6px">Meeting</span>
  <div style="font-size:15px;color:var(--text-primary)">QBR with exec sponsor</div>
</div>
```
Click-through: each card's `onclick` sends a request to expand THAT entry (names the account + date + subject); the account name in a timeline header is also a click-through → the account summary. Contrast: date = `var(--text-secondary)` (not `--text-muted`). Every circle is a **light tint** with a readable icon — including **Call** (`#E6E9EC` circle, `#3C4A57` icon); never a dark/transparent circle with a muted icon. By type: Meeting `#E6F0FD`/`#034AA3` · Email `#EBFBEE`/`#0F8754` · Note `#FFF3D1`/`#DA7309` · Call `#E6E9EC`/`#3C4A57`.

### Scorecard-measure card — name + weight · status chip · submeasures
One per measure. Chip colored by that measure's own `score_color`; unscored → a neutral `— · Unscored` chip.
```html
<div style="display:grid;grid-template-columns:1fr auto;align-items:center;gap:12px;background:var(--surface-1);border:1px solid var(--border-strong);border-radius:8px;padding:12px 14px;margin-bottom:8px">
  <div>
    <div style="font-size:15px;font-weight:500;color:var(--text-primary)">Customer outcomes <span style="font-size:13px;font-weight:400;color:var(--text-secondary)">· 75% weight</span></div>
    <div style="font-size:13px;color:var(--text-secondary);margin-top:2px">Engagement · Breadth of adoption · ROI</div>
  </div>
  <span class="chip" style="background:TINT_OF_SCORE_COLOR"><span style="width:9px;height:9px;border-radius:50%;background:SCORE_COLOR;display:inline-block;flex:0 0 auto"></span><span>72</span></span>
</div>
```
`SCORE_COLOR` = the measure's own `score_color`; `TINT_OF_SCORE_COLOR` = a light tint of it (same treatment as the portfolio health chip). Unscored measure → `<span class="chip" style="background:var(--surface-2);color:var(--text-secondary)">— · Unscored</span>`. Tag unweighted measures "informational" in place of the weight.

### Trend line chart (pattern 8) — the only chart
Load `read_me` with `modules: ["chart"]` first, then render one Chart.js line chart from the CDN allowlist (`cdnjs.cloudflare.com`). One `<canvas>`, x = time, y = metric, Horizon colors, `<script>` last (per the Visualizer streaming rule). Round all displayed numbers. Header above the chart: `<metric> trend — account · <period>`. Never draw a chart for a single data point — use the KPI tile with its ↑/↓ delta instead.

### Next-step buttons (always end with 2–3) — `sendPrompt` sends a chat message
`sendPrompt` feeds the text back through the model, so a follow-up may re-render as plain
text if the skill doesn't re-trigger. **Do NOT prefix the sent text with `/gainsight-viz`
(or "Using gainsight-viz, …")** — it shows as a visible command in the chat. Instead, phrase
the button's sent text as an explicit Gainsight data request that **names the account/object**
(e.g. "…the scorecard measures for Acme Inc.", "…open CTAs for Acme Inc."). The skill's
description re-triggers on that phrasing, so the dashboard re-renders with no visible command
prefix. Still best-effort — a skill can't guarantee re-trigger; the real fix (buttons that
call a tool and re-render in place, with no text round-trip) requires the MCP Apps build.

**Buttons ALWAYS use the accent style (consistency rule).** Every next-step button uses `color:var(--text-accent); background:var(--bg-accent); border:none` — the blue accent pill, exactly as below. **NEVER** emit a bare/default `<button>` (it renders grey and looks unstyled). Same styling on every render, even when other skills are active.
```html
<button onclick="sendPrompt('Show the scorecard measures for Acme Inc.')" style="font-size:14px;color:var(--text-accent);background:var(--bg-accent);border:none;border-radius:var(--radius);padding:8px 14px;cursor:pointer">Scorecard measures</button>
```

---

# Gainsight MCP tools

## CS (Customer Success) — live, read + write
**Tools:** `resolve_customer`, `resolve_user`, `get_records`, `run_query`, `ask_scorecard`, `fetch_cta_list`, `fetch_success_plan_list`, `fetch_timeline_activity_list`, `create_timeline_activity`, `update_timeline_activity`, `manage_cockpit_actions`, `manage_success_plan_actions`, `fetch_report_data`, `report_search_tool`, `get_portfolio_filters`, `fetch_customer_contacts`, `get_object_metadata`, `get_picklist_values`, `get_activity_types_config`.
Always `resolve_customer` FIRST — TWO calls: `mode="resolve"` for the GSID, then
`mode="add_attributes"` with `company_ids=[gsid]` for attributes. Then pass the GSID on.
**Reads:** account summary, health scores, CTAs + tasks, success plans, timeline, scorecards, reports, portfolio, contacts. **Writes:** CTAs, tasks, success plans, timeline activities.

---

# Data wiring — every visual must come from a real tool response

## HARD RULE: never fabricate Gainsight data

Every number, name, date, score, and status in a visualization MUST come from a tool
response in THIS conversation. NEVER invent sample values (no "$485K", no "Priya
Sharma", no made-up health score). If you have not called the tool, call it. If the
data source is not connected (see the table), render an honest empty state that names
the missing connector — do NOT fill it with plausible-looking numbers.

## Data correctness — non-negotiable (verified failures, do NOT regress)

1. **Health bands come from Gainsight, not from us.** Use `overall_label` + `score_color`
   from `ask_scorecard`. Never hardcode 70/40 cutoffs or the words "Healthy/At risk". (See
   the health-color rule above.) A 72 shown as green "Healthy" while Gainsight says "Yellow"
   is a correctness bug.
2. **"my / mine / I / my book of business" ⇒ scope to the current user. Never tenant-wide.**
   - CTAs: `fetch_cta_list` MUST filter `OwnerId` with literal `CURRENT_USER` (+ `IsClosed EQ false`).
     Unscoped returns the whole tenant (tens of thousands of CTAs) — wrong.
   - Portfolio: call `get_portfolio_filters` and **check `has_portfolio_filters`**. If `false`
     ("proceed without portfolio scoping"), do NOT render every account as the user's book —
     instead scope by `Csm`/owner = `CURRENT_USER`, or, if truly unscoped, label it plainly
     as tenant-wide (not "Portfolio health") and cap the set. Silently rendering all 50k+
     accounts under a "your portfolio" header is the worst failure — it looks authoritative
     and is wrong.
3. **`resolve_customer` is TWO calls, not one:** first `mode="resolve"` to get the GSID, then
   `mode="add_attributes"` with `company_ids=[gsid]` for ARR/CSM/stage/renewal. One call does
   not return attributes.
4. **Cap `ask_scorecard` batches.** ~3 accounts ≈ 56 KB, so a 40-account book (~500 KB) dies
   before rendering. For portfolio/KPI: request overall scores only (not full measures),
   batch in chunks (≤ ~15 IDs per call), and cap the rendered set (e.g., top N by ARR/risk).
5. **An account can have MULTIPLE success plans** (even identically named on different
   relationships). Don't assume one — disambiguate by relationship, or list them; never
   silently pick one.

## Which patterns can pull real data here

Only the **CS** Gainsight MCP is connected in this tenant, and every remaining pattern
is CS-sourced — there are no unconnected patterns to fall back for.

| # | Pattern | Source | Live? | How to fetch real data |
|---|---|---|---|---|
| 1 | Account summary | CS | ✅ | `resolve_customer(mode="resolve")` → GSID, then `resolve_customer(mode="add_attributes", company_ids=[gsid])` → industry/ARR/owner/renewal/stage; `ask_scorecard(company_ids=[gsid])` → `overall_label`+`score_color`+measures; `fetch_cta_list(where CompanyId EQ id AND IsClosed EQ false)`; `fetch_timeline_activity_list`. Gauge label/color = tenant's `overall_label`/`score_color`. |
| 2 | Portfolio health | CS | ✅ | `get_portfolio_filters("company")` → **if `has_portfolio_filters:false`, scope by `Csm=CURRENT_USER` or label as tenant-wide (never "your portfolio")**; else `run_query("company", filters)` → GSIDs+ARR+renewal (cap N) → `ask_scorecard` **in ≤15-ID batches, overall scores only** → bucket by `overall_label` |
| 3 | Success plan | CS | ✅ | `fetch_success_plan_list(where CompanyId EQ id)` → may be **>1 plan** (disambiguate by relationship / list); PercentComplete, Status, Type; objectives via `run_query("call_to_action", where CtaGroupId EQ sp_id)` |
| 4 | CTA pipeline | CS | ✅ | "my/open CTAs" → `fetch_cta_list(where OwnerId literal CURRENT_USER AND IsClosed EQ false)` — **always owner-scoped**; account view adds `CompanyId EQ id`. Fields: Name, Company, TypeId__gr.Name, PriorityId__gr.Name, Owner, DueDate, OverdueTaskCount |
| 5 | KPI dashboard | CS | ✅ | portfolio-scoped `run_query("company", …)` (see #2 scoping) with `SUM(Arr)`/`COUNT` + `ask_scorecard` (batched, overall only) for avg health + `fetch_cta_list` count |

Every visualization ends with 2–3 `sendPrompt` next-step buttons. When data is sparse
or unscored, render the empty/blocked state honestly (like the unscored-scorecard alert)
rather than inventing numbers.
