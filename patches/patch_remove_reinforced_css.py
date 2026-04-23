from pathlib import Path
import shutil
import re
import sys

FILE = Path("src/pages/guild-checker.astro")

if not FILE.exists():
    print(f"❌ File not found: {FILE}")
    sys.exit(1)

text = FILE.read_text(encoding="utf-8")
original = text

backup = FILE.with_suffix(FILE.suffix + ".bak_remove_reinforced_css")
shutil.copy2(FILE, backup)

changes = []

patterns = [
    (r'\n\s*\.reinforced-chips\s*\{[^}]*\}\s*', '\n', "Removed .reinforced-chips CSS"),
    (r'\n\s*\.reinforced-chip\s*\{[^}]*\}\s*', '\n', "Removed .reinforced-chip CSS"),
    (r'\n\s*\.reinforced-chip-count\s*\{[^}]*\}\s*', '\n', "Removed .reinforced-chip-count CSS"),
]

for pattern, repl, label in patterns:
    new_text, count = re.subn(pattern, repl, text, count=1, flags=re.DOTALL)
    if count:
        text = new_text
        changes.append(f"✅ {label}")
    else:
        changes.append(f"❌ {label}")

text = re.sub(r'\n{3,}', '\n\n', text)
changes.append("✅ Cleaned spacing")

if text != original:
    FILE.write_text(text, encoding="utf-8")
    print(f"✅ Patched {FILE}")
    print(f"🗂 Backup created: {backup}")
else:
    print("ℹ️ No changes applied")
    print(f"🗂 Backup created: {backup}")

print("\nPatch report:")
for c in changes:
    print(c)