#!/bin/bash
# ============================================================
# PermiePortal Converter v3 Migration Script
# Run as user: dracos
# Project root: ~/apps/permieportal
# Usage: bash migrate_v3.sh
# ============================================================

set -euo pipefail

PROJECT="$HOME/apps/permieportal"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

step() { echo -e "\n${CYAN}${BOLD}▶ $1${NC}"; }
ok()   { echo -e "  ${GREEN}✅ $1${NC}"; }
warn() { echo -e "  ${YELLOW}⚠️  $1${NC}"; }
fail() { echo -e "  ${RED}❌ $1${NC}"; exit 1; }
info() { echo -e "  ${NC}   $1${NC}"; }

echo ""
echo -e "${BOLD}============================================${NC}"
echo -e "${BOLD}  PermiePortal — Converter v3 Migration${NC}"
echo -e "${BOLD}============================================${NC}"
echo ""

# ── Preflight ────────────────────────────────────────────────────────────────
step "Preflight checks"

[ -d "$PROJECT" ]           || fail "Project not found at $PROJECT"
[ -f "$PROJECT/sync.sh" ]   || fail "sync.sh not found"
cd "$PROJECT"
ok "Project root: $PROJECT"

# Require the new v3 files to already be in place
[ -f "$PROJECT/convert_permie_data.py" ] || fail "convert_permie_data.py not found — copy v3 file first"
[ -f "$PROJECT/automate.py" ]            || fail "automate.py not found — copy v5 file first"

# Check Python
python3 --version > /dev/null 2>&1 || fail "python3 not found"
python3 -c "import yaml" 2>/dev/null || {
    warn "pyyaml not installed — installing..."
    pip3 install pyyaml --quiet --break-system-packages
}
ok "Python + pyyaml ready"

# ── Backup ───────────────────────────────────────────────────────────────────
step "Backing up current data files"

BACKUP_DIR="$PROJECT/backups/migration_v3_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

for f in \
    src/data/plants.json \
    src/data/pests.json \
    src/data/relationships.json \
    exports/plants.json \
    exports/pests.json \
    exports/relationships.json; do
    if [ -f "$PROJECT/$f" ]; then
        cp "$PROJECT/$f" "$BACKUP_DIR/$(basename $f)"
        ok "Backed up $f"
    else
        warn "$f not found — skipping backup of this file"
    fi
done

info "Backup location: $BACKUP_DIR"

# ── Scan for practitioner_notes ──────────────────────────────────────────────
step "Scanning for deprecated practitioner_notes field"

PN_COUNT=$(grep -rl "practitioner_notes" "$PROJECT/src/seeds/plants/" 2>/dev/null | wc -l | tr -d ' ')

if [ "$PN_COUNT" -gt 0 ]; then
    warn "$PN_COUNT YAML file(s) still contain practitioner_notes"
    echo ""
    echo -e "  ${YELLOW}Files with practitioner_notes:${NC}"
    grep -rl "practitioner_notes" "$PROJECT/src/seeds/plants/" | head -20 | while read f; do
        echo "    $(basename $f)"
    done
    echo ""
    echo -e "  ${YELLOW}Content preview (first 5 files):${NC}"
    grep -rh -A1 "practitioner_notes" "$PROJECT/src/seeds/plants/" 2>/dev/null | head -20
    echo ""
    read -p "  Remove practitioner_notes from all YAML seeds now? [y/N] " REMOVE_PN
    if [[ "$REMOVE_PN" =~ ^[Yy]$ ]]; then
        python3 - <<'PYEOF'
import re
from pathlib import Path

