#!/usr/bin/env python3
"""
patch_converter.py
==================
Applies the function routing changes to convert_permie_data.py.
Safe: patches by string replacement, backs up original first.

Run AFTER fix_35_plants.py, BEFORE ./sync.sh
"""

from pathlib import Path
import shutil

CONVERTER = Path("convert_permie_data.py")
BACKUP    = Path("convert_permie_data.py.pre_routing_patch")


def apply_patch():
    if not CONVERTER.exists():
        print("❌ convert_permie_data.py not found")
        return False

    # Backup
    shutil.copy2(CONVERTER, BACKUP)
    print(f"✅ Backed up to {BACKUP.name}")

    text = CONVERTER.read_text(encoding='utf-8')

    # ── PATCH 1: Add FUNCTION_ROUTING after VALID_FUNCTIONS ──────────────────
    ROUTING_BLOCK = '''
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
}
'''

    ANCHOR_1 = '# ── PURPOSE LINE FORMAT ─'
    if ANCHOR_1 in text:
        text = text.replace(ANCHOR_1, ROUTING_BLOCK + '\n' + ANCHOR_1)
        print("✅ Patch 1: FUNCTION_ROUTING block inserted")
    else:
        print("❌ Patch 1 anchor not found — check converter version")
        return False

    # ── PATCH 2: Replace plant_function validation in process_plant() ────────
    OLD_VALIDATION = '''    # ── plant_function validation ───────────────────────────────────────────
    raw_functions = norm_list(data.get('plant_function', []))
    invalid_functions = [f for f in raw_functions if f not in VALID_FUNCTIONS]
    if invalid_functions:
        warnings.append(
            f"  ⚠️  FUNCTION INVALID [{common_name}]: "
            f"unrecognized values: {invalid_functions}"
        )'''

    NEW_VALIDATION = '''    # ── plant_function validation + routing ─────────────────────────────────
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

    raw_functions = clean_functions'''

    if OLD_VALIDATION in text:
        text = text.replace(OLD_VALIDATION, NEW_VALIDATION)
        print("✅ Patch 2: plant_function routing logic applied")
    else:
        print("❌ Patch 2 anchor not found — check converter version")
        return False

    # ── PATCH 3: Add new fields to process_plant return dict ─────────────────
    OLD_RETURN = '        "plant_function":          raw_functions,'
    NEW_RETURN = '''        "plant_function":            raw_functions,
        "plant_traits":              plant_traits,
        "human_uses":                human_uses,
        "ecological_role":           ecological_role,
        "plant_function_unresolved": fn_unresolved,'''

    if OLD_RETURN in text:
        text = text.replace(OLD_RETURN, NEW_RETURN)
        print("✅ Patch 3: new fields added to process_plant return dict")
    else:
        print("❌ Patch 3 anchor not found — check converter version")
        return False

    CONVERTER.write_text(text, encoding='utf-8')
    print(f"\n✅ All patches applied to {CONVERTER.name}")
    return True


if __name__ == "__main__":
    success = apply_patch()
    if success:
        print("\nNext steps:")
        print("  python3 fix_35_plants.py")
        print("  ./sync.sh --check 2>&1 | grep -E 'FUNCTION|Warnings:'")
        print("  ./sync.sh")
    else:
        print("\n❌ Patch failed — original file unchanged (backup at .pre_routing_patch)")
