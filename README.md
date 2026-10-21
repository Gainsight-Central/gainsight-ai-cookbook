# gainsight-ai-cookbook

Example prompts, agent skills, and Admin CLI kits for putting Gainsight to work in the AI agent of your choice.

The site at <https://gainsight-central.github.io/gainsight-ai-cookbook/> 

| If you are | Start here |
|---|---|
| I manage customers | [Copilot prompts](gainsight-cs-mcp-skills/prompts/). Paste one into Gainsight Copilot. Customer name only. Staircase is used when it is connected. |
| I'm in CS Ops | [Admin CLI starter kit](cs-admin-cli-starter-kit/). Read-only. |

## Contents

| Kit | What it does |
|---|---|
| **[Copilot prompts](gainsight-cs-mcp-skills/prompts/)** | Seventeen prompts a CSM or CS leader pastes into Gainsight Copilot, built from the Agentic and headless use cases. Nothing to install. |
| **[CS Admin CLI Starter Kit](cs-admin-cli-starter-kit/)** | Use the Gainsight Admin CLI with an AI coding agent to understand what your CS tenant is configured to do. Read-only prompts plus an optional skill. |
| **[CS Admin CLI Advanced Kit](cs-admin-cli-advanced-kit/)** | Give an AI agent a local copy of your tenant so later questions do not start over. It can also change configuration, and only after you say yes. |
| **[Agentforce CS Agent](agentforce-cs-agent/)** | A Salesforce Agentforce subagent that answers Customer Success questions from Gainsight data, plus four response templates that keep its answers evidence-backed. |
| **[Gainsight CS MCP Skills](gainsight-cs-mcp-skills/)** | Agent skills for the AI tool you already use: rendered dashboards, weekly call briefs, executive prep notes, and Timeline risk updates. Install individually. |
| **[CSM Adoption Agent](gainsight-nba/)** | A skill for the AI agent you already use. Spots adoption gaps in the book of business, recommends a goal or takes one a CSM defines, and drafts outreach they review and approve. The download is release 0.1.36. |

Kit zips for the site live in [`docs/downloads/`](docs/downloads/). Rebuild them with `scripts/package-kits.sh` after a kit changes.
