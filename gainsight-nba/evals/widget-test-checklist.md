# Paginated review widget: manual test (Desktop chat)

Run once per release that changes `reference/widgets/paginated-review.html`. Use a run with at least 12 drafts, at least 2 flagged. Record the plugin version, the date, and pass or fail for each line. Screenshots of any fail.

If any line 1 to 8 fails, review falls back to the typed reply as the main path and the widget stays marked experimental in `plugin-maintainer-notes.md`.

| # | Check | Pass looks like |
| --- | --- | --- |
| 1 | The widget renders in one message with the counts strip | First draft card is open. No click needed. |
| 2 | Card layout | Name and goal line, gauge, status chip, Why this account block (headline and up to 3 bullets), 4 tiles, Why this contact, Recommended action, Evidence box, buttons. No checkbox. |
| 3 | Next and Prev | The page changes and the "n of N" text changes. No chat message is posted. |
| 4 | Approve | The chip reads "Marked to approve", the dot turns green, the widget moves to the next draft. No chat message is posted. |
| 5 | Reject and Edit | The chip and dot change (red, amber). No chat message is posted. |
| 6 | All drafts | The list shows every draft with dot, subject, group and the Why this account headline on a second line. A row opens that draft. The button label flips to Back to draft. |
| 7 | Approve all ready | Marks every Ready draft with no risk note. A flagged draft and any Needs a look draft stay unmarked. |
| 8 | Send decisions | One message is posted that names every decision with draft number, recipient and account, and lists the bulk approvals. With nothing marked, nothing is posted. |
| 9 | After Send decisions | The agent replies with the result chips and counts, asks "What should change in the draft for <name>?" for the first Edit, then shows the next widget or the batch step. No dialog. |
| 10 | Over 10 drafts | A Next 10 button appears and shows the next set. |
| 11 | Gauge | The color and label come from the tenant scorecard band. If a second health value differs, the gauge says Scorecard and the other value is in the Grounding box with its source. |
| 12 | Dark and light mode | Text and chips stay readable in both. |
| 13 | Typed reply | "approve all ready, reject 4" works with the widget on screen. |
| 14 | Failed render | If forced to fail, the agent says so once, prints the full draft, and asks for a typed reply. No dialog. |
| 15 | Why this account | Sits above the tiles. Every fact in the headline appears in a bullet with sourced or inferred and a source. A draft with no signal shows "No usage signal, drafted from account context." and no bullets. |

Notes to record: widget size at 10 drafts (did it render or retry smaller), time to render, anything that looked clipped.
