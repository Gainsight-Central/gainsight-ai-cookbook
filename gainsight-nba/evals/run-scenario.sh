#!/bin/sh
# Manual: runs the data layer of eval 2 through the real agent (file adapter, no CS platform,
# no mail, no context). Costs tokens and needs the claude CLI. Not part of run-tests.sh.
# It stops after the funnel, so it does NOT cover the goal confirm or the sample drafts.
#
# It runs in a temp copy so the committed fixtures never change, and it rewrites the ledger
# row to 4 days ago so the "contacted in last 7 days" skip holds on any date.
# Compare the transcript with evals/fixtures/file-adapter/expected.json and eval 2 in evals.json.
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$(mktemp -d)
cp -R "$HERE/fixtures/file-adapter/." "$WORK/"
python3 -I - "$WORK" <<'PY'
import sys, json, datetime
w = sys.argv[1]
d = (datetime.date.today() - datetime.timedelta(days=4)).isoformat()
rows = [json.loads(l) for l in open(f"{w}/ledger.jsonl") if l.strip()]
for r in rows:
    r["timestamp"] = d + "T10:00:00Z"
open(f"{w}/ledger.jsonl", "w").write("\n".join(json.dumps(r) for r in rows) + "\n")
open(f"{w}/goal.txt", "w").write(
    "Users who never logged in, or have not logged in for more than 30 days. As of "
    + datetime.date.today().isoformat() + ".\n")
PY
cd "$WORK" || exit 1
echo "Working copy: $WORK"
claude --plugin-dir "$HERE/.." -p "Start the NBA agent. Goal: $(cat goal.txt) Stop after the funnel and the how-these-numbers-were-arrived-at note." < /dev/null
