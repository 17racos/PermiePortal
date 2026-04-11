#!/usr/bin/env python3
"""
PermiePortal Warning Fixer
Fixes the 15 remaining unmatched pest slug warnings.

Run from project root:
  python3 fix_warnings.py
  python3 fix_warnings.py --dry-run
"""

import re
import argparse
from pathlib import Path

PROJECT      = Path(__file__).parent
SEEDS_PLANTS = PROJECT / "src/seeds/plants"
QUEUE_PESTS  = PROJECT / "queue_pests.txt"

# ── REMAP: old slug -> existing pest slug ────────────────────────────────────
REMAP = {
    'fruit-fly':                          'caribbean-fruit-fly',
    'lace-bug':                           'avocado-lace-bug',
    'scale':                              'scale-insects',
    'powdery-mildew-in-humid-conditions': 'powdery-mildew',
    'root-rot-caused-by-excessive-moisture': 'root-rot-fungus',
}

# ── REMOVE: junk entries that should just be gone ────────────────────────────
REMOVE = {
    'none',
    'none-significant',
    'weevil',   # too generic — specific weevil species exist
}

# ── ADD: legitimate pests to queue for new profiles ──────────────────────────
# These will be added to queue_pests.txt for automate.py to process
NEW_PESTS = [
    'Azalea Caterpillar',
    'Bamboo Mite',
    'Banana Weevil',
    'Locust Borer',
    'Locust Leaf Miner',
    'Leaf Spot',
    'Heart Rot',
]


def fix_yaml_file(filepath, dry_run=False):
    """Fix pest slug references in a single YAML file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ⚠️  Could not read {filepath.name}: {e}")
        return False

    original = content
    changes = []

    # Process each line in the pests section
    lines = content.splitlines()
    new_lines = []
    in_pests = False
    skip_line = False

    for line in lines:
        stripped = line.strip()

        # Track when we enter/exit the pests: section
        if re.match(r'^  pests:', line):
            in_pests = True
            new_lines.append(line)
            continue

        # Exit pests section when we hit another top-level key
        if in_pests and re.match(r'^  \w', line) and not re.match(r'^  -', line):
            in_pests = False

        if in_pests and stripped.startswith('- '):
            slug = stripped[2:].strip()

            if slug in REMOVE:
                changes.append(f"  removed: '{slug}'")
                continue  # skip this line

            if slug in REMAP:
                new_slug = REMAP[slug]
                new_line = line.replace(f'- {slug}', f'- {new_slug}')
                changes.append(f"  remapped: '{slug}' -> '{new_slug}'")
                new_lines.append(new_line)
                continue

        new_lines.append(line)

    new_content = '\n'.join(new_lines)
    # Preserve trailing newline
    if content.endswith('\n'):
        new_content += '\n'

    if changes:
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
        action = "[DRY RUN]" if dry_run else "Fixed"
        print(f"  {action} {filepath.name}:")
        for c in changes:
            print(c)
        return True

    return False


def add_to_pest_queue(new_pests, dry_run=False):
    """Add new pest names to queue_pests.txt."""
    # Check which ones aren't already in the queue
    existing = set()
    if QUEUE_PESTS.exists():
        existing = set(
            l.strip().lower()
            for l in QUEUE_PESTS.read_text().splitlines()
            if l.strip()
        )

    to_add = [p for p in new_pests if p.lower() not in existing]

    if not to_add:
        print("  ✅ All new pests already in queue")
        return

    if dry_run:
        print(f"  [DRY RUN] Would add to queue_pests.txt:")
        for p in to_add:
            print(f"    + {p}")
        return

    with open(QUEUE_PESTS, 'a') as f:
        for p in to_add:
            f.write(p + '\n')

    print(f"  Added {len(to_add)} pests to queue_pests.txt:")
    for p in to_add:
        print(f"    + {p}")


def main():
    parser = argparse.ArgumentParser(description='Fix warning slugs in plant YAMLs')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show changes without writing files')
    args = parser.parse_args()

    print("\n🔧 PermiePortal Warning Fixer")
    print("=" * 45)

    if args.dry_run:
        print("DRY RUN — no files will be changed\n")

    # ── FIX YAML FILES ───────────────────────────────────────────
    print("\n📝 Fixing plant YAML files...")

    all_slugs_to_fix = set(REMAP.keys()) | REMOVE
    fixed_count = 0

    for yml in sorted(SEEDS_PLANTS.glob("*.yml")):
        if '_archived' in str(yml):
            continue
        try:
            content = yml.read_text(encoding='utf-8')
        except Exception:
            continue

        # Quick check — does this file contain any of our target slugs?
        needs_fix = False
        for slug in all_slugs_to_fix:
            if f'- {slug}' in content:
                needs_fix = True
                break

        if needs_fix:
            changed = fix_yaml_file(yml, dry_run=args.dry_run)
            if changed:
                fixed_count += 1

    print(f"\n  {'Would fix' if args.dry_run else 'Fixed'} {fixed_count} files")

    # ── ADD NEW PESTS TO QUEUE ────────────────────────────────────
    print("\n🐛 Adding new pests to queue...")
    add_to_pest_queue(NEW_PESTS, dry_run=args.dry_run)

    # ── NEXT STEPS ────────────────────────────────────────────────
    if not args.dry_run:
        print(f"""
{'='*45}
✅ Done

Next steps:
  1. Process new pests:
     python3 automate.py pests --file queue_pests.txt

  2. Enrich new pest stubs in Cursor Agent

  3. Rebuild:
     ./sync.sh

  4. Verify warnings are gone:
     python3 convert_permie_data.py --no-copy 2>&1 | grep "Warnings:"
{'='*45}
""")
    else:
        print(f"\n✅ Dry run complete — run without --dry-run to apply\n")


if __name__ == '__main__':
    main()
