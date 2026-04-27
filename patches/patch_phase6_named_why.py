from pathlib import Path
import re
import shutil

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
backup = f.with_suffix(".astro.bak_named_why")
shutil.copy2(f, backup)

new_fn = r"""// ── Why This Guild Works narrative ───────────────────────────────────────────
function generateWhyNarrative(guildSlugs, fnAnalysis, r) {
  const c = fnAnalysis.counts;
  const pests = r.sharedPests || [];
  const results = [];

  const plants = guildSlugs
    .map(slug => plantBySlug[slug])
    .filter(Boolean);

  const byRole = (role) =>
    plants.filter(p => (p.plant_function || []).includes(role));

  const names = (arr, limit = 2) =>
    arr.slice(0, limit).map(p => p.common_name || p.slug).join(arr.length > 1 ? ' and ' : '');

  const nitrogenPlants = byRole('Nitrogen Fixer');
  const mulchPlants = byRole('Mulcher');
  if (nitrogenPlants.length && mulchPlants.length) {
    results.push(`${names(nitrogenPlants)} help feed the system with nitrogen, while ${names(mulchPlants)} add biomass that breaks down into soil fertility.`);
  } else if (nitrogenPlants.length) {
    results.push(`${names(nitrogenPlants)} help feed nearby plants by adding nitrogen support to the guild.`);
  } else if (mulchPlants.length) {
    results.push(`${names(mulchPlants)} add biomass that can feed soil life and build organic matter over time.`);
  }

  const groundPlants = byRole('Ground Cover');
  if (groundPlants.length) {
    results.push(`${names(groundPlants)} protect exposed soil, hold moisture, and help reduce weed pressure.`);
  }

  const pollPlants = byRole('Pollinator');
  const pestPlants = byRole('Pest Management');
  if (pollPlants.length && pestPlants.length) {
    results.push(`${names(pollPlants)} support pollinators, while ${names(pestPlants)} help disrupt pests and keep insect pressure more balanced.`);
  } else if (pollPlants.length) {
    results.push(`${names(pollPlants)} support pollinators and beneficial insects that help the whole guild function.`);
  } else if (pestPlants.length) {
    results.push(`${names(pestPlants)} help confuse, repel, or interrupt pest pressure naturally.`);
  }

  const shadePlants = byRole('Shade Provider');
  const anchors = plants.filter(p => p.food_role === 'anchor');
  if (shadePlants.length) {
    results.push(`${names(shadePlants)} add shade and structure, creating a more stable micro-environment for nearby plants.`);
  } else if (anchors.length) {
    results.push(`${names(anchors)} act as long-term anchor plants, giving the guild structure instead of just short-season production.`);
  } else if (r.resilience > 70) {
    results.push(`This guild spreads growth across multiple layers, which makes the system more stable than a flat planting of similar crops.`);
  }

  const accumPlants = byRole('Dynamic Accumulator');
  if (accumPlants.length) {
    results.push(`${names(accumPlants)} help cycle nutrients by pulling them from deeper soil and returning them through leaf drop, chop-and-drop, or dieback.`);
  }

  if (pests.length > 0 && r.breakdown.pestOverlap < 40) {
    results.push(`Some shared pest pressure exists, but the guild spreads risk across different plants instead of relying on one crop.`);
  }

  if (fnAnalysis.reinforced.length >= 3) {
    results.push(`Several key jobs are backed up by more than one plant, so the system is less dependent on any single species.`);
  }

  return results.slice(0, 5);
}

// ── Guild Pattern Recognition (Phase 5) ──────────────────────────────────────"""

# Replace existing generateWhyNarrative block
pattern = r"// ── Why This Guild Works narrative ─[\s\S]*?// ── Guild Pattern Recognition \(Phase 5\) ─+"
text2, count = re.subn(pattern, new_fn, text, count=1)

if count != 1:
    print("❌ Could not replace generateWhyNarrative block")
else:
    text = text2
    print("✅ Replaced generateWhyNarrative with named-plant version")

# Update function call
old_call = "const whyPoints = generateWhyNarrative(fnAnalysis, r);"
new_call = "const whyPoints = generateWhyNarrative(guildSlugs, fnAnalysis, r);"

if old_call in text:
    text = text.replace(old_call, new_call, 1)
    print("✅ Updated renderResults call")
elif new_call in text:
    print("✅ renderResults call already updated")
else:
    print("❌ Could not find generateWhyNarrative call")

f.write_text(text)
print(f"🗂 Backup created: {backup}")