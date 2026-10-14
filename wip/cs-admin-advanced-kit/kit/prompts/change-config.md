# Change configuration (rules, Journey, scorecards, objects/fields, dropdowns)

**What this does:** plans a configuration change against your real tenant, checks what it touches, drafts it in your tenant's conventions, and makes the change only after you approve each write.

**How to run:** describe the change, for example *"Add a rule that creates a Risk CTA when health drops to red,"* *"Add a Churn Reason Detail text field to Company,"* or *"Add a value Budget cut to the churn reason dropdown."* The AI agent follows the steps below. You can also paste the box.

---

```
Help me make this configuration change. Follow CLAUDE.md, including the WRITE GATE.

1. UNDERSTAND + FIND PRIOR ART
   - Restate the change in one line.
   - Look for something similar that already exists (config/rules.tsv, config/jo_programs.tsv,
     config/measures.tsv, schema/_field_index.tsv, config/dropdowns.tsv, exemplars/rules/, exemplars/jo/).
     If something already does this (or nearly), tell me before building a duplicate.
   - Read conventions.md so names, folders, CTA types/reasons, priorities and playbooks match.

2. CHECK WHAT IT TOUCHES (read-only)
   - Object/field changes: `gs-admin data-management dependencies check --name <Object> --json`.
   - Changes to a field, picklist or CTA reason that others use: grep rules.tsv / reports.tsv and describe
     the hits that matter.
   - Rules: `rules-engine rules list-task-outputs --rule-id <id>` for available source fields.
     Check that the CTA type, reason, priority and status values exist (`journey cta options --json`).
   - Journey: describe a similar program, and `journey email templates` / `journey surveys list` for assets.

3. DRAFT THE PLAN. Present:
   - what will be created or changed, in plain English
   - the exact gs-admin commands, in order (multi-step builds, e.g. a rule: create → set-source →
     add-criteria → add-action → schedule)
   - real-world effects (emails sent, CTAs created for CSMs, data overwritten) and when they would start
   - environment (sandbox/production) and, if production, whether to try sandbox first
   - how to roll back (what to delete, deactivate, or revert)
   Use `gs-admin <command> --help` to confirm flags. Don't guess them.

4. EXECUTE STEP BY STEP, ONLY WITH MY YES
   - Get approval for the plan, then confirm before each step that has real-world effects (schedule,
     run-now, publish, resume).
   - Leave rules inactive/unscheduled and Journey programs unpublished unless I explicitly ask to turn them on.
   - For Journey programs, run `journey programs validate --id` (read-only) before asking to publish.

5. VERIFY + RECORD
   - Describe what you created or changed and compare it with the plan. Report any differences.
   - For rules, offer `rules-engine rules debug` / a test run only if I want it, and say first what it would do.
   - Append to tenants/<slug>/changelog.md (time, what/why, commands, IDs, verification).
   - Refresh the affected snapshot section (`python3 scripts/snapshot.py pull <section> && … index`).
```
