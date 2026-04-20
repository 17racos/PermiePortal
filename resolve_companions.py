#!/usr/bin/env python3
"""
resolve_companions.py v4
========================
Companion cleanup pipeline — four-bucket, zero data loss.

Changes in v4:
  - Normalization table audited: removed all generic→specific mappings
  - Added GENERICS set: terms that must go to UNRESOLVED, never forced to a slug
  - Duplicate safety: dedup by slug only, preserve provenance
  - Strict no-assumption rule enforced in classify logic
  - Post-write YAML validation (ruamel bug guard)

Buckets:
  RESOLVED    — direct slug or name or aka match in plant index
  NORMALIZED  — safe alias/variant/plural/spelling match (traceable)
  UNRESOLVED  — valid plant-like name, not resolvable (preserved as {name, original})
  CATEGORY    — non-plant: system description, ecosystem entity, junk

Safety rules:
  - NEVER resolve a generic term to a specific species
  - NEVER drop input data
  - NEVER guess a slug from ecological context
  - Normalization ONLY for: plurals of same plant, spelling variants, known aliases

Run:
  python3 resolve_companions.py --dry-run           # no writes
  python3 resolve_companions.py --dry-run --report  # + full bucket breakdown
  python3 resolve_companions.py                     # write + validate YAML
  python3 resolve_companions.py --verbose           # per-plant detail
  python3 resolve_companions.py --targets "Plant A" "Plant B"
"""

import re
import io
import json
import argparse
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
    ruamel instance with correct sequence indent settings.
    best_sequence_dash_offset=2 prevents the indent bug where dict keys
    in sequences are written at the wrong level.
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
    """
    Extract candidate plant name from annotated string.
    - Strip scientific names in parens: (Genus species)
    - Split ONLY on ' — ' or ' -- ' (not ' - ')
    - Preserve original for traceability
    """
    s = raw.strip()
    s = re.sub(r'\s*\([A-Z][a-z]+ [a-z]+[^)]*\)', '', s).strip()
    for sep in [' \u2014 ', ' -- ']:
        if sep in s:
            s = s.split(sep)[0].strip()
            break
    return s


# ── NORMALIZATION TABLE ───────────────────────────────────────────────────────
# STRICT RULES:
#   ✅ Allowed: plural→singular of SAME plant, spelling variant, known alias,
#               scientific name→common name, formatting variant
#   ❌ NOT allowed: generic→specific species, ecological inference,
#                  crop group→single species, "best match" guessing
#
# Each entry must have a comment explaining WHY the mapping is safe.

NORMALIZATION_TABLE = {
    # Case / punctuation variants (safe: same plant, different formatting)
    "beach sunflower":          "Beach Sunflower",
    "trout lily":               "Trout Lily",
    "purple coneflower":        "Purple Coneflower",
    "oakleaf hydrangea":        "Oakleaf Hydrangea",
    "prickly pear":             "Prickly Pear",
    "red maple":                "Red Maple",
    "red-osier dogwood":        "Red Osier Dogwood",
    "solomon seal":             "Solomon's Seal",         # missing apostrophe

    # Scientific name → common name (safe: unambiguous 1:1 mapping)
    "echinacea purpurea (purple coneflower)": "Echinacea",
    "monarda fistulosa (wild bergamot)": "Wild Bergamot",
    "solidago canadensis":      "Goldenrod",

    # Spacing / hyphen variants (safe: same plant)
    "lemon grass":              "Lemongrass",
    "sea grape":                "Seagrape",
    "cocoplum":                 "Coco Plum",

    # Known aliases (safe: documented common name synonyms)
    "goumi berry":              "Goumi",
    "sea almond":               "Tropical Almond",        # Terminalia catappa
    "seaberry":                 "Sea Buckthorn",
    "red mombin":               "Spanish Plum",           # Spondias purpurea
    "golden apple":             "June Plum",              # Spondias dulcis

    # Descriptor variants — same species (safe)
    "carambola tree":           "Carambola",
    "jakfruit":                 "Jackfruit",              # spelling variant
    "ice cream bean":           "Ice Cream Bean Tree",

    # Safe plurals — unambiguous same plant
    "bananas":                  "Banana",
    "carrots":                  "Carrot",
    "potatoes":                 "Potato",
    "tomatoes":                 "Tomato",
    "sunflowers":               "Sunflower",
    "cucumbers":                "Cucumber",
    "chive":                    "Chives",                 # singular→plural

    # Safe descriptor variants
    "american beautyberry":     "Beautyberry",
    "narrowleaf sunflower":     "Narrowleaf Sunflower",
    "syzygium australe":        "Brush Cherry",
    "southern dewberry":        "Dewberry",

    # REMOVED — were unsafe:
    # "peppers" → "Bell Pepper"       ❌ generic plural → specific species
    # "roses" → "Roselle"             ❌ WRONG: Rose ≠ Roselle
    # "ferns" → "Cinnamon Fern"       ❌ generic → specific
    # "beans" → "Fava Bean"           ❌ generic → specific
    # "brassicas" → "Broccoli"        ❌ genus group → specific
    # "marsh blazingstar" → "Dense Blazingstar"  ❌ different species
    # "black elderberry" → "Elderberry"  ❌ lossy (specific→generic)
    # "beech" → "American Beech"      ❌ generic → specific
    # "southern hackberry" → "Sugar Hackberry"  ❌ regional→specific (verify needed)
    # "showy partridge pea" → "Partridge Pea"  ❌ different variety (verify needed)
    # "strawberries" → "Strawberry"   removed — verify Strawberry is in index
}