seeds = Path("src/seeds/plants")
count = 0
for f in sorted(seeds.glob("*.yml")):
    if '_archived' in str(f):
        continue
    text = f.read_text(encoding='utf-8')
    if 'practitioner_notes' not in text:
        continue
    # Remove practitioner_notes key + its scalar or block value
    # Handles both:
    #   practitioner_notes: "some value"
    #   practitioner_notes: |-
    #     multi
    #     line
    cleaned = re.sub(
        r'\n[ \t]*practitioner_notes:[ \t]*.*?(?=\n[ \t]*[a-z#]|\Z)',
        '',
        text,
        flags=re.DOTALL
    )
    if cleaned != text:
        f.write_text(cleaned, encoding='utf-8')
        count += 1

print(f"  Cleaned practitioner_notes from {count} file(s)")
PYEOF
        ok "practitioner_notes removed from seeds"
    else
        warn "Skipped — converter will emit deprecation warnings for these files (harmless)"
    fi
else
    ok "No practitioner_notes found in seeds — already clean"
fi

# ── Dry run ──────────────────────────────────────────────────────────────────
step "Running converter dry-run (validation only)"

echo ""
python3 convert_permie_data.py --dry-run 2>&1 | tee /tmp/permie_dryrun.log
echo ""

WARN_COUNT=$(grep -c "⚠️" /tmp/permie_dryrun.log 2>/dev/null || echo 0)
info "Dry-run warnings: $WARN_COUNT"

if [ "$WARN_COUNT" -gt 0 ]; then
    echo ""
    warn "Warnings found. Breakdown by category:"
    echo ""
    # Tally warning types
    grep "⚠️" /tmp/permie_dryrun.log \
        | grep -oP '\[.*?\]' \
        | sort | uniq -c | sort -rn \
        | while read count tag; do
            echo "    $count  $tag"
        done
    echo ""
    echo -e "  ${YELLOW}These warnings are expected on first run.${NC}"
    echo -e "  ${YELLOW}They surface pre-existing data problems — not converter bugs.${NC}"
    echo ""
    read -p "  Continue with full sync? [y/N] " CONTINUE
    [[ "$CONTINUE" =~ ^[Yy]$ ]] || { warn "Aborted — no files changed"; exit 0; }
else
    ok "Zero warnings — data is clean"
fi

# ── Full sync ────────────────────────────────────────────────────────────────
step "Running full sync (./sync.sh)"

echo ""
./sync.sh 2>&1 | tee /tmp/permie_sync.log
echo ""

SYNC_EXIT=${PIPESTATUS[0]}
if [ "$SYNC_EXIT" -ne 0 ]; then
    fail "sync.sh exited with code $SYNC_EXIT — check /tmp/permie_sync.log"
fi
ok "Sync complete"

# ── Verify JSON outputs ───────────────────────────────────────────────────────
step "Verifying JSON outputs"

for f in plants.json pests.json relationships.json; do
    TARGET="$PROJECT/src/data/$f"
    if [ ! -f "$TARGET" ]; then
        fail "$f not found in src/data/"
    fi
    python3 -c "import json; data=json.load(open('$TARGET')); print(f'  {len(data)} records')" \
        && ok "$f valid"
done

# ── Spot-check new fields ─────────────────────────────────────────────────────
step "Spot-checking new fields on output JSON"

python3 - <<'PYEOF'
import json, sys
from pathlib import Path

errors = []

# --- plants.json checks ---
plants = json.load(open("src/data/plants.json"))
print(f"  Plants loaded: {len(plants)}")

sample = next((p for p in plants if p.get('common_name') == 'Moringa'), plants[0])
name = sample.get('common_name', 'unknown')

# zone_min / zone_max
if 'zone_min' not in sample:
    errors.append(f"MISSING zone_min on {name}")
elif sample['zone_min'] is not None:
    print(f"  ✅ zone_min/zone_max present ({name}: {sample['zone_min']}–{sample['zone_max']})")
else:
    print(f"  ⚠️  zone_min is null on {name} — zone may be unparseable")

# data_quality_score
if 'data_quality_score' not in sample:
    errors.append(f"MISSING data_quality_score on {name}")
else:
    score = sample['data_quality_score']
    dims  = sample.get('data_quality_dimensions', {})
    print(f"  ✅ data_quality_score present ({name}: {score})")
    print(f"     Dimensions: {dims}")

