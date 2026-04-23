from pathlib import Path
import shutil
import sys

FILE = Path("src/pages/guild-checker.astro")

if not FILE.exists():
    print(f"❌ File not found: {FILE}")
    sys.exit(1)

text = FILE.read_text(encoding="utf-8")
original = text

backup = FILE.with_suffix(FILE.suffix + ".bak_score_label")
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

replace_once(
    '<div class="score-label" id="score-label">LOW PRESSURE — RESILIENCE: 100</div>',
    '<div class="score-label" id="score-label">Resilience: 100 — low pest overlap</div>',
    "Updated default score label"
)

replace_once(
    "labelEl.textContent = `${pressureLabel} PEST OVERLAP — RESILIENCE: ${r.resilience}`;",
    "labelEl.textContent = `Resilience: ${r.resilience} — ${pressureLabel.toLowerCase()} pest overlap`;",
    "Made runtime score label resilience-first"
)

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
print("grep -n -C 2 \"score-label\\|labelEl.textContent\" src/pages/guild-checker.astro")