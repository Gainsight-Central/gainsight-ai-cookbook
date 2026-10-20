# Design system for widgets

Tokens, colors, icons, and component styles for the funnel, review queue, draft card, and dashboard. Layout and sequence are in `steps/review.md`. This file holds styling only. It is a trimmed copy of the Gainsight viz skill: the account, portfolio, CTA, timeline, scorecard, and data-wiring sections were left out on purpose.

## Render flow

1. Have the data first. A widget never holds a number that did not come from a tool response or the run.
2. Call `mcp__visualize__read_me` once per session with `modules: ["mockup"]` before the first `show_widget`. Do not narrate it.
3. Call `mcp__visualize__show_widget` with one HTML fragment. It renders inline.
4. In the reply, add a short note and the next step. Do not repeat the widget's content as text.
5. No `.html`, `.jsx`, or `.tsx` file artifact. Those open in a side panel.

If a render fails: at most 2 attempts in total. Check that `read_me` was called. Retry once, smaller: 10 rows or fewer, no gradients, no `<script>`, plain divs with host variables, balanced tags, no external URLs. Then say plainly "the inline visual failed to render" and use the text fallback from `review.md`. Never split one answer across widgets. Empty data is not a failure: render the empty state.

Format by count: 10 items or fewer, cards. 11 or more, one compact table with one text row each, in a single widget.

## Visualizer contract

- HTML fragment only. No `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`.
- The outermost element is transparent. The host provides the page background.
- First element: `<h2 class="sr-only">one-sentence summary</h2>`.
- Font weights 400 and 500 only. Never 600 or 700.
- Sentence case everywhere, including table headers. No Title Case, no ALL CAPS.
- Body text 16px, line-height 1.7. Card corners 12px. Control corners `var(--radius)`.
- Text on a colored background uses the darkest shade of that color family. Never black or gray.
- Single-sided borders get `border-radius: 0`.
- Never `position: fixed`.
- No emoji. Icons are inline SVG, never the Tabler webfont (class `ti`). The font drew as empty squares in a Desktop chat run on 2026-10-08. Section titles and labels carry no icon.

## Host variables (light and dark)

These are the only theme variables. Do not invent others.

```
Surfaces:  var(--surface-2) inset   var(--surface-1) card bg   var(--surface-0) page bg
Tints:     var(--bg-accent) var(--bg-success) var(--bg-warning) var(--bg-danger)
Text:      var(--text-primary) var(--text-secondary) var(--text-muted)
           var(--text-accent) var(--text-success) var(--text-warning) var(--text-danger)
Borders:   var(--border) var(--border-strong)
Layout:    var(--radius) var(--pad-sm|md|lg|xl) var(--gap-xs|sm|md|lg|xl)
```

## Hardcoded hex, only where a variable cannot express it

- Status chips: label `#181F26` on a tint. Success `#D5F5DB`, warning `#FFECB8`, danger `#FDDFDC`, orange `#FFE5D2`. Each has a leading filled icon.
- Health or score color: the tenant's own band from the source (`score_color`, label verbatim). Bands are tenant-configured, so a 72 may be "Yellow", not "Healthy". Fallback only when the source returns no color (lower bound inclusive, so 50 is Yellow; caption it "standard scale", never a band name): 0-30 Red `#DC3626`, 30-50 Orange `#E8833A`, 50-75 Yellow `#F4A702`, 75-90 Lime `#7DBB34`, 90-100 Green `#13AD68`. Never invent "Healthy" or "At risk" text that the source does not say.
- Distribution bar segments: `#13C77F`, `#FFBB00`, `#F75D4F`.
- Banner: a full-width bar in chip colors. Background `#FFECB8` (warning), `#FDDFDC` (danger), or `#D5F5DB` (success), text always `#181F26`, 12px radius, the chip's leading SVG icon. Never a dark or translucent tinted background, and never dark text on a dark background.
- Text color on the surface (percentages, deltas, labels): use `var(--text-success)`, `var(--text-warning)`, `var(--text-danger)`. The dark hexes are for dark text on a light chip only.
- Green means done or active only. A priority or count is never a green chip.
- Do not color a plain count. A count uses `var(--text-primary)`. Only a score or a trend delta carries a status color.
- Cards use an outline, not a shadow: `border:1px solid var(--border-strong)`. No `box-shadow`.
- `var(--text-muted)` is for de-emphasized text only. Labels and table headers use `var(--text-secondary)`.

