#!/usr/bin/env bash
# Unattended heavy campaign on Soulkiller.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p results/campaign logs
LOG="logs/campaign_$(date +%Y%m%d_%H%M%S).log"
# leave a few cores for interactive use
WORKERS="${WORKERS:-80}"
MC="${MC:-2000}"

echo "Starting campaign workers=$WORKERS mc=$MC log=$LOG"
# no GPU needed; pin to all CPUs, nice it slightly
nohup python -u scripts/05_heavy_campaign.py --workers "$WORKERS" --mc "$MC" \
  >"$LOG" 2>&1 &
echo $! > results/campaign/campaign.pid
echo "PID=$(cat results/campaign/campaign.pid)"
echo "Tail: tail -f $ROOT/$LOG"
echo "Progress: cat $ROOT/results/campaign/progress.json"
