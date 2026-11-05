#!/bin/sh
# Build the NBA plugin zip served from docs/downloads.
# Run from anywhere: sh gainsight-nba/scripts/package-nba.sh
# Runs verify-release.sh first and stops if it fails. The version comes from
# .claude-plugin/plugin.json. Older gainsight-nba-*.zip files are removed.
# scripts/, .gitignore, evals/ and .DS_Store stay out of the zip.
set -eu
PLUGIN=$(cd "$(dirname "$0")/.." && pwd)
OUT="$PLUGIN/../docs/downloads"

sh "$PLUGIN/scripts/verify-release.sh" || { echo "Not building: verify-release.sh failed." >&2; exit 1; }

VERSION=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$PLUGIN/.claude-plugin/plugin.json")
[ -n "$VERSION" ] || { echo "No version in plugin.json." >&2; exit 1; }

mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
TMP="$OUT/.gainsight-nba-build.zip"
rm -f "$TMP"
cd "$PLUGIN"
zip -r -q "$TMP" . -x 'scripts/*' '.gitignore' 'evals/*' '*.DS_Store'

rm -f "$OUT"/gainsight-nba-*.zip
mv "$TMP" "$OUT/gainsight-nba-$VERSION.zip"
echo "Built docs/downloads/gainsight-nba-$VERSION.zip"