## Icons

Inline SVG only. 16px, `viewBox="0 0 16 16"`, `fill="none"`, `stroke="currentColor"`, stroke width 1.7, round caps and joins, `aria-hidden="true"`. Color through the parent's `color`. Do not hand-draw other icons. Use only these:

```html
<!-- chevron-right (clickable tiles and queue rows, color var(--text-muted)) -->
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>
<!-- arrow-left (Back to review queue) -->
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 8H3M7 4L3 8l4 4"/></svg>
```

The filled circle and triangle icons inside status chips are in the Status chip component. Nothing else gets an icon.

## Components

### KPI tile (always a card)

Every stat is a carded tile. The label stays on one line (`white-space:nowrap;overflow:hidden;text-overflow:ellipsis`). If a label does not fit, shorten it. It never wraps onto the value. N stats are N identical tiles in a `repeat(N,1fr)` grid, N up to 4 (5 if wide). Never leave a tile alone on a second row.

```html
<div style="background:var(--surface-1);border:1px solid var(--border-strong);border-radius:12px;padding:14px">
  <div style="font-size:13px;color:var(--text-secondary);margin-bottom:6px">Drafts</div>
  <div style="font-size:26px;font-weight:500;color:var(--text-primary);line-height:1.2">14</div>
  <div style="font-size:13px;color:var(--text-secondary)">to review</div>
</div>
```

### Counts strip

