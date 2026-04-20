#!/usr/bin/env python3
"""
fix_35_plants.py
================
Fixes the 35 mid-quality plants by:

1. Routing invalid plant_function values to correct fields:
     Drought Tolerant    → plant_traits
     Timber              → human_uses
     Dye Plant / Dye     → human_uses
     Decomposer          → ecological_role
     Water Purifier      → plant_function: Water Purification (spelling fix)
     Border Plant -Ground Cover → plant_function: Ground Cover (spelling fix)
     Soil Improvement /
     Soil Builder /
     Cover Crop          → plant_function_unresolved + FUNCTION REVIEW warning

2. Fixing purpose lines missing ' -- ' separator by inserting it at the
   first sentence boundary ('. ') within the line.

3. Removing purpose lines whose function name was routed OUT of plant_function
   (they no longer have a valid plant_function entry to align with).

Safe: uses ruamel.yaml for round-trip preservation of formatting.
Only touches files for the 35 identified plants.
"""

import re
import io
import json
from pathlib import Path
from ruamel.yaml import YAML

# ── CONFIG ────────────────────────────────────────────────────────────────────
PLANTS_JSON  = Path("src/data/plants.json")
SEEDS_DIR    = Path("src/seeds/plants")

VALID_FUNCTIONS = frozenset({
    "Edible", "Medicinal", "Nitrogen Fixer", "Dynamic Accumulator",
    "Mulcher", "Pollinator", "Wildlife Attractor", "Erosion Control",
    "Animal Fodder", "Windbreaker", "Border Plant", "Pest Management",
    "Ground Cover", "Shade Provider", "Water Retention", "Fiber",
    "Biomass", "Aquatic", "Ornamental", "Water Purification",
    "Plant Growth Stimulant", "Biofuel",
})

# Invalid value → (destination_field, canonical_value)
# canonical_value=None means quarantine to plant_function_unresolved
FUNCTION_ROUTING = {
    "Drought Tolerant":           ("plant_traits",              "Drought Tolerant"),
    "Cold Hardy":                 ("plant_traits",              "Cold Hardy"),
    "Fast Growing":               ("plant_traits",              "Fast Growing"),
    "Timber":                     ("human_uses",                "Timber"),
    "Dye Plant":                  ("human_uses",                "Dye"),
    "Dye":                        ("human_uses",                "Dye"),
    "Decomposer":                 ("ecological_role",           "Decomposer"),
    "Mycorrhizal":                ("ecological_role",           "Mycorrhizal"),
    # Spelling corrections → stay in plant_function with canonical name
    "Water Purifier":             ("plant_function",            "Water Purification"),
    "Border Plant -Ground Cover": ("plant_function",            "Ground Cover"),
    # Ambiguous → quarantine
    "Soil Improvement":           ("plant_function_unresolved", "Soil Improvement"),
    "Soil Builder":               ("plant_function_unresolved", "Soil Builder"),
    "Cover Crop":                 ("plant_function_unresolved", "Cover Crop"),
}

PURPOSE_LINE_RE = re.compile(r'^([A-Za-z][A-Za-z\s]+):\s+.+\s+--\s+.+$')


def fix_purpose_line(line):
    """
    Insert ' -- ' separator into a purpose line that's missing it.
    Strategy: find the first '. ' after the colon and use that as the split point.
    If no '. ' found, try ' and ' as a fallback.
    If neither found, leave unchanged (can't safely fix automatically).
    """
    stripped = line.strip()
    if not stripped or ':' not in stripped:
        return line

    # Already valid
    if PURPOSE_LINE_RE.match(stripped):
        return line

    colon_pos = stripped.index(':')
    fn_name = stripped[:colon_pos].strip()
    rest = stripped[colon_pos+1:].strip()

    # Find first '. ' after at least 20 chars of content
    dot_pos = rest.find('. ', 20)
    if dot_pos != -1:
        before = rest[:dot_pos].rstrip()
        after  = rest[dot_pos+2:].strip()
        # Lowercase the start of the second sentence
        if after:
            after = after[0].lower() + after[1:]
        return f"{fn_name}: {before} -- {after}"

    # Fallback: split on ' and ' if present
    and_pos = rest.find(' and ', 20)
    if and_pos != -1:
        before = rest[:and_pos].rstrip()
        after  = rest[and_pos+5:].strip()
        return f"{fn_name}: {before} -- and {after}"

    # Can't fix automatically
    return line


