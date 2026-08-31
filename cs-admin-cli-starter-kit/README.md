# Gainsight CS Admin CLI Starter Kit

> Part of the [Gainsight AI Cookbook](../). Sample code — not a supported product.

Use the Gainsight Admin CLI with an AI coding agent to understand what your tenant is configured to do.

This is a starting point—not a complete tenant audit. Every Gainsight instance reflects different business processes, naming conventions, and years of configuration. Start with the tenant overview prompt, see what it finds, and then ask the questions that matter in your environment.

## What you can learn

- Which Customer Success processes are configured in your tenant
- Where a concept such as ARR, Risk, Health, or Segment is defined and used
- How one process works from detection through response
- Which configuration looks active, duplicated, unclear, or worth reviewing

The prompts are read-only. They ask your agent to inspect configuration and save understandable reports locally. They do not create, edit, publish, run, or delete tenant configuration.

## Start here

1. [Install and connect the Gainsight Admin CLI](https://support.gainsight.com/gainsight_nxt/AI_Assistants/Admin_CLI/Configure_Admin_CLI).
2. Open an empty working folder in an AI coding agent that can run terminal commands.
3. Copy and run [`prompts/00-start-here.md`](prompts/00-start-here.md).
4. Review the commands as the agent runs them and read the reports it creates under `./intent/`.

The starter prompt explicitly tells the agent to use the local `gs-admin` command. It also creates durable instructions in your working folder so a future agent knows how to answer requests such as “list all rules in my tenant.”

## What a run costs

A full tenant-overview run reads roughly 100K tokens of configuration — typically **under $2** of API usage. If you are using Claude or ChatGPT on a subscription, there is no extra charge at all.

That number is deliberate, not lucky: the prompt reads record *counts* without downloading every record, so sizing your tenant costs almost nothing. Very large tenants read more, because listing thousands of rules or reports means paging through them.

## Choose your next question

| I want to… | Prompt | Example output |
|---|---|---|
| See what my tenant is configured to do | [`00-start-here.md`](prompts/00-start-here.md) | [`tenant-overview.md`](examples/tenant-overview.md) |
| Find where ARR, Risk, Health, Segment, or another concept lives | [`where-is.md`](prompts/where-is.md) | [`where-is-arr.md`](examples/where-is-arr.md) |
| Understand one process end to end | [`map-a-process.md`](prompts/map-a-process.md) | [`risk-process.md`](examples/risk-process.md) |

The examples are illustrative. They mirror the shape of a real read-only run, but asset names, counts, and thresholds are synthetic and do not describe any single tenant. Your output will be different—and that is the point.

## Prompts first, skill when you are ready

We recommend starting with the prompts. They are short enough to read, show the method, and let you see exactly what the agent is being asked to do.

If you trust the workflow and want the agent to choose the right path automatically, use the optional [`map-gainsight-tenant` skill](skills/map-gainsight-tenant/SKILL.md). It follows the same read-only method; it does not unlock a more privileged mode.

To install, copy the complete `map-gainsight-tenant` folder into your client's skills directory:

- **Claude Code** — copy to `.claude/skills/` in your working folder, then run `/map-gainsight-tenant`. The agent may also pick it up automatically from the skill description.
- **Other clients that read `SKILL.md`** — check your client's documentation for its skills directory and invocation syntax.

The prompts require no skill installation.

## A few important limits

- Configuration proves that something exists; it does not always prove that people still use it.
- Sandbox dates and Journey program status can be misleading after a refresh.
- Similar names are clues, not proof that two fields or rules mean the same thing.
- Generated files may contain sensitive tenant configuration. Treat them as confidential and do not share them outside your organization. Add `intent/` to the `.gitignore` of whatever folder you run this in, so local tenant snapshots are never committed.

Read [`SAFETY.md`](SAFETY.md) for the complete safety boundary.

## What's in this kit

```text
prompts/    readable prompts to copy and run
examples/   illustrative sample outputs
skills/     optional reusable automation
SAFETY.md   read-only boundary and data handling
```

## Feedback

Open an issue in this repository. This is sample code intended as a starting point, not a supported Gainsight product — for help with the Admin CLI itself, use [Gainsight Support](https://support.gainsight.com/).
