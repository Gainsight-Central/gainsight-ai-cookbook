# Step: ground (context and knowledge match)

Capabilities used: `context`, `knowledge`. The use case supplies `grounding_questions`.

## 1. Context

For each kept account, ask `context` the use case's `grounding_questions`. Collect 2-4 facts per account (health, sentiment, a recent theme), each with its source id. Get the health score and its band from the scorecard when the capability map has one (see the adapter), one account at a time. Keep the health value, the source's band label and color, and the date: the review step shows them on the queue group header and on each draft card. Do not map a band to your own labels.

- Thin first pass: if an account has fewer than 2 sourced facts about its own recent engagement or sentiment, widen the context search once (the last 180 days instead of the default window) before marking it thin. Say the window you used. If it is still thin, mark it `Grounding incomplete` and say what is missing. Do not pad the email with facts from another account.
- Apply the use case's exclusion rules. An account with an active risk that should pause outreach gets the status the use case names. Do not draft for it. Explain the risk in one line.
- Tied-to-recipient rule: a fact may appear in an email only if it concerns that recipient or their own account. A fact about another contact, or an internal note, may inform the choice of action and never the wording.
- If `context` is `none`, ground on `signal` and `knowledge` only, and label every row "context not available".
- If grounding for an account is thin, mark it `Grounding incomplete` and say what is missing.

## 1b. Recent thread (for the opening line)

For each recipient's account, find what was said recently, so the email can open by acknowledging it.

- Ask `context` for the last 90 days of communications (emails, calls, meetings, tickets) and timeline notes. If fewer than 2 usable items come back, widen once to 180 days and say the window. Fetch the full text of any item you plan to rely on. A summary is not quotable.
- Keep each item with its source, date, who said it, and a short verbatim quote.
- Sort every item into one of two groups:
  - **Customer-visible, may acknowledge:** something the customer said or asked, a request they raised, or a follow-up the customer was told we would do (an offered walkthrough, a promised answer, an open support request they raised). The customer already knows about it.
  - **Internal, may inform only:** CTAs, internal tasks, risk flags, health or sentiment notes, renewal or pricing notes, anything written for the team. It can shape the choice of item. It never appears in the wording.
- A customer-visible item belongs to the recipient's own account. If it was said by a different contact, it may inform the draft. It may be acknowledged only if the recipient was on that thread.
- Pick at most one item to acknowledge: the most recent customer-visible item that bears on adoption or on the recommended feature and is either an open follow-up or from the last 30 days. An older, closed or unrelated thread is not acknowledged. The draft then uses the sourced goal usage fact as its context line (usecase.md, Draft intent). A usage number that appears only in a CTA or internal note is internal and is not used. If an open follow-up exists, prefer it and say what is still open, in the customer's terms. Do not claim it is done or promise a date you did not find.
- If no customer-visible item exists, record `thread: none`. The draft skips the acknowledgement and the card says "Personalization: thin". Do not invent one.

## 2. Knowledge match

Map the account's gap to one item in `knowledge.md`.

- Describe the item the way its source does. Every name, capability, and benefit in a draft traces to `knowledge.md` or a page you fetched raw.
- Prefer an item that speaks to the goal the user defined, when one fits.
- **Product fit.** Each item in `knowledge.md` names the product it belongs to. Before you choose an item, check the account's own products from the source (a purchased-products field, subscriptions, or product relationships, as the adapter names them). The check applies when `knowledge.md` names more than one product. If every item belongs to one product, or none names a product, skip the check and have the card say "Product fit: not checked, single product". When it applies, recommend only an item whose product the account has. If the account has none of the item's products, pick another item. If no item fits, or the account's products are not recorded, set `Grounding incomplete: product not confirmed` and do not draft. The `products` line in `config.md` lists the vendor's products. It never says what an account owns, so do not use it as the account's products. Never infer the product from the account's name, segment, or what similar accounts have.
- Items marked as paid: flag `[verify entitlement]` unless the account's entitlement is known.
- Do not invent feature names or capabilities.

## Output

Per account or recipient: the thread to acknowledge (or `thread: none`), the grounded facts (each `sourced` or `inferred`), the one item to recommend with its one-line value and source, and any status flag.

## Delegating

A subagent does not inherit this skill's context. If you split grounding across subagents, each prompt names the `context` adapter and server, the account, the goal, the tied-to-recipient rule, and the output format above. Merge the results yourself and keep the source id on every fact.
