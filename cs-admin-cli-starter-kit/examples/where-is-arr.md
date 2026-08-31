# Example: Where is ARR defined and used?

> Illustrative example. The structure mirrors a real read-only run, but asset names, counts, and thresholds are synthetic and do not describe any single tenant. Your output will look different.

## Short answer

`Company.Arr` is the canonical-looking account-level ARR field. It is a standard, tracked currency field and appears in at least 48 saved reports. The tenant also has renewal-state and relationship-level ARR fields; these look related rather than automatically duplicated.

## Evidence

| Asset | Exact locus | Observed reference | Confidence |
|---|---|---|---|
| Company field | `Arr` — label `ARR`, standard tracked currency | At least 48 saved reports | High |
| Company field | `Contracted_ARR__gc` — custom currency | 3 matching report definitions | High |
| Company field | `Committed_ARR__gc` — custom currency | 5 matching report definitions | High |
| Relationship field | `Arr` — label `ARR`, standard currency | Relationship-level field exists | High |
| Report filter | High-value renewals report | `Company.Arr > 250000` | High |
| Report filter | Customers by stage and ARR | `Company.Arr > 0` | High |

## Interpretation

- `Company.Arr` is the strongest canonical candidate because it is standard, tracked, and widely referenced.
- Contracted ARR appears to mean the amount under current contract.
- Committed ARR appears to mean the amount confirmed for the next term.
- Relationship ARR is at a different entity grain.
- MRR is related but not interchangeable without confirmed conversion logic.

No direct contradiction was proven. Multiple fields alone are not evidence of drift.

## Visible impact

Changing the meaning or population of `Company.Arr` has a visible lower-bound impact of 48 report definitions across renewal, risk, expansion, health, and executive-engagement use cases. Two reports contain exact ARR thresholds that may change behavior if the field changes.

## Unknowns

- The upstream system that populates Company ARR was not proven.
- Saved-report existence does not show dashboard usage or execution frequency.
- Field-filtered dependency lookup was unavailable in the CLI version used for this run.

## Admin checks

1. Confirm which integration writes `Company.Arr` and how often.
2. Confirm the definitions of Contracted ARR and Committed ARR.
3. Check whether Relationship ARR rolls up to Company ARR.
4. Review the two visible report thresholds.
5. Identify which of the 48 saved reports are used in active dashboards.
