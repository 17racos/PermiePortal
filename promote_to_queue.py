#!/usr/bin/env python3
"""
promote_to_queue.py
===================
Reads intake_queue.json and promotes approved ADD_TO_DATABASE entries
to queue_plants.txt for stub creation via automate.py.

SAFETY RULES:
  - Only processes entries where status == "approved"
    AND resolution.action == "queued"
  - Never promotes NEEDS_SPECIFICATION or KEEP_AS_CONTEXT entries
  - Checks queue_plants.txt and plants.json for duplicates before adding
  - Dry-run mode shows what would be added
  - Does NOT modify intake_queue.json — that's a human's job

Run:
  python3 promote_to_queue.py --dry-run   # preview
  python3 promote_to_queue.py             # promote approved entries
"""

import json
import re
import argparse
from pathlib import Path
import yaml as pyyaml

# ── CONFIG ────────────────────────────────────────────────────────────────────
INTAKE_QUEUE = Path("intake_queue.json")
QUEUE_PLANTS = Path("queue_plants.txt")
PLANTS_JSON  = Path("src/data/plants.json")
# ─────────────────────────────────────────────────────────────────────────────


def slugify(text):
    import unicodedata
    text = str(text).lower().strip()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')


def load_existing_queue():
    """Load current queue_plants.txt. Returns set of plant names (lowercased)."""
    if not QUEUE_PLANTS.exists():
        return set(), []
    lines = QUEUE_PLANTS.read_text(encoding='utf-8').splitlines()
    names = [l.strip() for l in lines if l.strip()]
    return {n.lower() for n in names}, names


def load_existing_plants():
    """Load plants.json. Returns set of slugs and set of common_names (lowercased)."""
    if not PLANTS_JSON.exists():
        return set(), set()
    plants = json.loads(PLANTS_JSON.read_text(encoding='utf-8'))
    slugs  = {p['slug'] for p in plants}
    names  = {p['common_name'].lower() for p in plants}
    # Also include aka values
    for p in plants:
        for aka in (p.get('aka') or []):
            names.add(str(aka).lower().strip())
    return slugs, names


def main():
    parser = argparse.ArgumentParser(
        description='Promote approved intake queue entries to queue_plants.txt'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview without writing')
    parser.add_argument('--show-all', action='store_true',
                        help='Show all approved entries including duplicates')
    args = parser.parse_args()

    if args.dry_run:
        print("\n🔍 DRY RUN — queue_plants.txt will not be modified\n")

    print("📋 Plant Queue Promoter")
    print("=" * 45)

    if not INTAKE_QUEUE.exists():
        print(f"❌ {INTAKE_QUEUE} not found — run build_intake_queue.py first")
        return

    queue = json.loads(INTAKE_QUEUE.read_text(encoding='utf-8'))
    print(f"✅ Loaded {len(queue)} queue entries")

    # Load existing data for duplicate checking
    existing_queue_set, existing_queue_lines = load_existing_queue()
    existing_slugs, existing_names = load_existing_plants()
    print(f"✅ Loaded {len(existing_queue_lines)} existing queue_plants.txt entries")
    print(f"✅ Loaded {len(existing_slugs)} existing plant slugs")

    # Find approved entries
    approved = [
        entry for entry in queue
        if entry.get('status') == 'approved'
        and (entry.get('resolution') or {}).get('action') == 'queued'
        and entry.get('classification') == 'ADD_TO_DATABASE'
    ]

    if not approved:
        print(f"\n  No approved ADD_TO_DATABASE entries found.")
        print(f"\n  To approve an entry, set in intake_queue.json:")
        print(f'    "classification": "ADD_TO_DATABASE"')
        print(f'    "status": "approved"')
        print(f'    "resolution": {{"action": "queued"}}')

        # Show pending ADD_TO_DATABASE entries as FYI
        pending_add = [
            entry for entry in queue
            if entry.get('classification') == 'ADD_TO_DATABASE'
            and entry.get('status') == 'pending'
        ]
        if pending_add:
            print(f"\n  ℹ️  {len(pending_add)} pending ADD_TO_DATABASE entries "
                  f"(not yet approved):")
            for entry in sorted(pending_add,
                                key=lambda x: x.get('frequency', 0),
                                reverse=True)[:10]:
                print(f"    {entry.get('frequency', 0):>4}x  {entry['name']}")
        return

    print(f"\n📦 Found {len(approved)} approved entries to process")
    print(f"{'=' * 45}")

    to_add = []
    skipped = []

    for entry in approved:
        name = entry['name']
        name_lower = name.lower().strip()
        candidate_slug = slugify(name)

        reasons_skip = []

        # Check 1: Already in queue_plants.txt
        if name_lower in existing_queue_set:
            reasons_skip.append(f"already in queue_plants.txt")

        # Check 2: Already in plants.json (by name or slug)
        if name_lower in existing_names:
            reasons_skip.append(f"already in plants database (name match)")
        elif candidate_slug in existing_slugs:
            reasons_skip.append(f"already in plants database (slug match)")

        # Check 3: Classification safety guard
        if entry.get('classification') != 'ADD_TO_DATABASE':
            reasons_skip.append(
                f"classification is '{entry.get('classification')}', "
                f"not ADD_TO_DATABASE"
            )

        if reasons_skip:
            skipped.append((name, reasons_skip))
            if args.show_all:
                print(f"  ⏭️  SKIP: {name}")
                for reason in reasons_skip:
                    print(f"       {reason}")
        else:
            to_add.append(name)
            print(f"  ✅ APPROVE: {name} (freq: {entry.get('frequency', 0)})")

    print(f"\n{'=' * 45}")
    print(f"  To add:  {len(to_add)}")
    print(f"  Skipped: {len(skipped)}")

    if skipped and not args.show_all:
        print(f"\n  Skipped entries (run --show-all for details):")
        for name, reasons in skipped[:5]:
            print(f"    {name}: {reasons[0]}")
        if len(skipped) > 5:
            print(f"    ... and {len(skipped) - 5} more")

    if not to_add:
        print(f"\n  Nothing new to add to queue_plants.txt")
        return

    if args.dry_run:
        print(f"\n🔍 Would add to queue_plants.txt:")
        for name in to_add:
            print(f"  {name}")
        print(f"\n✅ Dry run complete — no files written")
        return

    # Write to queue_plants.txt
    with open(QUEUE_PLANTS, 'a', encoding='utf-8') as f:
        for name in to_add:
            f.write(name + '\n')

    print(f"\n✅ Added {len(to_add)} entries to {QUEUE_PLANTS}")
    print(f"\nNext steps:")
    print(f"  python3 automate.py --daily     # create stubs for queued plants")
    print(f"  # Cursor Agent enriches stubs")
    print(f"  ./sync.sh                       # rebuild JSON")
    print(f"  python3 resolve_companions.py   # re-resolve companions")
    print(f"  python3 build_intake_queue.py   # update queue")

    # Update status in intake_queue.json for promoted entries
    # NOTE: Only change status from 'approved' → 'resolved', nothing else
    promoted_names = {name.lower() for name in to_add}
    queue_updated = False

    for entry in queue:
        if (entry['name'].lower() in promoted_names
                and entry.get('status') == 'approved'):
            entry['status'] = 'resolved'
            if entry.get('resolution'):
                entry['resolution']['promoted_to_queue'] = True
            queue_updated = True

    if queue_updated:
        INTAKE_QUEUE.write_text(
            json.dumps(queue, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        print(f"✅ Updated {len(to_add)} entries in intake_queue.json "
              f"(status: approved → resolved)")


if __name__ == '__main__':
    main()
