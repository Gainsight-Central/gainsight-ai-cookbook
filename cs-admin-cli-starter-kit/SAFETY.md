# Safety

## Read-only by default

The prompts and skill in this kit use discovery commands such as `whoami`, `list`, `describe`, `query execute`, and `report schema`. `query execute` is used only with an explicit `--select` field list to read records.

They never ask the agent to create, update, edit, publish, run, save, or delete configuration. The Admin CLI itself may support write operations; this starter kit does not use them.

## Check the tenant first

Every workflow begins with `gs-admin whoami`. Confirm the tenant URL and the `Token:` line before continuing. If either is wrong, stop and correct the login rather than querying another tenant.

Ignore the `Auth mode:` line. It reads `not configured — run 'gs-admin login'` even when the token is perfectly valid, so it looks like a failure and is not one. Only the `Token:` line tells you whether the session works.

## Use the local CLI

The prompts require the locally installed `gs-admin` executable in the terminal. They tell the agent not to silently substitute another Gainsight MCP integration, which may expose a different capability set.

## Protect local output

Tenant configuration may reveal internal processes, object names, fields, rules, and business logic. Review generated files before sharing them.

The agent writes output to `intent/` inside whatever folder you run it in — which is your folder, not this repository. Add `intent/` to that folder's `.gitignore` yourself so local tenant snapshots are never committed. The `.gitignore` shipped here only protects this kit's own directory.

## Review the result

AI-generated interpretation is advisory. The reports distinguish observed configuration from interpretation and include items for an admin to validate in the Gainsight application.

