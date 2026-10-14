# Backlog: where the work stands

_Last updated: 2026-10-14. Update this file at the end of every session._

## Current goal

Ship the kit with **5–10 everyday use cases that the CLI uniquely solves** (bulk, cross-asset, or repetitive work that is slow or impossible in the UI), each written as a worked example an admin can copy.

## What's proven so far

Tested on a large Gainsight demo tenant (~550 objects, ~9,200 fields, ~850 reports, ~100 rules, ~125 Journey programs):

- **Initialize, phases 0–2 work.** The snapshot pull and index ran, and 15 of 17 report exemplars ran successfully through `report run`.
- **One gated write worked end to end:** plain English → `report run` → `report create` → `describe` and `run-saved` read-back → changelog entry.
- **The CLI facts in `kit/reference/cli-reference.md` were checked live.**

## Known gaps (audit, 2026-10-11)

| # | Gap | Next step |
|---|---|---|
| G1 | Initialize **phases 3–6 never ran**: rule and Journey exemplars, conventions, process inventory, `TENANT.md`, self-test. The README describes their outputs, but they're unproven. | LOCAL RUN NEEDED: finish initialize on a sandbox. |
| G2 | "Verified" exemplar means **the command ran**, not that it reproduces the saved report. Example: a "CTAs due this week" exemplar lost its OR filter and date filter, so it returns all CTAs. | Add a "fidelity" status to exemplars (`exact` / `partial: <what was lost>`), and have `snapshot.py exemplar` set it. |
| G3 | Only **report** syntax is verified. Rule build (`create → set-source → add-criteria → add-action → schedule`), Journey node building, `dropdowns upload-csv` and `objects add-field` are untested. `prompts/change-config.md` is a generic checklist. | Verify each command needed by the chosen use cases, and add it to `cli-reference.md`. |
| G4 | The "What this exemplar teaches" section is still a placeholder in every exemplar. | Make it part of initialize phase 2, or have `snapshot.py` generate a first draft. |
| G5 | **No use-case examples exist.** The README has only a seven-row "then just ask" table. | This is the current goal; see below. |
| G6 | The CLI can't set **relative-date or OR filters** through `report run/create`, and many everyday asks need them ("due this week", "next quarter"). | Each example states the workaround: absolute dates, or finish it in the report builder UI. |
| G7 | Distribution hygiene: the shipped zip must contain no `tenants/<slug>/` data, `.DS_Store` or `__pycache__`. | Add a packaging checklist or script. |

## Proposed use cases: awaiting maintainer selection

| # | Use case | Persona | Mode | Key commands |
|---|---|---|---|---|
| U1 | **"What breaks if I change X?"** Impact of retiring a field or object, or changing a picklist | Admin | Read | `data-management dependencies check`, plus a search of the rules, reports and Journey indexes |
| U2 | **Config-debt audit.** DNU, "copy of" and test assets, inactive rules, measures no scorecard uses, duplicate ARR fields | Admin | Read | snapshot indexes |
| U3 | **Rule failure triage.** Which rules failed recently, and why | Admin | Read | `rules-engine rules executions`, `rules execution` with drilldown |
| U4 | **Connector and data-load watch.** Failed jobs, and who changed connector config | Admin | Read | `connectors activity`, `connectors audit`, `connectors jobs` |
| U5 | **Tenant data dictionary.** "Where does ARR live, and which field is canonical?" Also an onboarding handbook for new admins | Admin, new hire | Read | snapshot, `TENANT.md` |
| U6 | **Plain English → saved reports.** Several `CLI - …` reports in one sitting, each tested before saving | Admin, CS Ops | Write (gated) | `report run`, then `report create` |
| U7 | **Bulk dropdown update from a CSV.** Add or sync many picklist values | Admin | Write (gated) | `data-management dropdowns upload-csv` |
| U8 | **Sandbox ↔ production diff.** Snapshot both, show what differs, replay approved changes | Admin | Read, then gated write | `snapshot.py` on each tenant, then diff |
| U9 | _(optional)_ **Rule from a spec**, e.g. "Risk CTA when health turns red", created inactive in the tenant's conventions | Admin | Write (gated) | `rules-engine rules create … add-action` |

**Proposed example format** (`kit/examples/NN-<slug>.md`):
1. When you'd use this (persona, trigger)
2. What to say to Claude (the prompt)
3. What Claude does (steps and exact commands; read or write called out)
4. Example output (redacted, illustrative values)
5. Why the CLI (what this would take in the UI)
6. Limits and workarounds

## Next steps

1. Maintainer picks the final set from U1–U9.
2. Draft U1 as the template example, review it with `VERIFY.md`, and lock the format.
3. Draft the remaining read-only examples (U2–U5). List the LOCAL RUN NEEDED blocks for real output.
4. Write examples (U6–U8): verify the commands locally on a sandbox first (closes G3 for those commands).
5. Update `kit/README.md`: link the examples and replace the "then just ask" table.
