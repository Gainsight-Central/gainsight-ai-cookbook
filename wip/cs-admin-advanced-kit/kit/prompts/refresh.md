# Refresh the local tenant brain

**What you get.** An updated copy of the configuration on your machine, plus a short list of what changed since the last copy. This step only reads. It does not change Gainsight.

**How to run.** Say **"Refresh my tenant brain."** You can name a part, for example **"Refresh reports and rules."** You can also paste the box below.

---

```
Refresh my local tenant brain. Read only. Follow CLAUDE.md.

1. Run `gs-admin whoami` and confirm it is the same tenant as tenants/<slug>/.
   Run `python3 scripts/snapshot.py status` and show me when each part was last read.

2. Copy the current indexes to tenants/<slug>/.previous/ so you can compare them.
   Replace any older copy. Then refresh what I asked for.
   If I did not name a part, refresh anything older than 14 days:
   `python3 scripts/snapshot.py pull <sections>` then `python3 scripts/snapshot.py index`.
   Parts: objects, bi, picklists, rules, rule-details, reports, scorecards, journey, integrations.

3. Compare the new indexes with .previous/. Do not read the files whole.
   Tell me what changed: objects or fields added or removed, rules added, removed, or turned on or off,
   new reports, and dropdown values added or removed.

4. Check the key definitions for reports. The files are under exemplars/reports/.
   Run `python3 scripts/snapshot.py exemplar` with every report id in exemplars/reports/_index.tsv.
   Tell me which ones no longer run. A field may have been renamed or removed.
   Call them key definitions when you talk to me.

5. Update TENANT.md (counts, the date, and the main fields if they changed) and conventions.md
   if a new naming pattern showed up. Do not add a changelog line. The changelog is only for changes
   made in Gainsight.
```
