from pathlib import Path
import shutil
import re

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
backup = f.with_suffix(".astro.bak_phase6_ui_translation")
shutil.copy2(f, backup)

changes = 0

def replace(old, new, label):
    global text, changes
    if old in text:
        text = text.replace(old, new)
        changes += 1
        print(f"✅ {label}")
    else:
        print(f"❌ {label}")

# 1. Add UI-only role label map
anchor = "const ALL_TRACKED_ROLES = [...FOUNDATIONAL_ROLES, ...CONTEXTUAL_ROLES];"
insert = """const ALL_TRACKED_ROLES = [...FOUNDATIONAL_ROLES, ...CONTEXTUAL_ROLES];

const ROLE_LABELS = {
  'Nitrogen Fixer': 'Soil Feeding',
  'Ground Cover': 'Living Groundcover',
  'Pollinator': 'Pollinator Support',
  'Pest Management': 'Plant Health Defense',
  'Mulcher': 'Biomass / Mulch',
  'Dynamic Accumulator': 'Nutrient Cycling',
  'Erosion Control': 'Soil Holding',
  'Shade Provider': 'Shade / Microclimate',
};

function roleLabel(role) {
  return ROLE_LABELS[role] || role;
}"""

if "const ROLE_LABELS =" not in text:
    replace(anchor, insert, "Added UI role label map")
else:
    print("✅ ROLE_LABELS already present")

# 2. Rename section title
replace("Function Balance", "Guild Jobs Covered", "Renamed Function Balance")

# 3. Replace role display text in common render patterns
replace("${role}", "${roleLabel(role)}", "Mapped template role labels")
replace("tag.textContent = role;", "tag.textContent = roleLabel(role);", "Mapped tag role label")
replace("label.textContent = role;", "label.textContent = roleLabel(role);", "Mapped label role")
replace("title.textContent = role;", "title.textContent = roleLabel(role);", "Mapped title role")

# 4. Humanize status wording
replace("reinforced", "reinforced", "Kept reinforced wording")
replace("present", "covered", "Changed present → covered")
replace("contextual", "supporting", "Changed contextual → supporting")

# 5. Rename pest/mitigation language
replace("Pest Buffering", "Plant Health Defense", "Renamed Pest Buffering")
replace("Weak buffering", "Weak defense", "Renamed weak buffering")
replace("Moderate mitigation", "Moderate defense", "Renamed moderate mitigation")
replace("Strong mitigation", "Strong defense", "Renamed strong mitigation")
replace("Shared Pest Signals (supporting detail)", "Common Problems to Watch", "Renamed pest signals heading")
replace("Shared Pest Signals", "Common Problems to Watch", "Renamed pest signals fallback")

# 6. Make pest tags clickable
old_pest = """tag.innerHTML = `${p.name}<span class="pest-count">×${p.count}</span>`;"""
new_pest = """const pestSlug = String(p.name).toLowerCase()
          .replace(/&/g, 'and')
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-+|-+$/g, '');
        tag.innerHTML = `<a href="/pests/${pestSlug}" class="pest-link">${p.name}<span class="pest-count">×${p.count}</span></a>`;"""

if old_pest in text:
    replace(old_pest, new_pest, "Linked pest tags to pest pages")
else:
    print("❌ Pest tag render line not found")

# 7. Add pest link CSS
css_anchor = ".pest-tag {"
css_insert = """.pest-link { color: inherit; text-decoration: none; }
  .pest-link:hover { color: var(--lime); text-decoration: underline; }
  .pest-tag {"""

if ".pest-link {" not in text and css_anchor in text:
    replace(css_anchor, css_insert, "Added pest link CSS")
else:
    print("✅ pest link CSS already present or anchor missing")

f.write_text(text)
print(f"\\n{changes} patch groups applied")
print(f"Backup: {backup}")