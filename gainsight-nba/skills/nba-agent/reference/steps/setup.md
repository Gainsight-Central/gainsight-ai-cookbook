# Setup (one time per customer)

Three steps. Run only for the blockers that are missing. Ask once, save, never ask again unless the user asks to change something. Do not invent any of it. Ground each answer in what the user provides or a tool returned.

## How to ask

- One question per message. Never list several. Use `AskUserQuestion` with short options where the answer is a choice. For an open answer (a pasted email, a URL, a work email), ask one plain sentence.
- Offer the safe default as the first option, labeled "(Recommended)", where one exists.
- Skip always works. A skip applies the stated default, says so in one line, and moves on. A skipped question never comes back as a prerequisite. Only a required capability that no connected tool can fill stops the run, and then say which one and how to connect it.
- If the user gives several answers in one message, take them all, skip the questions they answered, and say what you took.
- Every question stands alone. Someone who sees only the question and its options must know which setup step it belongs to, what is being decided, and what each option does. Start the question with the step name and put the proposal inside the question or the option descriptions, not in earlier chat text. A question dialog can hide the text above it. Never ask a bare "Use these, or change something?" or "Save this?".
- Before asking, check whether the answer is already known from a connected tool, a saved file, the chat, or an earlier answer. Never ask for something you can read.

## Progress

The total is 3. Say so once at the start, in one line: "Setup is 3 short steps."

- At the start of each step, and once at the end, show the progress card from `reference/design.md`: "Step 2 of 3: Tone and knowledge", the filled bar, and the finished steps with a check. Inside the card add a line for the question, for example "Question 1 of 2". Where the count is open, write "Email 2" and do not invent a total.
- If `show_widget` is not available, print the progress line as the first line of every setup message, with a text bar. One block per finished step, one empty block per step left (the same share as the widget bar): `Setup ▰▱▱  Step 2 of 3: Tone and knowledge · Connect ✓`. Add `· Question 1 of 2` only where a count exists. Never put it mid-message or at the end.
- A step already done is shown as done, and the total stays 3. Never show a step as done before its content is confirmed.

## 1. Connect

Questions: the data sources, then who is running it. Ask only what you cannot find. The catalog probe in item 4 asks nothing.

1. **Data sources.** Match each capability in `reference/capabilities.md` to the connected tools by adapter in `reference/adapters/`. Ask one question with the mapping inside it: "Connect: I matched these tools: identity and book to Gainsight CS, context to Staircase, mail to <mail tool>, ledger to a file. Use this mapping?" with options "Use this mapping (Recommended)" and "Change one". List only the capabilities that matched. Ask about a single capability only if nothing matched it, and offer `none` where the capability is optional. If a required capability has no tool, stop here and say which tool to connect.
2. **Who is running it.** The connected CS tool cannot say who is signed in: its lookup needs a name or email, and nothing it returns names the current user. Use a name or work email already known from the chat or a saved file. If none is known, ask one open question: "Connect: what is your work email?" Resolve the CSM through `identity` and state the result in the next message: "Found you: <name>, <role>." Ask a question only if the lookup finds no one or finds more than one: then ask which CSM to run for, with the candidates as options. Save `csm_name` and `csm_email`.
3. **Customer.** Take the tenant name from the connected server (its URL or connector name) and state it with the line above: "Running for <tenant>." If no name can be read, ask one open question: "Connect: which company's product are the emails about?" If the CSM runs the agent for a different vendor than the tenant, they say so and you ask the same question.

4. **Catalog.** Right after the mapping is confirmed, probe what the data can measure. No question is asked. Use the `signal`, `book`, and `goals` adapters (the adapter says how). Say one line: "Checking what your data can measure."
   - Metrics: every adoption metric the `signal` source holds. For each, note whether it is per user or per account and whether it has a timestamp. Use the source's own name for it.
   - Coverage: sample up to 5 accounts from the CSM's book for each metric, and record how many had a value ("3 of 5"). One sampled account is too thin to rule a metric in or out. Say the sample size.
   - Segments: account fields that group accounts (a segment, tier, region, lifecycle stage, and so on). For each, read its real values with counts.
   - Not found: say what the probe looked for and did not find, such as feature-level usage.
   - Save it under `## Catalog` in `config.md` with the date. Record only what a tool or file returned. Never fill an entry from memory.
   - Keep the probe small. Use small selects. If a response is too large for the chat, save it to a file and search it, as the adapter says.
   - Show the result in one line: "Found 3 adoption metrics and 2 segment fields. Not found: feature-level usage." If `metrics` is empty, do not stop. Go to the fallback ladder in `reference/steps/goal-check.md`.
   - Refresh the catalog only when the CSM asks, or once after a goal check fails and the CSM says the data exists.

