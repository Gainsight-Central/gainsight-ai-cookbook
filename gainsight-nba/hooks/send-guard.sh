#!/bin/sh
# Send guard for the gainsight-nba plugin. Runs before Gmail send_message, reply, and forward.
#
# Scope: only projects that use the agent (a .nba-agent/ directory exists). Elsewhere it allows.
# In an agent project it allows the call when:
#   - send_enabled is true in .nba-agent/config.md, or
#   - every email address in the call is the CSM's own address (the test-send).
# Everything else is denied. It reads the tool input as raw JSON, so it does not
# depend on the connector's parameter names. A call with no address in it
# (for example send_message with only a draftId) is denied while send_enabled is false.
#
# Fail-open rule: the guard gates only what it can identify as an agent project
# send. No .nba-agent/ directory means it is not an agent project, so it allows.
# Once the directory exists, anything it cannot resolve (missing config, missing
# csm_email, no recipient) is denied. Fail open outside the project, fail closed inside.
#
# Every denial starts with [gainsight-nba send-guard] so a user can tell this guard
# from Claude Code's own permission prompts.
#
# What this enforces: the flag and CSM-only test-sends. It does not enforce caps,
# quiet hours, or suppression. Those are instructions in the skill.

DIR="${CLAUDE_PROJECT_DIR:-.}/.nba-agent"
CONFIG="$DIR/config.md"
INPUT=$(cat)

deny() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$1"
  exit 0
}

# Not an agent project: leave Gmail alone.
[ -d "$DIR" ] || exit 0

[ -f "$CONFIG" ] || deny "[gainsight-nba send-guard] .nba-agent/ exists but config.md is missing. Run setup first. Sends are blocked."

SEND_ENABLED=$(grep -E '^send_enabled:' "$CONFIG" | head -1 | sed 's/^send_enabled:[[:space:]]*//' | tr -d '[:space:]' | tr 'A-Z' 'a-z')
[ "$SEND_ENABLED" = "true" ] && exit 0

CSM_EMAIL=$(grep -E '^csm_email:' "$CONFIG" | head -1 | sed 's/^csm_email:[[:space:]]*//' | tr -d '[:space:]' | tr 'A-Z' 'a-z')
[ -n "$CSM_EMAIL" ] || deny "[gainsight-nba send-guard] csm_email is not set in config. Sends are blocked."

ADDRS=$(printf '%s' "$INPUT" | grep -Eo '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' | tr 'A-Z' 'a-z' | sort -u)
[ -n "$ADDRS" ] || deny "[gainsight-nba send-guard] send_enabled is false and the call names no recipient. Blocked. A test-send must pass the CSM address in to."

for A in $ADDRS; do
  [ "$A" = "$CSM_EMAIL" ] || deny "[gainsight-nba send-guard] send_enabled is false, so only test-sends to $CSM_EMAIL are allowed. Blocked a send to $A."
done

exit 0