def process_plant_file(filepath, warnings):
    ryaml = YAML()
    ryaml.preserve_quotes = True
    ryaml.width = 10000
    ryaml.indent(mapping=2, sequence=2, offset=2)

    text = filepath.read_text(encoding='utf-8')
    data = ryaml.load(io.StringIO(text))

    if not isinstance(data, (dict, list)):
        return False

    items = data if isinstance(data, list) else [data]
    changed = False

    for item in items:
        if not isinstance(item, dict):
            continue

        name = item.get('common_name', filepath.stem)
        raw_functions = list(item.get('plant_function', []) or [])

        # ── Route invalid function values ─────────────────────────────────
        clean_functions  = []
        plant_traits     = list(item.get('plant_traits', []) or [])
        human_uses       = list(item.get('human_uses', []) or [])
        ecological_role  = list(item.get('ecological_role', []) or [])
        fn_unresolved    = list(item.get('plant_function_unresolved', []) or [])
        # Track which function names were routed OUT of plant_function
        routed_out = set()

        for fn in raw_functions:
            if fn in VALID_FUNCTIONS:
                clean_functions.append(fn)
            elif fn in FUNCTION_ROUTING:
                dest_field, canonical = FUNCTION_ROUTING[fn]
                if dest_field == "plant_function":
                    # Spelling correction — stays in plant_function
                    if canonical not in clean_functions:
                        clean_functions.append(canonical)
                    warnings.append(
                        f"  ✏️  FUNCTION CORRECTED [{name}]: "
                        f"'{fn}' → '{canonical}' (spelling fix)"
                    )
                elif dest_field == "plant_function_unresolved":
                    if canonical not in fn_unresolved:
                        fn_unresolved.append(canonical)
                    routed_out.add(fn)
                    warnings.append(
                        f"  ⚠️  FUNCTION REVIEW [{name}]: "
                        f"'{fn}' is ambiguous → plant_function_unresolved"
                    )
                else:
                    # plant_traits / human_uses / ecological_role
                    target = {"plant_traits": plant_traits,
                              "human_uses": human_uses,
                              "ecological_role": ecological_role}[dest_field]
                    if canonical not in target:
                        target.append(canonical)
                    routed_out.add(fn)
                    warnings.append(
                        f"  ✅ FUNCTION ROUTED [{name}]: "
                        f"'{fn}' → {dest_field}.{canonical}"
                    )
            else:
                # Truly unknown — keep in unresolved
                if fn not in fn_unresolved:
                    fn_unresolved.append(fn)
                routed_out.add(fn)
                warnings.append(
                    f"  ⚠️  FUNCTION UNKNOWN [{name}]: "
                    f"'{fn}' not in canonical set → plant_function_unresolved"
                )

        # Write back cleaned plant_function
        if clean_functions != raw_functions:
            item['plant_function'] = clean_functions
            changed = True

        # Write new fields only if populated
        if plant_traits != list(item.get('plant_traits', []) or []):
            item['plant_traits'] = plant_traits
            changed = True
        elif plant_traits and 'plant_traits' not in item:
            item['plant_traits'] = plant_traits
            changed = True

        if human_uses != list(item.get('human_uses', []) or []):
            item['human_uses'] = human_uses
            changed = True
        elif human_uses and 'human_uses' not in item:
            item['human_uses'] = human_uses
            changed = True

        if ecological_role != list(item.get('ecological_role', []) or []):
            item['ecological_role'] = ecological_role
            changed = True
        elif ecological_role and 'ecological_role' not in item:
            item['ecological_role'] = ecological_role
            changed = True

        if fn_unresolved != list(item.get('plant_function_unresolved', []) or []):
            item['plant_function_unresolved'] = fn_unresolved
            changed = True
        elif fn_unresolved and 'plant_function_unresolved' not in item:
            item['plant_function_unresolved'] = fn_unresolved
            changed = True

        # ── Fix purpose lines missing ' -- ' ─────────────────────────────
        purpose_raw = item.get('purpose', '') or ''
        if purpose_raw:
            fixed_lines = []
            purpose_changed = False
            for line in purpose_raw.splitlines():
                stripped = line.strip()
                if not stripped:
                    fixed_lines.append(line)
                    continue

                # Skip purpose lines whose function was routed OUT
                # (they're now orphaned — no matching plant_function entry)
                if ':' in stripped:
                    fn_name = stripped.split(':')[0].strip()
                    if fn_name in routed_out:
                        warnings.append(
                            f"  🗑️  PURPOSE REMOVED [{name}]: "
                            f"'{fn_name}' line removed (function routed out)"
                        )
                        purpose_changed = True
                        continue

                fixed = fix_purpose_line(line)
                if fixed != line:
                    purpose_changed = True
                    warnings.append(
                        f"  ✏️  PURPOSE FIXED [{name}]: "
                        f"'{stripped[:60]}...'"
                    )
                fixed_lines.append(fixed)

            if purpose_changed:
                item['purpose'] = '\n'.join(fixed_lines)
                changed = True

    if changed:
        out = io.StringIO()
        ryaml.dump(data, out)
        filepath.write_text(out.getvalue(), encoding='utf-8')

    return changed


def main():
    # Load the 35 mid-quality plant names from JSON
    plants = json.loads(PLANTS_JSON.read_text())
    mid_names = {
        p['common_name']
        for p in plants
        if 0.5 <= p['data_quality_score'] < 0.8
    }

    print(f"🔧 Fixing {len(mid_names)} plants\n")

    warnings = []
    fixed_files = 0
    not_found = []

    for name in sorted(mid_names):
        # Find the YAML file for this plant
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')

        # Try common filename patterns
        candidates = [
            SEEDS_DIR / f"{slug}-data.yml",
            SEEDS_DIR / f"{slug}.yml",
            SEEDS_DIR / f"{slug}.data.yml",
        ]
        # Also glob in case of slight name differences
        glob_hits = list(SEEDS_DIR.glob(f"{slug}*.yml"))

        found = None
        for c in candidates:
            if c.exists():
                found = c
                break
        if not found and glob_hits:
            found = glob_hits[0]

        if not found:
            not_found.append(name)
            continue

        if process_plant_file(found, warnings):
            fixed_files += 1
            print(f"  ✅ {name} ({found.name})")
        else:
            print(f"  ➖ {name} — no changes needed")

    # Print all warnings/actions
    if warnings:
        print(f"\n📋 Actions taken ({len(warnings)}):")
        for w in warnings:
            print(w)

    if not_found:
        print(f"\n⚠️  Could not find YAML for {len(not_found)} plants:")
        for n in not_found:
            print(f"  {n}")

    print(f"\n{'='*50}")
    print(f"✅ Fixed {fixed_files} files")
    print(f"\nNext: ./sync.sh --check 2>&1 | grep -E 'FUNCTION|Warnings:'")


if __name__ == "__main__":
    main()
