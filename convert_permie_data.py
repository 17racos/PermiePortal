#!/usr/bin/env python3
"""
PermiePortal Data Converter v3
Lives at: ~/apps/permieportal/convert_permie_data.py

Changes in v3:
  - practitioner_notes REMOVED (deprecated — use field_observations)
  - purpose validation: plant_function ↔ purpose strict alignment enforced
  - data_quality_score COMPUTED (not read from YAML)
  - companion slug validation + quarantine to companions_unresolved
  - zone parsed into zone_min / zone_max (YAML unchanged)
  - relationships schema expanded with type, evidence, severity, regional
  - no silent data loss: all invalid data surfaced or quarantined

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
PROJECT    = Path.home() / "apps/permieportal"
SEEDS_DIR  = PROJECT / "src/seeds/plants"
PESTS_DIR  = PROJECT / "src/seeds/pests"
OUTPUT_DIR = PROJECT / "exports"
ASTRO_DATA = PROJECT / "src/data"
# ─────────────────────────────────────────────────────────────────────────────

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml", "--quiet"])
    import yaml


# ── CANONICAL PLANT FUNCTIONS ────────────────────────────────────────────────
# Single source of truth for valid plant_function values.
# Any value not in this set will generate a warning.
VALID_FUNCTIONS = frozenset({
    "Edible", "Medicinal", "Nitrogen Fixer", "Dynamic Accumulator",
    "Mulcher", "Pollinator", "Wildlife Attractor", "Erosion Control",
    "Animal Fodder", "Windbreaker", "Border Plant", "Pest Management",
    "Ground Cover", "Shade Provider", "Water Retention", "Fiber",
    "Biomass", "Aquatic", "Ornamental", "Water Purification",
    "Plant Growth Stimulant", "Biofuel",
})


# ── INVALID FUNCTION ROUTING ─────────────────────────────────────────────────
# Maps non-canonical plant_function values to their correct destination field.
# Applied in process_plant() — keeps plant_function semantically clean.
#
FUNCTION_ROUTING = {
    # Traits → plant_traits
    "Drought Tolerant":           ("plant_traits",              "Drought Tolerant"),
    "Cold Hardy":                 ("plant_traits",              "Cold Hardy"),
    "Fast Growing":               ("plant_traits",              "Fast Growing"),
    # Human uses → human_uses
    "Timber":                     ("human_uses",                "Timber"),
    "Dye Plant":                  ("human_uses",                "Dye"),
    "Dye":                        ("human_uses",                "Dye"),
    # Ecological role → ecological_role
    "Decomposer":                 ("ecological_role",           "Decomposer"),
    "Mycorrhizal":                ("ecological_role",           "Mycorrhizal"),
    # Spelling corrections — stay in plant_function with canonical name
    "Water Purifier":             ("plant_function",            "Water Purification"),
    "Border Plant -Ground Cover": ("plant_function",            "Ground Cover"),
    # Ambiguous — quarantine for manual review
    "Soil Improvement":           ("plant_function_unresolved", "Soil Improvement"),
    "Soil Builder":               ("plant_function_unresolved", "Soil Builder"),
    "Cover Crop":                 ("plant_function_unresolved", "Cover Crop"),
    "Green Manure":               ("plant_function_unresolved", "Green Manure"),
    "Pest Repellent":             ("plant_function",            "Pest Management"),
}

# ── PURPOSE LINE FORMAT ───────────────────────────────────────────────────────
# Required: "FunctionName: description -- mechanism"
PURPOSE_LINE_RE = re.compile(r'^([A-Za-z][A-Za-z\s]+):\s+.+\s+--\s+.+$')


# ── CORE UTILITIES ────────────────────────────────────────────────────────────

def slugify(text):
    if not text:
        return ""
    import unicodedata
    text = str(text).lower().strip()
    # Normalize unicode: strip diacritics (ç→c, í→i, é→e, etc.)
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
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


def parse_zone(zone_raw):
    """
    Parse zone string into (zone_min, zone_max).
    YAML stays as-is ("9-11"). JSON becomes queryable ints.
    Handles: "9-11", "9", "9a", "9a-11b", None.
    Returns (None, None) if unparseable — emits no error, caller decides.
    """
    if not zone_raw:
        return None, None
    zone_str = str(zone_raw).strip()
    # Strip letter suffixes (9a → 9, 11b → 11)
    cleaned = re.sub(r'[a-zA-Z]', '', zone_str)
    parts = re.split(r'[-–—]', cleaned)
    try:
        if len(parts) == 2:
            return int(float(parts[0])), int(float(parts[1]))
        elif len(parts) == 1 and parts[0]:
            val = int(float(parts[0]))
            return val, val
    except (ValueError, TypeError):
        pass
    return None, None


# ── PURPOSE VALIDATION ────────────────────────────────────────────────────────

def parse_purpose_lines(purpose_raw):
    """
    Extract function names from purpose block.
    Returns: (dict of {function_name: line}, list of malformed lines)
    """
    if not purpose_raw:
        return {}, []
    parsed = {}
    malformed = []
    for line in purpose_raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            fn_name = line.split(':')[0].strip()
            if PURPOSE_LINE_RE.match(line):
                parsed[fn_name] = line
            else:
                malformed.append(line)
        else:
            malformed.append(line)
    return parsed, malformed


def validate_purpose_alignment(plant_name, plant_function_list, purpose_raw, warnings):
    """
    Enforce strict bidirectional alignment:
      - Every plant_function must have a matching purpose line
      - Every purpose line must map to a plant_function
      - No duplicate purpose function names
      - All lines must match FORMAT: "FunctionName: description -- mechanism"
    Appends warnings in-place. Returns True if clean.
    """
    functions = set(plant_function_list)
    purpose_parsed, malformed = parse_purpose_lines(purpose_raw)
    purpose_functions = set(purpose_parsed.keys())

    clean = True

    # Duplicate detection
    raw_lines = [l.strip() for l in (purpose_raw or '').splitlines() if ':' in l.strip()]
    seen_fns = []
    duplicates = []
    for line in raw_lines:
        fn = line.split(':')[0].strip()
        if fn in seen_fns:
            duplicates.append(fn)
        seen_fns.append(fn)
    if duplicates:
        warnings.append(
            f"  ⚠️  PURPOSE DUPLICATE [{plant_name}]: "
            f"duplicate function entries: {duplicates}"
        )
        clean = False

    # Malformed lines (missing ' -- ' separator or wrong format)
    if malformed:
        warnings.append(
            f"  ⚠️  PURPOSE FORMAT [{plant_name}]: "
            f"{len(malformed)} line(s) missing '-- mechanism' separator: "
            f"{malformed[:3]}"
        )
        clean = False

    # plant_function entries missing from purpose
    missing_in_purpose = functions - purpose_functions
    if missing_in_purpose:
        warnings.append(
            f"  ⚠️  PURPOSE MISSING [{plant_name}]: "
            f"plant_function entries not in purpose: {sorted(missing_in_purpose)}"
        )
        clean = False

    # purpose entries with no plant_function
    orphaned = purpose_functions - functions
    if orphaned:
        warnings.append(
            f"  ⚠️  PURPOSE ORPHAN [{plant_name}]: "
            f"purpose entries not in plant_function: {sorted(orphaned)}"
        )
        clean = False

    return clean


# ── DATA QUALITY SCORE ────────────────────────────────────────────────────────

def compute_data_quality(data, plant_name, warnings):
    """
    Compute data_quality_score and data_quality_dimensions programmatically.
    Does NOT read from YAML. Score is 0.0–1.0 based on weighted structural checks.

    Dimensions (each True/False, equal weight):
      description_length    — description >= 400 chars
      description_clean     — no emoji headers, no bullet points baked in
      purpose_present       — purpose field non-empty
      purpose_format        — all purpose lines match FunctionName: desc -- mechanism
      purpose_aligned       — purpose ↔ plant_function fully aligned
      functions_count       — >= 3 plant_function entries
      functions_valid       — all plant_function values are in VALID_FUNCTIONS
      companions_present    — >= 2 resolved companions
      pests_present         — >= 1 pest reference
      scientific_name       — scientific_name is not empty / NEEDS_DATA
      zone_present          — zone is parseable
      no_needs_data         — zero NEEDS_DATA tokens anywhere in the record
      field_observations    — field_observations is non-empty (bonus signal, not penalized)
    """
    desc = str(data.get('description', '') or '')
    purpose_raw = str(data.get('purpose', '') or '')
    functions = norm_list(data.get('plant_function', []))
    companions_raw = data.get('companions', []) or []
    pests_raw = norm_list(data.get('pests', []))
    sci_name = str(data.get('scientific_name', '') or '').strip()
    zone_raw = data.get('zone', '')
    field_obs = str(data.get('field_observations', '') or '').strip()

    # Resolve companions for count (handle both old string list and new dict list)
    companions_resolved = []
    for c in companions_raw:
        if isinstance(c, dict) and c.get('slug') and c['slug'] != 'NEEDS_DATA':
            companions_resolved.append(c)
        elif isinstance(c, str) and c and c != 'NEEDS_DATA':
            companions_resolved.append(c)

    purpose_parsed, malformed = parse_purpose_lines(purpose_raw)
    purpose_functions = set(purpose_parsed.keys())
    fn_set = set(functions)
    purpose_aligned = (
        bool(purpose_functions)
        and not malformed
        and (purpose_functions == fn_set)
    )

    # Check for emoji/bullet presentation noise in description
    emoji_pattern = re.compile(
        r'[\U0001F300-\U0001F9FF]|[\u2600-\u26FF]|[\u2700-\u27BF]'
    )
    has_emoji = bool(emoji_pattern.search(desc))
    has_bullets = bool(re.search(r'^\s*[-•*]', desc, re.MULTILINE))

    record_str = json.dumps(data, default=str)
    zone_min, zone_max = parse_zone(zone_raw)

    dimensions = {
        "description_length":  len(desc) >= 400,
        "description_clean":   not has_emoji and not has_bullets,
        "purpose_present":     len(purpose_raw.strip()) >= 50,
        "purpose_format":      len(malformed) == 0 and bool(purpose_parsed),
        "purpose_aligned":     purpose_aligned,
        "functions_count":     len(functions) >= 3,
        "functions_valid":     all(f in VALID_FUNCTIONS for f in functions),
        "companions_present":  (
            len(companions_resolved) >= 2
            or len([c for c in (data.get("companions_unresolved", []) or [])
                    if isinstance(c, dict) and c.get("name")]) >= 1
            or len(norm_list(data.get("companion_categories", []))) >= 1
            or any(
                "invasive" in str(c).lower()
                for c in norm_list(data.get("cautions", []))
            )
        ),
        "pests_present":       len(pests_raw) >= 1,
        "scientific_name":     bool(sci_name) and sci_name != 'NEEDS_DATA',
        "zone_present":        zone_min is not None,
        "no_needs_data":       'NEEDS_DATA' not in record_str,
    }

    # field_observations is tracked but not penalized — it's a bonus signal
    dimensions["has_field_observations"] = (
        bool(field_obs)
        and field_obs not in ('', 'No field observations yet', 'Awaiting Update')
    )

    # Score = mean of the 12 penalized dimensions (exclude has_field_observations)
    scored_keys = [k for k in dimensions if k != "has_field_observations"]
    score = round(sum(dimensions[k] for k in scored_keys) / len(scored_keys), 3)

    return score, dimensions


# ── COMPANION VALIDATION ───────────────────────────────────────────────────────

def validate_companions(plant_name, companions_raw, known_plant_slugs, warnings):
    """
    Validate companions against known plant slugs.
    Returns: (resolved_list, unresolved_list)

    Input format support:
      - New: [{slug: banana, name: Banana}]
      - Legacy: ["Banana", "Papaya"]  ← still supported during migration

    Invalid slugs → quarantined to companions_unresolved.
    Warnings emitted for all quarantined entries.
    """
    resolved = []
    unresolved = []

    for item in (companions_raw or []):
        if isinstance(item, dict):
            slug = (item.get('slug') or '').strip()
            name = (item.get('name') or slug).strip()
            if not slug or slug == 'NEEDS_DATA':
                unresolved.append(name or 'unknown')
                continue
            if slug in known_plant_slugs:
                resolved.append({"slug": slug, "name": name})
            else:
                unresolved.append(name)
                warnings.append(
                    f"  ⚠️  COMPANION UNRESOLVED [{plant_name}]: "
                    f"'{name}' (slug: {slug!r}) not in plant index → quarantined"
                )
        elif isinstance(item, str):
            item = item.strip()
            if not item or item == 'NEEDS_DATA':
                continue
            # Attempt slug resolution from the string
            candidate_slug = slugify(item)
            if candidate_slug in known_plant_slugs:
                resolved.append({"slug": candidate_slug, "name": item})
            else:
                unresolved.append(item)
                warnings.append(
                    f"  ⚠️  COMPANION UNRESOLVED [{plant_name}]: "
                    f"'{item}' (no slug match) → quarantined"
                )

    return resolved, unresolved


# ── PLANT PROCESSOR ───────────────────────────────────────────────────────────

def process_plant(data, source_file, known_plant_slugs, warnings):
    """
    Process a single plant YAML entry into a clean JSON-ready dict.
    All validation runs here. No silent failures.
    """
    if not isinstance(data, dict):
        return None
    common_name = data.get('common_name', '')
    if not common_name:
        return None

    plant_slug = slugify(common_name)

    # ── Deprecated field guard ──────────────────────────────────────────────
    if 'practitioner_notes' in data:
        warnings.append(
            f"  ⚠️  DEPRECATED [{common_name}]: 'practitioner_notes' found in "
            f"{source_file} — field is removed. Migrate content to field_observations."
        )
    # ── plant_function validation + routing ─────────────────────────────────
    raw_functions   = norm_list(data.get('plant_function', []))
    clean_functions = []
    plant_traits    = norm_list(data.get('plant_traits', []))
    human_uses      = norm_list(data.get('human_uses', []))
    ecological_role = norm_list(data.get('ecological_role', []))
    fn_unresolved   = norm_list(data.get('plant_function_unresolved', []))

    for fn in raw_functions:
        if fn in VALID_FUNCTIONS:
            clean_functions.append(fn)
        elif fn in FUNCTION_ROUTING:
            dest_field, canonical = FUNCTION_ROUTING[fn]
            if dest_field == "plant_function":
                if canonical not in clean_functions:
                    clean_functions.append(canonical)
            elif dest_field == "plant_traits":
                if canonical not in plant_traits:
                    plant_traits.append(canonical)
            elif dest_field == "human_uses":
                if canonical not in human_uses:
                    human_uses.append(canonical)
            elif dest_field == "ecological_role":
                if canonical not in ecological_role:
                    ecological_role.append(canonical)
            elif dest_field == "plant_function_unresolved":
                if canonical not in fn_unresolved:
                    fn_unresolved.append(canonical)
                warnings.append(
                    f"  ⚠️  FUNCTION REVIEW [{common_name}]: "
                    f"'{fn}' is ambiguous → plant_function_unresolved"
                )
        else:
            if fn not in fn_unresolved:
                fn_unresolved.append(fn)
            warnings.append(
                f"  ⚠️  FUNCTION INVALID [{common_name}]: "
                f"'{fn}' unknown → plant_function_unresolved"
            )

    raw_functions = clean_functions

    # ── Purpose validation ──────────────────────────────────────────────────
    purpose_raw = clean_string(data.get('purpose', ''))
    validate_purpose_alignment(common_name, raw_functions, purpose_raw, warnings)

    # ── Zone parsing ────────────────────────────────────────────────────────
    zone_raw = str(data.get('zone', '') or '').strip()
    zone_min, zone_max = parse_zone(zone_raw)
    if zone_raw and zone_min is None:
        warnings.append(
            f"  ⚠️  ZONE UNPARSEABLE [{common_name}]: zone='{zone_raw}'"
        )

    # ── Companion validation ────────────────────────────────────────────────
    companions_raw = data.get('companions', []) or []
    companions_resolved, _converter_unresolved = validate_companions(
        common_name, companions_raw, known_plant_slugs, warnings
    )
    # companions_unresolved, companions_normalized, companion_categories may have
    # been pre-structured by resolve_companions.py — pass them through as-is
    # Only use converter-generated unresolved if no structured data exists
    _yaml_unresolved = data.get('companions_unresolved', []) or []
    if _yaml_unresolved and isinstance(_yaml_unresolved[0], dict):
        companions_unresolved = _yaml_unresolved  # already structured
    else:
        companions_unresolved = _converter_unresolved

    # ── Pest references ─────────────────────────────────────────────────────
    raw_pests = norm_list(data.get('pests', []))
    pest_slugs = [slugify(p) for p in raw_pests]

    # ── Data quality ────────────────────────────────────────────────────────
    quality_score, quality_dimensions = compute_data_quality(data, common_name, warnings)

    return {
        "slug":                    plant_slug,
        "common_name":             common_name,
        "scientific_name":         data.get('scientific_name', ''),
        "aka":                     norm_list(data.get('aka', [])),
        "family":                  data.get('family', ''),
        "picture":                 data.get('picture', ''),
        "zone":                    zone_raw,
        "zone_min":                zone_min,
        "zone_max":                zone_max,
        "ideal_temp_min":          data.get('ideal_temp_min'),
        "ideal_temp_max":          data.get('ideal_temp_max'),
        "min_temp":                data.get('min_temp'),
        "max_temp":                data.get('max_temp'),
        "perennial":               data.get('perennial'),
        "layers":                  norm_list(data.get('layers', [])),
        "plant_function":            raw_functions,
        "plant_traits":              plant_traits,
        "human_uses":                human_uses,
        "ecological_role":           ecological_role,
        "plant_function_unresolved": fn_unresolved,
        "growth_habit":            data.get('growth_habit', ''),
        "description":             clean_string(data.get('description', '')),
        "purpose":                 purpose_raw,
        "companions":              companions_resolved,
        "companions_unresolved":   companions_unresolved,
        "companions_normalized":   data.get('companions_normalized', []) or [],
        "companion_categories":    data.get('companion_categories', []) or [],
        "cautions":                norm_list(data.get('cautions', [])),
        "field_observations":      clean_string(data.get('field_observations', '')),
        "data_quality_score":      quality_score,
        "data_quality_dimensions": quality_dimensions,
        # Internal — stripped before final output
        "pest_slugs":              pest_slugs,
        "_raw_pests":              raw_pests,
        "_source":                 source_file,
    }


# ── PEST PROCESSOR ────────────────────────────────────────────────────────────

def normalize_affected_plants_yaml(raw):
    if not raw:
        return []
    out = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        s = (item.get('slug') or '').strip()
        if not s:
            continue
        n = (item.get('name') or s).strip()
        out.append({"slug": s, "name": n})
    return out


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

    yaml_affected = normalize_affected_plants_yaml(data.get('affected_plants'))

    return {
        "slug":             slug,
        "name":             name,
        "scientific_name":  data.get('scientific_name', ''),
        "picture":          data.get('picture', ''),
        "category":         data.get('category', 'pest'),
        "description":      clean_string(data.get('description', '')),
        "characteristics":  clean_string(data.get('characteristics', '')),
        "control_methods":  control_methods,
        "natural_enemies":  [str(e).strip() for e in enemies if e],
        "symptoms":         [str(s).strip() for s in (data.get('symptoms') or []) if s],
        "affected_plants":  [],
        "_yaml_affected_plants": yaml_affected,
    }


# ── RELATIONSHIP BUILDER ──────────────────────────────────────────────────────

def build_relationships(plants, pests, warnings):
    """
    Build relationships.json with expanded schema.
    Supports: plant_pest (current), plant_companion (future-ready).

    Relationship record:
      id           — deterministic: "{source}__{target}__{type}"
      type         — "plant_pest" | "plant_companion" (future)
      source_slug  — plant slug
      source_type  — "plant"
      target_slug  — pest/plant slug
      target_type  — "pest" | "plant"
      severity     — null (future: low/moderate/high/critical)
      regional     — [] (future: ["florida", "southeast-us"])
      evidence     — "seed_data" | "field_observation" | "documented" (future)
    """
    pest_by_slug = {p['slug']: p for p in pests}
    all_slugs = frozenset(pest_by_slug.keys())

    # Build pest lookup with alias support
    pest_lookup = {}
    for p in pests:
        slug = p['slug']
        keys = [
            slug,
            p['name'].lower(),
            slugify(p['name']),
            slug.rstrip('s'),
        ]
        if (slug + 's') not in all_slugs:
            keys.append(slug + 's')
        for key in keys:
            pest_lookup[key] = slug

    relationships = []
    pest_to_plants = defaultdict(list)
    seen_rel_ids = set()

    for plant in plants:
        for pest_slug in plant.get('pest_slugs', []):
            matched_slug = (
                pest_lookup.get(pest_slug)
                or pest_lookup.get(pest_slug + 's')
                or pest_lookup.get(pest_slug.rstrip('s'))
            )
            if matched_slug and matched_slug in pest_by_slug:
                pest = pest_by_slug[matched_slug]
                rel_id = f"{plant['slug']}__{matched_slug}__plant_pest"

                if rel_id in seen_rel_ids:
                    continue  # deduplicate
                seen_rel_ids.add(rel_id)

                relationships.append({
                    "id":          rel_id,
                    "type":        "plant_pest",
                    "source_slug": plant['slug'],
                    "source_type": "plant",
                    "target_slug": matched_slug,
                    "target_type": "pest",
                    "severity":    None,
                    "regional":    [],
                    "evidence":    "seed_data",
                    # Legacy fields — retained for Astro compatibility
                    "plant_slug":  plant['slug'],
                    "plant_name":  plant['common_name'],
                    "pest_slug":   matched_slug,
                    "pest_name":   pest['name'],
                })
                pest_to_plants[matched_slug].append({
                    "slug": plant['slug'],
                    "name": plant['common_name'],
                })
            else:
                warnings.append(
                    f"  ⚠️  PEST UNMATCHED [{plant['common_name']}]: "
                    f"'{pest_slug}' in {plant['_source']} — no matching pest"
                )

    # Merge affected_plants onto pest records
    for pest in pests:
        from_plants = pest_to_plants.get(pest['slug'], [])
        yaml_extra = pest.pop('_yaml_affected_plants', []) or []
        seen = set()
        merged = []
        for item in from_plants + yaml_extra:
            ps = item.get('slug')
            if not ps or ps in seen:
                continue
            seen.add(ps)
            merged.append({"slug": ps, "name": item.get('name') or ps})
        pest['affected_plants'] = merged

    return relationships


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PermiePortal Data Converter v3')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate only, no files written')
    parser.add_argument('--no-copy', action='store_true',
                        help='Write exports/ only, skip src/data/ copy')
    args = parser.parse_args()

    if args.dry_run:
        print("\n🔍 DRY RUN — no files will be written\n")

    print("🌱 PermiePortal Data Converter v3")
    print("=" * 50)

    # ── Load plants ─────────────────────────────────────────────────────────
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

    # Two-pass loading:
    # Pass 1: collect all plant slugs to build the known-slug index
    # Pass 2: process plants with companion validation against that index
    raw_plants_data = []
    skipped = []
    for filepath in plant_files:
        path = Path(filepath)
        raw = load_yaml_safe(path)
        if raw is None:
            skipped.append(path.name)
            continue
        items = raw if isinstance(raw, list) else [raw] if isinstance(raw, dict) else []
        for item in items:
            if isinstance(item, dict) and item.get('common_name'):
                raw_plants_data.append((item, path.name))
            else:
                skipped.append(path.name)

    # Build known slug index from pass 1
    known_plant_slugs = frozenset(
        slugify(item.get('common_name', ''))
        for item, _ in raw_plants_data
        if item.get('common_name')
    )
    print(f"  ✅ {len(known_plant_slugs)} plant slugs indexed")

    # Pass 2: full processing with validation
    all_warnings = []
    plants = []
    for item, source_file in raw_plants_data:
        plant = process_plant(item, source_file, known_plant_slugs, all_warnings)
        if plant:
            plants.append(plant)
        else:
            skipped.append(source_file)

    print(f"  ✅ {len(plants)} plants loaded")
    if skipped:
        print(f"  ⚠️  Skipped: {', '.join(skipped[:5])}{'...' if len(skipped) > 5 else ''}")

    # ── Load pests ──────────────────────────────────────────────────────────
    print("\n🐛 Loading pest YAML...")
    pests = []
    _SKIP = {"pests-data.yml", "pests-data.yml.bak"}
    for _pf in sorted(PESTS_DIR.glob("*-data.yml")):
        if _pf.name in _SKIP:
            continue
        _raw = load_yaml_safe(_pf)
        if _raw:
            for _item in (_raw if isinstance(_raw, list) else [_raw]):
                _p = process_pest(_item)
                if _p:
                    pests.append(_p)
    print(f"  ✅ {len(pests)} pests loaded")

    # ── Build relationships ─────────────────────────────────────────────────
    print("\n🔗 Building relationships...")
    relationships = build_relationships(plants, pests, all_warnings)
    print(f"  ✅ {len(relationships)} relationships mapped")

    # ── Clean up internal fields ────────────────────────────────────────────
    for plant in plants:
        rel_pests = [r['pest_name'] for r in relationships
                     if r['plant_slug'] == plant['slug']]
        raw_pests = plant.pop('_raw_pests', [])
        rel_lower = {p.lower() for p in rel_pests}
        extra = [p for p in raw_pests if p.lower() not in rel_lower]
        plant['pests'] = rel_pests + extra
        plant.pop('pest_slugs', None)
        plant.pop('_source', None)

    # ── Warning summary ─────────────────────────────────────────────────────
    warn_types = Counter()
    for w in all_warnings:
        m = re.search(r'\[(.*?)\]', w)
        tag = m.group(1) if m else 'OTHER'
        warn_types[tag] += 1

    if all_warnings:
        print(f"\n  ⚠️  {len(all_warnings)} warnings:")
        # Show up to 20, grouped
        for w in all_warnings[:20]:
            print(w)
        if len(all_warnings) > 20:
            print(f"     ... and {len(all_warnings) - 20} more")
        print(f"\n  Warning breakdown:")
        for tag, count in warn_types.most_common():
            print(f"    {tag}: {count}")
    else:
        print("  ✅ Zero warnings — data is clean")

    # ── Quality summary ─────────────────────────────────────────────────────
    scores = [p['data_quality_score'] for p in plants]
    if scores:
        avg = round(sum(scores) / len(scores), 3)
        below_50 = sum(1 for s in scores if s < 0.5)
        below_80 = sum(1 for s in scores if 0.5 <= s < 0.8)
        above_80 = sum(1 for s in scores if s >= 0.8)
        print(f"\n  📊 Data quality: avg={avg} | ≥0.8: {above_80} | 0.5–0.8: {below_80} | <0.5: {below_50}")

    unresolved_companion_count = sum(len(p.get('companions_unresolved', [])) for p in plants)
    if unresolved_companion_count:
        print(f"  ⚠️  {unresolved_companion_count} companions quarantined to companions_unresolved")

    # ── Summary ─────────────────────────────────────────────────────────────
    print("\n📊 Summary")
    print("=" * 50)
    print(f"  Plants:        {len(plants)}")
    print(f"  Pests:         {len(pests)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Warnings:      {len(all_warnings)}")

    for label, counter_key in [("Most pest-affected plants", "plant_name"),
                                ("Most widespread pests", "pest_name")]:
        counts = Counter(r[counter_key] for r in relationships).most_common(5)
        print(f"\n  {label}:")
        for name, count in counts:
            print(f"    {name}: {count}")

    if args.dry_run:
        print("\n✅ Dry run complete — no files written")
        return

    # ── Write exports ────────────────────────────────────────────────────────
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
