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

backup = FILE.with_suffix(FILE.suffix + ".bak_food_guild_sanity")
shutil.copy2(FILE, backup)

changes = []

def literal_once(old, new, label):
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

def ensure_insert_once(anchor_pattern, insert_text, label, flags=re.DOTALL):
    global text
    if insert_text.strip() in text:
        changes.append(f"✅ {label} already present")
        return True
    m = re.search(anchor_pattern, text, flags=flags)
    if not m:
        changes.append(f"❌ {label}")
        return False
    idx = m.end()
    text = text[:idx] + insert_text + text[idx:]
    changes.append(f"✅ {label}")
    return True


# ------------------------------------------------------------
# 1) Make Food Production complete missing gaps require Pest Management
# ------------------------------------------------------------

# If food_production profile has anchorRoles but no Pest Management, add it.
regex_once(
    r"(food_production\s*:\s*\{.*?anchorRoles\s*:\s*\{)(.*?)(\}\s*,)",
    lambda m: (
        m.group(1) + m.group(2)
        if "Pest Management" in m.group(2)
        else m.group(1) + m.group(2).rstrip() + (
            ("," if m.group(2).strip() and not m.group(2).strip().endswith(",") else "")
            + "\n      'Pest Management': 1\n    "
        ) + m.group(3)
    ),
    "Added Pest Management to food_production.anchorRoles",
    flags=re.DOTALL
)

# ------------------------------------------------------------
# 2) Exclude clearly bad Food Production suggestions/candidates
# ------------------------------------------------------------

# Add Roselle to Food Production exclusions if not already there.
# This assumes a FOOD_PRODUCTION_EXCLUDE array exists.
regex_once(
    r"(const\s+FOOD_PRODUCTION_EXCLUDE\s*=\s*\[)(.*?)(\];)",
    lambda m: (
        m.group(1) + m.group(2) + m.group(3)
        if "'roselle'" in m.group(2) or '"roselle"' in m.group(2)
        else m.group(1) + m.group(2).rstrip() + (
            ("," if m.group(2).strip() and not m.group(2).strip().endswith(",") else "")
            + "\n  'roselle'"
        ) + "\n" + m.group(3)
    ),
    "Added roselle to FOOD_PRODUCTION_EXCLUDE",
    flags=re.DOTALL
)

# ------------------------------------------------------------
# 3) Add a simple habitat sanity helper
# ------------------------------------------------------------

sanity_helper = r"""

function isBadDrylandFoodGuildCandidate(p) {
  if (!p) return false;
  const name = (p.common_name || '').toLowerCase();
  const funcs = Array.isArray(p.plant_function) ? p.plant_function.map(x => String(x).toLowerCase()) : [];
  const habit = String(p.growth_habit || '').toLowerCase();
  const layers = Array.isArray(p.layers) ? p.layers.map(x => String(x).toLowerCase()) : [];

  // Hard-name guardrails for clearly wrong suggestions in standard dryland food guilds
  const bannedNames = [
    'bladderwort',
    'butterwort'
  ];
  if (bannedNames.some(x => name.includes(x))) return true;

  // Generic habitat-ish guardrails if represented indirectly
  if (habit.includes('aquatic')) return true;
  if (layers.includes('aquatic')) return true;
  if (funcs.includes('aquatic')) return true;
  if (funcs.includes('wetland')) return true;
  if (funcs.includes('bog')) return true;

  return false;
}
"""

if "function isBadDrylandFoodGuildCandidate(p)" not in text:
    inserted = ensure_insert_once(
        r"(function\s+getZoneFit\s*\([^\)]*\)\s*\{.*?\n\})",
        "\n" + sanity_helper,
        "Inserted dryland food guild sanity helper",
        flags=re.DOTALL
    )
    if not inserted:
        # fallback: place before generateGoalGuild
        ensure_insert_once(
            r"(function\s+generateGoalGuild\s*\()",
            sanity_helper + "\n",
            "Inserted sanity helper before generateGoalGuild",
            flags=re.DOTALL
        )
else:
    changes.append("✅ dryland food guild sanity helper already present")

# ------------------------------------------------------------
# 4) Apply sanity filter inside pickBestForRole()
# ------------------------------------------------------------

regex_once(
    r"(if\s*\(\s*goalKey\s*===\s*'food_production'\s*&&\s*requiredRole\s*===\s*'Edible'\s*\)\s*\{.*?\n\s*\})",
    lambda m: m.group(1) + "\n\n        if (goalKey === 'food_production' && isBadDrylandFoodGuildCandidate(p)) continue;",
    "Added sanity filter to pickBestForRole",
    flags=re.DOTALL
)

# fallback if above misses
regex_once(
    r"(if\s*\(\s*getZoneFit\(p,\s*userZone\)\s*===\s*'out'\s*\)\s*continue;\s*)",
    r"\1        if (goalKey === 'food_production' && isBadDrylandFoodGuildCandidate(p)) continue;\n",
    "Added fallback sanity filter near zone check in pickBestForRole",
    flags=re.DOTALL
)

# ------------------------------------------------------------
# 5) Apply sanity filter inside Phase 2 generation loop
# ------------------------------------------------------------

regex_once(
    r"(if\s*\(\s*goalKey\s*===\s*'food_production'\s*&&\s*p\.food_role\s*===\s*'specialty'\s*\)\s*continue;\s*)",
    r"\1        if (goalKey === 'food_production' && isBadDrylandFoodGuildCandidate(p)) continue;\n",
    "Added sanity filter to Phase 2 generation loop",
    flags=re.DOTALL
)

# ------------------------------------------------------------
# 6) Apply sanity filter inside getNextBestPlants()
# ------------------------------------------------------------

# Try to inject after dismissedSuggestions continue
regex_once(
    r"(if\s*\(\s*dismissedSuggestions\.has\(p\.slug\)\s*\)\s*continue;\s*)",
    r"\1      if (selectedGoal === 'food_production' && isBadDrylandFoodGuildCandidate(p)) continue;\n",
    "Added sanity filter to getNextBestPlants after dismissedSuggestions",
    flags=re.DOTALL
)

# fallback: inject after removedByUser continue
regex_once(
    r"(if\s*\(\s*removedByUser\.has\(p\.slug\)\s*\)\s*continue;\s*)",
    r"\1      if (selectedGoal === 'food_production' && isBadDrylandFoodGuildCandidate(p)) continue;\n",
    "Added fallback sanity filter to getNextBestPlants after removedByUser",
    flags=re.DOTALL
)

# ------------------------------------------------------------
# 7) Mild penalty for trap-crop-ish Roselle in Food Production even if not excluded elsewhere
# ------------------------------------------------------------

regex_once(
    r"(if\s*\(\s*goalKey\s*===\s*'food_production'\s*&&\s*zoneFit\s*===\s*'microclimate'\s*\)\s*score\s*-=\s*1\.0;\s*)",
    r"\1        if (goalKey === 'food_production' && p.slug === 'roselle') score -= 3.0;\n",
    "Added Roselle penalty in scorePlant flow",
    flags=re.DOTALL
)

# ------------------------------------------------------------
# 8) Clean spacing
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
    print("ℹ️ No changes were written")
    print(f"🗂 Backup created: {backup}")

print("\nPatch report:")
for c in changes:
    print(c)

print("\nVerify with:")
print("grep -n \"Pest Management\\|roselle\\|isBadDrylandFoodGuildCandidate\\|bladderwort\\|butterwort\" src/pages/guild-checker.astro")
print("npm run build")