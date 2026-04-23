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

backup = FILE.with_suffix(FILE.suffix + ".bak_resilience_ui")
shutil.copy2(FILE, backup)

changes = []

def replace_once(old, new, label):
    global text
    if old in text:
        text = text.replace(old, new, 1)
        changes.append(f"✅ {label}")
        return True
    changes.append(f"❌ {label}")
    return False

def replace_all(old, new, label):
    global text
    count = text.count(old)
    if count:
        text = text.replace(old, new)
        changes.append(f"✅ {label} ({count}x)")
        return True
    changes.append(f"❌ {label}")
    return False

def regex_once(pattern, repl, label, flags=re.DOTALL):
    global text
    new_text, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count:
        text = new_text
        changes.append(f"✅ {label}")
        return True
    changes.append(f"❌ {label}")
    return False

# -------------------------------------------------------------------
# 1) Straight label changes
# -------------------------------------------------------------------

replace_all("Shared Pest Pressure", "System Resilience", "Renamed Shared Pest Pressure")
replace_all("Top Shared Pests", "Shared Pest Signals", "Renamed Top Shared Pests")
replace_all("Resilience Factors", "Risk Drivers & Stability", "Renamed Resilience Factors")

# -------------------------------------------------------------------
# 2) Change pest-first subtitle language where possible
# -------------------------------------------------------------------

# Example target:
# LOW SHARED PEST PRESSURE — RESILIENCE: 83
# -> STRUCTURALLY RESILIENT — LOW PEST OVERLAP
regex_once(
    r"([\"'`>])\s*\$\{pestLabel\}\s+SHARED\s+PEST\s+PRESSURE\s+—\s+RESILIENCE:\s*\$\{resilience\}",
    r'\1STRUCTURALLY RESILIENT — \${pestLabel} PEST OVERLAP',
    "Reworded pest-first subtitle template"
)

# Slightly more generic fallback if above misses
regex_once(
    r"SHARED PEST PRESSURE\s+—\s+RESILIENCE:",
    "PEST OVERLAP — RESILIENCE:",
    "Softened SHARED PEST PRESSURE phrasing"
)

# -------------------------------------------------------------------
# 3) Hide raw pest score if rendered as a standalone metric block
# Conservative: only removes obvious assignment/template for the big number
# -------------------------------------------------------------------

# Common patterns like:
# <div class="metric-value">${sharedPestPressure}</div>
# <div class="score-number">${score}</div>
# where nearby text references pest pressure
regex_once(
    r"""
    (<div[^>]*class="[^"]*(?:metric-value|score-number|pressure-score|summary-score)[^"]*"[^>]*>\s*)
    (\$\{[^}]*(?:sharedPest|pestPressure|sharedPestPressure|pressureScore)[^}]*\})
    (\s*</div>)
    """,
    r'\1<span style="display:none;">\2</span>\3',
    "Hidden raw pest score block",
    flags=re.DOTALL | re.VERBOSE
)

# If your UI stores innerHTML strings instead
regex_once(
    r"""
    (<div[^>]*class=\\?["'][^"']*(?:metric-value|score-number|pressure-score|summary-score)[^"']*\\?["'][^>]*>\s*)
    (\$\{[^}]*(?:sharedPest|pestPressure|sharedPestPressure|pressureScore)[^}]*\})
    (\s*</div>)
    """,
    r'\1<span style="display:none;">\2</span>\3',
    "Hidden escaped-template pest score block",
    flags=re.DOTALL | re.VERBOSE
)

# -------------------------------------------------------------------
# 4) Reword the pest warning sentence to sound more diagnostic
# -------------------------------------------------------------------

replace_all(
    "⚠️ Shared pest pressure detected — ",
    "⚠️ Pest overlap detected — ",
    "Reworded pest warning prefix"
)

replace_all(
    "affect multiple plants in this guild.",
    "recur across multiple plants in this guild.",
    "Reworded pest warning suffix"
)

# -------------------------------------------------------------------
# 5) Optional: if a section description says score is based on pests first,
# soften it toward broader stability
# -------------------------------------------------------------------

replace_all(
    "Plants scored by role coverage, family diversity, and pest overlap with your current guild.",
    "Plants scored by role coverage, family diversity, resilience impact, and pest overlap with your current guild.",
    "Expanded suggestion scoring description"
)

# -------------------------------------------------------------------
# 6) Write file if changed
# -------------------------------------------------------------------

if text != original:
    FILE.write_text(text, encoding="utf-8")
    print(f"✅ Patched {FILE}")
    print(f"🗂 Backup created: {backup}")
else:
    print("ℹ️ No file changes were written")
    print(f"🗂 Backup created: {backup}")

print("\nPatch report:")
for c in changes:
    print(c)

print("\nRecommended follow-up checks:")
print("grep -n \"System Resilience\\|Shared Pest Signals\\|Risk Drivers & Stability\\|PEST OVERLAP\\|STRUCTURALLY RESILIENT\" src/pages/guild-checker.astro")
print("npm run build")