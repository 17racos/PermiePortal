#!/usr/bin/env python3
"""
patch_converter_normalized.py
=============================
Adds companions_normalized field to the converter output.
Apply after resolve_companions.py has run.
"""
from pathlib import Path
import shutil

CONVERTER = Path("convert_permie_data.py")
BACKUP    = Path("convert_permie_data.py.pre_normalized_patch")


def apply():
    if not CONVERTER.exists():
        print("❌ convert_permie_data.py not found")
        return False

    shutil.copy2(CONVERTER, BACKUP)
    text = CONVERTER.read_text(encoding='utf-8')

    OLD = (
        '        "companions_unresolved":   companions_unresolved,\n'
        '        "companion_categories":    norm_list(data.get(\'companion_categories\', [])),\n'
        '        "companion_ecosystem":     norm_list(data.get(\'companion_ecosystem\', [])),\n'
    )
    NEW = (
        '        "companions_unresolved":   companions_unresolved,\n'
        '        "companions_normalized":   data.get(\'companions_normalized\', []) or [],\n'
        '        "companion_categories":    data.get(\'companion_categories\', []) or [],\n'
    )

    if OLD in text:
        text = text.replace(OLD, NEW)
        CONVERTER.write_text(text, encoding='utf-8')
        print("✅ companions_normalized added to converter output")
        print("   companion_ecosystem field removed (merged into companion_categories)")
        return True
    else:
        # Try simpler anchor
        OLD2 = '        "companions_unresolved":   companions_unresolved,'
        NEW2 = (
            '        "companions_unresolved":   companions_unresolved,\n'
            '        "companions_normalized":   data.get(\'companions_normalized\', []) or [],'
        )
        if OLD2 in text:
            text = text.replace(OLD2, NEW2)
            CONVERTER.write_text(text, encoding='utf-8')
            print("✅ companions_normalized added (simple patch)")
            return True

    print("❌ Anchor not found — check converter manually")
    return False


if __name__ == '__main__':
    apply()