# companions structure
companions = sample.get('companions', [])
if companions and isinstance(companions[0], dict):
    print(f"  ✅ companions are structured dicts ({name}: {len(companions)} resolved)")
elif companions:
    errors.append(f"companions still flat strings on {name} — converter may not have run")
else:
    print(f"  ℹ️  companions empty on {name}")

# companions_unresolved
unres_total = sum(len(p.get('companions_unresolved', [])) for p in plants)
print(f"  ℹ️  companions_unresolved total across all plants: {unres_total}")

# field_observations — should NOT contain "Awaiting Update"
awaiting = [p['common_name'] for p in plants
            if p.get('field_observations','').strip() == 'Awaiting Update']
if awaiting:
    print(f"  ⚠️  {len(awaiting)} plant(s) still have 'Awaiting Update' in field_observations")
    for n in awaiting[:5]:
        print(f"       {n}")
else:
    print(f"  ✅ No 'Awaiting Update' strings in field_observations")

# practitioner_notes — must not appear in output
pn_plants = [p['common_name'] for p in plants if 'practitioner_notes' in p]
if pn_plants:
    errors.append(f"practitioner_notes still in JSON output: {pn_plants[:5]}")
else:
    print(f"  ✅ practitioner_notes absent from all plant records")

# --- relationships.json checks ---
rels = json.load(open("src/data/relationships.json"))
print(f"\n  Relationships loaded: {len(rels)}")

sample_rel = rels[0] if rels else {}
required_rel_fields = ['id', 'type', 'source_slug', 'source_type',
                       'target_slug', 'target_type', 'severity', 'regional', 'evidence']
missing_fields = [f for f in required_rel_fields if f not in sample_rel]
if missing_fields:
    errors.append(f"Relationship missing fields: {missing_fields}")
else:
    print(f"  ✅ Relationship schema fields all present")
    print(f"     Sample: id={sample_rel.get('id')} type={sample_rel.get('type')}")

# Legacy fields still present (Astro compat)
legacy_fields = ['plant_slug', 'plant_name', 'pest_slug', 'pest_name']
missing_legacy = [f for f in legacy_fields if f not in sample_rel]
if missing_legacy:
    errors.append(f"Legacy relationship fields missing (Astro will break): {missing_legacy}")
else:
    print(f"  ✅ Legacy relationship fields retained (Astro compatible)")

# --- Summary ---
if errors:
    print(f"\n  ❌ {len(errors)} verification error(s):")
    for e in errors:
        print(f"     {e}")
    sys.exit(1)
else:
    print(f"\n  ✅ All spot-checks passed")
PYEOF

CHECK_EXIT=$?
if [ "$CHECK_EXIT" -ne 0 ]; then
    fail "Spot-checks failed — review output above. Backups are at: $BACKUP_DIR"
fi

# ── Quality report ────────────────────────────────────────────────────────────
step "Data quality report"

python3 - <<'PYEOF'
import json
from collections import Counter

plants = json.load(open("src/data/plants.json"))
scores = [p['data_quality_score'] for p in plants if 'data_quality_score' in p]

if not scores:
    print("  ⚠️  No quality scores found")
else:
    avg   = round(sum(scores) / len(scores), 3)
    hi    = sum(1 for s in scores if s >= 0.8)
    mid   = sum(1 for s in scores if 0.5 <= s < 0.8)
    lo    = sum(1 for s in scores if s < 0.5)

    print(f"  Average quality score : {avg}")
    print(f"  ≥ 0.8 (good)          : {hi} plants")
    print(f"  0.5–0.8 (needs work)  : {mid} plants")
    print(f"  < 0.5 (poor)          : {lo} plants")

    # Most common failing dimensions
    failing = Counter()
    for p in plants:
        dims = p.get('data_quality_dimensions', {})
        for k, v in dims.items():
            if not v and k != 'has_field_observations':
                failing[k] += 1

    if failing:
        print(f"\n  Most common failing dimensions:")
        for dim, count in failing.most_common(8):
            pct = round(count / len(plants) * 100)
            print(f"    {dim:<30} {count:>5} plants  ({pct}%)")

    # Bottom 10 plants
    bottom = sorted(
        [(p['common_name'], p['data_quality_score']) for p in plants],
        key=lambda x: x[1]
    )[:10]
    print(f"\n  Lowest quality scores:")
    for name, score in bottom:
        print(f"    {score:.3f}  {name}")
