# Example: Risk process map

> Illustrative example. The structure mirrors a real read-only run, but asset names, counts, and thresholds are synthetic and do not describe any single tenant. Your output will look different.

## What Risk means here

Risk is a mature response taxonomy backed by several detection paths. The tenant detects risk through recent Timeline sentiment, health-score deterioration, and support volume, then creates Risk CTAs or launches recovery and escalation programs.

## Detect → respond

| Detection | Exact evidence | Response |
|---|---|---|
| Recent Timeline sentiment | Active rule `Set Scorecard: Timeline Sentiment` reads Timeline status from the past week | Sets Sentiment Risk to N/A, Green, Yellow, or Red |
| Health deterioration | Active rule `Create Risk CTA on Health Decline` | Creates a Risk CTA assigned to the company CSM with reason Company Risk |
| High support volume | Active rule `High Support Volume` joins support cases to Company | Creates a Risk CTA/playbook and sets support score values |
| Low adoption or red health | Four recovery/escalation-named Journey programs | Digital recovery or support escalation; Journey liveness not proven in the sandbox |

## Response taxonomy

The active Risk CTA type has 9 direct reasons:

`Company Risk`, `Technical Risk`, `Sentiment Risk`, `Executive Alignment Risk`, `Support Risk`, `Adoption Risk`, `Stakeholder Risk`, `Integration Risk`, and `Contract Risk`.

`Usage Decline` and `Low License Utilization` are additional risk-adjacent reasons.

## Footprint

| Asset type | Total candidates | Live or used |
|---|---:|---:|
| Risk/health/support rules | 9 | 8 |
| Risk/health/support measures | 14 | 12 |
| Direct Risk CTA reasons | 9 | 9 |
| Recovery/escalation Journey programs | 4 | Unknown in sandbox |

## Finding worth reviewing

`High Support Volume` creates a Risk CTA with reason `Other`, even though the active `Support Risk` reason exists. An admin should confirm whether this is intentional.

Also review whether the two earlier versions of the support-volume rule and `Support Ticket Threshold` encode distinct thresholds or overlapping automation.
