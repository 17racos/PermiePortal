from pathlib import Path
import re
import shutil
import sys

FILE = Path("src/pages/guild-checker.astro")

if not FILE.exists():
    print(f"❌ File not found: {FILE}")
    sys.exit(1)

text = FILE.read_text(encoding="utf-8")
original = text

backup = FILE.with_suffix(FILE.suffix + ".bak2")
shutil.copy2(FILE, backup)

changes = []

# Find getNextBestPlants block
fn_match = re.search(
    r"function\s+getNextBestPlants\s*\([^\)]*\)\s*\{",
    text,
    flags=re.DOTALL
)

if not fn_match:
    print("❌ Could not find getNextBestPlants()")
    sys.exit(1)

start = fn_match.start()

# crude function block extraction by brace counting
i = fn_match.end() - 1
depth = 0
end = None
for idx in range(i, len(text)):
    ch = text[idx]
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0:
            end = idx + 1
            break

if end is None:
    print("❌ Could not determine end of getNextBestPlants()")
    sys.exit(1)

block = text[start:end]

if "removedByUser.has(" in block:
    print("ℹ️ getNextBestPlants() already appears to reference removedByUser")
    print(f"🗂 Backup created: {backup}")
    sys.exit(0)

patched = block

patterns = [
    (
        r"(if\s*\(\s*currentSlugs\.includes\(p\.slug\)\s*\)\s*continue;\s*)"
        r"(if\s*\(\s*dismissedSuggestions\.has\(p\.slug\)\s*\)\s*continue;\s*)",
        r"\1\2      if (removedByUser.has(p.slug)) continue;\n",
        "Inserted removedByUser filter after currentSlugs + dismissedSuggestions",
    ),
    (
        r"(if\s*\(\s*currentSlugs\.includes\(p\.slug\)\s*\)\s*return\s+false;\s*)"
        r"(if\s*\(\s*dismissedSuggestions\.has\(p\.slug\)\s*\)\s*return\s+false;\s*)",
        r"\1\2      if (removedByUser.has(p.slug)) return false;\n",
        "Inserted removedByUser filter in filter-return block",
    ),
    (
        r"(if\s*\(\s*dismissedSuggestions\.has\(p\.slug\)\s*\)\s*continue;\s*)",
        r"\1      if (removedByUser.has(p.slug)) continue;\n",
        "Inserted removedByUser filter after dismissedSuggestions continue",
    ),
    (
        r"(if\s*\(\s*dismissedSuggestions\.has\(p\.slug\)\s*\)\s*return\s+false;\s*)",
        r"\1      if (removedByUser.has(p.slug)) return false;\n",
        "Inserted removedByUser filter after dismissedSuggestions return false",
    ),
]

applied = None
for pattern, repl, label in patterns:
    new_block, count = re.subn(pattern, repl, patched, count=1, flags=re.DOTALL)
    if count:
        patched = new_block
        applied = label
        break

if not applied:
    # fallback: inject near the top of the function after currentSlugs declaration if present
    fallback_patterns = [
        (
            r"(\bconst\s+currentSet\s*=\s*new\s+Set\([^\n]*\);\s*)",
            r"\1\n    const removedSet = removedByUser;\n",
            "Inserted fallback removedSet alias",
        ),
        (
            r"(\bfor\s*\(\s*const\s+p\s+of\s+plantIndex\s*\)\s*\{\s*)",
            r"\1\n      if (removedByUser.has(p.slug)) continue;\n",
            "Inserted removedByUser filter at top of plant loop",
        ),
        (
            r"(\.filter\s*\(\s*p\s*=>\s*)",
            r"\1!removedByUser.has(p.slug) && ",
            "Inserted removedByUser filter in .filter() chain",
        ),
    ]
    for pattern, repl, label in fallback_patterns:
        new_block, count = re.subn(pattern, repl, patched, count=1, flags=re.DOTALL)
        if count:
            patched = new_block
            applied = label
            break

if not applied:
    print("⚠️ Could not automatically patch getNextBestPlants()")
    print(f"🗂 Backup created: {backup}")
    sys.exit(1)

new_text = text[:start] + patched + text[end:]

FILE.write_text(new_text, encoding="utf-8")

print(f"✅ Patched {FILE}")
print(f"🗂 Backup created: {backup}")
print(f"✅ {applied}")
print("\nVerify with:")
print("grep -n \"function getNextBestPlants\\|removedByUser.has(p.slug)\" src/pages/guild-checker.astro")