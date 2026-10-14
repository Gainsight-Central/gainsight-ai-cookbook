# Guardrails (1 minute)

**1. Initialization and questions are read-only.** The snapshot script can only run the read commands in its `READ_COMMANDS` allow-list (`scripts/snapshot.py`, top of file). Any other command is refused in code. `report run` is included because it executes a report ad hoc and saves nothing.

**2. Changes go through the write gate, every time.** For anything that creates, changes, deletes, schedules, publishes, or runs something, the AI agent must explain the plan and what else it touches, show the exact command, name the environment (sandbox or production), wait for your explicit yes for that specific change, then read it back and log it in `tenants/<tenant>/changelog.md`. Approving one change does not approve the next.

**3. Real-world effects are called out before they happen.** Running a rule now, publishing or resuming a Journey Orchestrator program, and load-to-object actions can email customers, create CTAs for CSMs, or overwrite data. The AI agent leaves new rules inactive and new programs unpublished unless you ask, and says what will happen before turning anything on.

**4. Sandbox first.** Initialize your sandbox as well as production. They get separate `tenants/` folders. For a production change, the AI agent recommends trying it in sandbox first.

**5. Your data stays with you.** Everything runs on your machine with your CLI login and your AI agent. The local tenant brain lives in this folder. Nothing is sent to Gainsight beyond the CLI's normal API calls. Do not commit `tenants/` to a shared or public repository.

**6. Approved models only.** Use an approved model with your AI agent. Do not use Fable or Mythos-class models with tenant data (data-retention policy).

**7. Permissions.** Reading admin config (rules, scorecards, Journey, data management) needs a **super-admin** CLI login. Writes are also limited by what that user is allowed to do in Gainsight.

**8. Dates in a sandbox can mislead you.** A sandbox refresh resets created and modified dates and deactivates Journey Orchestrator programs. The AI agent judges what is live from signals that do not depend on those dates: active flags, whether a scorecard uses a measure, and names such as DNU, "copy of", or test.

**9. You stay accountable.** The AI agent drafts, checks, and runs commands on your instruction. Review plans the way you would review a teammate's change, especially in production.

**10. The AI agent does not overload the API.** It reads the local tenant brain instead of describing the same object again, it inventories rules in pages, and it stops when a command fails twice with the same arguments or when the API returns HTTP 429. The snapshot script describes two objects at a time and stops when the tenant throttles the calls.
