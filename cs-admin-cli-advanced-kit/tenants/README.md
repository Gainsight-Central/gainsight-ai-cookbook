# tenants/

`prompts/initialize.md` creates one folder here per Gainsight tenant. The folder name is the first part of the tenant URL (`https://acme.gainsightcloud.com` becomes `acme/`). Sandbox and production sit side by side.

Each folder is the local tenant brain for that tenant: a copy of the configuration, plus the key definitions the agent uses when it builds something new. Keep these folders on your machine. Do not commit them to a shared or public repository.