# ── GENERICS SET ─────────────────────────────────────────────────────────────
# These terms are valid ecological references but too broad to map to a single
# plant slug. They MUST go to UNRESOLVED, never forced to a specific species.
# Do NOT add these to the normalization table.

GENERICS = frozenset({
    # Crop groups
    'corn', 'bean', 'beans', 'pea', 'peas', 'grain', 'grains',
    'clover', 'fern', 'ferns', 'grass', 'grasses',
    'rose', 'roses', 'pepper', 'peppers', 'brassica', 'brassicas',
    'oak', 'maple', 'pine', 'fir', 'spruce', 'birch', 'elm', 'hickory',
    'willow', 'magnolia', 'dogwood', 'hawthorn', 'serviceberry',
    'blueberry', 'blackberry', 'raspberry', 'currant', 'grape', 'grapes',
    'citrus', 'peach', 'pear', 'plum', 'cherry', 'apple',
    'sunflower', 'marigold', 'lavender', 'sage', 'thyme', 'oregano',
    'basil', 'mint', 'rosemary', 'chamomile', 'yarrow',
    'squash', 'pumpkin', 'cucumber', 'melon',
    'tomato', 'eggplant', 'potato', 'carrot', 'beet', 'turnip',
    'lettuce', 'spinach', 'kale', 'cabbage', 'broccoli',
    'mushroom', 'fungus', 'lichen', 'moss',
    'vegetables', 'herbs', 'legumes', 'grains',
    # Genus-level concepts that map to multiple species in the index
    'echinacea', 'salvia', 'rudbeckia', 'liatris', 'solidago',
    'baptisia', 'verbena', 'penstemon', 'aster', 'goldenrod',
    'milkweed', 'ironweed', 'coneflower',
})


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
    """
    Strict resolution pipeline. Returns (bucket, result_dict).

    Order:
    1. Junk check
    2. Ecosystem check
    3. Category substring check
    4. GENERICS check → UNRESOLVED (no species inference)
    5. Direct slug match → RESOLVED
    6. Name match → RESOLVED
    7. AKA match → RESOLVED
    8. Normalization table → NORMALIZED (safe transforms only)
    9. Prose/verb heuristic → CATEGORY
    10. Default → UNRESOLVED (safe fallback)
    """
    original   = raw.strip()
    candidate  = extract_name(original)
    cand_lower = candidate.lower().strip()
    cand_slug  = slugify(candidate)

    # 1. Junk
    for pat in JUNK_PATTERNS:
        if re.match(pat, candidate, re.IGNORECASE):
            return 'CATEGORY', {
                'name': candidate, 'original': original, 'type': 'junk'
            }

    # 2. Ecosystem
    if cand_lower in ECOSYSTEM_EXACT:
        return 'CATEGORY', {
            'name': candidate, 'original': original, 'type': 'ecosystem'
        }
    for prefix in ECOSYSTEM_STARTS:
        if cand_lower.startswith(prefix):
            return 'CATEGORY', {
                'name': candidate, 'original': original, 'type': 'ecosystem'
            }

    # 3. Category substrings
    for term in CATEGORY_SUBSTRINGS:
        if term.lower() in cand_lower:
            return 'CATEGORY', {
                'name': candidate, 'original': original, 'type': 'system'
            }

    # 4. GENERICS — valid ecological reference but too broad to force a slug
    #    Send directly to UNRESOLVED. Do NOT attempt normalization or slug match.
    if cand_lower in GENERICS:
        return 'UNRESOLVED', {
            'name': candidate, 'original': original,
            'note': 'generic_term'
        }

    # 5. Direct slug match
    if cand_slug in slug_index:
        return 'RESOLVED', {
            'slug': cand_slug,
            'name': slug_index[cand_slug],
            'original': original,
        }

    # 6. Case-insensitive name match
    nm = name_index.get(cand_lower)
    if nm:
        return 'RESOLVED', {
            'slug': nm,
            'name': slug_index[nm],
            'original': original,
        }

    # 7. AKA match (from plant index aka fields)
    aka_m = aka_index.get(cand_lower)
    if aka_m:
        return 'RESOLVED', {
            'slug': aka_m,
            'name': slug_index[aka_m],
            'original': original,
        }

    # 8. Normalization table (safe transforms only)
    norm_target = (
        NORMALIZATION_TABLE.get(cand_lower)
        or NORMALIZATION_TABLE.get(original.lower().strip())
    )
    if norm_target:
        norm_slug = name_index.get(norm_target.lower())
        if norm_slug:
            return 'NORMALIZED', {
                'slug': norm_slug,
                'name': norm_target,
                'original': original,
            }
        # Normalization target not in index → preserve in UNRESOLVED
        return 'UNRESOLVED', {
            'name': norm_target,
            'original': original,
            'note': 'normalization_target_not_in_index',
        }

    # 9. Prose / verb heuristic → CATEGORY
    words     = candidate.split()
    has_verb  = bool(VERB_RE.search(candidate))
    has_comma = ',' in candidate
    too_long  = len(words) > 6
    has_prose = bool(re.search(r'\w \u2014 \w|\w -- \w', candidate))

    if has_verb or has_comma or too_long or has_prose:
        return 'CATEGORY', {
            'name': candidate, 'original': original, 'type': 'system'
        }

    # 10. Default: valid plant-like name, not resolvable → UNRESOLVED
    return 'UNRESOLVED', {
        'name': candidate,
        'original': original,
    }


