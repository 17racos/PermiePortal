#!/usr/bin/env python3
"""
resolve_companions.py
=====================
Companion cleanup pipeline — four-bucket, zero data loss.
v3: Fixed ruamel indentation bug, post-write YAML validation.

Buckets:
  RESOLVED    — matched to known plant slug
  NORMALIZED  — matched via known name variant/alias table
  UNRESOLVED  — valid plant name, not in index (preserved as {name, original})
  CATEGORY    — non-plant entry (preserved as {name, original, type})

Run:
  python3 resolve_companions.py --dry-run           # no writes
  python3 resolve_companions.py --dry-run --report  # + full bucket breakdown
  python3 resolve_companions.py                     # write + validate YAML
  python3 resolve_companions.py --verbose           # per-plant detail
  python3 resolve_companions.py --targets "Plant A" "Plant B"  # specific plants
"""

import re
import io
import json
import argparse
import subprocess
from pathlib import Path
from collections import Counter
from ruamel.yaml import YAML

# ── CONFIG ────────────────────────────────────────────────────────────────────
PLANTS_JSON  = Path("src/data/plants.json")
SEEDS_DIR    = Path("src/seeds/plants")
QUEUE_PLANTS = Path("queue_plants.txt")
# ─────────────────────────────────────────────────────────────────────────────

def make_ryaml():
    """
    Create a ruamel YAML instance with settings that produce valid YAML
    for nested dicts inside sequences.

    The critical setting is best_sequence_indent / best_sequence_dash_offset.
    With indent(mapping=2, sequence=2, offset=2), ruamel writes:
      - key1: val
      key2: val    ← WRONG: key2 at same level as dash

    With offset=2 and sequence_dash_offset=2, it writes:
      - key1: val
        key2: val  ← CORRECT: key2 indented under dash
    """
    ry = YAML()
    ry.preserve_quotes = True
    ry.width = 10000
    ry.best_sequence_indent = 2
    ry.best_sequence_dash_offset = 2
    ry.best_map_flow_style = False
    return ry


def validate_yaml(filepath):
    """Return True if file parses cleanly with pyyaml."""
    import yaml
    try:
        yaml.safe_load(filepath.read_text(encoding='utf-8'))
        return True
    except Exception:
        return False


def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')


def find_yaml(plant_slug, plant_name):
    for c in [SEEDS_DIR / f"{plant_slug}-data.yml",
              SEEDS_DIR / f"{plant_slug}.yml",
              SEEDS_DIR / f"{plant_slug}.data.yml"]:
        if c.exists():
            return c
    hits = list(SEEDS_DIR.glob(f"{plant_slug}*.yml"))
    if hits:
        return hits[0]
    name_slug = slugify(plant_name)
    if name_slug != plant_slug:
        for c in [SEEDS_DIR / f"{name_slug}-data.yml",
                  SEEDS_DIR / f"{name_slug}.yml"]:
            if c.exists():
                return c
        hits = list(SEEDS_DIR.glob(f"{name_slug}*.yml"))
        if hits:
            return hits[0]
    return None


# ── STEP 1: SAFE NAME EXTRACTION ─────────────────────────────────────────────

def extract_name(raw):
    s = raw.strip()
    s = re.sub(r'\s*\([A-Z][a-z]+ [a-z]+[^)]*\)', '', s).strip()
    for sep in [' \u2014 ', ' -- ']:
        if sep in s:
            s = s.split(sep)[0].strip()
            break
    return s


# ── NORMALIZATION TABLE ───────────────────────────────────────────────────────

