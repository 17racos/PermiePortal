#!/usr/bin/env python3
"""
apply_aka_resolutions.py
========================
Reads intake_queue.json and applies NORMALIZE_TO_EXISTING resolutions
by adding aka entries to target plant YAML files.

SAFETY RULES:
  - Only processes entries where resolution.action == "aka"
  - Checks for global aka conflicts before writing anything
  - Never overwrites existing aka values
  - Never modifies classification, status, or notes in the queue
  - Validates YAML output before committing write
  - Dry-run mode shows all changes without touching files

Run:
  python3 apply_aka_resolutions.py --dry-run   # preview, no writes
  python3 apply_aka_resolutions.py             # apply and log
"""

import json
import io
import re
import argparse
from pathlib import Path
from ruamel.yaml import YAML
import yaml as pyyaml

# ── CONFIG ────────────────────────────────────────────────────────────────────
INTAKE_QUEUE = Path("intake_queue.json")
SEEDS_DIR    = Path("src/seeds/plants")
PLANTS_JSON  = Path("src/data/plants.json")
# ─────────────────────────────────────────────────────────────────────────────


def make_ryaml():
    ry = YAML()
    ry.preserve_quotes = True
    ry.width = 10000
    ry.best_sequence_indent = 2
    ry.best_sequence_dash_offset = 2
    return ry


def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')


def find_yaml(slug, seeds_dir):
    """Find YAML file for a plant slug."""
    for pattern in [f"{slug}-data.yml", f"{slug}.yml", f"{slug}.data.yml"]:
        f = seeds_dir / pattern
        if f.exists():
            return f
    hits = list(seeds_dir.glob(f"{slug}*.yml"))
    return hits[0] if hits else None


def build_global_aka_index(seeds_dir):
    """
    Build a complete index of all existing aka values across all plants.
    Returns: dict of aka_string.lower() → [plant_slug, ...]

    Used for conflict detection: if an aka string already maps to a DIFFERENT
    plant, adding it to another plant creates ambiguity.
    """
    aka_index = {}  # aka_lower → [slug, ...]

    for f in sorted(seeds_dir.glob("*.yml")):
        if '_archived' in str(f):
            continue
        try:
            data = pyyaml.safe_load(f.read_text(encoding='utf-8'))
        except Exception:
            continue

        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            slug = slugify(item.get('common_name', f.stem))
            for aka in (item.get('aka', []) or []):
                aka_lower = str(aka).lower().strip()
                if aka_lower not in aka_index:
                    aka_index[aka_lower] = []
                if slug not in aka_index[aka_lower]:
                    aka_index[aka_lower].append(slug)

            # Also index the common_name itself
            cn = item.get('common_name', '')
            if cn:
                cn_lower = cn.lower().strip()
                if cn_lower not in aka_index:
                    aka_index[cn_lower] = []
                if slug not in aka_index[cn_lower]:
                    aka_index[cn_lower].append(slug)

    return aka_index


def apply_aka_to_file(filepath, aka_value, plant_slug, dry_run):
    """
    Add aka_value to the target plant YAML file.

    Returns: (success: bool, message: str)
    """
    ryaml = make_ryaml()

    try:
        text = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Could not read file: {e}"

    # Validate YAML before touching
    try:
        pyyaml.safe_load(text)
    except Exception as e:
        return False, f"File has existing YAML errors: {e}"

    try:
        data = ryaml.load(io.StringIO(text))
    except Exception as e:
        return False, f"ruamel parse error: {e}"

    items = data if isinstance(data, list) else [data]
    changed = False

    for item in items:
        if not isinstance(item, dict):
            continue
        # Match by slug
        item_slug = slugify(item.get('common_name', ''))
        if item_slug != plant_slug and len(items) > 1:
            continue

        current_aka = list(item.get('aka', []) or [])
        aka_lower = aka_value.lower().strip()

        # Check if already present
        existing_lowers = [str(a).lower().strip() for a in current_aka]
        if aka_lower in existing_lowers:
            return False, f"SKIPPED — '{aka_value}' already in aka list"

        # Add the new aka value
        current_aka.append(aka_value)
        item['aka'] = current_aka
        changed = True
        break

    if not changed:
        return False, f"SKIPPED — could not find plant '{plant_slug}' in {filepath.name}"

    if dry_run:
        return True, f"DRY RUN — would add '{aka_value}' to {filepath.name}"

    # Write with validation
    out = io.StringIO()
    ryaml.dump(data, out)
    new_text = out.getvalue()

    try:
        pyyaml.safe_load(new_text)
    except Exception as e:
        return False, f"WRITE ABORTED — output would be invalid YAML: {e}"

    filepath.write_text(new_text, encoding='utf-8')
    return True, f"ADDED '{aka_value}' to {filepath.name}"


