# Use case: adoption

Version 2. Requires config schema 2. Follows `reference/use-case-contract.md`.

## Fields

| Field | Value |
| --- | --- |
| `id` | `adoption` |
| `trigger` | `threshold`. A user or account falls below the goal's threshold. When the CSM picks "Accounts I name" from the fallback ladder, the run is `manual` for that run: a list the CSM gives, with no threshold signal. |
| `unit` | `user`. One email per low-adoption user. |
| `recipient_rule` | The user flagged by the signal, from `contacts`. If the signal is account-level only, a short list of candidate contacts chosen by the rules in Choosing recipients. The CSM confirms. |
| `actions_allowed` | `email_draft`. CTA proposals are a later phase. |
| `cadence` | `one_shot` |
| `outcome_metric` | Drafts approved, and the share approved without edits |

## Capabilities

| Capability | Need | If missing |
| --- | --- | --- |
| `identity`, `book`, `contacts`, `signal`, `knowledge` | required | Block the run |
| `goals` | optional | Run discovery against the signal. Label rows "no recorded goal". |
| `context` | optional | Ground on signal and knowledge only. Label rows "context not available". |
| `mail`, `ledger` | optional | See `capabilities.md` |

## Goal schema

A goal has: `metric` (a feature, license or seat use, usage frequency, a health-score driver, or any adoption metric the data source holds and the catalog lists), `threshold`, `window`, and `scope` (the CSM's book, a segment, or named accounts).

`goal_examples` (shown as cards on the ready banner, in this order, only when the catalog holds the metric and the adapter declares any scope field the card needs):

1. Declining usage: "accounts where <usage metric> has gone down over the last 90 days". Needs a usage metric with a timestamp. Without one, the trend cannot be computed: leave this card out.
2. Under-used features vs objectives: "accounts where a recorded objective maps to a product feature not used in the last 90 days". Shown only when `goals` is mapped. It needs the account's objectives from `goals` and feature usage from the signal source. If either is missing when the goal is mapped, say which, and offer the other examples.
3. Renewal pairing: "accounts renewing in the next 90 days where <usage metric> is low". Needs a usage metric and a declared renewal date field.
4. License use: "accounts with licenses assigned but no activity in the last 90 days, or using more licenses than purchased".
5. Login activity: "accounts where fewer than 30% of licensed users have logged in over the last 30 days". Last, because typed requests rarely start with login.

Source for the ordering: an internal sheet of 30 days of typed MCP prompts (Gainsight_MCP_Prompts_30d, 13 Sep to 12 Oct 2026). Usage and adoption wording and license use were common. Login and "never logged in" were rare. The sample is Copilot-heavy and has no Claude rows, and 45% of prompts are cut off, so it guides wording only. No prompt text is copied into the plugin.

**Scope fields** the goal check can offer, each only if the adapter declares it (see the adapter's Scope fields) or the catalog holds it: a renewal window ("renewing in N days"), a health band filter ("red" or "at risk", by the source's own band), the CSM's book, a single account, a named group of accounts, and any segment value in the catalog.

**Defaults.** Window: 90 days when the CSM gives none. Threshold: the metric's own band when the source returns one, else the goal confirm proposes one and the CSM adjusts it. Say both in the interpretation. Few typed requests state a threshold.

`catalog_cards` (built from the `## Catalog` in `config.md`, used when the fixed examples above do not fill 3 slots):

- One per metric, ranked by coverage (most sampled accounts with a value first): "accounts where <metric name> is low". The threshold is the measure's own band if the source returns one. If it returns none, the goal confirm asks for it. Never invent a threshold or a color band.
- One renewal variant per top metric, when a renewal date field is declared: "accounts renewing in the next 90 days where <metric name> is low".
- One per metric within the largest segment value: "accounts in <segment value> where <metric name> is low (<n> accounts)". Use a real value from the catalog.
- A metric with no value on any sampled account gets no card and is not named on the banner. If the CSM types that metric as a goal, the goal check says it had no values on the sampled accounts.
- Cards show up to 3 in total: fixed examples that pass first, in the order above, then catalog cards. Then the scan card.

1. The user states the goal in plain words, for example "accounts where fewer than 30% of licensed users have logged in over 30 days".
2. Run the goal check in `reference/steps/goal-check.md` against the `## Catalog` in `config.md`. A metric or scope the data cannot answer is stopped here, with real options. If no metric fits, use the fallback ladder in that file.
3. Map it to a metric and source from the capability map. Show the interpretation back: metric, source, threshold, window, scope.
4. Ask the goal confirm from `reference/questions.md`, with the interpretation inside the question. Do not go on until they confirm.

**"Not sure" path.** Run a theme scan over `goals` and `context` across the book. Group adoption mentions by theme (for example feature not used, seats not activated, low login). Show each theme with a count and one verbatim example with source and date. Offer 2-4 suggested goals built from those themes. The user picks one, rewrites one, or types their own. The final goal still goes through the confirm above.

## Named accounts, no signal (fallback ladder option 4)

The CSM names the accounts. The cohort is those accounts, scoped to the CSM's book and the suppression rules. Skip the Signal section. Recipients come from Choosing recipients, with no signal-flagged user, so the CSM confirms every recipient. Ground each account from `context` and `knowledge` as usual. Label every row and card "no usage signal". The email anchors on one recent thread and one recommended item, and makes no claim about usage. The funnel's Flagged by signal tile reads "n/a, no signal".

## Discovery (goal-scoped)

Look for discussions of the confirmed goal in, as the capability map provides:

- `goals`: recorded goals, success plans, objectives tied to the account.
- `context`: timeline entries, notes, and communications that mention the goal's topic.

Rules:

- A match is a goal or discussion whose text concerns the goal's metric or topic, about the customer's own use of the product being tracked. Do not count text about the customer's own product or end users. Keep login-error, access, and activation tickets in a separate group named for what they are ("access problems"). They are not evidence of low login activity. In a real run, 11 of 25 matched accounts fell in that group.
- Keep each match verbatim with source and date.
- Narrow the book to accounts with at least one match. Show: accounts in scope, accounts with a match, the top themes.
- Several accounts may match the same topic in different words. Group them. Do not rename a theme in words that appear in no source. If the source rows carry no topic label, name the group with a phrase quoted from one of its rows, and mark the grouping `inferred`. One example is one mention, not a pattern. Say how many rows were in the book and how many were scanned.
- Quote only text you fetched in full (for a context source, fetch the evidence first). A search summary is not a quote.
- Say which sources the scan covered (success plans, CTAs, timeline, communications), how many pages or rows were read, and which were not.
- If no account matches, say so and ask the no-match question from `reference/questions.md`.
- Cap the scan to the CSM's scoped book. For a large book, search by the goal's topic terms, not account by account.

## Signal

If the source holds an account-level figure only (for example active users and licenses on the company record), the signal is account-level, the unit is the account, and the recipient is the account's admin or champion contact. Say so in the interpretation. State which denominator you used (purchased or assigned) and flag when the other would change the result. Some license types cannot log in. If context says so (for example a ticket stating that a license type has no login access), say the ratio may understate use and name the license type. Say when a value has no timestamp.

Measure the goal's `metric` against its `threshold` and `window` from the configured source, ranked in one query. Return the user or account value and whether it crossed the threshold. The signal source is whichever data layer the config names. The use case does not assume one.

Split the flagged cohort when the data allows it. For a login-style metric, that is "never logged in" and "logged in but low usage" (shelfware). For a feature metric, "never used" and "used rarely".

## Choosing recipients

When the signal is account-level, the agent proposes recipients, and the CSM decides.

1. Start from the account's contacts.
2. Remove: no email, opted out, marked do-not-contact, bounced, no longer at the account, matching the suppression list, or a shared mailbox (for example billing or AP inboxes).
3. Remove contacts whose email domain is not the customer's, and the vendor's own staff, unless config says otherwise. A subdomain of the customer's domain is a match to flag, not to drop silently. A near-miss such as a typo domain or a `.invalid` address is removed and listed.
4. Prefer contacts who can log in to the product (license type allows it) and were seen recently. If the data has no license or login field, say so.
5. Rank the rest by role: product admin, then adoption champion, then the account's day-to-day contact. Role names differ by tenant. Map the tenant's role values to these three, say which mapping you used, and say when a role has no clear match. Decision makers with no license are not adoption recipients. Mention them to the CSM as a different conversation.
6. Propose one primary and at most two others. Admins who tie get ordered by last seen, and you say so. If a proposed contact looks like the customer's own CSM or an internal owner, ask the CSM whether that person should get the nudge. For each, show name, title, role, why chosen (the fields), and anything odd: duplicate record, name that does not match its email, missing opt-out value.
7. Say how many contacts were read and how many exist. A candidate list built from the first page of a long list is a sample.
8. Ask the recipients question from `reference/questions.md` before drafting, with each person's name and role inside it. Never email a contact the CSM did not see.

## Grounding questions

Ask `context` for each kept account:

- What has the account raised about adoption, onboarding, or this topic recently?
- What is the account's current health and sentiment?
- Are there active risk signals (churn, escalation, offboarding)?

Exclusions: an account in churn or offboarding, or with an open escalation, gets `Flagged risk`. No draft. One-line reason. An account whose context is critical risk, or whose sources conflict (for example an active status next to a note that the customer wants to cancel), also gets `Flagged risk` with the conflict stated, and the CSM decides. An account with a near renewal or a questioned-value note may still get a draft, but the draft is shown with that risk named above it and no pricing or contract terms.

## Draft intent

- Purpose: acknowledge one recent thread from the recipient's own account, then show how the one recommended item from `knowledge` helps with the gap and the goal, and ask for one next step.
- Structure: a one-line acknowledgement of the thread (see `ground.md`, Recent thread), two to three sentences on what the item lets them do, in the words of its source, then the ask. With `thread: none`, skip the acknowledgement and do not mention history.
- Excitement comes from the specific benefit to this recipient's gap, stated plainly. No superlatives, no claims the source does not make, no invented numbers. Paid items keep `[verify entitlement]`.
- Length: about 150 words. One screen.
- One ask: one link or one next step.
- Anchor: the recommended item, described only as its source describes it, plus one grounded fact about the user's own usage if retrieved.
- The email body carries `sourced` facts only. See `draft.md`, Fact check.
- Never mention in the email: health score, sentiment, risk, renewal or pricing, a CTA or internal task, or anything from the internal group in `ground.md`.

## Funnel stages

| Stage | Produced by |
| --- | --- |
| Book | `book` in `data.md` |
| With goal | discovery |
| Flagged by signal | `signal` in `data.md` |
| Matched contacts | `contacts` in `data.md` |
| Drafts to review | `draft.md` |

Skipped is shown as its own tile.

## Status badges

| Badge | Earned by |
| --- | --- |
| `Email draft` + `High confidence` | A draft exists, it passed the fact check, every fact in it is `sourced`, and the item's product is one the account has (or the product check was skipped because knowledge names one product). The card states these checks in one line, see `review.md`. |
| `Thread follow-up only` | The email acknowledges the thread and recommends no item. Never shown with `High confidence`. |
| `Sample reviewed` | The draft was one of the three in the tone check the CSM saw before the rest were drafted |
| `Approved` | The CSM approved the draft this session. It is not yet in the mail tool until the batch step. |
| `Drafted in mail` | A draft was created in the mail tool |
| `Sent` | A real send or a confirmed test-send completed this session |
| `Already adopting` | The signal shows healthy use. No nudge. Say why in the row (the number and window). |
| `Flagged risk` | Grounding found an active risk. No draft. Say why. |
| `Grounding incomplete` | Context or knowledge could not confirm enough. Say what is missing. |

Never show `Sent` without a completed send in this session.

## Evals

`evals/` in the plugin root holds the adoption fixtures.