NORMALIZATION_TABLE = {
    "beach sunflower":          "Beach Sunflower",
    "trout lily":               "Trout Lily",
    "purple coneflower":        "Purple Coneflower",
    "oakleaf hydrangea":        "Oakleaf Hydrangea",
    "prickly pear":             "Prickly Pear",
    "red maple":                "Red Maple",
    "red-osier dogwood":        "Red Osier Dogwood",
    "solomon seal":             "Solomon's Seal",
    "echinacea purpurea (purple coneflower)": "Echinacea",
    "monarda fistulosa (wild bergamot)": "Wild Bergamot",
    "lemon grass":              "Lemongrass",
    "sea grape":                "Seagrape",
    "cocoplum":                 "Coco Plum",
    "goumi berry":              "Goumi",
    "black elderberry":         "Elderberry",
    "sea almond":               "Tropical Almond",
    "carambola tree":           "Carambola",
    "jakfruit":                 "Jackfruit",
    "bananas":                  "Banana",
    "carrots":                  "Carrot",
    "potatoes":                 "Potato",
    "tomatoes":                 "Tomato",
    "peppers":                  "Bell Pepper",
    "roses":                    "Roselle",
    "ferns":                    "Cinnamon Fern",
    "sunflowers":               "Sunflower",
    "strawberries":             "Strawberry",
    "beans":                    "Fava Bean",
    "cucumbers":                "Cucumber",
    "brassicas":                "Broccoli",
    "hostas":                   "Hosta",
    "chive":                    "Chives",
    "solidago canadensis":      "Goldenrod",
    "american beautyberry":     "Beautyberry",
    "narrowleaf sunflower":     "Narrowleaf Sunflower",
    "showy partridge pea":      "Partridge Pea",
    "marsh blazingstar":        "Dense Blazingstar",
    "syzygium australe":        "Brush Cherry",
    "southern dewberry":        "Dewberry",
    "southern hackberry":       "Sugar Hackberry",
    "red mombin":               "Spanish Plum",
    "golden apple":             "June Plum",
    "ice cream bean":           "Ice Cream Bean Tree",
    "seaberry":                 "Sea Buckthorn",
    "beech":                    "American Beech",
}


# ── CATEGORY PATTERNS ─────────────────────────────────────────────────────────

CATEGORY_SUBSTRINGS = [
    ' tolerant', 'understory', ' guild', ' herbs', ' grasses', ' species',
    'systems only', 'contained', 'associates', 'philosophy',
    'cover crop', 'groundcover', 'trellis trees', 'nitrogen companions',
    'nothing fragile', 'strong trellis', 'edge plants', 'coastal scrub',
    'scrub species', 'annual legume', 'wet meadow', 'ornamental grass',
    'shade grasses', 'lavender cotton', 'perennial vine',
    'fragile the vine', 'managed for', 'restoration mix', 'mulch circles',
    'pollinator strips', 'small grains', 'shade trees', 'desert legumes',
    'living trellis', 'host insects', 'best grown alone',
]

ECOSYSTEM_EXACT = {'fish', 'duck', 'azolla', 'duckweed', 'koi'}
ECOSYSTEM_STARTS = ['aquaponic', 'fish that', 'duck ', 'azolla (', 'duckweed (']

JUNK_PATTERNS = [
    r'^\s*$', r'^none\b', r'^n/a\b', r'^tbd\b', r'^needs.?data',
    r'^none outdoors', r'^none documented',
]

VERB_RE = re.compile(
    r'\b(shares|uses|provides|fixes|grows|tolerates|handles|reduces|supports|'
    r'adds|helps|creates|marks|makes|fills|holds|knits|feeds|stabilizes|signals|'
    r'defines|extend|occupy|manage|improve|prevent|thrive|accepts|builds|capture|'
    r'filters|protect|reads|expect|demand|complements|contrasts|mirrors|matches|'
    r'pairs|layers|staggered|attracts|repels|suppresses)\b',
    re.IGNORECASE
)


# ── STEP 2: RESOLUTION PIPELINE ──────────────────────────────────────────────

def resolve(raw, slug_index, name_index, aka_index):
    original  = raw.strip()
    candidate = extract_name(original)
    cand_lower = candidate.lower().strip()
    cand_slug  = slugify(candidate)

    for pat in JUNK_PATTERNS:
        if re.match(pat, candidate, re.IGNORECASE):
            return 'CATEGORY', {'name': candidate, 'original': original, 'type': 'junk'}

    if cand_lower in ECOSYSTEM_EXACT:
        return 'CATEGORY', {'name': candidate, 'original': original, 'type': 'ecosystem'}
    for prefix in ECOSYSTEM_STARTS:
        if cand_lower.startswith(prefix):
            return 'CATEGORY', {'name': candidate, 'original': original, 'type': 'ecosystem'}

    for term in CATEGORY_SUBSTRINGS:
        if term.lower() in cand_lower:
            return 'CATEGORY', {'name': candidate, 'original': original, 'type': 'system'}

    # Direct slug match
    if cand_slug in slug_index:
        return 'RESOLVED', {'slug': cand_slug, 'name': slug_index[cand_slug], 'original': original}

    # Name match
    nm = name_index.get(cand_lower)
    if nm:
        return 'RESOLVED', {'slug': nm, 'name': slug_index[nm], 'original': original}

    # AKA match
    aka_m = aka_index.get(cand_lower)
    if aka_m:
        return 'RESOLVED', {'slug': aka_m, 'name': slug_index[aka_m], 'original': original}

    # Normalization table
    norm_target = NORMALIZATION_TABLE.get(cand_lower) or NORMALIZATION_TABLE.get(original.lower().strip())
    if norm_target:
        norm_slug = name_index.get(norm_target.lower())
        if norm_slug:
            return 'NORMALIZED', {'slug': norm_slug, 'name': norm_target, 'original': original}
        return 'UNRESOLVED', {'name': norm_target, 'original': original, 'note': 'normalization_target_not_in_index'}

    # Heuristic
    words     = candidate.split()
    has_verb  = bool(VERB_RE.search(candidate))
    has_comma = ',' in candidate
    too_long  = len(words) > 6
    has_prose = bool(re.search(r'\w \u2014 \w|\w -- \w', candidate))

    if has_verb or has_comma or too_long or has_prose:
        return 'CATEGORY', {'name': candidate, 'original': original, 'type': 'system'}

    return 'UNRESOLVED', {'name': candidate, 'original': original}


