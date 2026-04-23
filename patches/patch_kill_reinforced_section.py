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

backup = FILE.with_suffix(FILE.suffix + ".bak_kill_reinforced")
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


# ------------------------------------------------------------
# 1) Remove the HTML block (section-reinforced)
# ------------------------------------------------------------

regex_once(
    r'''
    <div\s+class="result-section"\s+id="section-reinforced".*?</div>
    ''',
    '',
    "Removed section-reinforced HTML block",
    flags=re.DOTALL | re.VERBOSE
)


# ------------------------------------------------------------
# 2) Remove the JS rendering logic block
# ------------------------------------------------------------

regex_once(
    r'''
    //\s*──\s*Reinforced\s*Functions.*?
    \}\s*else\s*\{
\s*reinforcedSection\.style\.display\s*=\s*['"]none['"];
\s*\}
    ''',
    '',
    "Removed reinforced rendering logic block",
    flags=re.DOTALL | re.VERBOSE
)


# ------------------------------------------------------------
# 3) Cleanup leftover variable declarations
# ------------------------------------------------------------

regex_once(
    r'\s*const\s+reinforcedSection\s*=.*?;\n',
    '',
    "Removed reinforcedSection variable"
)

regex_once(
    r'\s*const\s+reinforcedChips\s*=.*?;\n',
    '',
    "Removed reinforcedChips variable"
)

regex_once(
    r'\s*const\s+reinforcedRoles\s*=.*?;\n',
    '',
    "Removed reinforcedRoles variable"
)


# ------------------------------------------------------------
# 4) Clean up spacing
# ------------------------------------------------------------

text = re.sub(r'\n{3,}', '\n\n', text)
changes.append("✅ Cleaned spacing")


# ------------------------------------------------------------
# Write file
# ------------------------------------------------------------

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

print("\nVerify:")
print('grep -n "section-reinforced\\|reinforced-chips\\|reinforcedSection\\|reinforcedRoles" src/pages/guild-checker.astro')
print("npm run build")