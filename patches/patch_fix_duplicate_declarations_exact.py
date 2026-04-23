from pathlib import Path
import shutil
import sys

FILE = Path("src/pages/guild-checker.astro")

if not FILE.exists():
    print(f"❌ File not found: {FILE}")
    sys.exit(1)

text = FILE.read_text(encoding="utf-8")
original = text

backup = FILE.with_suffix(FILE.suffix + ".bak_fix_dup_exact")
shutil.copy2(FILE, backup)

changes = []

# --- Find the meaningful gate block explicitly ---
start_marker = "// ── Meaningful contribution gate"
start_idx = text.find(start_marker)

if start_idx == -1:
    print("❌ Could not find Meaningful contribution gate")
    sys.exit(1)

# take a reasonable slice after the marker to operate on
end_idx = text.find("if (!improves) continue;", start_idx)

if end_idx == -1:
    print("❌ Could not find end of meaningful gate")
    sys.exit(1)

end_idx += len("if (!improves) continue;")

block = text[start_idx:end_idx]
original_block = block

# --- Remove ONLY the duplicate declarations ---
if "const fam = plantToFamily[p.slug]" in block:
    block = block.replace("const fam = plantToFamily[p.slug] || '__none__';\n", "")
    block = block.replace("const fam = plantToFamily[p.slug] || '__none__';", "")
    changes.append("✅ Removed duplicate 'const fam'")

if "const layer = inferLayer(p);" in block:
    # remove only ONE occurrence (the duplicate one inside the gate)
    first = block.find("const layer = inferLayer(p);")
    if first != -1:
        # remove only the first match inside this block
        block = block[:first] + block[first:].replace("const layer = inferLayer(p);", "", 1)
        changes.append("✅ Removed duplicate 'const layer'")

# --- Replace block back ---
text = text[:start_idx] + block + text[end_idx:]

# --- Clean spacing ---
import re
text = re.sub(r'\n{3,}', '\n\n', text)
changes.append("✅ Cleaned spacing")

# --- Write file ---
if text != original:
    FILE.write_text(text, encoding="utf-8")
    print(f"✅ Patched {FILE}")
    print(f"🗂 Backup created: {backup}")
else:
    print("ℹ️ No changes made")
    print(f"🗂 Backup created: {backup}")

print("\nPatch report:")
for c in changes:
    print(c)

print("\nVerify:")
print("grep -n -C 5 \"Meaningful contribution gate\" src/pages/guild-checker.astro")
print("npm run build")