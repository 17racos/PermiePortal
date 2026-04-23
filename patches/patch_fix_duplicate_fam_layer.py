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

backup = FILE.with_suffix(FILE.suffix + ".bak_fix_duplicate_fam_layer")
shutil.copy2(FILE, backup)

changes = []

# Replace only inside the meaningful contribution gate:
# const fam -> use existing fam
# const layer -> use existing layer
patterns = [
    (
        r"(\s*// ── Meaningful contribution gate.*?)(\n\s*const fam = plantToFamily\[p\.slug\] \|\| '__none__';)(.*?)(\n\s*const layer = inferLayer\(p\);)(.*?if \(!improves\) continue;)",
        lambda m: m.group(1) + m.group(3) + m.group(5),
        "Removed duplicate fam/layer declarations inside meaningful gate",
    ),
]

applied = False
for pattern, repl, label in patterns:
    new_text, count = re.subn(pattern, repl, text, count=1, flags=re.DOTALL)
    if count:
        text = new_text
        changes.append(f"✅ {label}")
        applied = True
        break

# Fallbacks in case spacing differs
fallbacks = [
    (
        r"(\s*// ── Meaningful contribution gate.*?\n)\s*const fam = plantToFamily\[p\.slug\] \|\| '__none__';\n",
        r"\1",
        "Removed duplicate fam declaration in meaningful gate",
    ),
    (
        r"(\s*// ── Meaningful contribution gate.*?\n(?:.*\n){0,20}?)\s*const layer = inferLayer\(p\);\n",
        r"\1",
        "Removed duplicate layer declaration in meaningful gate",
    ),
]

for pattern, repl, label in fallbacks:
    new_text, count = re.subn(pattern, repl, text, count=1, flags=re.DOTALL)
    if count:
        text = new_text
        changes.append(f"✅ {label}")

text = re.sub(r'\n{3,}', '\n\n', text)
changes.append("✅ Cleaned spacing")

if text != original:
    FILE.write_text(text, encoding="utf-8")
    print(f"✅ Patched {FILE}")
    print(f"🗂 Backup created: {backup}")
else:
    print("ℹ️ No changes were written")
    print(f"🗂 Backup created: {backup}")

print("\nPatch report:")
for c in changes:
    print(c)

print("\nVerify with:")
print(r"grep -n -C 3 \"Meaningful contribution gate\|const fam = plantToFamily\[p.slug\]\|const layer = inferLayer\(p\)\" src/pages/guild-checker.astro")
print("npm run build")