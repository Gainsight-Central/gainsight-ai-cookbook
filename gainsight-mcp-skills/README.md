# Gainsight MCP Skills

> Part of the [Gainsight AI Cookbook](../).

Agent skills that turn Gainsight CS data into the things a CSM or CS leader actually needs — a rendered account dashboard, a weekly call brief, an executive prep note, a risk update logged to Timeline.

Each skill is installed independently. Take the ones that match your role.

## Prerequisites

These skills are instructions for an AI agent — they don't ship code. They call MCP servers, which you need connected first:

| Server | Needed by | Purpose |
|---|---|---|
| **Gainsight CS MCP** | all four | Accounts, scorecards, CTAs, Success Plans, Timeline |
| **Visualizer** (`mcp__visualize__*`) | `gainsight-viz`, `weekly-call-briefs` | Renders dashboards inline in the conversation |
| ***Staircase AI MCP*** | *`exec-prep-note`, `weekly-call-briefs`, `risk-update`* | *Conversation intelligence — sentiment, transcripts, risk scores. Optional; without it these skills fall back to Gainsight data and say so.* |
| **Gmail / Calendar** | `weekly-call-briefs` | Reads your week, drafts pre-call emails |
| **Web search** | `exec-prep-note` | Business-model and earnings research for the "how they make money" section |

## Install

Skills install per-folder. Copy the one you want into your agent's skills directory:

```bash
# Claude Code — one skill
cp -r skills/gainsight-viz ~/.claude/skills/

# or all four
cp -r skills/* ~/.claude/skills/
```

Other clients that read `SKILL.md` use their own skills directory — check your client's docs. Nothing needs building or installing beyond copying the folder.

**Install `gainsight-viz` first.** It governs how every Gainsight answer renders, so the other skills look better with it present.

---

## The skills

### `gainsight-viz` — inline visual dashboards

Renders any Gainsight answer as a dashboard instead of a wall of bullets. Fires automatically whenever you ask about an account, so you never have to request it.

**You say:** *"How is Acme Inc doing?"* · *"Show my portfolio health"* · *"What's Acme's health trend over the last 6 months?"*

**You get** one of 9 fixed layouts — the same request type always produces the same structure:

```
┌──────────────────────────────────────────────────────────────┐
│ 🏢  Acme Inc · Enterprise                    ╭─────╮         │
│     Account summary                          │ 62  │ Yellow  │
│                                              ╰─────╯         │
├──────────────────────────────────────────────────────────────┤
│  ARR          RENEWAL       OPEN CTAS      STAGE             │
│  $450K        Mar 14        3              Adopt             │
├──────────────────────────────────────────────────────────────┤
│  Open CTAs                                                   │
│   ● Risk · Sentiment Risk          High     due Feb 2        │
│   ● Risk · Support Risk            Medium   due Feb 11       │
├──────────────────────────────────────────────────────────────┤
│  Recent timeline                                             │
│   Jan 28  Executive sync · Call        Renewal scoping       │
│   Jan 19  Support escalation · Note    3 open P1s            │
└──────────────────────────────────────────────────────────────┘
```

The discipline is the point: a defined KPI tile is never dropped — a missing value shows `—`, never an invented number. Health bands use *your tenant's* configured colors and labels, not a hardcoded red/amber/green. And "no open CTAs" is rendered differently from "the CTA source isn't connected," because those mean opposite things.

**Layouts:** account summary · portfolio health · success plan · CTA pipeline · KPI dashboard · timeline activity · scorecard measures · trend chart · comparison/ranking

---

### `weekly-call-briefs` — your week, prepped

An interactive Mon–Fri dashboard of every external client call on your calendar, each card expandable into a full brief with draft emails ready to send.

**You say:** *"Prep my week"* · *"Weekly call brief"* · *"Calls next week"* · *"Week of Apr 14"*

**You get** a card per call, expanding to:

