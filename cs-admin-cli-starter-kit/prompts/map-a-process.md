# Map one CS process end to end

Use this for Risk, Renewal, Onboarding, Adoption, Advocacy, or another process found by Start Here.

Replace `<PROCESS>` before running. [See an example Risk output](../examples/risk-process.md).

```text
Map the "<PROCESS>" process end to end in my Gainsight tenant.

USE THE ADMIN CLI:
- Run the local `gs-admin` executable in the terminal. Do not silently substitute another MCP integration.
- Run `gs-admin whoami` first and verify the tenant URL and valid token.

SAFETY:
- Read-only: whoami, list, describe, query execute, and report schema only.
- Never create, update, edit, publish, run, save, or delete configuration.
- Reuse relevant files under `./intent/` when present.

1. DETECT
Find the fields, scorecard measures, and active rules that identify or measure this process. Describe the
strongest matched rules and capture their exact source, criteria, and actions. A measure is used when
scorecardsCount > 0.

2. RESPOND
Find the active CTA types, reasons, statuses, Success Plan types, playbooks, and Journey programs used to
respond. Query da_picklist with GSID so IDs in rule actions can be translated to human names.

3. EXTEND
Identify tenant-specific behavior beyond the standard CS process. Do not invent meanings for opaque names.

4. CHECK
Look for overlapping automation, unused measures, obvious DNU/test/copy assets, and mismatches between the
configured taxonomy and what rules actually create. Use date-free liveness; sandbox dates and Journey status
are unreliable. Do not treat "mig" as dead because Migration may be a real process.

5. WRITE THE RESULT
Create `./intent/reports/<process>_process.md` with:
- A two- or three-sentence synthesis
- A small Detect → Respond mapping table
- Exact evidence behind the strongest claims
- Tenant-specific extensions
- A compact live/total footprint
- Concrete items for an admin to validate

Keep the main report concise. Separate evidence from interpretation and say plainly when a surface could not
be checked.
```

