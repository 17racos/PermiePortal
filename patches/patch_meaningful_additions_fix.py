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

backup = FILE.with_suffix(FILE.suffix + ".bak_meaningful_fix")
shutil.copy2(FILE, backup)

changes = []

old_block_pattern = r"""
        //\s*──\s*Meaningful\ contribution\ gate.*?
        if\s*\(!improves\)\s*continue;
"""

new_block = """        // ── Meaningful contribution gate ─────────────────────────────
        let improves = false;

        // Compute missing foundational roles from the current generated guild
        const currentCounts = {};
        for (const existingSlug of generated) {
          const existingPlant = plantBySlug[existingSlug];
          if (!existingPlant) continue;
          for (const fn of (existingPlant.plant_function || [])) {
            currentCounts[fn] = (currentCounts[fn] || 0) + 1;
          }
        }

        const missingFoundational = FOUNDATIONAL_ROLES.filter(role => (currentCounts[role] || 0) === 0);

        // 1. Fills a currently missing foundational role
        if (p.plant_function && p.plant_function.some(role => missingFoundational.includes(role))) {
          improves = true;
        }

        // 2. Adds new family
        const fam = plantToFamily[p.slug] || '__none__';
        if (!famSeen[fam]) improves = true;

        // 3. Adds new layer
        const layer = inferLayer(p);
        if (!layerSeen[layer]) improves = true;

        // 4. Mild fallback: only allow if score is high and guild is still small
        if (!improves && generated.length < 5 && score > 2.5) {
          improves = true;
        }

        if (!improves) continue;
"""

new_text, count = re.subn(old_block_pattern, new_block, text, count=1, flags=re.DOTALL | re.VERBOSE)
if count:
    text = new_text
    changes.append("✅ Replaced fnAnalysis-based meaningful gate with local generated-guild analysis")
else:
    changes.append("❌ Could not find meaningful gate block to replace")

text = re.sub(r'\n{3,}', '\n\n', text)
changes.append("✅ Cleaned spacing")

if text != original:
    FILE.write_text(text, encoding="utf-8")
    print(f"✅ Patched {FILE}")
    print(f"🗂 Backup created: {backup}")
else:
    print("ℹ️ No changes were written")
    print(f"🗂 Backup created: {backup}")

print("\nPatch report:")
for c in changes:
    print(c)

print("\nVerify with:")
print('grep -n "Meaningful contribution gate\\|missingFoundational\\|fnAnalysis" src/pages/guild-checker.astro')
print("npm run build")