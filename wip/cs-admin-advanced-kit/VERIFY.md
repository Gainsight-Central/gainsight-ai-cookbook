# Verify a change (for a second model)

You are reviewing work another model did on the CS Admin CLI Advanced Kit. Read `HANDOFF.md` first. Your job is to find problems, not to rewrite. Don't edit files unless asked.

Review what you are pointed at (a file, a diff, or an example) against these checks:

1. **Correctness of CLI usage.** Every `gs-admin` command, flag and JSON shape matches `kit/reference/cli-reference.md`, or is clearly marked unverified with a LOCAL RUN NEEDED block. Watch for the known traps:
   - picklist filters use labels instead of GSIDs
   - relative-date or OR filters passed to `report run/create`
   - `"summarize"` not in title case
   - data-management object names used in report commands instead of BI names
   - `query execute` used with a filter
2. **Safety.** Every write goes through the write gate in `kit/CLAUDE.md`: plan, blast radius, environment, exact command, an explicit yes, read-back and changelog. Real-world effects (emails, CTAs, data overwrites) are named before they happen. Nothing is turned on (rule scheduled, program published) without an explicit ask.
3. **Is it really unique to the CLI?** The example shows something the UI can't do, or does far more slowly. If an admin could do it in two clicks in the UI, say so.
4. **Honest output.** The example output is either real (redacted) or clearly labeled illustrative. No invented results presented as real. Limits and workarounds are stated.
5. **Public-repo hygiene.** No tenant URLs or slugs, GSIDs, customer or company names, real people's names, emails or real figures.
6. **Readability for admins.** A CS admin who isn't a developer can follow it. It's short, the steps are in order, and it doesn't assume knowledge of the snapshot internals.
7. **Consistency.** It matches the kit's existing prompts, file names and conventions (`CLI - …` report names), and `BACKLOG.md` reflects the change.

Report findings as a list, most severe first. For each one, give the file and line, the problem, a concrete failure scenario, and a suggested fix. End with one verdict line: **ready**, **ready with minor fixes**, or **needs another pass**.