PYEOF

# ── Unresolved companions report ──────────────────────────────────────────────
step "Unresolved companions report"

python3 - <<'PYEOF'
import json

plants = json.load(open("src/data/plants.json"))
has_unresolved = [
    (p['common_name'], p['companions_unresolved'])
    for p in plants if p.get('companions_unresolved')
]
total_strings = sum(len(u) for _, u in has_unresolved)

if not has_unresolved:
    print("  ✅ No unresolved companions — all linked by slug")
else:
    print(f"  {len(has_unresolved)} plants have unresolved companions ({total_strings} total strings)")
    print(f"\n  Top 15 plants with most unresolved companions:")
    for name, unres in sorted(has_unresolved, key=lambda x: len(x[1]), reverse=True)[:15]:
        print(f"    {name}: {unres}")

    # What are the most common unresolved strings? (likely categories or misspellings)
    from collections import Counter
    all_unres = [s for _, urs in has_unresolved for s in urs]
    common = Counter(all_unres).most_common(15)
    print(f"\n  Most frequent unresolved companion strings:")
    for string, count in common:
        print(f"    {count:>4}x  '{string}'")
PYEOF

# ── VALID_FUNCTIONS audit ─────────────────────────────────────────────────────
step "Scanning for unknown plant_function values"

FUNC_WARN=$(grep "FUNCTION INVALID" /tmp/permie_sync.log 2>/dev/null | wc -l | tr -d ' ')
if [ "$FUNC_WARN" -gt 0 ]; then
    warn "$FUNC_WARN FUNCTION INVALID warnings found"
    echo ""
    echo -e "  ${YELLOW}Unknown function values (add to VALID_FUNCTIONS if legitimate):${NC}"
    grep "FUNCTION INVALID" /tmp/permie_sync.log \
        | grep -oP '\[.*?\]' | sort | uniq -c | sort -rn | head -20
    echo ""
    info "Edit VALID_FUNCTIONS in convert_permie_data.py to add legitimate values"
    info "Then run: ./sync.sh --check to verify"
else
    ok "All plant_function values are in the canonical set"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}============================================${NC}"
echo -e "${GREEN}${BOLD}  Migration complete${NC}"
echo -e "${BOLD}============================================${NC}"
echo ""
echo -e "  Backup location   : ${CYAN}$BACKUP_DIR${NC}"
echo -e "  Sync log          : ${CYAN}/tmp/permie_sync.log${NC}"
echo ""
echo -e "  ${BOLD}Next steps:${NC}"
echo ""
echo -e "  1. Review unresolved companions above and update YAML"
echo -e "     to use {slug, name} format for each one"
echo ""
echo -e "  2. Fix PURPOSE warnings:"
echo -e "     ${CYAN}grep 'PURPOSE' /tmp/permie_sync.log | head -40${NC}"
echo ""
echo -e "  3. Add any legitimate functions to VALID_FUNCTIONS:"
echo -e "     ${CYAN}grep 'FUNCTION INVALID' /tmp/permie_sync.log${NC}"
echo ""
echo -e "  4. When warnings are resolved, commit:"
echo -e "     ${CYAN}git add -A && git commit -m 'converter v3: quality + companion validation'${NC}"
echo ""
echo -e "  5. Push to deploy:"
echo -e "     ${CYAN}git push origin development${NC}"
echo ""