Products are not asked here. They come from the knowledge step.

## 2. Tone and knowledge

1. **Tone.** Ask for one real email the customer has sent, pasted in, with a "Skip, use a neutral tone" option. One sample is enough. Say that more samples make the tone more reliable, and that the CSM can add more later by pasting them. Read it and extract: greeting and sign-off patterns, sentence length, formality, and any do or don't you can see. Write `style.md` from the example only. If the sample does not show something, do not assert it. If the CSM skips, write a short neutral style, mark it `source: default, no samples`, and say so. This is not another customer's tone.
2. **Knowledge.** Ask for one help-center or product-doc URL, with no skip option, because the agent can only recommend what a source describes. Fetch the page raw (curl or a scrape tool, not a summarizer that could alter or add text). For each feature or offer capture: the name as the doc names it, the product it belongs to as the doc names it, a one-line value, the gap it addresses, entitlement note if the doc says it is paid, and the source URL. Mark anything you cannot extract with confidence as `[verify]`. Say what you found in one line ("4 features from this page"). Set `products` in config to the products the doc names. If it names none, leave `products` unset and say so.

Rules (hard constraints the emails must follow) are not asked in setup. Say once, at the end, that the CSM can add a rule at any time by saying "add a rule".

## 3. Safety and save

Ask once, in the glance format from `SKILL.md` guardrail 13. The progress line comes first, for example `Setup ▰▰▱  Step 3 of 3: Safety · Connect ✓ · Tone and knowledge ✓`. Then one labeled line each:

- **Contact flags:** the contacts that are skipped when choosing recipients. Name the flags in plain words with the field codes in brackets, from the fields the connected `contacts` adapter lists. A missing flag counts as unknown, not a block.
- **Limits:** the caps and suppression defaults in the table below.
- **Sending:** off. Nothing is sent.

Then the action, last and bold: "Save your setup?" Put the same action inside the question text. Options: `Save (Recommended)` and `Change one`. Do not list basis for sending, region, language, or timezone here. Basis and region are asked at the first send (`send.md`), because nothing before a send reads them. Language comes from the tone sample. Timezone and quiet hours are asked at the first send.

| Setting | Proposed value | Where it comes from |
| --- | --- | --- |
| Opt-out source | Any explicit opt-out, unsubscribe, do-not-contact, or bounce flag the contacts source returns blocks the contact. A missing value counts as unknown, not as a block. | The fields the connected `contacts` adapter lists. |
| Language | The language of the tone sample, else English. Saved without asking. | `style.md` |
| Caps | The values under Guardrails in `reference/config-schema.md` | Defaults. Say so. |
| Suppression | Unsubscribed, open support escalation, contacted in the last 7 days | Defaults. Say so. |
| Basis for sending, region, timezone and quiet hours | Not set now | Asked at the first send, see `send.md`. Drafting does not use them. |

If the user picks "Change one", ask which setting (options are the rows, plus Tone and Knowledge), then that one question. Do not walk through the rest.

Write `send_enabled: false`. Never write `true`. Tell the user in one line that sending is turned on only by editing that line in `.nba-agent/config.md` by hand.

On "Save":

- Files available: write `config.md`, `style.md`, `knowledge.md`, and `rules.md` (empty) to `.nba-agent/`.
- No filesystem: create each as an artifact. Tell the user to save them to project knowledge, and that later runs will read them from there or ask for a paste.

Until the user says "Save", nothing is saved. Then show the progress card with all 3 steps done and go to the ready banner.

The Gainsight files in `reference/example-config/gainsight/` show a finished set. Use them as a format example. Never copy them in as a customer's defaults.
