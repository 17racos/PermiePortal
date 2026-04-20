#!/usr/bin/env python3
"""
build_intake_queue.py
=====================
Aggregates all companions_unresolved entries from plants.json into
a structured intake_queue.json for human review and classification.

DESIGN PRINCIPLES:
  - Zero data loss
  - Idempotent: re-running preserves all human decisions
  - No automatic classification of ambiguous entries
  - No inference of species from generic names
  - Full audit trail

Run:
  python3 build_intake_queue.py              # build/update queue
  python3 build_intake_queue.py --report     # show queue summary
  python3 build_intake_queue.py --pending    # show only unclassified entries
"""

import json
import re
import argparse
from datetime import date
from pathlib import Path
from collections import defaultdict

# ── CONFIG ────────────────────────────────────────────────────────────────────
PLANTS_JSON  = Path("src/data/plants.json")
INTAKE_QUEUE = Path("intake_queue.json")

VALID_CLASSIFICATIONS = {
    "ADD_TO_DATABASE",       # specific, valid plant not in DB
    "NORMALIZE_TO_EXISTING", # variant of existing plant → add as aka
    "NEEDS_SPECIFICATION",   # too generic to safely resolve
    "KEEP_AS_CONTEXT",       # not a plant, belongs in companion_categories
}

VALID_STATUSES = {
    "pending",   # awaiting human review
    "approved",  # human approved the resolution
    "resolved",  # resolution has been applied
    "deferred",  # consciously left unresolved
}
# ─────────────────────────────────────────────────────────────────────────────


def normalize_name(name):
    """Normalize a companion name for deduplication.
    Lowercase, strip punctuation, collapse whitespace.
    Does NOT stem or infer variants — that's a human decision.
    """
    n = str(name).lower().strip()
    n = re.sub(r'[^\w\s-]', '', n)
    n = re.sub(r'\s+', ' ', n)
    return n.strip()


def make_id(normalized_name):
    """Generate a stable ID from normalized name."""
    return re.sub(r'[\s]+', '-', normalized_name).strip('-')


def load_existing_queue():
    """Load existing intake_queue.json. Returns dict keyed by id."""
    if not INTAKE_QUEUE.exists():
        return {}
    try:
        data = json.loads(INTAKE_QUEUE.read_text(encoding='utf-8'))
        return {entry['id']: entry for entry in data}
    except Exception as e:
        print(f"⚠️  Could not load existing queue: {e}")
        print("   Proceeding with empty queue — existing file preserved as backup")
        backup = INTAKE_QUEUE.with_suffix('.json.bak')
        INTAKE_QUEUE.rename(backup)
        print(f"   Backed up to: {backup}")
        return {}


def extract_unresolved(plants):
    """
    Extract all companions_unresolved entries from plants.json.
    Returns: dict of normalized_name → {name, slugs, raw_originals}

    Handles both:
      - string entries (legacy)
      - dict entries {name, original} (current format)
    """
    aggregated = defaultdict(lambda: {
        'display_name': None,
        'referenced_by': set(),
        'raw_originals': set(),
    })

    for plant in plants:
        plant_slug = plant.get('slug', '')
        unresolved = plant.get('companions_unresolved', []) or []

        for entry in unresolved:
            if isinstance(entry, dict):
                name = entry.get('name') or entry.get('original') or ''
                original = entry.get('original') or name
            elif isinstance(entry, str):
                name = entry
                original = entry
            else:
                continue

            name = name.strip()
            if not name:
                continue

            norm = normalize_name(name)
            if not norm:
                continue

            agg = aggregated[norm]

            # Use the most specific / best-cased display name seen
            if agg['display_name'] is None:
                agg['display_name'] = name
            elif len(name) > len(agg['display_name']):
                # Prefer longer/more specific form
                agg['display_name'] = name

            if plant_slug:
                agg['referenced_by'].add(plant_slug)

            if original and original != name:
                agg['raw_originals'].add(original)

    return aggregated


def build_queue_entry(norm_name, agg_data, existing_entry=None):
    """
    Build or update a single queue entry.

    CRITICAL: If existing_entry has human decisions (classification, status,
    resolution, notes), NEVER overwrite them. Only update frequency data
    and last_seen.
    """
    today = str(date.today())
    referenced_by = sorted(agg_data['referenced_by'])
    frequency = len(referenced_by)
    display_name = agg_data['display_name'] or norm_name.title()

    if existing_entry:
        # UPDATE: preserve all human decisions, only refresh data fields
        entry = dict(existing_entry)  # copy
        entry['name']            = display_name  # may have improved
        entry['normalized_name'] = norm_name
        entry['frequency']       = frequency
        entry['referenced_by']   = {
            'count':    frequency,
            'examples': referenced_by[:10],  # show up to 10
            'all':      referenced_by,
        }
        entry['last_seen'] = today

        # PRESERVE: classification, status, resolution, notes
        # These are set by humans — never overwrite
        if 'classification' not in entry:
            entry['classification'] = None
        if 'status' not in entry:
            entry['status'] = 'pending'
        if 'resolution' not in entry:
            entry['resolution'] = None
        if 'notes' not in entry:
            entry['notes'] = ''
        if 'first_seen' not in entry:
            entry['first_seen'] = today

        return entry

    else:
        # NEW ENTRY: all fields initialized, no classification assumed
        return {
            'id':             make_id(norm_name),
            'name':           display_name,
            'normalized_name': norm_name,
            'frequency':      frequency,
            'referenced_by':  {
                'count':    frequency,
                'examples': referenced_by[:10],
                'all':      referenced_by,
            },
            'classification': None,    # human sets this
            'status':         'pending',
            'resolution':     None,    # human sets this
            'notes':          '',
            'first_seen':     today,
            'last_seen':      today,
        }


