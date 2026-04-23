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
changes = []

backup = FILE.with_suffix(FILE.suffix + ".bak")
shutil.copy2(FILE, backup)


def apply_regex(pattern, repl, label, flags=re.DOTALL):
    global text
    new_text, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count:
        text = new_text
        changes.append(f"✅ {label}")
        return True
    changes.append(f"❌ {label}")
    return False


def ensure_once(snippet, label):
    if snippet in text:
        changes.append(f"✅ {label}")
        return True
    changes.append(f"❌ {label}")
    return False


# -------------------------------------------------------------------
# 1) Make sure suggestion filtering excludes removedByUser
# Tries to patch the common filter block inside getNextBestPlants().
# -------------------------------------------------------------------

filter_patterns = [
    (
        r"(if\s*\(\s*currentSlugs\.includes\(p\.slug\)\s*\)\s*return\s+false;\s*)"
        r"(if\s*\(\s*dismissedSuggestions\.has\(p\.slug\)\s*\)\s*return\s+false;\s*)",
        r"\1\2      if (removedByUser.has(p.slug)) return false;\n",
        "Added removedByUser filter after currentSlugs + dismissedSuggestions",
    ),
    (
        r"(if\s*\(\s*guild\.some\(\s*g\s*=>\s*g\.slug\s*===\s*p\.slug\s*\)\s*\)\s*return\s+false;\s*)"
        r"(if\s*\(\s*dismissedSuggestions\.has\(p\.slug\)\s*\)\s*return\s+false;\s*)",
        r"\1\2      if (removedByUser.has(p.slug)) return false;\n",
        "Added removedByUser filter after guild.some + dismissedSuggestions",
    ),
    (
        r"(if\s*\(\s*dismissedSuggestions\.has\(p\.slug\)\s*\)\s*return\s+false;\s*)",
        r"\1      if (removedByUser.has(p.slug)) return false;\n",
        "Added removedByUser filter after dismissedSuggestions",
    ),
]

already_has_filter = "removedByUser.has(p.slug)" in text
if already_has_filter:
    changes.append("✅ removedByUser suggestion filter already present")
else:
    patched_filter = False
    for pattern, repl, label in filter_patterns:
        if apply_regex(pattern, repl, label):
            patched_filter = True
            break
    if not patched_filter:
        changes.append("⚠️ Could not automatically patch suggestion filter")


# -------------------------------------------------------------------
# 2) Patch remove button handler in renderGuild()
# We inject removedByUser.add(slug); right after removal from guild.
# -------------------------------------------------------------------

remove_patterns = [
    (
        r"(guild\s*=\s*guild\.filter\(\s*p\s*=>\s*p\.slug\s*!==\s*slug\s*\);\s*)",
        r"\1\n      removedByUser.add(slug);\n      dismissedSuggestions.delete(slug);\n",
        "Patched guild.filter(...) remove handler",
    ),
    (
        r"(guild\.splice\(\s*idx\s*,\s*1\s*\);\s*)",
        r"\1\n      removedByUser.add(slug);\n      dismissedSuggestions.delete(slug);\n",
        "Patched guild.splice(...) remove handler",
    ),
    (
        r"(guild\.splice\(\s*index\s*,\s*1\s*\);\s*)",
        r"\1\n      removedByUser.add(slug);\n      dismissedSuggestions.delete(slug);\n",
        "Patched guild.splice(index, 1) remove handler",
    ),
]

# Avoid double-injecting if already present near removal logic
already_has_remove_memory = "removedByUser.add(slug);" in text
if already_has_remove_memory:
    changes.append("✅ remove handler already tracks removedByUser")
else:
    patched_remove = False
    for pattern, repl, label in remove_patterns:
        if apply_regex(pattern, repl, label):
            patched_remove = True
            break
    if not patched_remove:
        changes.append("⚠️ Could not automatically patch remove handler")


# -------------------------------------------------------------------
# 3) Optional safety: if Clear Guild exists, clear remembered removals too
# This prevents old suppressed plants hanging around after reset.
# -------------------------------------------------------------------

if "removedByUser.clear();" in text:
    changes.append("✅ Clear Guild already resets removedByUser")
else:
    clear_patterns = [
        (
            r"(guild\s*=\s*\[\s*\]\s*;\s*renderGuild\(\)\s*;\s*renderResults\(\)\s*;)",
            r"guild = [];\n      removedByUser.clear();\n      dismissedSuggestions.clear();\n      renderGuild();\n      renderResults();",
            "Patched inline Clear Guild reset",
        ),
        (
            r"(guild\s*=\s*\[\s*\]\s*;)",
            r"\1\n      removedByUser.clear();\n      dismissedSuggestions.clear();",
            "Patched generic guild reset",
        ),
    ]
    patched_clear = False
    for pattern, repl, label in clear_patterns:
        if apply_regex(pattern, repl, label):
            patched_clear = True
            break
    if not patched_clear:
        changes.append("⚠️ Could not automatically patch Clear Guild reset")


# -------------------------------------------------------------------
# Write file if changed
# -------------------------------------------------------------------

if text != original:
    FILE.write_text(text, encoding="utf-8")
    print(f"✅ Patched {FILE}")
    print(f"🗂 Backup created: {backup}")
else:
    print("ℹ️ No file changes were written")

print("\nPatch report:")
for c in changes:
    print(c)

print("\nQuick checks:")
print(" - Search for: removedByUser.add(slug);")
print(" - Search for: removedByUser.has(p.slug)")
print(" - Search for: removedByUser.clear();")