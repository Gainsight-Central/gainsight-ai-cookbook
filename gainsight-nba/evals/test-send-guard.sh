#!/bin/sh
# Scripted tests for hooks/send-guard.sh. Run from anywhere: sh evals/test-send-guard.sh
HERE=$(cd "$(dirname "$0")" && pwd)
GUARD="$HERE/../hooks/send-guard.sh"
TMP=$(mktemp -d)
mkdir -p "$TMP/.nba-agent"
export CLAUDE_PROJECT_DIR="$TMP"
FAIL=0

run() { printf '%s' "$1" | sh "$GUARD"; }
expect_deny()  { OUT=$(run "$2"); case "$OUT" in *'"deny"'*) echo "PASS $1";; *) echo "FAIL $1: $OUT"; FAIL=1;; esac; }
expect_allow() { OUT=$(run "$2"); [ -z "$OUT" ] && echo "PASS $1" || { echo "FAIL $1: $OUT"; FAIL=1; }; }

# Not an agent project (no .nba-agent dir): guard stays out of the way
rmdir "$TMP/.nba-agent"
expect_allow "non-agent project allowed"   '{"to":"a@b.com"}'
mkdir -p "$TMP/.nba-agent"

# Agent project, no config
expect_deny  "dir without config blocks"   '{"to":"a@b.com"}'

printf 'csm_email: csm@corp.com\nsend_enabled: false\n' > "$TMP/.nba-agent/config.md"
expect_allow "test-send to CSM allowed"    '{"to":"CSM@corp.com","subject":"[TEST] hi"}'
expect_deny  "send to customer blocked"    '{"to":"user@customer.com","subject":"hi"}'
expect_deny  "mixed recipients blocked"    '{"to":"csm@corp.com","cc":"user@customer.com"}'
expect_deny  "no recipient blocked"        '{"subject":"hi"}'
expect_deny  "draftId-only send blocked"   '{"draftId":"r-123"}'
expect_deny  "reply to customer blocked"   '{"messageId":"m1","to":["user@customer.com"]}'
expect_deny  "forward to customer blocked" '{"messageId":"m1","to":["user@customer.com"]}'

# Matcher covers all three sending tools and skips the rest
for T in mcp__claude_ai_Gmail__send_message mcp__claude_ai_Gmail__reply mcp__claude_ai_Gmail__forward; do
  printf '%s' "$T" | grep -Eq 'mcp__.*[Gg]mail.*__(send_message|reply|forward)' && echo "PASS matcher hits $T" || { echo "FAIL matcher misses $T"; FAIL=1; }
done
for T in mcp__claude_ai_Gmail__create_draft mcp__claude_ai_Gmail__search_threads; do
  printf '%s' "$T" | grep -Eq 'mcp__.*[Gg]mail.*__(send_message|reply|forward)' && { echo "FAIL matcher hits $T"; FAIL=1; } || echo "PASS matcher skips $T"
done

printf 'csm_email: csm@corp.com\nsend_enabled: true\n' > "$TMP/.nba-agent/config.md"
expect_allow "send allowed when enabled"   '{"to":"user@customer.com"}'

printf 'send_enabled: false\n' > "$TMP/.nba-agent/config.md"
expect_deny  "missing csm_email blocked"   '{"to":"csm@corp.com"}'

# Regression cases
printf 'csm_email: Csm@Corp.com\nsend_enabled: FALSE\n' > "$TMP/.nba-agent/config.md"
expect_allow "mixed-case config and address"  '{"to":["csm@corp.com"]}'
printf 'csm_email: csm@corp.com\nsend_enabled: false\n' > "$TMP/.nba-agent/config.md"
expect_deny  "address only in body blocked"   '{"to":["csm@corp.com"],"body":"cc me at other@customer.com"}'
OUT=$(run '{"to":"user@customer.com"}'); case "$OUT" in *"[gainsight-nba send-guard]"*) echo "PASS denial carries prefix";; *) echo "FAIL prefix: $OUT"; FAIL=1;; esac

rm -rf "$TMP"
exit $FAIL
