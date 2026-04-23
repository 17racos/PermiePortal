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

backup = FILE.with_suffix(FILE.suffix + ".bak_resilience_ui_pass2")
shutil.copy2(FILE, backup)

changes = []

def regex_once(pattern, repl, label, flags=re.DOTALL):
    global text
    new_text, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count:
        text = new_text
        changes.append(f"✅ {label}")
        return True
    changes.append(f"❌ {label}")
    return False

def regex_all(pattern, repl, label, flags=re.DOTALL):
    global text
    new_text, count = re.subn(pattern, repl, text, flags=flags)
    if count:
        text = new_text
        changes.append(f"✅ {label} ({count}x)")
        return True
    changes.append(f"❌ {label}")
    return False

def literal_once(old, new, label):
    global text
    if old in text:
        text = text.replace(old, new, 1)
        changes.append(f"✅ {label}")
        return True
    changes.append(f"❌ {label}")
    return False


# ------------------------------------------------------------
# 1) Reword the subtitle more aggressively
# Catch common template variants after first-pass rename
# ------------------------------------------------------------

subtitle_patterns = [
    (
        r"(\$\{pestLabel\}\s+PEST OVERLAP\s+—\s+RESILIENCE:\s*\$\{resilience\})",
        r"Resilience: ${resilience} — ${pestLabel.lower ? pestLabel.lower() : pestLabel} pest overlap",
        "Reworded pest-first subtitle template variant A",
    ),
    (
        r"(\$\{pestLabel\}\s+PEST OVERLAP\s+—\s+RESILIENCE:\s*\$\{resilienceScore\})",
        r"Resilience: ${resilienceScore} — ${pestLabel.lower ? pestLabel.lower() : pestLabel} pest overlap",
        "Reworded pest-first subtitle template variant B",
    ),
    (
        r"([A-Z]+\s+PEST OVERLAP\s+—\s+RESILIENCE:\s*\$\{[^}]+\})",
        lambda m: m.group(1).replace("PEST OVERLAP — RESILIENCE:", "resilience-first"),
        "Marked hardcoded pest-first subtitle for manual fallback",
    ),
]

for pattern, repl, label in subtitle_patterns:
    if regex_once(pattern, repl, label):
        break

# Clean up the fallback marker if used
literal_once("resilience-first", "Resilience:", "Cleaned subtitle fallback marker")


# ------------------------------------------------------------
# 2) Hide the raw top number block more aggressively
# We target metric blocks near System Resilience heading
# ------------------------------------------------------------

# Case A: direct heading + metric block pattern
regex_once(
    r"""
    (System\ Resilience.*?)
    (<div[^>]*class="[^"]*(?:metric-value|score-number|summary-score|pressure-score)[^"]*"[^>]*>\s*)
    (\$\{[^}]+\}|[0-9]+)
    (\s*</div>)
    """,
    r"\1\2<span style=\"display:none;\">\3</span>\4",
    "Hidden raw number block near System Resilience",
    flags=re.DOTALL | re.VERBOSE
)

# Case B: escaped string-template version
regex_once(
    r"""
    (System\ Resilience.*?)
    (<div[^>]*class=\\?["'][^"']*(?:metric-value|score-number|summary-score|pressure-score)[^"']*\\?["'][^>]*>\s*)
    (\$\{[^}]+\}|[0-9]+)
    (\s*</div>)
    """,
    r"\1\2<span style=\"display:none;\">\3</span>\4",
    "Hidden escaped raw number block near System Resilience",
    flags=re.DOTALL | re.VERBOSE
)

# Case C: generic "metric-value" right after a resilience heading block
regex_once(
    r"""
    (<h3[^>]*>\s*System\ Resilience\s*</h3>.*?)
    (<div[^>]*class="[^"]*metric-value[^"]*"[^>]*>\s*)
    (\$\{[^}]+\}|[0-9]+)
    (\s*</div>)
    """,
    r"\1\2<span style=\"display:none;\">\3</span>\4",
    "Hidden metric-value under h3 System Resilience",
    flags=re.DOTALL | re.VERBOSE
)


# ------------------------------------------------------------
# 3) Reword the pest warning prefix more aggressively
# ------------------------------------------------------------

prefix_variants = [
    (
        "⚠️ Shared pest pressure detected — ",
        "⚠️ Pest overlap detected — ",
        "Reworded pest warning prefix literal A",
    ),
    (
        "⚠️ Shared pest pressure detected",
        "⚠️ Pest overlap detected",
        "Reworded pest warning prefix literal B",
    ),
    (
        "Shared pest pressure detected — ",
        "Pest overlap detected — ",
        "Reworded pest warning prefix literal C",
    ),
    (
        "Shared pest pressure detected",
        "Pest overlap detected",
        "Reworded pest warning prefix literal D",
    ),
]

for old, new, label in prefix_variants:
    if literal_once(old, new, label):
        break

# catch template-built warning text
regex_once(
    r"([\"'`])⚠️\s*Shared pest pressure detected\s*—\s*",
    r"\1⚠️ Pest overlap detected — ",
    "Reworded pest warning prefix template"
)


# ------------------------------------------------------------
# 4) Make pest details feel more diagnostic than central
# ------------------------------------------------------------

literal_once(
    "Shared Pest Signals",
    "Shared Pest Signals (supporting detail)",
    "Softened Shared Pest Signals heading"
)

# Optional wording improvement if present
literal_once(
    "Pest Mitigation",
    "Pest Buffering",
    "Renamed Pest Mitigation"
)

literal_once(
    "Weak mitigation",
    "Weak buffering",
    "Renamed weak mitigation"
)


# ------------------------------------------------------------
# 5) Write out
# ------------------------------------------------------------

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

print("\nRecommended checks:")
print("grep -n \"System Resilience\\|Pest overlap detected\\|Shared Pest Signals\\|Pest Buffering\\|Weak buffering\\|Resilience:\" src/pages/guild-checker.astro")
print("npm run build")