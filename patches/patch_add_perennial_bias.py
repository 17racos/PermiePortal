from pathlib import Path

file = Path("src/pages/guild-checker.astro")
text = file.read_text()

original = text
changes = 0

# --------------------------------------------------
# 1. Patch scorePlant()
# --------------------------------------------------

if "Perennial bias (Permaculture principle)" not in text:
    import re

    pattern = r"(function scorePlant\(.*?\{.*?)(\n)"
    match = re.search(pattern, text, flags=re.DOTALL)

    if match:
        insert_block = """
  // ── Perennial bias (Permaculture principle) ─────────────────
  if (goalKey === 'food_production') {
    if (p.perennial === true) {
      goalScore += 1.2;
    } else if (p.perennial === false) {
      goalScore -= 1.0;
    }
  }
"""
        # Insert after function start
        start = match.end(1)
        text = text[:start] + insert_block + text[start:]
        changes += 1
        print("✅ Added perennial bias to scorePlant()")
    else:
        print("❌ Could not find scorePlant()")

else:
    print("⚠️ scorePlant() already patched")

# --------------------------------------------------
# 2. Patch getNextBestPlants()
# --------------------------------------------------

if "perennialBias" not in text:
    import re

    # Find scoring section inside getNextBestPlants
    pattern = r"(function getNextBestPlants\(.*?\{.*?)(let score = )"
    match = re.search(pattern, text, flags=re.DOTALL)

    if match:
        insert_block = """
      let perennialBias = 0;

      if (selectedGoal === 'food_production') {
        if (p.perennial === true) perennialBias = 1.2;
        else if (p.perennial === false) perennialBias = -1.0;
      }

"""

        insert_pos = match.end(1)
        text = text[:insert_pos] + insert_block + text[insert_pos:]
        changes += 1
        print("✅ Added perennial bias variable to getNextBestPlants()")
    else:
        print("❌ Could not find getNextBestPlants()")

    # Add to score line
    text = text.replace(
        "let score =",
        "let score = perennialBias +",
        1
    )

else:
    print("⚠️ getNextBestPlants() already patched")

# --------------------------------------------------
# Write file
# --------------------------------------------------

if text != original:
    backup = file.with_suffix(".astro.bak_perennial")
    backup.write_text(original)
    file.write_text(text)
    print(f"🗂 Backup created: {backup}")
    print("🎯 Patch complete")
else:
    print("No changes made")