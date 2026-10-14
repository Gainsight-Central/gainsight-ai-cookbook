# Change configuration

Use this when you want to add or change a rule, a Journey Orchestrator program, a scorecard, a field, or a dropdown value.

**What you get.** A plan in plain English, the exact commands, and a list of what else the change touches. Nothing is created until you say yes. New rules stay inactive. New programs stay unpublished, unless you ask for them to be turned on.

**How to run.** Describe the change, for example:

- "Add a rule that creates a Risk CTA when health drops to red."
- "Add a Churn Reason Detail text field on Company."
- "Add a Budget cut value to the churn reason dropdown."

You can also paste the box below.

---

```
Help me make this configuration change. Follow CLAUDE.md. Ask me before you change anything in Gainsight.

1. Restate the change in one sentence.
   Look for something that already does this, or nearly does: rules, Journey Orchestrator programs,
   measures, fields, dropdowns, and the key definitions under exemplars/rules/ and exemplars/jo/.
   If a close match exists, tell me before you build a second one.
   Read conventions.md so the name, folder, CTA type, reason, and priority match this tenant.

2. See what else the change touches. Read only.
   - For an object or field: `gs-admin data-management dependencies check --name <Object> --json`.
     Say clearly that this is the object, not the field.
   - Search the rule and report indexes for the field, dropdown, or CTA reason, and describe only the matches that matter.
   - For a rule, list the source fields the rule can use, and confirm the CTA type, reason, priority, and status exist.
   - For a program, read a similar program and the email templates or surveys it would use.

3. Show me the plan before any command that changes Gainsight:
   - What will be created or changed, in plain English.
   - The exact commands, in order. A rule is several steps: create, set the source, add the criteria, add the action, then schedule.
   - Whether this can email a customer, create a CTA, or overwrite data, and when that would start.
   - Whether this is sandbox or production. In production, say if I should try sandbox first.
   - How I would undo it.
   Confirm flags with `gs-admin <command> --help`. Do not guess a flag.

4. Make the change only after I say yes.
   Ask again before any step that sends email, creates CTAs, overwrites data, runs a rule now, or publishes a program.
   Leave rules inactive and programs unpublished unless I explicitly ask you to turn them on.
   For a program, run the read-only validate command before you ask me to publish.

5. Read back what you created and compare it with the plan. Tell me any difference.
   Add a line to tenants/<slug>/changelog.md: when, what, why, the commands, the IDs, and how you checked it.
   Refresh that part of the local tenant brain (`python3 scripts/snapshot.py pull <section>`, then `index`).
```
