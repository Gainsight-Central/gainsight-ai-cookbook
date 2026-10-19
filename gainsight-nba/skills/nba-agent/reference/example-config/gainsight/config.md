---
schema_version: 2
---
# Config: Gainsight (example)

## Identity
customer: Gainsight
products: Gainsight CS
csm_email: csm@example.com
csm_name: Example CSM

## Capabilities
identity: gainsight-cs
book: gainsight-cs
contacts: gainsight-cs
goals: gainsight-cs
signal: gainsight-cs
context: staircase
knowledge: file
mail: gmail
ledger: file

## Servers
identity_server: <server name, only if more than one Gainsight CS server is connected>
signal_server: <server name, same rule>

## Catalog
checked: <date of the probe>
metrics:
  - <metric name as the source names it> | level: <user | account> | timestamp: <yes | no> | coverage: <n of m sampled accounts had a value> | source: <where it came from>
segments:
  - <field name> | object: <account | contact> | values: <value (count), ...>
not_found: <what the probe did not find>

## Compliance
region: US
opt_out_source: contacts capability, unsubscribed or do-not-contact flag
allowed_basis: existing customer relationship
language: en
timezone_source: <contact or account field, or one fixed timezone>

## Guardrails
draft_cap_per_run: 25
ground_top_n: 25
frequency_cap: 1 per 14 days
quiet_hours: 08:00-18:00 recipient local time
suppress: unsubscribed, open support escalation, contacted in last 7 days
send_enabled: false

## Tenant notes (Gainsight production, found 2026-10-07)

The `company` object holds account-level usage fields that worked as a signal: `Day_Active_Users_via_PX__gc` (30 Day Active Users via PX), `Provisioned_Licenses__gc` (Purchased Licenses), and `Assigned_Licenses__gc` (Assigned Licenses). One `run_query` returned all accounts in a CSM's book. Other tenants use their own fields. Nine of thirty accounts had no value, and the fields carry no timestamp.
