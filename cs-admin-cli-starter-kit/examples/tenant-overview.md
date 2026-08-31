# Example: Tenant overview

> Illustrative example. The structure mirrors a real read-only run, but asset names, counts, and thresholds are synthetic and do not describe any single tenant. Your output will look different.

## Short answer

This tenant has all 12 common CS process areas represented. Its strongest configured motions are Risk, Adoption & Usage, and Success Planning. It also has tenant-specific emphasis on multi-product health, value realization, and automated insights.

The tenant is not obviously full of inactive configuration: all 94 process-taxonomy records were active. However, four active rules had test, copy, or migration-style names and need human review before being called live or obsolete.

## Tenant size

| Surface | Count |
|---|---:|
| Reports | 612 |
| Rules | 74 |
| Journey programs | 83 |
| Objects | 418 |
| Scorecards | 11 |
| Scorecard measures | 78 |

## Process spine

| Configuration | Active / total |
|---|---:|
| CTA reasons | 22 / 22 |
| CTA types | 10 / 10 |
| Success Plan types | 7 / 7 |
| Objective categories | 8 / 8 |
| CTA statuses | 5 / 5 |

## What this tenant appears to do

| Process | Tenant evidence | Interpretation |
|---|---|---|
| Risk & Churn | Risk CTA type; 9 direct risk reasons; sentiment, health-drop, and support rules | A mature response taxonomy with several detection paths |
| Adoption & Usage | Adoption CTA; Usage Decline and Low License Utilization reasons; used adoption measures | Adoption is measured and linked to intervention |
| Renewal & Retention | Renewal CTA/reasons; four renewal rules; renewal success plans | A clear renewal preparation motion |
| Voice of Customer | Survey Response reason; NPS/CSAT rules and measures | Survey signals feed the operating model |
| Success Planning | 7 Success Plan types and 8 objective categories | Outcomes, ROI, and account planning are prominent |
| Advocacy | Reference Request CTA and Advocacy reason | Advocacy exists, with lighter rule evidence |

## Tenant-specific extensions

- **Multi-product health:** two product lines are scored separately rather than rolled into a single health score.
- **Value realization:** ROI and business-outcome language appears across Success Plan types and objective categories.
- **Automated insight:** a dedicated CTA type for system-generated insights, plus sentiment and engagement measures, extend the standard model.

## Admin checks

1. Review the four active rules with test/copy/migration-style names. Migration is a legitimate process here, so name matching alone is not enough.
2. Confirm what the opaque CTA type `RB` means.
3. Choose one important process—Risk is a good candidate—and map its exact rules and responses next.
