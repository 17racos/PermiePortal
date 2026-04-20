#!/usr/bin/env python3
"""
patch_converter_companions.py
=============================
Adds companion_categories and companion_ecosystem fields to the converter.
Also updates companions_present quality check to count categories as partial credit.

Apply AFTER resolve_companions.py has run at least once.
"""

from pathlib import Path
import shutil

CONVERTER = Path("convert_permie_data.py")
BACKUP    = Path("convert_permie_data.py.pre_companion_patch")


def apply():
    if not CONVERTER.exists():
        print("❌ convert_permie_data.py not found")
        return False

    shutil.copy2(CONVERTER, BACKUP)
    print(f"✅ Backed up to {BACKUP.name}")

    text = CONVERTER.read_text(encoding='utf-8')

    # ── PATCH 1: Add new fields to process_plant return dict ─────────────────
    OLD = '        "companions_unresolved":   companions_unresolved,'
    NEW = '''        "companions_unresolved":   companions_unresolved,
        "companion_categories":    norm_list(data.get('companion_categories', [])),
        "companion_ecosystem":     norm_list(data.get('companion_ecosystem', [])),'''

    if OLD in text:
        text = text.replace(OLD, NEW)
        print("✅ Patch 1: companion_categories + companion_ecosystem added to output")
    else:
        print("❌ Patch 1 anchor not found")
        return False

    # ── PATCH 2: Update companions_present quality check ─────────────────────
    # companions_present currently only counts resolved companions.
    # Update to also count category entries as partial signal — a plant with
    # companion_categories but no resolved companions is NOT penalized as
    # "no companion data", it just hasn't been fully resolved yet.
    OLD2 = (
        '        "companions_present":  len(companions_resolved) >= 2 or any(\n'
        '            "invasive" in str(c).lower()\n'
        '            for c in norm_list(data.get("cautions", []))\n'
        '        ),'
    )
    NEW2 = (
        '        "companions_present":  (\n'
        '            len(companions_resolved) >= 2\n'
        '            or len(norm_list(data.get("companion_categories", []))) >= 1\n'
        '            or any(\n'
        '                "invasive" in str(c).lower()\n'
        '                for c in norm_list(data.get("cautions", []))\n'
        '            )\n'
        '        ),'
    )

    if OLD2 in text:
        text = text.replace(OLD2, NEW2)
        print("✅ Patch 2: companions_present check updated for categories")
    else:
        print("⚠️  Patch 2 anchor not found — companions_present check unchanged")
        # Non-fatal — converter still works without this

    CONVERTER.write_text(text, encoding='utf-8')
    print(f"\n✅ Converter patched")
    return True


if __name__ == '__main__':
    success = apply()
    if success:
        print("\nNext: python3 resolve_companions.py --dry-run")