def validate_existing_entries(existing_queue):
    """
    Validate that existing human decisions are still coherent.
    Flags issues but does NOT modify any human-set fields.
    """
    issues = []
    for entry_id, entry in existing_queue.items():
        classification = entry.get('classification')
        status = entry.get('status')
        resolution = entry.get('resolution')

        if classification and classification not in VALID_CLASSIFICATIONS:
            issues.append(
                f"  ⚠️  [{entry_id}]: unknown classification '{classification}'"
            )
        if status and status not in VALID_STATUSES:
            issues.append(
                f"  ⚠️  [{entry_id}]: unknown status '{status}'"
            )
        if status == 'approved' and not resolution:
            issues.append(
                f"  ⚠️  [{entry_id}]: status=approved but no resolution set"
            )
        if classification == 'NORMALIZE_TO_EXISTING':
            if not resolution or resolution.get('action') != 'aka':
                issues.append(
                    f"  ⚠️  [{entry_id}]: NORMALIZE classification but no aka resolution"
                )
    return issues


def print_report(queue_entries):
    """Print a summary of the intake queue state."""
    total = len(queue_entries)
    by_status = defaultdict(int)
    by_class = defaultdict(int)
    pending_high_freq = []

    for entry in queue_entries:
        status = entry.get('status', 'pending')
        classification = entry.get('classification') or 'unclassified'
        by_status[status] += 1
        by_class[classification] += 1

        if status == 'pending' and entry.get('frequency', 0) >= 5:
            pending_high_freq.append(entry)

    print(f"\n📊 Intake Queue Summary")
    print(f"{'=' * 45}")
    print(f"  Total entries:     {total}")
    print(f"\n  By status:")
    for status, count in sorted(by_status.items()):
        print(f"    {status:<20} {count}")
    print(f"\n  By classification:")
    for cls, count in sorted(by_class.items()):
        print(f"    {cls:<30} {count}")

    if pending_high_freq:
        pending_high_freq.sort(key=lambda x: x['frequency'], reverse=True)
        print(f"\n  🔥 High-frequency pending entries (≥5 references):")
        for entry in pending_high_freq[:15]:
            print(f"    {entry['frequency']:>4}x  {entry['name']}")


def main():
    parser = argparse.ArgumentParser(
        description='Build/update plant companion intake queue'
    )
    parser.add_argument('--report', action='store_true',
                        help='Show queue summary after building')
    parser.add_argument('--pending', action='store_true',
                        help='Show only unclassified/pending entries')
    args = parser.parse_args()

    print("🌱 Plant Intake Queue Builder")
    print("=" * 45)

    # Load inputs
    if not PLANTS_JSON.exists():
        print(f"❌ {PLANTS_JSON} not found — run ./sync.sh first")
        return

    plants = json.loads(PLANTS_JSON.read_text(encoding='utf-8'))
    print(f"✅ Loaded {len(plants)} plants from {PLANTS_JSON}")

    existing_queue = load_existing_queue()
    print(f"✅ Loaded {len(existing_queue)} existing queue entries")

    # Validate existing human decisions before touching anything
    issues = validate_existing_entries(existing_queue)
    if issues:
        print(f"\n⚠️  Validation issues in existing queue:")
        for issue in issues:
            print(issue)
        print("   These will NOT be overwritten — fix manually in intake_queue.json")

    # Extract current unresolved companions
    print(f"\n🔍 Extracting companions_unresolved...")
    aggregated = extract_unresolved(plants)
    print(f"✅ Found {len(aggregated)} unique normalized names")

    # Build updated queue
    new_entries = 0
    updated_entries = 0
    queue_entries = []

    for norm_name, agg_data in sorted(aggregated.items()):
        entry_id = make_id(norm_name)
        existing = existing_queue.get(entry_id)

        entry = build_queue_entry(norm_name, agg_data, existing)
        queue_entries.append(entry)

        if existing:
            updated_entries += 1
        else:
            new_entries += 1

    # Check for entries in existing queue that are no longer in unresolved
    # These may have been resolved — keep them but mark last_seen as stale
    existing_ids = {make_id(normalize_name(k)) for k in aggregated.keys()}
    for entry_id, existing_entry in existing_queue.items():
        if entry_id not in existing_ids:
            # Entry no longer appears in companions_unresolved
            # Preserve it — may have been resolved and removed, or data changed
            entry = dict(existing_entry)
            entry['notes'] = (
                entry.get('notes', '') +
                f" [Note: no longer found in companions_unresolved as of {date.today()}]"
            ).strip()
            queue_entries.append(entry)
            print(f"  ℹ️  Preserved stale entry: {entry_id} (no longer in unresolved)")

    # Sort by frequency desc, then name
    queue_entries.sort(key=lambda x: (-x.get('frequency', 0), x.get('name', '')))

    # Write output
    INTAKE_QUEUE.write_text(
        json.dumps(queue_entries, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )

    print(f"\n{'=' * 45}")
    print(f"✅ intake_queue.json written")
    print(f"   New entries:     {new_entries}")
    print(f"   Updated entries: {updated_entries}")
    print(f"   Total:           {len(queue_entries)}")

    if args.report or args.pending:
        print_report(queue_entries)

    if args.pending:
        pending = [e for e in queue_entries
                   if e.get('status') == 'pending' and e.get('classification') is None]
        print(f"\n📋 Unclassified pending entries ({len(pending)}):")
        for entry in pending:
            print(f"  {entry['frequency']:>4}x  {entry['name']:<30} "
                  f"refs: {', '.join(entry['referenced_by']['examples'][:3])}")

    print(f"\nNext: review intake_queue.json and set classification + resolution")
    print(f"Then: python3 apply_aka_resolutions.py --dry-run")


if __name__ == '__main__':
    main()
