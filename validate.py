#!/usr/bin/env python3
"""
PermiePortal Enrichment Validator
===================================
Run this AFTER every Cursor Agent enrichment session, BEFORE ./sync.sh

Catches:
- Invented pest slugs not in pests-data.yml
- Descriptions too short (< 400 chars)
- Missing propagation/sun/water sections in description
- Vague companions (categories instead of species)
- Growing conditions in cautions field — acceptable per policy
- NEEDS_DATA fields still remaining
- North Florida geographic framing
- Singular pest names when plural exists (Whitefly vs Whiteflies)

Usage:
  python3 validate.py              # check all seeds
  python3 validate.py --fix        # auto-fix what can be fixed safely
  python3 validate.py --since 2h   # only check files modified in last 2 hours
  python3 validate.py --file src/seeds/plants/moringa-data.yml  # check one file
"""

import re
import sys
import argparse
import yaml
from pathlib import Path
from datetime import datetime, timedelta

PROJECT      = Path(__file__).parent
SEEDS_PLANTS = PROJECT / "src/seeds/plants"
PESTS_FILE   = PROJECT / "src/seeds/pests/pests-data.yml"

# ── LOAD VALID PEST NAMES ─────────────────────────────────────────────────────

def load_valid_pests():
    if not PESTS_FILE.exists():
        return set(), {}
    try:
        data = yaml.safe_load(PESTS_FILE.read_text(encoding='utf-8'))
        # Map: display name (lower) -> canonical display name
        valid = {}
        for p in (data or []):
            name = p.get('name', '')
            if name:
                valid[name.lower()] = name
        return set(valid.keys()), valid
    except Exception as e:
        print(f"⚠️  Could not load pests file: {e}")
        return set(), {}


# ── VALIDATION RULES ──────────────────────────────────────────────────────────

# Vague companion patterns — only match entries that are PURELY a category
# with no specific plant name. Entries like "Pigeon Pea — nitrogen fixer..."
# are valid because they start with a specific species name.
# We check the START of the string, not anywhere within it.
VAGUE_COMPANION_PATTERNS = [
    r'^nitrogen.fix',
    r'^dynamic acc',
    r'^ground cover',
    r'^fruit tree',
    r'^legumes?$',
    r'^herbs?$',
    r'^flowering plant',
    r'^native plant',
    r'^aromatic plant',
    r'^tropical plant',
    r'^subtropical',
    r'^any ',
    r'^most ',
    r'^many ',
    r'^various ',
    r'^other ',
    r'^plants? that',
    r'^plants? which',
    r'^trees? that',
    r'^shrubs? that',
    r'^low ground',
]


# Plants that legitimately have fewer companions/functions due to their nature
SPECIALIST_PLANTS = {
    'Air Potato',       # invasive — no companions recommended
    'Singapore Daisy',  # invasive
    'Water Hyacinth',   # invasive aquatic
    'Fennel',           # allelopathic — grows alone
    'Venus Flytrap',    # carnivorous
    'Bladderwort',      # carnivorous aquatic
    'Nepenthes',        # carnivorous
    'Pitcher Plant',    # carnivorous
    'Chaga Host',       # mushroom substrate host
    'Turkey Tail Host', # mushroom substrate host
    'Reishi Host',      # mushroom substrate host
    'Cordyceps Host',   # mushroom substrate host
    'Stinging Tree',    # naturally pest/companion resistant
    'Kratom',           # legal specialist, minimal data
    'Duckweed',         # aquatic
    'Floating Heart',   # aquatic
    'Water Lettuce',    # aquatic
    'Milkweed',         # specialist pollinator host
}

CONDITION_WORDS = [
    'shade', 'soil', 'drainage', 'frost', 'stagnation',
    'boggy', 'waterlogged', 'overwatered', 'clay', 'sand',
    'humidity', 'wind', 'cold snap', 'heat stress', 'standing water',
    'poorly drained', 'compacted', 'salinity', 'alkaline', 'acidic',
]

NORTH_FLORIDA_PATTERNS = [
    r'north florida',
    r'northern florida',
    r'n\. florida',
]

