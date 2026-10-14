# tenants/

`prompts/initialize.md` creates one folder here per Gainsight tenant, named after the first part of the tenant URL (`https://acme.gainsightcloud.com` → `acme/`). Sandbox and production sit side by side.

These folders contain an export of your tenant's configuration. Keep them on your machine, and don't commit them to a shared or public repository.
