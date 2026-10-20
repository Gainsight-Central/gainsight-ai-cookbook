---
schema_version: 2
---
# Config: Fixture Co

## Identity
customer: Fixture Co
products: Fixture App
csm_email: csm@fixture.example
csm_name: Fixture CSM

## Capabilities
identity: file
book: file
contacts: file
goals: none
signal: file
context: none
knowledge: file
mail: none
ledger: file

## Catalog
checked: 2026-10-07
metrics:
  - last_login_days | level: user | timestamp: no | coverage: 8 of 9 signal rows had a value (a blank means never logged in) | source: signal.csv
segments:
  - none found in signal.csv or contacts.csv
not_found: feature-level usage, seat or license counts, renewal date, health band

## File maps
signal: file=signal.csv; account=account; user=user_email; metric=last_login_days; blank_means=never
contacts: file=contacts.csv; user=user_email; name=name; account=account; role=role; opt_out=opted_out; timezone=timezone
book: derived from signal.csv column account

## Compliance
region: US
opt_out_source: contacts.csv column opted_out
allowed_basis: existing customer relationship
language: en
timezone_source: contacts.csv column timezone

## Guardrails
draft_cap_per_run: 25
ground_top_n: 25
frequency_cap: 1 per 14 days
quiet_hours: 08:00-18:00 recipient local time
suppress: opted_out, contacted in last 7 days
send_enabled: false
