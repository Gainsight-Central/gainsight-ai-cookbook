#!/bin/sh
# Pre-release check. Run from anywhere: sh scripts/verify-release.sh
# Exit 1 if anything blocks a release. Warnings do not block.
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT" || exit 1
FAIL=0
block() { echo "BLOCK $1"; FAIL=1; }
warn()  { echo "WARN  $1"; }
ok()    { echo "ok    $1"; }

# 1. Open placeholders (code and docs, not this script)
HITS=$(grep -rn '\[NEED' . --exclude-dir=.git --exclude=verify-release.sh | grep -v 'evals/evals.json')
if [ -n "$HITS" ]; then block "open [NEED] placeholders:"; echo "$HITS" | sed 's/^/        /'; else ok "no [NEED] placeholders"; fi

# 1b. Customer and contact names must not ship
NM=$(grep -rniE 'accruent|cristiana|fabiani|orbus|\bABB\b|workiva|teamworks|@gainsight\.com' . --exclude-dir=.git --exclude=verify-release.sh)
if [ -n "$NM" ]; then block "customer or contact names found:"; echo "$NM" | sed 's/^/        /'; else ok "no customer names"; fi

# 2. Placeholder hosts in the MCP config
if grep -q '\.invalid' .mcp.json 2>/dev/null; then block ".mcp.json still has .invalid placeholder URLs"; else ok ".mcp.json has no placeholder hosts"; fi

# 3. Em dashes
ED=$(grep -rn '—' . --exclude-dir=.git --exclude=verify-release.sh)
if [ -n "$ED" ]; then block "em dashes found:"; echo "$ED" | sed 's/^/        /'; else ok "no em dashes"; fi

# 4. Removed dependencies must not come back
PX=$(grep -rniE '\bpx\b|px_' . --exclude-dir=.git --exclude=verify-release.sh | grep -v 'Day_Active_Users_via_PX__gc')
if [ -n "$PX" ]; then block "PX references found:"; echo "$PX" | sed 's/^/        /'; else ok "no PX references"; fi

# 5. Tool names belong in adapters and example config only
TN=$(grep -rnE 'resolve_user|fetch_customer_contacts|ask_scorecard|staircase_(account|analyze|fetch|list|semantic|query|run|get|generate|report)[a-z_]*|run_query|fetch_success_plan' . --exclude-dir=.git --exclude-dir=adapters --exclude-dir=example-config --exclude=verify-release.sh)
if [ -n "$TN" ]; then block "tool names outside adapters/ and example-config/:"; echo "$TN" | sed 's/^/        /'; else ok "tool names stay in adapters/"; fi

# 5b. Shared files stay mail-vendor neutral (Gmail belongs in its adapter, example config, send.md, and the README)
GM=$(grep -rn 'Gmail' skills commands --exclude-dir=adapters --exclude-dir=example-config --exclude=send.md)
if [ -n "$GM" ]; then block "Gmail named outside adapters/, example-config/, and send.md:"; echo "$GM" | sed 's/^/        /'; else ok "mail wording stays vendor neutral"; fi

# 6. Config schema in the example
grep -q '^schema_version:' skills/nba-agent/reference/example-config/gainsight/config.md && ok "example config has schema_version" || block "example config missing schema_version"

# 7. JSON validity
for F in .claude-plugin/plugin.json .claude-plugin/marketplace.json .mcp.json hooks/hooks.json evals/evals.json; do
  python3 -c "import json;json.load(open('$F'))" 2>/dev/null && ok "valid JSON $F" || block "invalid JSON $F"
done

# 8. Hook is executable and tests pass
[ -x hooks/send-guard.sh ] && ok "send-guard.sh is executable" || block "send-guard.sh is not executable"
sh evals/run-tests.sh >/dev/null 2>&1 && ok "hook tests pass" || block "hook tests fail (run: sh evals/run-tests.sh)"

# 9. Plugin validator, if the CLI exists
if command -v claude >/dev/null 2>&1; then
  claude plugin validate . >/dev/null 2>&1 && ok "claude plugin validate passes" || block "claude plugin validate fails"
else
  warn "claude CLI not found, skipped plugin validate"
fi

[ $FAIL -eq 0 ] && echo "RELEASE OK" || echo "RELEASE BLOCKED"
exit $FAIL