def main():
    parser = argparse.ArgumentParser(
        description='Apply aka resolutions from intake_queue.json'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without writing any files')
    args = parser.parse_args()

    if args.dry_run:
        print("\n🔍 DRY RUN — no files will be written\n")

    print("🔗 AKA Resolution Applicator")
    print("=" * 45)

    if not INTAKE_QUEUE.exists():
        print(f"❌ {INTAKE_QUEUE} not found — run build_intake_queue.py first")
        return

    queue = json.loads(INTAKE_QUEUE.read_text(encoding='utf-8'))
    print(f"✅ Loaded {len(queue)} queue entries")

    # Find entries to process
    to_process = [
        entry for entry in queue
        if (entry.get('resolution') or {}).get('action') == 'aka'
        and entry.get('status') in ('pending', 'approved')
    ]

    if not to_process:
        print("\n  No aka resolutions found in queue.")
        print("  To add one, set in intake_queue.json:")
        print('    "classification": "NORMALIZE_TO_EXISTING"')
        print('    "resolution": {"action": "aka", "target_slug": "banana", "aka_value": "Bananas"}')
        return

    print(f"✅ Found {len(to_process)} aka resolutions to process")

    # Build global aka conflict index
    print("\n🔍 Building global aka conflict index...")
    aka_index = build_global_aka_index(SEEDS_DIR)
    print(f"✅ Indexed {len(aka_index)} existing aka/name entries")

    # Process each resolution
    results = {
        'added':     [],
        'skipped':   [],
        'conflicts': [],
        'errors':    [],
    }

    print(f"\n{'=' * 45}")

    for entry in to_process:
        resolution = entry.get('resolution', {})
        entry_name = entry.get('name', entry.get('id', 'unknown'))
        target_slug = resolution.get('target_slug', '')
        aka_value   = resolution.get('aka_value', '')

        print(f"\n📌 {entry_name}")
        print(f"   → aka '{aka_value}' on slug '{target_slug}'")

        # Validate resolution fields
        if not target_slug:
            msg = "SKIPPED — resolution missing 'target_slug'"
            print(f"   ⚠️  {msg}")
            results['errors'].append((entry_name, msg))
            continue

        if not aka_value:
            msg = "SKIPPED — resolution missing 'aka_value'"
            print(f"   ⚠️  {msg}")
            results['errors'].append((entry_name, msg))
            continue

        # Conflict detection
        aka_lower = aka_value.lower().strip()
        existing_mappings = aka_index.get(aka_lower, [])
        conflicts = [s for s in existing_mappings if s != target_slug]

        if conflicts:
            msg = (f"CONFLICT — '{aka_value}' already maps to: "
                   f"{conflicts}. Cannot also map to '{target_slug}'.")
            print(f"   ❌ {msg}")
            results['conflicts'].append((entry_name, aka_value, target_slug, conflicts))
            continue

        # Find target YAML file
        filepath = find_yaml(target_slug, SEEDS_DIR)
        if not filepath:
            msg = f"ERROR — could not find YAML for slug '{target_slug}'"
            print(f"   ❌ {msg}")
            results['errors'].append((entry_name, msg))
            continue

        # Apply
        success, message = apply_aka_to_file(
            filepath, aka_value, target_slug, args.dry_run
        )

        if success:
            print(f"   ✅ {message}")
            results['added'].append((entry_name, aka_value, target_slug))
        else:
            print(f"   ⚠️  {message}")
            results['skipped'].append((entry_name, message))

    # Summary
    print(f"\n{'=' * 45}")
    print(f"📊 Results:")
    print(f"   Added:     {len(results['added'])}")
    print(f"   Skipped:   {len(results['skipped'])}")
    print(f"   Conflicts: {len(results['conflicts'])}")
    print(f"   Errors:    {len(results['errors'])}")

    if results['conflicts']:
        print(f"\n❌ Conflicts requiring manual review:")
        for name, aka_val, target, conflicts in results['conflicts']:
            print(f"   '{aka_val}' → wanted: {target}, conflicts with: {conflicts}")
            print(f"   Fix in intake_queue.json: update target_slug or remove resolution")

    if results['errors']:
        print(f"\n⚠️  Errors:")
        for name, msg in results['errors']:
            print(f"   [{name}]: {msg}")

    if args.dry_run:
        print(f"\n✅ Dry run complete — no files written")
        if results['added']:
            print(f"\nTo apply these {len(results['added'])} changes, run without --dry-run")
    else:
        if results['added']:
            print(f"\nNext steps:")
            print(f"  ./sync.sh                          # rebuild JSON with new aka values")
            print(f"  python3 resolve_companions.py      # re-resolve companions")
            print(f"  python3 build_intake_queue.py      # update queue (resolved entries will shrink)")


if __name__ == '__main__':
    main()