# ── STEP 3: PROCESS YAML FILE ─────────────────────────────────────────────────

def to_raw(item):
    """Normalize: unresolved entries may be dicts or strings."""
    if isinstance(item, dict):
        return item.get('original') or item.get('name') or str(item)
    return str(item)


def process_yaml(filepath, plant_name, unresolved_strings,
                 slug_index, name_index, aka_index,
                 dry_run, stats, verbose):
    import yaml as pyyaml

    if not validate_yaml(filepath):
        print(f"  ⚠️  Skipping {filepath.name} — already invalid before edit")
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

        # Separate existing resolved dicts from legacy strings in companions
        current = list(item.get('companions', []) or [])
        resolved_companions = [c for c in current
                               if isinstance(c, dict) and c.get('slug')]
        legacy_strings      = [c for c in current
                               if isinstance(c, str) and c.strip()]

        # Dedup by slug (slug is the canonical key, not raw string)
        existing_slugs = {}  # slug → first-seen name
        deduped_resolved = []
        for c in resolved_companions:
            slug = c['slug']
            if slug not in existing_slugs:
                existing_slugs[slug] = c['name']
                deduped_resolved.append(c)
            # Duplicate slug: silently skip (slug already in graph)

        resolved_companions = deduped_resolved

        normalized_companions = list(item.get('companions_normalized', []) or [])
        unresolved_companions  = list(item.get('companions_unresolved', []) or [])
        category_companions    = list(item.get('companion_categories', []) or [])

        # Build processing list from unresolved_strings + legacy strings
        all_raws = [to_raw(s) for s in unresolved_strings]
        for s in legacy_strings:
            r = to_raw(s)
            if r not in all_raws:
                all_raws.append(r)

        seen_originals = set()

        for raw in all_raws:
            if raw in seen_originals:
                continue
            seen_originals.add(raw)

            bucket, result = resolve(raw, slug_index, name_index, aka_index)
            stats[bucket] += 1

            if bucket == 'RESOLVED':
                slug = result['slug']
                if slug not in existing_slugs:
                    resolved_companions.append({
                        'slug': slug,
                        'name': result['name'],
                    })
                    existing_slugs[slug] = result['name']
                    stats['resolved_promoted'] += 1
                    if verbose:
                        print(f"    ✅ RESOLVED:    '{raw}' → {slug}")
                # Duplicate slug: no re-add, no error

            elif bucket == 'NORMALIZED':
                slug = result['slug']
                if slug not in existing_slugs:
                    resolved_companions.append({
                        'slug': slug,
                        'name': result['name'],
                    })
                    existing_slugs[slug] = result['name']
                    stats['normalized_promoted'] += 1
                # Always record normalization for traceability
                already = any(n.get('original') == result['original']
                              for n in normalized_companions)
                if not already:
                    normalized_companions.append({
                        'original': result['original'],
                        'resolved_slug': slug,
                        'name': result['name'],
                    })
                if verbose:
                    print(f"    🔄 NORMALIZED: '{raw}' → {slug} ({result['name']})")

            elif bucket == 'UNRESOLVED':
                # Preserve: dedup by name to avoid repeated entries
                already = any(
                    u.get('original') == result['original']
                    or u.get('name') == result['name']
                    for u in unresolved_companions
                )
                if not already:
                    entry = {
                        'name': result['name'],
                        'original': result['original'],
                    }
                    if result.get('note'):
                        entry['note'] = result['note']
                    unresolved_companions.append(entry)
                if verbose:
                    note = f" [{result.get('note','')}]" if result.get('note') else ''
                    print(f"    🔍 UNRESOLVED: '{raw}' → '{result['name']}'{note}")

            elif bucket == 'CATEGORY':
                already = any(c.get('original') == result['original']
                              for c in category_companions)
                if not already:
                    category_companions.append({
                        'name': result['name'],
                        'original': result['original'],
                        'type': result.get('type', 'system'),
                    })
                if verbose:
                    print(f"    📂 CATEGORY:   '{raw}' [{result.get('type')}]")

        # Write back — only set fields if populated
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

        # Remove legacy field
        if 'companion_ecosystem' in item:
            del item['companion_ecosystem']

        changed = True
        break

    if not changed or dry_run:
        return changed

    # Write with post-write validation
    out = io.StringIO()
    ryaml.dump(data, out)
    new_text = out.getvalue()

    import yaml as pyyaml
    try:
        pyyaml.safe_load(new_text)
    except Exception as e:
        print(f"  ❌ WRITE ABORTED {filepath.name} — invalid output: {e}")
        return False

    filepath.write_text(new_text, encoding='utf-8')
    return True


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Companion resolution pipeline v4')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--report', action='store_true',
                        help='Print full unresolved name list')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--targets', nargs='+',
                        help='Process only specific plant names')
    args = parser.parse_args()

    if args.dry_run:
        print("\n🔍 DRY RUN — no files will be written\n")

    plants     = json.loads(PLANTS_JSON.read_text())
    slug_index = {p['slug']: p['common_name'] for p in plants}
    name_index = {p['common_name'].lower(): p['slug'] for p in plants}
    aka_index  = {}
    for p in plants:
        for aka in (p.get('aka') or []):
            aka_index[str(aka).lower().strip()] = p['slug']

    print(f"🌱 Plant index: {len(slug_index)} plants, {len(aka_index)} aka entries")

    affected = [p for p in plants if p.get('companions_unresolved')]
    if args.targets:
        target_set = {t.lower() for t in args.targets}
        affected = [p for p in affected
                    if p['common_name'].lower() in target_set]

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
    all_unresolved_names = set()

    for plant in affected:
        filepath = find_yaml(plant['slug'], plant['common_name'])
        if not filepath:
            files_not_found.append(plant['common_name'])
            continue

        if args.verbose:
            print(f"\n🌿 {plant['common_name']} ({len(plant['companions_unresolved'])} strings)")

        if args.report:
            for raw in plant['companions_unresolved']:
                r = to_raw(raw)
                _, result = resolve(r, slug_index, name_index, aka_index)
                if result.get('name'):
                    all_unresolved_names.add(
                        (result['name'], result.get('note', ''))
                    )

        result = process_yaml(
            filepath, plant['common_name'], plant['companions_unresolved'],
            slug_index, name_index, aka_index,
            args.dry_run, stats, args.verbose
        )
        if result is True:
            files_changed += 1
        elif result is False and not args.dry_run:
            files_aborted += 1

    # Summary
    total_classified = sum(
        stats[b] for b in ['RESOLVED', 'NORMALIZED', 'UNRESOLVED', 'CATEGORY']
    )
    print(f"\n📊 Results ({total_classified} total):")
    print(f"  {'RESOLVED':<22} {stats['RESOLVED']:>5}  "
          f"(added to companions: {stats['resolved_promoted']})")
    print(f"  {'NORMALIZED':<22} {stats['NORMALIZED']:>5}  "
          f"(promoted + traced: {stats['normalized_promoted']})")
    print(f"  {'UNRESOLVED':<22} {stats['UNRESOLVED']:>5}  "
          f"→ companions_unresolved (preserved)")
    print(f"  {'CATEGORY':<22} {stats['CATEGORY']:>5}  "
          f"→ companion_categories (preserved)")
    print(f"\n  Files changed:   {files_changed}")
    if files_aborted:
        print(f"  Files aborted:   {files_aborted}  (originals preserved)")
    if files_not_found:
        print(f"  Files not found: {len(files_not_found)}")
        for n in sorted(files_not_found):
            print(f"    {n}")

    if args.report and all_unresolved_names:
        print(f"\n── UNRESOLVED names ({len(all_unresolved_names)}) ──────────────")
        for name, note in sorted(all_unresolved_names):
            tag = f" [{note}]" if note else ""
            print(f"  {name}{tag}")

    if args.dry_run:
        print("\n✅ Dry run complete — no files written")
        return

    print("\n✅ Done — run ./sync.sh to rebuild JSON")


if __name__ == '__main__':
    main()
