#!/bin/bash
# PermiePortal Data Sync
# Lives at: ~/apps/permieportal/sync.sh
#
# Usage:
#   ./sync.sh           — rebuild everything, update src/data/
#   ./sync.sh --check   — validate only, see warnings without changing anything

set -e

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONVERTER="$PROJECT/convert_permie_data.py"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${GREEN}🌱 PermiePortal Sync${NC}"
echo "================================"

if [ ! -f "$CONVERTER" ]; then
  echo -e "${RED}❌ Converter not found at $CONVERTER${NC}"
  exit 1
fi

if [[ "$1" == "--check" || "$1" == "--dry-run" ]]; then
  echo -e "${YELLOW}Validation mode — no files will be changed${NC}\n"
  python3 "$CONVERTER" --dry-run
  exit 0
fi

python3 "$CONVERTER"

# Re-resolve companions after every sync — new plants auto-promote from unresolved
python3 "$PROJECT/resolve_companions.py" 2>&1 | grep -E "RESOLVED|NORMALIZED|Files changed|not found" || true

# Re-resolve companions after every sync — new plants auto-promote from unresolved
python3 "$PROJECT/resolve_companions.py" 2>&1 | grep -E "RESOLVED|NORMALIZED|Files changed|not found" || true

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ Sync complete${NC}"
echo ""
echo "Next steps:"
echo "  • Check http://localhost:4321/plants and /pests"
echo "  • Commit: git add -A && git commit -m 'update plant/pest data'"
echo ""
