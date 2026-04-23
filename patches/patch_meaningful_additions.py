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

backup = FILE.with_suffix(FILE.suffix + ".bak_meaningful")
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
# 1) Inject meaningful contribution gate into Phase 2 loop
# ------------------------------------------------------------

pattern = r"(let\s+score\s*=\s*scorePlant\(p,\s*generated\)\s*-\s*layerPenalty;\s*)"

replacement = r"""\1

        // ── Meaningful contribution gate ─────────────────────────────
        let improves = false;

        // 1. Fills missing foundational role
        if (fnAnalysis && fnAnalysis.missingFoundational) {
          for (const role of fnAnalysis.missingFoundational) {
            if (p.plant_function && p.plant_function.includes(role)) {
              improves = true;
              break;
            }
          }
        }

        // 2. Adds new family
        const fam = plantToFamily[p.slug] || '__none__';
        if (!famSeen[fam]) improves = true;

        // 3. Adds new layer
        const layer = inferLayer(p);
        if (!layerSeen[layer]) improves = true;

        // 4. Mild fallback: only allow if score is high AND guild is small
        if (!improves && generated.length < 5 && score > 2.5) {
          improves = true;
        }

        if (!improves) continue;
"""

regex_once(
    pattern,
    replacement,
    "Added meaningful contribution gate to Phase 2",
)

# ------------------------------------------------------------
# 2) Clean spacing
# ------------------------------------------------------------

text = re.sub(r'\n{3,}', '\n\n', text)
changes.append("✅ Cleaned spacing")

# ------------------------------------------------------------
# Write
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
print("grep -n \"Meaningful contribution gate\" src/pages/guild-checker.astro")
print("npm run build")