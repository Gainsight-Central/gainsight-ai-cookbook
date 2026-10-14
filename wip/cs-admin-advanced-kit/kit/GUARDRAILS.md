# Guardrails (1 minute)

**1. Initialization and questions are read-only.** The snapshot script can only run the read commands in its `READ_COMMANDS` allow-list (`scripts/snapshot.py`, top of file). Any other command is refused in code. `report run` is included because it executes a report ad hoc and saves nothing.

**2. Writes go through the write gate, every time.** For anything that creates, changes, deletes, schedules, publishes or runs something, Claude must: explain the plan and blast radius, show the exact command, name the environment (sandbox or production), wait for your explicit yes **for that specific write**, then verify by reading it back and log it in `tenants/<tenant>/changelog.md`. Approving one write doesn't approve the next.

**3. Real-world effects are called out before they happen.** Running a rule now, publishing or resuming a Journey program, and load-to-object actions can email customers, create CTAs for CSMs, or overwrite data. Claude leaves new rules inactive and new programs unpublished unless you ask, and says what will happen before turning anything on.

**4. Sandbox first.** Initialize your sandbox as well as production. They get separate `tenants/` folders. For production writes, Claude recommends trying the change in sandbox first.

**5. Your data stays with you.** Everything runs on your machine with your CLI login and your Claude session. The snapshot lives in this folder. Nothing is sent to Gainsight beyond the CLI's normal API calls. Don't commit `tenants/` to a shared or public repository.

**6. Approved models only.** Use an approved Claude model. Don't use Fable / Mythos-class models with tenant data (data-retention policy).

**7. Permissions.** Reading admin config (rules, scorecards, Journey, data management) needs a **super-admin** CLI login. Writes are also limited by what that user is allowed to do in Gainsight.

**8. Dates lie in sandboxes.** A sandbox refresh resets created/modified dates and deactivates Journey programs. Claude judges live vs. legacy from date-free signals: active flags, whether a scorecard uses a measure, and names like DNU / "copy of" / test.

**9. You stay accountable.** Claude drafts, checks and executes on your instruction. Review plans the way you'd review a teammate's change, especially in production.

**10. The agent does not hammer the API.** It reads the snapshot instead of describing the same object again, it inventories rules in one call, and it stops when a command fails twice with the same arguments or when the API returns 429. The snapshot script describes two objects at a time and stops the pull on a throttle.