# ── STEP 3: PROCESS YAML FILE ─────────────────────────────────────────────────

def process_yaml(filepath, plant_name, unresolved_strings,
                 slug_index, name_index, aka_index,
                 dry_run, stats, verbose):
    import yaml as pyyaml

    # Validate before touching
    if not validate_yaml(filepath):
        print(f"  ⚠️  Skipping {filepath.name} — already broken before edit")
        return False

    ryaml = make_ryaml()
    try:
        text = filepath.read_text(encoding='utf-8')
        data = ryaml.load(io.StringIO(text))
    except Exception as e:
        print(f"  ⚠️  ruamel parse error {filepath.name}: {e}")
        return False

    if not isinstance(data, (dict, list)):
        return False

    items = data if isinstance(data, list) else [data]
    changed = False

    for item in items:
        if not isinstance(item, dict):
            continue
        if len(items) > 1 and item.get('common_name', '').lower() != plant_name.lower():
            continue

        current = list(item.get('companions', []) or [])
        resolved_companions = [c for c in current if isinstance(c, dict) and c.get('slug')]
        legacy_strings      = [c for c in current if isinstance(c, str) and c.strip()]
        existing_slugs      = {c['slug'] for c in resolved_companions}

        normalized_companions = list(item.get('companions_normalized', []) or [])
        unresolved_companions  = list(item.get('companions_unresolved', []) or [])
        category_companions    = list(item.get('companion_categories', []) or [])

        # Normalize: unresolved_strings may contain dicts {name,original} or strings
        def to_raw(item):
            if isinstance(item, dict):
                return item.get('original') or item.get('name') or str(item)
            return str(item)

        all_strings = [to_raw(s) for s in unresolved_strings]
        for s in legacy_strings:
            raw_s = to_raw(s)
            if raw_s not in all_strings:
                all_strings.append(raw_s)

        seen = set()

        for raw in all_strings:
            if raw in seen:
                continue
            seen.add(raw)

            bucket, result = resolve(raw, slug_index, name_index, aka_index)
            stats[bucket] += 1

            if bucket == 'RESOLVED':
                slug = result['slug']
                if slug not in existing_slugs:
                    resolved_companions.append({'slug': slug, 'name': result['name']})
                    existing_slugs.add(slug)
                    stats['resolved_promoted'] += 1
                    if verbose:
                        print(f"    ✅ RESOLVED:    '{raw}' → {slug}")

            elif bucket == 'NORMALIZED':
                slug = result['slug']
                if slug not in existing_slugs:
                    resolved_companions.append({'slug': slug, 'name': result['name']})
                    existing_slugs.add(slug)
                    stats['normalized_promoted'] += 1
                already = any(n.get('original') == result['original'] for n in normalized_companions)
                if not already:
                    normalized_companions.append({
                        'original': result['original'],
                        'resolved_slug': slug,
                        'name': result['name'],
                    })
                if verbose:
                    print(f"    🔄 NORMALIZED: '{raw}' → {slug}")

            elif bucket == 'UNRESOLVED':
                already = any(u.get('original') == result['original']
                              or u.get('name') == result['name']
                              for u in unresolved_companions)
                if not already:
                    entry = {'name': result['name'], 'original': result['original']}
                    if result.get('note'):
                        entry['note'] = result['note']
                    unresolved_companions.append(entry)
                if verbose:
                    print(f"    🔍 UNRESOLVED: '{raw}' → '{result['name']}'")

            elif bucket == 'CATEGORY':
                already = any(c.get('original') == result['original'] for c in category_companions)
                if not already:
                    category_companions.append({
                        'name': result['name'],
                        'original': result['original'],
                        'type': result.get('type', 'system'),
                    })
                if verbose:
                    print(f"    📂 CATEGORY:   '{raw}' (type: {result.get('type')})")

        item['companions'] = resolved_companions

        if normalized_companions:
            item['companions_normalized'] = normalized_companions
        elif 'companions_normalized' in item:
            del item['companions_normalized']

        if unresolved_companions:
            item['companions_unresolved'] = unresolved_companions
        elif 'companions_unresolved' in item:
            del item['companions_unresolved']

        if category_companions:
            item['companion_categories'] = category_companions
        elif 'companion_categories' in item:
            del item['companion_categories']

        if 'companion_ecosystem' in item:
            del item['companion_ecosystem']

        changed = True
        break

    if not changed:
        return False

    if dry_run:
        return True

    # Write and validate
    out = io.StringIO()
    ryaml.dump(data, out)
    new_text = out.getvalue()

    # Post-write validation — parse with pyyaml before committing
    try:
        pyyaml.safe_load(new_text)
    except Exception as e:
        print(f"  ❌ WRITE ABORTED {filepath.name} — output would be invalid: {e}")
        return False

    filepath.write_text(new_text, encoding='utf-8')
    return True


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Companion resolution pipeline v3')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--report', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--targets', nargs='+',
                        help='Process only specific plant names')
    args = parser.parse_args()

    if args.dry_run:
        print("\n🔍 DRY RUN — no files will be written\n")

    plants = json.loads(PLANTS_JSON.read_text())
    slug_index  = {p['slug']: p['common_name'] for p in plants}
    name_index  = {p['common_name'].lower(): p['slug'] for p in plants}
    aka_index   = {}
    for p in plants:
        for aka in (p.get('aka') or []):
            aka_index[str(aka).lower().strip()] = p['slug']

    print(f"🌱 Plant index: {len(slug_index)} plants, {len(aka_index)} aka entries")

    affected = [p for p in plants if p.get('companions_unresolved')]
    if args.targets:
        target_set = {t.lower() for t in args.targets}
        affected = [p for p in affected if p['common_name'].lower() in target_set]

    total = sum(len(p['companions_unresolved']) for p in affected)
    print(f"📋 Plants to process: {len(affected)}")
    print(f"📋 Total unresolved strings: {total}")
    print("=" * 55)

    stats = Counter({
        'RESOLVED': 0, 'NORMALIZED': 0, 'UNRESOLVED': 0, 'CATEGORY': 0,
        'resolved_promoted': 0, 'normalized_promoted': 0,
    })
    files_changed   = 0
    files_aborted   = 0
    files_not_found = []

    for plant in affected:
        filepath = find_yaml(plant['slug'], plant['common_name'])
        if not filepath:
            files_not_found.append(plant['common_name'])
            continue

        if args.verbose:
            print(f"\n🌿 {plant['common_name']} ({len(plant['companions_unresolved'])} strings)")

        result = process_yaml(
            filepath, plant['common_name'], plant['companions_unresolved'],
            slug_index, name_index, aka_index,
            args.dry_run, stats, args.verbose
        )
        if result is True:
            files_changed += 1
        elif result is False and not args.dry_run:
            files_aborted += 1

    total_classified = sum(stats[b] for b in ['RESOLVED','NORMALIZED','UNRESOLVED','CATEGORY'])
    print(f"\n📊 Results ({total_classified} total):")
    print(f"  {'RESOLVED':<22} {stats['RESOLVED']:>5}  (promoted: {stats['resolved_promoted']})")
    print(f"  {'NORMALIZED':<22} {stats['NORMALIZED']:>5}  (promoted: {stats['normalized_promoted']})")
    print(f"  {'UNRESOLVED':<22} {stats['UNRESOLVED']:>5}  → companions_unresolved")
    print(f"  {'CATEGORY':<22} {stats['CATEGORY']:>5}  → companion_categories")
    print(f"\n  Files changed:   {files_changed}")
    if files_aborted:
        print(f"  Files aborted:   {files_aborted}  ← ruamel produced invalid YAML, originals preserved")
    if files_not_found:
        print(f"  Files not found: {len(files_not_found)}")
        for n in sorted(files_not_found):
            print(f"    {n}")

    if args.report:
        print(f"\n── UNRESOLVED (unique names) ───────────────────────")
        seen = set()
        for p in affected:
            for raw in p.get('companions_unresolved', []):
                _, result = resolve(raw, slug_index, name_index, aka_index)
                name = result.get('name', raw)
                if name not in seen:
                    seen.add(name)
                    print(f"  {name}")

    if args.dry_run:
        print("\n✅ Dry run complete — no files written")
        return

    print("\n✅ Done — run ./sync.sh to rebuild JSON")


if __name__ == '__main__':
    main()