```
▼  Tue 10:00   Acme Inc — Quarterly Business Review
   ────────────────────────────────────────────────────────────
   BRIEF     Engagement has been steady but narrowing to a single
             champion since December. Active workstream is the HAU
             rollout, now two weeks behind the agreed date.
             Sentiment trending down; renewal is 61 days out.

   THEMES    HAU Adoption Drop · Champion Concentration
             Renewal Scoping · Support Backlog

   TALKING   1. Reset the HAU timeline — get a date they'll commit to
   POINTS    2. Ask who else should be in the renewal conversation
             3. Close the three open P1s before pricing comes up

   ┌─ Draft pre-call agenda ──┐ ┌─ Exec email (3 variants) ──┐
   │  → one click to Gmail    │ │  → one click to Gmail      │
   └──────────────────────────┘ └────────────────────────────┘
   [ Update Success Plan ]  [ Generate Risk Update ]
```

Ships with [`config.md`](skills/weekly-call-briefs/config.md) — set your name, CRM user ID, and timezone once and the skill reads them on every run. Gmail drafts are drafts: nothing sends without your click.

---

### `exec-prep-note-generic` — brief an exec before a call

Your VP is joining the Acme call in an hour and knows nothing about the account. This produces the note they'll actually read, and posts it to Timeline so it's on the record.

**You say:** *"Exec prep note for Acme Inc"* · *"Get my VP ready for the Globex call"* · *"Executive briefing for Acme"*

**You get** seven fixed sections:

| Section | What goes in it |
|---|---|
| Executive Summary | 4–5 sentences — where the account stands and why this call matters |
| Why We're Having This Call | 1–2 bullets |
| How This Client Makes Money | 1–2 bullets from web + earnings research, so the exec speaks their language |
| Key Strategic Objectives | Success Plan objectives from the last 180 days |
| Key Contacts | Who's in the room, role, engagement level |
| Risk Overview | Gainsight risk CTAs combined with conversation-intelligence signals |
| Client Maturity Index | Where they sit on the adoption curve |

Then it posts the note to the account's Gainsight Timeline automatically, so the next person to open the account sees the same briefing.

---

### `risk-update-skill` — log risk updates to Timeline

You own eight active risk tasks and none have been updated in three weeks. This reads each account's recent calls, cross-references them against what's already in Timeline, and writes the update.

**You say:** *"Update my risk tasks"* · *"Post risk updates"* · *"Log risk notes from my calls"*

**You get** a structured HTML entry posted to each risk task's Timeline:

```
🔴 Risk Update — Acme Inc
Task: Sentiment Risk  |  Reason: Champion Departure  |  Priority: High  |  Updated: Feb 3

RISK SUMMARY
Primary champion left in January and no replacement sponsor has been
identified. Sentiment dropped from 0.62 to 0.31 across the last three
calls. Renewal is 61 days out with no procurement contact engaged.

KEY RISK SIGNALS
 • Champion departed Jan 12; no successor named
 • Sentiment down 50% over three calls
 • Three P1 support cases open more than 21 days
 • No exec engagement since November

RECENT CALL CONTEXT
Operational Call  |  Jan 28  |  Source: Conversation Intelligence
Team raised the support backlog unprompted and asked whether the
rollout date was still realistic...

RECOMMENDED NEXT STEPS
 1. Schedule an exec sponsor check-in within 7 days
 2. Escalate the three open P1s to support leadership
 3. Identify and map a replacement champion before renewal scoping
```

It deliberately cross-references transcripts against existing Timeline notes first, so it adds what's missing rather than restating what you already logged.

---

## What these skills won't do

- **They don't invent data.** Every one refuses to fabricate a metric, a risk, or an activity. Empty states are explicit — "No open CTAs" is a rendered state, not a gap.
- **They don't act without you.** Emails are drafts. Success Plan and risk updates surface for review. The two skills that write to Timeline (`exec-prep-note`, `risk-update`) say so plainly above.
- **They don't assume your field names.** `ARR`, `Health Score`, and tier fields differ per tenant; the skills discover them rather than hardcoding.

## Adding more

This is the first set. Eight further skills exist — a CSM book pulse, a single-account workbench, EBR scheduling, stakeholder reconnection, a post-call workflow, an exec renewal radar, a churn retrospective, and a renewal priority planner — but they depend on a shared foundation layer that isn't published yet. They'll land here once that ships.