At the start of review, one row of N KPI tiles in a `repeat(N,1fr)` grid, N up to 5 (book, the goal's flagged stage, contacts, drafts, skipped). Same tile as above but smaller: 12px label on one line with ellipsis, 22px value at weight 500, padding 10px. Not clickable, no chevron. A muted 13px line under the row says "N drafts ready".

### Status chip

Leading filled icon, light tint, dark label `#181F26`. Pick the variant by meaning: success (green circle, white check), danger (red circle, white cross), warning (amber triangle, white mark).

```html
<span style="display:inline-flex;align-items:center;gap:6px;padding:4px 12px 4px 7px;border-radius:10px;font-size:13px;font-weight:500;color:#181F26;background:#D5F5DB;line-height:1">
  <svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="#13AD68"/><path d="M4.6 8.3l2 2 4-4.6" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>Approved</span>
<!-- danger: bg #FDDFDC, circle fill #DC3626, white cross path "M5.5 5.5l5 5M10.5 5.5l-5 5" -->
<!-- warning: bg #FFECB8, triangle fill #F4A702, white "!" -->
```

### Table

One table, sorted by a fixed key, inside a card. `table-layout:fixed` with a `<colgroup>`. Cells single-line with ellipsis. Header row: weight 500, `var(--text-secondary)`, `var(--surface-2)` background, `2px solid var(--border)` bottom border. A status column is pilled in every row or in none.

### Distribution bar

```html
<div style="height:10px;border-radius:6px;overflow:hidden;background:var(--surface-2);display:flex">
  <div style="width:58%;background:#13C77F"></div>
  <div style="width:26%;background:#FFBB00"></div>
  <div style="width:16%;background:#F75D4F"></div>
</div>
```

Full width, no gaps, widths sum to 100%.

### Gauge (arc offset = 100.5 x (1 - score/100))

```html
<svg viewBox="0 0 84 52" width="72" aria-hidden="true">
  <path d="M10 44 A32 32 0 0 1 74 44" fill="none" stroke="var(--border)" stroke-width="6" stroke-linecap="round"/>
  <path d="M10 44 A32 32 0 0 1 74 44" fill="none" stroke="SCORE_COLOR" stroke-width="6" stroke-linecap="round" stroke-dasharray="100.5" stroke-dashoffset="28"/>
  <text x="42" y="44" text-anchor="middle" font-size="20" font-weight="500" fill="SCORE_COLOR">72</text>
</svg>
```

`SCORE_COLOR` is the source's color for that value. Unscored: draw the gray track only and put a dash in `var(--text-muted)` at `y=44`.

The gauge is always this half-circle arc, never a full ring. Use it for the account's health score, in the source's band color, with the band label beneath. Use it only for a value that is a score with a band from the source. For any other goal metric (a percentage change, a count, a ratio), show the value as a number (26px, weight 500) with the metric name beneath, and draw no gauge.

### Progress bar (setup)

A card with the title "Setup", a line "Step 2 of 3: Tone and knowledge", a muted sub-line for the question ("Question 1 of 2", or "Email 2" when the count is open), a 10px bar (filled share in `var(--text-accent)`, track `var(--surface-2)`), and the steps as a row of labels: finished steps with the success-chip check SVG, the current step in `var(--text-primary)`, the rest in `var(--text-secondary)`. No percentage text. The filled share is finished steps divided by the total.

```html
<div style="background:var(--surface-1);border:1px solid var(--border-strong);border-radius:12px;padding:14px">
  <div style="font-size:13px;color:var(--text-secondary);margin-bottom:6px">Setup</div>
  <div style="font-size:16px;font-weight:500;color:var(--text-primary);margin-bottom:10px">Step 2 of 3: Tone and knowledge</div>
  <div style="height:10px;border-radius:6px;overflow:hidden;background:var(--surface-2)"><div style="width:33%;height:10px;background:var(--text-accent)"></div></div>
</div>
```

### Paginated review card

Spec for `reference/widgets/paginated-review.html`. One widget, up to 10 drafts, one `<section class="pg">` per draft. Page layout (top to bottom): account name and goal line with the gauge at the right, a status chip, a muted "why this badge" line, the Why this account block (accent left border, a 16px headline, up to 3 bullets), four KPI tiles, an optional banner, the Why this contact box, the Recommended action box, the Evidence box, then the buttons. Below the pages: status dots, one count line, and the buttons Prev, Next, Approve all ready, Send decisions. A top-right "All drafts" button swaps to the list view.

- Script goes last. State lives in script variables. No external URLs, no storage, no network calls. The only outbound call is `sendPrompt`.
- Status dot and chip colors: approve `#13AD68` on `#D5F5DB`, reject `#DC3626` on `#FDDFDC`, edit `#F4A702` on `#FFECB8`, none `var(--border-strong)`.
- Every button that calls `sendPrompt` or runs the script uses the accent pill.
- If the render fails twice, use 5 drafts per widget, then the text fallback in `review.md`.

### Ready banner and goal cards

Banner: one card. Row 1: the success chip's check icon (the filled green circle, 24px) beside the headline (20px, weight 500) and a `var(--text-secondary)` sub-line. Row 2: connected chips in a flex row with wrap off at the container and `white-space:nowrap` on each chip. A connected source uses the success chip colors. A source set to none or not connected uses a neutral chip (`var(--surface-2)` background, `var(--text-secondary)`). Send chip: warning colors for "Drafts only, sending off". Row 3, only when needed: the save notice as a full-width warning bar (banner colors above). Row 4: "What's next" as four equal small labels in a row, the current one in `var(--text-primary)` weight 500 with a 2px `var(--text-accent)` underline, the rest in `var(--text-secondary)`.

Goal cards: a grid of up to four tiles, each a clickable card (outline, 12px radius, `cursor:pointer`, chevron SVG at the right). A bold title line, a muted one-line description. Each calls `sendPrompt`. The last tile, "Not sure: scan my book", is the same card with `var(--bg-accent)` as its background. Never put more than four tiles in the grid.

### Buttons

Every button that calls `sendPrompt` uses the accent pill. Never a bare `<button>`.

```html
<button onclick="sendPrompt('Show me the full draft for Jordan Lee at Acme')" style="font-size:14px;color:var(--text-accent);background:var(--bg-accent);border:none;border-radius:var(--radius);padding:8px 14px;cursor:pointer">Open draft</button>
```

Write the sent text as a plain request that names the account and the person. Do not prefix it with a skill name or slash command: it shows in the chat. `sendPrompt` goes back through the model, so the text must carry enough to act on without the widget.

## Source

Trimmed from the synced `gainsight-viz` skill on 2026-10-08. Re-sync when that skill changes its tokens or contract.
