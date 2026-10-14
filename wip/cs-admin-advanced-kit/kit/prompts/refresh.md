# Refresh the snapshot

**What this does:** re-pulls the parts of your tenant snapshot that are out of date and updates TENANT.md. Read-only.

**How to run:** say *"refresh my tenant snapshot"* (or name a section, e.g. *"refresh reports and rules"*), or paste the box.

---

```
Refresh my tenant snapshot. Read-only. Follow CLAUDE.md.

1. `gs-admin whoami` → confirm the tenant matches tenants/<slug>/. Run `python3 scripts/snapshot.py status` and
   show me each section's pulled_at age.
2. Before pulling, copy the current indexes so you can diff them: copy `config/` and `schema/_*.tsv` into
   `tenants/<slug>/.previous/` (replace any older copy).
   Then refresh what I asked for, or by default anything older than 14 days:
   `python3 scripts/snapshot.py pull <sections…>` then `python3 scripts/snapshot.py index`.
   Sections: objects, bi, picklists, rules, reports, scorecards, journey, integrations.
3. Diff the new indexes against `.previous/` (with a small python script, not by reading whole files). Tell me what changed: new/removed objects and fields, rules added, removed or
   activated/deactivated, new reports, picklist values added/removed.
4. Re-verify existing report exemplars: `python3 scripts/snapshot.py exemplar <all ids in exemplars/reports/_index.tsv>`.
   Report any that now fail (a field may have been renamed or removed).
5. Update TENANT.md (counts, snapshot date, core concepts if they changed) and conventions.md if new patterns
   appeared. Don't add to changelog.md (that file is for writes only).
```
