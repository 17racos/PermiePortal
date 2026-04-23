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

backup = FILE.with_suffix(FILE.suffix + ".bak_remove_score_number")
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

def regex_once(pattern, repl, label, flags=re.DOTALL):
    global text
    new_text, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count:
        text = new_text
        changes.append(f"✅ {label}")
        return True
    changes.append(f"❌ {label}")
    return False

# 1) Remove the old score-number div from the HTML seed block
html_patterns = [
    (
        r'\s*<div class="score-number" id="score-number">.*?</div>\s*',
        '\n',
        "Removed score-number div from static HTML block"
    ),
    (
        r'\s*<div[^>]*id="score-number"[^>]*>.*?</div>\s*',
        '\n',
        "Removed generic score-number div from static HTML block"
    ),
]

removed_html = False
for pattern, repl, label in html_patterns:
    if regex_once(pattern, repl, label):
        removed_html = True
        break

# 2) Remove JS that still writes to score-number
js_patterns = [
    (
        r'\s*scoreEl\.textContent\s*=\s*r\.score;\s*\n',
        '\n',
        "Removed scoreEl.textContent assignment"
    ),
    (
        r'\s*scoreEl\.className\s*=\s*`score-number\s*\$\{r\.riskLevel\s*!==\s*[\'"]low[\'"]\s*\?\s*r\.riskLevel\s*:\s*[\'"][\'"]\}`;\s*\n',
        '\n',
        "Removed scoreEl.className assignment"
    ),
    (
        r'\s*const\s+scoreEl\s*=\s*document\.getElementById\([\'"]score-number[\'"]\);\s*\n',
        '\n',
        "Removed scoreEl lookup"
    ),
]

for pattern, repl, label in js_patterns:
    regex_once(pattern, repl, label)

# 3) Optional cleanup: remove empty score-display wrapper if it only contains label + bar
# We do NOT aggressively remove the wrapper, only normalize double blank lines.
text = re.sub(r'\n{3,}', '\n\n', text)
changes.append("✅ Normalized extra blank lines")

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

print("\nVerify with:")
print("grep -n -C 2 \"score-number\\|scoreEl\\|System Resilience\" src/pages/guild-checker.astro")
print("npm run build")