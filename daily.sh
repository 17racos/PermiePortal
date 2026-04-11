#!/bin/bash
# PermiePortal Daily Automation
# Run manually or add to cron:
#   0 8 * * * /home/dracos/apps/permieportal/daily.sh >> /home/dracos/apps/permieportal/logs/daily.log 2>&1

set -e

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$PROJECT/logs"
mkdir -p "$LOG_DIR"

echo ""
echo "=========================================="
echo "PermiePortal Daily Run — $(date)"
echo "=========================================="

# Check queues have content
PLANT_COUNT=$(grep -c '[^[:space:]]' "$PROJECT/queue_plants.txt" 2>/dev/null || echo 0)
PEST_COUNT=$(grep -c '[^[:space:]]' "$PROJECT/queue_pests.txt" 2>/dev/null || echo 0)

if [ "$PLANT_COUNT" -eq 0 ] && [ "$PEST_COUNT" -eq 0 ]; then
  echo "Both queues empty — nothing to do."
  echo "Add names to queue_plants.txt or queue_pests.txt"
  exit 0
fi

echo "Plants in queue: $PLANT_COUNT"
echo "Pests in queue:  $PEST_COUNT"
echo ""

# Run automation
python3 "$PROJECT/automate.py" --daily

echo ""
echo "Done — $(date)"
echo ""
echo "Next step: open Cursor Agent and paste review/cursor_agent_prompt.md"
