# Adapter: file

Maps any capability to a local or uploaded file (CSV, JSON, markdown). Use it for a customer whose adoption data, contacts, goals, or knowledge sit in a file load.

| Capability | How |
| --- | --- |
| `knowledge` | `.nba-agent/knowledge.md` |
| `ledger` | `.nba-agent/ledger.jsonl`, one JSON row per drafted, sent, or edited email. Append only. |
| `signal`, `book`, `contacts`, `goals` | A file the user names in `config.md`, with a column map in the `## File maps` section of `config.md` (format below). Ask for the column map once during setup. |

## Column map format

Put a `## File maps` section in `config.md`, one line per capability that uses a file:

```
## File maps
signal: file=signal.csv; account=account; user=user_email; metric=last_login_days; blank_means=never
contacts: file=contacts.csv; user=user_email; name=name; account=account; role=role; opt_out=opted_out; timezone=timezone
book: derived from signal.csv column account
```

Paths are relative to the working directory. Ask for any missing mapping once during setup and save it.

## Scope fields

A renewal window or a health band scope is offered only when the `signal` or `book` column map names the column, for example `renewal_date=renewal` or `health=health_band`. Without the key, those scopes are not offered.

## Catalog probe

For a `signal` file, the catalog `metrics` are the columns the column map names as metrics, with a level of `user` or `account` from the map. A timestamp is `yes` only if the file carries a date column or the file has a modified date you stated in the funnel note. `segments` are the columns the CSM names as grouping fields, with the values and counts read from the file. Rebuild the catalog whenever the CSM loads a new file.

## Rules

- Read the file as given. Do not fix or fill columns.
- Say the file's date or modified time in the funnel note, so the CSM knows how old the signal is.
- Ledger rows are never edited or deleted by the agent.
- A row is written only when the CSM acts: at the batch step (create drafts or copyable list), on reject, on edit then save, on send, or on test send. Showing or approving a draft writes no row. Status meanings: `drafted` (a mail draft was created), `shown` (the CSM approved and `mail` is `none`, so the text was given to copy), `sent`, `test_sent`, `rejected`.
- Ledger row fields: `run_id`, `timestamp`, `use_case`, `account`, `recipient`, `subject`, `status` (`drafted`, `shown`, `sent`, `test_sent`, `rejected`), `edited`, `accepted_unedited`, `approved_in_bulk`, `draft_id`.
