#!/bin/sh
# Runs every evals/test-*.sh. New suites need no wiring: name them test-<thing>.sh.
HERE=$(cd "$(dirname "$0")" && pwd)
FAIL=0
for T in "$HERE"/test-*.sh; do
  echo "== $(basename "$T")"
  sh "$T" || FAIL=1
done
[ $FAIL -eq 0 ] && echo "ALL PASS" || echo "FAILURES"
exit $FAIL