REQUIRED_DESCRIPTION_SECTIONS = [
    ('sun', ['sun', 'light', 'shade', '☀️']),
    ('water', ['water', 'moisture', 'drought', 'irrigation', '💧']),
    ('propagat', ['propagat', 'seed', 'cutting', 'division', '✂️']),
]


def validate_file(yml_path, valid_pest_names, valid_pest_map, fix=False):
    """Validate a single plant YAML file. Returns list of issues."""
    issues = []
    fixes_applied = []

    try:
        content = yml_path.read_text(encoding='utf-8')
        data = yaml.safe_load(content)
        if not data or not isinstance(data, list):
            return [f"PARSE ERROR: could not parse {yml_path.name}"], []
        plant = data[0]
    except Exception as e:
        return [f"PARSE ERROR: {e}"], []

    name = plant.get('common_name', yml_path.stem)

    # ── NEEDS_DATA check ──────────────────────────────────────────────────────
    needs_count = content.count('NEEDS_DATA')
    if needs_count > 0:
        issues.append(f"NEEDS_DATA: {needs_count} fields still need enrichment")

    # ── Description checks ────────────────────────────────────────────────────
    desc = plant.get('description', '') or ''
    if len(desc) < 400:
        issues.append(f"SHORT_DESC: description is {len(desc)} chars (minimum 400)")

    for section_name, keywords in REQUIRED_DESCRIPTION_SECTIONS:
        if not any(kw.lower() in desc.lower() for kw in keywords):
            issues.append(f"MISSING_SECTION: description missing {section_name} information")

    # ── North Florida check ───────────────────────────────────────────────────
    for pattern in NORTH_FLORIDA_PATTERNS:
        if re.search(pattern, desc, re.IGNORECASE):
            issues.append(f"GEOGRAPHY: contains 'North Florida' — use 'Florida and Puerto Rico'")
            if fix:
                content = re.sub(
                    r'[Nn]orth(?:ern)?\s+[Ff]lorida',
                    'Florida and Puerto Rico',
                    content
                )
                fixes_applied.append("Fixed 'North Florida' -> 'Florida and Puerto Rico'")
            break

    # ── Companion checks ──────────────────────────────────────────────────────
    companions = plant.get('companions') or []
    if len(companions) < 3:
        specialist_indicators = [
            'invasive', 'aquatic', 'carnivorous', 'alone', 'isolated'
        ]
        purpose = str(plant.get('purpose', '')).lower()
        desc_lower = desc.lower()
        is_specialist = (
            name in SPECIALIST_PLANTS or
            any(w in desc_lower or w in purpose for w in specialist_indicators)
        )
        if not is_specialist:
            issues.append(f"FEW_COMPANIONS: only {len(companions)} companions (minimum 3 for non-specialist plants)")

    for comp in companions:
        comp_str = str(comp).lower()
        if any(re.search(pat, comp_str) for pat in VAGUE_COMPANION_PATTERNS):
            issues.append(f"VAGUE_COMPANION: '{comp}' is a category, not a species name")

    # ── Pest name validation ──────────────────────────────────────────────────
    pests = plant.get('pests') or []
    new_pests = list(pests)
    pest_changed = False

    for pest in pests:
        pest_str = str(pest).strip()
        pest_lower = pest_str.lower()

        if pest_lower in ('needs_data', 'none', 'none documented', 'none significant', ''):
            issues.append(f"INVALID_PEST: '{pest}' is not a valid pest name — use empty list if no pests")
            if fix:
                new_pests = [p for p in new_pests if str(p).strip().lower() not in
                             ('needs_data', 'none', 'none documented', 'none significant', '')]
                pest_changed = True
            continue

        if pest_lower not in valid_pest_names:
            # Check for close match
            close = [v for k, v in valid_pest_map.items() if pest_lower in k or k in pest_lower]
            hint = f" (did you mean: {close[0]}?)" if close else " (not in pests-data.yml)"
            issues.append(f"INVALID_PEST: '{pest}'{hint}")

    if fix and pest_changed:
        # Rebuild pests section in YAML
        # Simple string replacement approach
        old_pests_block = re.search(r'  pests:.*?(?=\n  \w|\Z)', content, re.DOTALL)
        if old_pests_block:
            if new_pests:
                new_block = '  pests:\n' + ''.join(f'  - {p}\n' for p in new_pests)
            else:
                new_block = '  pests: []\n'
            content = content[:old_pests_block.start()] + new_block + content[old_pests_block.end():]
            fixes_applied.append(f"Removed {len(pests) - len(new_pests)} invalid pest entries")

    # ── Avoid field check ─────────────────────────────────────────────────────
    # cautions field accepts both antagonistic plants AND growing condition
    # warnings — both are valid per .cursorrules policy. No validation needed.
    pass  # cautions field intentionally not validated

    # ── Plant function check ──────────────────────────────────────────────────
    functions = plant.get('plant_function') or []
    if len(functions) < 3 and name not in SPECIALIST_PLANTS:
        issues.append(f"FEW_FUNCTIONS: only {len(functions)} plant functions (minimum 3)")

    # ── Apply fixes ───────────────────────────────────────────────────────────
    if fix and fixes_applied:
        yml_path.write_text(content, encoding='utf-8')

    return issues, fixes_applied


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PermiePortal Enrichment Validator')
    parser.add_argument('--fix', action='store_true',
                        help='Auto-fix safe issues (geography, invalid pests)')
    parser.add_argument('--since', type=str,
                        help='Only check files modified in last N hours (e.g. --since 2h)')
    parser.add_argument('--file', type=str,
                        help='Check a single file')
    parser.add_argument('--summary', action='store_true',
                        help='Show summary only, not per-file details')
    args = parser.parse_args()

    print("\n🔍 PermiePortal Enrichment Validator")
    print("=" * 50)

    # Load valid pests
    valid_pest_names, valid_pest_map = load_valid_pests()
    print(f"Loaded {len(valid_pest_names)} valid pest names")

    # Determine which files to check
    if args.file:
        files = [Path(args.file)]
    else:
        files = [f for f in sorted(SEEDS_PLANTS.glob("*.yml"))
                 if '_archived' not in str(f)]

    # Filter by modification time if --since specified
    if args.since and not args.file:
        match = re.match(r'(\d+)(h|m|d)', args.since)
        if match:
            n, unit = int(match.group(1)), match.group(2)
            delta = {'h': timedelta(hours=n), 'm': timedelta(minutes=n),
                     'd': timedelta(days=n)}[unit]
            cutoff = datetime.now() - delta
            files = [f for f in files
                     if datetime.fromtimestamp(f.stat().st_mtime) > cutoff]
            print(f"Checking files modified in last {args.since}: {len(files)} files")

    print(f"Checking {len(files)} plant files...\n")

    # Run validation
    all_issues = {}
    all_fixes = {}
    issue_counts = {}

    for yml in files:
        issues, fixes = validate_file(yml, valid_pest_names, valid_pest_map, fix=args.fix)
        if issues:
            all_issues[yml.name] = issues
            all_fixes[yml.name] = fixes
            for issue in issues:
                issue_type = issue.split(':')[0]
                issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1

    # Report
    if not all_issues:
        print("✅ All files pass validation!")
    else:
        if not args.summary:
            for fname, issues in sorted(all_issues.items()):
                print(f"  📄 {fname}")
                for issue in issues:
                    print(f"    ⚠️  {issue}")
                if all_fixes.get(fname):
                    for fix in all_fixes[fname]:
                        print(f"    ✅ Fixed: {fix}")
                print()

        print("\n" + "=" * 50)
        print("📊 Summary")
        print("=" * 50)
        print(f"  Files with issues: {len(all_issues)} of {len(files)}")
        print(f"  Files clean:       {len(files) - len(all_issues)}")
        print()
        print("  Issue breakdown:")
        for issue_type, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
            print(f"    {count:3d}x  {issue_type}")

        if not args.fix:
            print(f"\n  Run with --fix to auto-correct safe issues")
            print(f"  Run with --since 2h to check only recent files")

    # Exit code for use in scripts
    sys.exit(0 if not all_issues else 1)


if __name__ == '__main__':
    main()
