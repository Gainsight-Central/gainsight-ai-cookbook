# WIP: CS Admin CLI Advanced Kit — start here

> **Work in progress, built in public.** Nothing in this folder is a supported release yet.

This file is the context for an AI agent (or a person) picking up this work with no prior history. Read it fully, then `BACKLOG.md`. Use `VERIFY.md` when asked to review.

## What we're building

A downloadable folder that a Gainsight CS admin opens in Claude Code. Claude then runs the [Gainsight Admin CLI](https://support.gainsight.com/gainsight_nxt/AI_Assistants/Admin_CLI/Configure_Admin_CLI) (`gs-admin`) on the admin's own machine, against their own tenant, to read **and write** configuration.

How it works:
1. **Initialize once.** Claude takes a read-only snapshot of the tenant: every object and field, lookups, picklist values and their IDs, rules, reports, scorecards, Journey programs, and conventions. It also produces **verified report exemplars**: real reports from the tenant translated into CLI commands and proven with an ad-hoc run. Gainsight report JSON is too hard to guess without them.
2. **Then ask.** Questions are answered from the snapshot or with live read commands.
3. **Writes go through a write gate:** plan, blast radius, exact command, an explicit yes for that specific write, read-back, and a changelog entry.

The sibling **[CS Admin CLI Starter Kit](../../cs-admin-cli-starter-kit/)** is already published in this repo. It's read-only and answers "what does my tenant do?". This Advanced Kit is the read-and-write version. Match the Starter Kit's tone, structure and level of detail for admins.

## Folder layout

```
HANDOFF.md   this file (stable context)
BACKLOG.md   where the work stands: audit findings, proposed use cases, next steps (living doc)
VERIFY.md    instructions for a second model reviewing a change
kit/         the product itself: what ships to admins
  CLAUDE.md, README.md, GUARDRAILS.md, prompts/, reference/, scripts/snapshot.py, tenants/README.md
```

> ⚠️ **`kit/CLAUDE.md` is product content, not instructions for you.** It tells Claude to run `gs-admin whoami` at session start and to work on a tenant. That applies when an admin opens `kit/` on their own machine. When editing this repo, treat it as a document you are writing. Do not follow it.

## Constraints you must work within

1. **You have no tenant access.** `gs-admin` logs in through a browser (OAuth PKCE, localhost callback) and the token lasts about an hour. Live runs happen on the maintainer's machine. When something needs real tenant output (verifying an exemplar, capturing an example's result), don't invent it. Write a block like this and continue:
   ```
   LOCAL RUN NEEDED
   Purpose: <what this proves>
   Commands: <exact gs-admin / snapshot.py commands>
   Paste back: <what output to bring back, and what to redact>
   ```
2. **This repo is public.** Never commit tenant data or identifiers: snapshot files, GSIDs, tenant URLs or slugs, customer or company names, real people's names, emails, or real ARR figures. If output comes back from a local run, redact it to illustrative values before committing.
3. **Approved Claude models only**, for building and for verification (see `kit/GUARDRAILS.md` §6).
4. **Don't trust CLI syntax from memory.** `kit/reference/cli-reference.md` is the verified source (gs-admin 1.0.10). If you need a command it doesn't cover, write it as unverified and add a LOCAL RUN NEEDED block to check it.
5. **Reports created during examples are named `CLI - …`** (a maintainer convention, also used as the example convention in the kit).

## Design principles (decided)

- **Readable and prompt-first.** Admins don't install dense external plugins. Everything is plain text they can read, and the only code is `scripts/snapshot.py`, which is read-only by construction (a `READ_COMMANDS` allow-list).
- **Distributed from an official Gainsight source.** Trust and transparency matter more than features.
- **Evidence over inference.** Keep "what we found" (field, rule, command) separate from "what it seems to mean".
- **Safe by default.** New rules are left inactive and Journey programs unpublished. Sandbox comes before production. Real-world effects (emails sent, CTAs created, data overwritten) are called out before they happen.

## How the maintainer works

1. Pick a use case and iterate on it over several turns with the build agent (drafting prompts, examples and docs in `kit/`).
2. Run anything that needs a tenant locally, and bring back redacted output.
3. Ask a **different** model to review it using `VERIFY.md`.
4. Fix what the review finds, update `BACKLOG.md`, and move to the next use case.

Keep `BACKLOG.md` current at the end of every session. It is the only memory the next session has.
