---
description: Show NBA agent status. Surface, config version, capability map, connected tools, send guard. Read-only.
---

Report the NBA agent's current state. Read only. Do not run the loop, do not create or edit any file, do not call any mail tool.

Gather these in order. Do not retry a failed check a different way to make it pass. Report what you found.

1. **Surface.** Can you read and write files? Is the `show_widget` tool available? Is this skill loaded from the plugin install (the skill's folder path contains `/plugins/`) or from a copied folder?
2. **Config.** Look for `.nba-agent/config.md`, `style.md`, `knowledge.md`, `rules.md`. For each: present or missing. If `config.md` exists, read `schema_version` and compare it with `reference/config-schema.md` in the skill (current is the last row of its Versioning table).
3. **Capability map.** For each of the nine capabilities in `reference/capabilities.md`: the adapter or file it maps to in `config.md`, whether it is required or optional, and the connected tool that matches the adapter (match by tool-name suffix, as in `reference/adapters/`). Mark each `ready`, `blocked` (required and no matching tool), `degraded` (optional and none), or `ambiguous` (more than one matching server and no `<capability>_server` saved).
4. **Send.** `send_enabled` as written in config (read it, do not change it). Whether the send guard counts as active: plugin install path, a mail adapter the guard covers, hooks run. State what Approve & send would do right now: available, off by flag, or off because no guard.
5. **Use cases.** The folders under `reference/use-cases/` and their versions.

Output one compact table per section, then a final line: `Ready to run`, or the list of blockers with the one action that clears each. Sentence case. No em dashes.
