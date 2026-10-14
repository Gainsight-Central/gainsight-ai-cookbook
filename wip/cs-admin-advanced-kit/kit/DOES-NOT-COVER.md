# What this kit does not do

These are real admin pains. The current CLI cannot close them, so this kit does not claim to.

| Pain | Why it is not in the kit |
|---|---|
| Salesforce fields arrive null, merges orphan companies, user deletions do not propagate | Connector commands show the mapping, the last activity, and the last config edit. They do not repair the row or the Salesforce merge. |
| Journey publish succeeds and nothing sends | `jo p validate` checks a program before publish. It does not explain a stalled audience sync or a deliverability failure. |
| Health scores stay visible while they are unfinished, or swing on small volumes | The kit can list measures and the rules that set them. Hiding a score, changing default weights, and null-reallocation rules are product behavior. |
| License overages, Viewer vs Full, SSO, sandbox super-admin lockout | No user, license, or SSO commands. SSO that blocks the CLI login blocks this kit too. |
| Power BI replaced the report builder; the same filter returns different counts | The kit runs a saved report. It does not make native reports match another tool, and it does not make dashboard, report, and Data Designer agree. |
| X-Org promotion fails | Example 06 diffs two snapshots. It does not promote. |
| Audit logs for security review, IP allowlists, retention | The changelog in `tenants/` records what the agent did on your machine. It is not a SIEM export. |

If a job would need one of these, the agent says so and stops. It does not approximate the answer with a nearby command.
