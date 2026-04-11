#!/usr/bin/env python3
"""
PermiePortal Data Converter v2
Lives at: ~/apps/permieportal/convert_permie_data.py

Usage:
  python3 convert_permie_data.py           # rebuild + update src/data/
  python3 convert_permie_data.py --dry-run # validate only, no writes
  python3 convert_permie_data.py --no-copy # write exports/ only
"""

import json
import re
import glob
import sys
import argparse
from pathlib import Path
from collections import Counter, defaultdict

# ── CONFIG ───────────────────────────────────────────────────────────────────
PROJECT     = Path.home() / "apps/permieportal"
SEEDS_DIR   = PROJECT / "src/seeds/plants"
PESTS_FILE  = PROJECT / "src/seeds/pests/pests-data.yml"
OUTPUT_DIR  = PROJECT / "exports"
ASTRO_DATA  = PROJECT / "src/data"
# ─────────────────────────────────────────────────────────────────────────────

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml", "--quiet"])
    import yaml


def slugify(text):
    if not text:
        return ""
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def load_yaml_safe(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lstrip()
        if content.startswith('---'):
            content = content[3:]
        return yaml.safe_load(content)
    except Exception as e:
        print(f"  ⚠️  Could not parse {Path(filepath).name}: {e}")
        return None


def clean_string(value):
    if not isinstance(value, str):
        return value
    return re.sub(r'\n{3,}', '\n\n', value).strip()


def norm_list(val):
    if not val:
        return []
    if isinstance(val, str):
        return [v.strip() for v in val.split(',') if v.strip()]
    return [str(v).strip() for v in val if v]


def process_plant(data, source_file):
    if not isinstance(data, dict):
        return None
    common_name = data.get('common_name', '')
    if not common_name:
        return None

    raw_pests = norm_list(data.get('pests', []))
    pest_slugs = [slugify(p) for p in raw_pests]

    return {
        "slug": slugify(common_name),
        "common_name": common_name,
        "scientific_name": data.get('scientific_name', ''),
        "aka": norm_list(data.get('aka', [])),
        "family": data.get('family', ''),
        "picture": data.get('picture', ''),
        "zone": str(data.get('zone', '')),
        "ideal_temp_min": data.get('ideal_temp_min'),
        "ideal_temp_max": data.get('ideal_temp_max'),
        "min_temp": data.get('min_temp'),
        "max_temp": data.get('max_temp'),
        "perennial": data.get('perennial'),
        "layers": norm_list(data.get('layers', [])),
        "plant_function": norm_list(data.get('plant_function', [])),
        "description": clean_string(data.get('description', '')),
        "purpose": clean_string(data.get('purpose', '')),
        "companions": norm_list(data.get('companions', [])),
        "avoid": norm_list(data.get('avoid', [])),
        "pest_slugs": pest_slugs,
        "_source": source_file,
    }


def process_pest(data):
    if not isinstance(data, dict):
        return None
    name = data.get('name', '')
    if not name:
        return None

    slug = data.get('slug', slugify(name))
    raw_cm = data.get('control_methods', {}) or {}
    control_methods = (
        {k: clean_string(v) for k, v in raw_cm.items() if v}
        if isinstance(raw_cm, dict)
        else {"notes": clean_string(str(raw_cm))}
    )
    enemies = data.get('natural_enemies', []) or []
    if isinstance(enemies, str):
        enemies = [e.strip() for e in enemies.split(',')]

    return {
        "slug": slug,
        "name": name,
        "scientific_name": data.get('scientific_name', ''),
        "picture": data.get('picture', ''),
        "description": clean_string(data.get('description', '')),
        "characteristics": clean_string(data.get('characteristics', '')),
        "control_methods": control_methods,
        "natural_enemies": [str(e).strip() for e in enemies if e],
        "affected_plants": [],
    }


def build_relationships(plants, pests):
    pest_by_slug = {p['slug']: p for p in pests}

    pest_lookup = {}
    for p in pests:
        for key in [p['slug'], p['name'].lower(), slugify(p['name']),
                    p['slug'] + 's', p['slug'].rstrip('s')]:
            pest_lookup[key] = p['slug']

    relationships = []
    pest_to_plants = defaultdict(list)
    warnings = []

    for plant in plants:
        for pest_slug in plant.get('pest_slugs', []):
            matched_slug = (
                pest_lookup.get(pest_slug) or
                pest_lookup.get(pest_slug + 's') or
                pest_lookup.get(pest_slug.rstrip('s'))
            )
            if matched_slug and matched_slug in pest_by_slug:
                pest = pest_by_slug[matched_slug]
                relationships.append({
                    "plant_slug": plant['slug'],
                    "plant_name": plant['common_name'],
                    "pest_slug": matched_slug,
                    "pest_name": pest['name'],
                })
                pest_to_plants[matched_slug].append({
                    "slug": plant['slug'],
                    "name": plant['common_name'],
                })
            else:
                warnings.append(
                    f"  ⚠️  '{pest_slug}' in {plant['_source']} "
                    f"(plant: {plant['common_name']}) — no matching pest"
                )

    for pest in pests:
        pest['affected_plants'] = pest_to_plants.get(pest['slug'], [])

    return relationships, warnings


def main():
    parser = argparse.ArgumentParser(description='PermiePortal Data Converter v2')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate only, no files written')
    parser.add_argument('--no-copy', action='store_true',
                        help='Write exports/ only, skip src/data/ copy')
    args = parser.parse_args()

    if args.dry_run:
        print("\n🔍 DRY RUN — no files will be written\n")

    print("🌱 PermiePortal Data Converter v2")
    print("=" * 45)

    # Load plants
    print("\n📦 Loading plant YAML files...")
    plant_files = sorted(set(
        glob.glob(str(SEEDS_DIR / "*-data.yml")) +
        glob.glob(str(SEEDS_DIR / "*.yml"))
    ))
    plant_files = [
        f for f in plant_files
        if not f.endswith('.bak')
        and not any(x in f for x in ['climate_data', 'semantic_tags', 'enhanced_semantic'])
    ]

    plants, skipped = [], []
    for filepath in plant_files:
        path = Path(filepath)
        raw = load_yaml_safe(path)
        if raw is None:
            skipped.append(path.name)
            continue
        items = raw if isinstance(raw, list) else [raw] if isinstance(raw, dict) else []
        for item in items:
            plant = process_plant(item, path.name)
            if plant:
                plants.append(plant)
            else:
                skipped.append(path.name)

    print(f"  ✅ {len(plants)} plants loaded")
    if skipped:
        print(f"  ⚠️  Skipped: {', '.join(skipped[:5])}{'...' if len(skipped) > 5 else ''}")

    # Load pests
    print("\n🐛 Loading pest YAML...")
    raw_pests = load_yaml_safe(PESTS_FILE)
    pests = [p for p in (process_pest(i) for i in (raw_pests or [])) if p]
    print(f"  ✅ {len(pests)} pests loaded")

    # Build relationships
    print("\n🔗 Building relationships...")
    relationships, warnings = build_relationships(plants, pests)
    print(f"  ✅ {len(relationships)} relationships mapped")

    if warnings:
        print(f"\n  ⚠️  {len(warnings)} unmatched references:")
        for w in warnings[:15]:
            print(w)
        if len(warnings) > 15:
            print(f"     ... and {len(warnings) - 15} more")
    else:
        print("  ✅ All pest references matched — zero broken links")

    # Clean up internals, add display names back
    for plant in plants:
        plant['pests'] = [r['pest_name'] for r in relationships
                          if r['plant_slug'] == plant['slug']]
        plant.pop('pest_slugs', None)
        plant.pop('_source', None)

    # Summary
    print("\n📊 Summary")
    print("=" * 45)
    print(f"  Plants:        {len(plants)}")
    print(f"  Pests:         {len(pests)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Warnings:      {len(warnings)}")

    for label, counter_key in [("Most pest-affected plants", "plant_name"),
                                ("Most widespread pests", "pest_name")]:
        counts = Counter(r[counter_key] for r in relationships).most_common(5)
        print(f"\n  {label}:")
        for name, count in counts:
            print(f"    {name}: {count}")

    if args.dry_run:
        print("\n✅ Dry run complete — no files written")
        return

    # Write exports
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n💾 Writing to {OUTPUT_DIR}/")

    def write_json(name, data):
        path = OUTPUT_DIR / name
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        print(f"  ✅ {name} — {path.stat().st_size / 1024:.0f} KB")

    write_json("plants.json", plants)
    write_json("pests.json", pests)
    write_json("relationships.json", relationships)

    # Copy to src/data/
    if not args.no_copy:
        import shutil
        ASTRO_DATA.mkdir(parents=True, exist_ok=True)
        print(f"\n📁 Updating src/data/")
        for fname in ["plants.json", "pests.json", "relationships.json"]:
            shutil.copy2(OUTPUT_DIR / fname, ASTRO_DATA / fname)
            print(f"  ✅ {fname}")
        print("\n✅ Done — Astro will hot-reload automatically")
    else:
        print(f"\n✅ Done — files in {OUTPUT_DIR}")
        print("   Run without --no-copy to update src/data/")


if __name__ == "__main__":
    main()
