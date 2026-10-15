#!/bin/sh
# Rebuild the kit zips served from docs/downloads.
set -eu
cd "$(dirname "$0")/.."
mkdir -p docs/downloads
for kit in cs-admin-cli-starter-kit cs-admin-cli-advanced-kit agentforce-cs-agent gainsight-cs-mcp-skills; do
  rm -f "docs/downloads/${kit}.zip"
  zip -r -q "docs/downloads/${kit}.zip" "$kit" -x '*.DS_Store'
done
