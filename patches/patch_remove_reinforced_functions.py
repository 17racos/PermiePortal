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

backup = FILE.with_suffix(FILE.suffix + ".bak_remove_reinforced")
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
# 1) Remove the HTML block for Reinforced Functions section
# ------------------------------------------------------------

html_patterns = [
    (
        r'''
        \s*<div[^>]*>\s*
        <p class="panel-label">Reinforced Functions</p>
        .*?
        </div>
        ''',
        '\n',
        "Removed generic Reinforced Functions panel block",
    ),
    (
        r'''
        \s*<section[^>]*>\s*
        <p class="panel-label">Reinforced Functions</p>
        .*?
        </section>
        ''',
        '\n',
        "Removed section-based Reinforced Functions block",
    ),
    (
        r'''
        \s*<div[^>]*id="[^"]*reinforced[^"]*"[^>]*>\s*
        .*?
        <p class="panel-label">Reinforced Functions</p>
        .*?
        </div>
        ''',
        '\n',
        "Removed id-based Reinforced Functions block",
    ),
]

removed_html = False
for pattern, repl, label in html_patterns:
    if regex_once(pattern, repl, label, flags=re.DOTALL | re.VERBOSE):
        removed_html = True
        break

# ------------------------------------------------------------
# 2) Remove likely JS references for rendering/toggling the section
# ------------------------------------------------------------

js_patterns = [
    (
        r'\s*const\s+reinforcedEl\s*=\s*document\.getElementById\([\'"][^\'"]*reinforced[^\'"]*[\'"]\);\s*\n',
        '\n',
        "Removed reinforcedEl lookup",
    ),
    (
        r'\s*const\s+reinforcedWrap\s*=\s*document\.getElementById\([\'"][^\'"]*reinforced[^\'"]*[\'"]\);\s*\n',
        '\n',
        "Removed reinforcedWrap lookup",
    ),
    (
        r'\s*reinforcedEl\.innerHTML\s*=.*?;\s*\n',
        '\n',
        "Removed reinforcedEl.innerHTML assignment",
    ),
    (
        r'\s*reinforcedWrap\.innerHTML\s*=.*?;\s*\n',
        '\n',
        "Removed reinforcedWrap.innerHTML assignment",
    ),
    (
        r'\s*reinforcedEl\.style\.display\s*=.*?;\s*\n',
        '\n',
        "Removed reinforcedEl display toggle",
    ),
    (
        r'\s*reinforcedWrap\.style\.display\s*=.*?;\s*\n',
        '\n',
        "Removed reinforcedWrap display toggle",
    ),
    (
        r'\s*if\s*\(\s*reinforcedEl\s*\)\s*reinforcedEl\.innerHTML\s*=.*?;\s*\n',
        '\n',
        "Removed guarded reinforcedEl assignment",
    ),
    (
        r'\s*if\s*\(\s*reinforcedWrap\s*\)\s*reinforcedWrap\.innerHTML\s*=.*?;\s*\n',
        '\n',
        "Removed guarded reinforcedWrap assignment",
    ),
]

for pattern, repl, label in js_patterns:
    regex_all(pattern, repl, label)

# ------------------------------------------------------------
# 3) Remove literal label references if still present
# ------------------------------------------------------------

literal_once("Reinforced Functions", "", "Removed leftover literal label")

# ------------------------------------------------------------
# 4) Clean up excessive blank lines
# ------------------------------------------------------------

text = re.sub(r'\n{3,}', '\n\n', text)
changes.append("✅ Normalized extra blank lines")

# ------------------------------------------------------------
# 5) Write file
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

print("\nVerify with:")
print('grep -n "Reinforced Functions\\|reinforcedEl\\|reinforcedWrap\\|reinforced" src/pages/guild-checker.astro')
print("npm run build")