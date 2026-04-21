#!/usr/bin/env python3
"""
patch_next_plant.py
===================
Adds "Suggested Next Plants" section to Guild Builder.
Inlines getNextBestPlants() logic from src/lib/nextPlant.js
(define:vars scripts cannot import ES modules).
"""
from pathlib import Path
import shutil

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

# ── 1. Copy nextPlant.js to src/lib/ ─────────────────────────────────────────
src = Path("nextPlant.js")
dst = Path("src/lib/nextPlant.js")
if src.exists() and not dst.exists():
    shutil.copy(src, dst)
    print("✅ nextPlant.js copied to src/lib/")
elif dst.exists():
    print("⏭️  src/lib/nextPlant.js already exists")
else:
    print("⚠️  nextPlant.js not found in current dir — skipping copy")

# ── 2. Add Suggested Next Plants HTML section ─────────────────────────────────
old_html = """      <div class="result-section" id="section-actions">
        <p class="result-section-title">Design Actions</p>
        <div class="actions-list" id="actions-list"></div>
      </div>"""

new_html = """      <div class="result-section" id="section-actions">
        <p class="result-section-title">Design Actions</p>
        <div class="actions-list" id="actions-list"></div>
      </div>

      <div class="result-section" id="section-next-plants" style="display:none">
        <p class="result-section-title">Suggested Next Plants</p>
        <p class="next-plants-note" id="next-plants-note"></p>
        <div class="next-plants-list" id="next-plants-list"></div>
      </div>"""

if old_html in text:
    text = text.replace(old_html, new_html)
    changes += 1; print("✅ 1: Suggested Next Plants HTML section added")
else: print("❌ 1: HTML anchor not found")

# ── 3. Add CSS for next plants section ───────────────────────────────────────
old_css = "  .reinforced-chip-count { font-family: 'Bebas Neue', sans-serif; font-size: 0.9rem; line-height: 1; color: var(--lime); opacity: 0.8; }"
new_css = """  .reinforced-chip-count { font-family: 'Bebas Neue', sans-serif; font-size: 0.9rem; line-height: 1; color: var(--lime); opacity: 0.8; }
  .next-plants-note { font-size: 0.78rem; color: var(--ash); font-style: italic; margin-bottom: 0.75rem; line-height: 1.5; }
  .next-plants-list { display: flex; flex-direction: column; gap: 0.5rem; }
  .next-plant-card { display: block; text-decoration: none; padding: 0.75rem 1rem; background: var(--bark); border: 1px solid rgba(139,184,58,0.15); transition: border-color 0.2s; }
  .next-plant-card:hover { border-color: rgba(139,184,58,0.35); }
  .next-plant-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.35rem; }
  .next-plant-name { font-family: 'Space Mono', monospace; font-size: 0.72rem; color: var(--paper); }
  .next-plant-family { font-size: 0.65rem; color: var(--ash); font-style: italic; }
  .next-plant-score { font-family: 'Bebas Neue', sans-serif; font-size: 1rem; color: var(--lime); line-height: 1; }
  .next-plant-reasons { display: flex; flex-wrap: wrap; gap: 0.3rem; }
  .next-plant-reason { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); padding: 0.1rem 0.45rem; border: 1px solid rgba(139,184,58,0.2); background: rgba(42,61,31,0.2); }"""

if old_css in text:
    text = text.replace(old_css, new_css)
    changes += 1; print("✅ 2: CSS added for next plants section")
else: print("❌ 2: CSS anchor not found")

# ── 4. Add getNextBestPlants() function before renderGuild() ─────────────────
old_fn_anchor = "// ── Render ────────────────────────────────────────────────────────────────────\nfunction renderGuild() {"
new_fn = """// ── Next Best Plant scorer (inlined from src/lib/nextPlant.js) ──────────────
// NOTE: Keep in sync with src/lib/nextPlant.js when changing logic.
const NEXT_FOUNDATIONAL_ROLES = [
  'Nitrogen Fixer', 'Ground Cover', 'Pollinator', 'Pest Management', 'Mulcher',
];

function getNextBestPlants(currentSlugs, limit = 5) {
  const guildSet = new Set(currentSlugs);
  const n = currentSlugs.length;
  if (n === 0) return [];

  // Guild context
  const guildFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
  const familyCounts = {};
  for (const s of currentSlugs) {
    const f = plantToFamily[s];
    if (f) familyCounts[f] = (familyCounts[f] || 0) + 1;
  }
  const dominantFamily = Object.entries(familyCounts).sort((a,b) => b[1]-a[1])[0]?.[0] || null;

  // Guild function counts
  const guildFnCounts = {};
  for (const role of NEXT_FOUNDATIONAL_ROLES) guildFnCounts[role] = 0;
  for (const slug of currentSlugs) {
    const p = plantBySlug[slug];
    if (!p) continue;
    for (const fn of (p.plant_function || [])) {
      if (guildFnCounts.hasOwnProperty(fn)) guildFnCounts[fn]++;
    }
  }
  const missingRoles = NEXT_FOUNDATIONAL_ROLES.filter(r => guildFnCounts[r] === 0);
  const weakRoles    = NEXT_FOUNDATIONAL_ROLES.filter(r => guildFnCounts[r] === 1);

  // Guild pest set
  const guildPests = new Set();
  for (const slug of currentSlugs) {
    for (const pest of (plantToPests[slug] || new Set())) guildPests.add(pest);
  }

  const candidates = [];
  for (const p of plantIndex) {
    if (guildSet.has(p.slug)) continue;
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    let roleScore = 0;
    const roleReasons = [];
    for (const fn of fns) {
      if (missingRoles.includes(fn)) {
        roleScore += 2;
        roleReasons.push(`Adds ${fn}`);
      } else if (weakRoles.includes(fn)) {
        roleScore += 1;
        roleReasons.push(`Strengthens ${fn}`);
      }
    }

    let sharedPestCount = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPestCount++; }

    let familyScore = 0;
    const familyReasons = [];
    if (family && !guildFamilies.has(family)) {
      familyScore = 1;
      familyReasons.push(`New family: ${family}`);
    } else if (family && family === dominantFamily) {
      familyScore = -1;
    }

    const pestReasons = [];
    if (sharedPestCount === 0 && pests.size > 0) pestReasons.push('No shared pests');
    else if (sharedPestCount <= 2 && pests.size > 0) pestReasons.push('Low pest overlap');

    const score = (roleScore * 2) + familyScore - (sharedPestCount * 0.5);
    if (score <= 0 && roleReasons.length === 0) continue;

    const reasons = [...roleReasons, ...familyReasons, ...pestReasons].slice(0, 3);
    if (reasons.length === 0) continue;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      reasons, score: Math.round(score * 10) / 10,
    });
  }

  candidates.sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));
  return candidates.slice(0, limit);
}

// ── Render ────────────────────────────────────────────────────────────────────
function renderGuild() {"""

if old_fn_anchor in text:
    text = text.replace(old_fn_anchor, new_fn)
    changes += 1; print("✅ 3: getNextBestPlants() function added")
else: print("❌ 3: render anchor not found")

# ── 5. Wire next plants rendering in renderResults() ─────────────────────────
old_wire = """  if (fnAnalysis) {
    // ── Reinforced Functions — chips display ──────────────────────────────────"""

new_wire = """  // ── Suggested Next Plants ──────────────────────────────────────────────────
  const nextSection = document.getElementById('section-next-plants');
  const nextNote    = document.getElementById('next-plants-note');
  const nextList    = document.getElementById('next-plants-list');

  if (guild.length >= 2) {
    const suggestions = getNextBestPlants(guild, 5);
    if (suggestions.length > 0) {
      nextNote.textContent = 'Plants scored by role coverage, family diversity, and pest overlap with your current guild.';
      nextList.innerHTML = suggestions.map(p => `
        <a href="/plants/${p.slug}" class="next-plant-card" target="_blank">
          <div class="next-plant-header">
            <div>
              <div class="next-plant-name">${p.name}</div>
              ${p.family ? `<div class="next-plant-family">${p.family}</div>` : ''}
            </div>
            <div class="next-plant-score">${p.score}</div>
          </div>
          <div class="next-plant-reasons">
            ${p.reasons.map(r => `<span class="next-plant-reason">${r}</span>`).join('')}
          </div>
        </a>
      `).join('');
      nextSection.style.display = 'block';
    } else {
      nextSection.style.display = 'none';
    }
  } else {
    nextSection.style.display = 'none';
  }

  if (fnAnalysis) {
    // ── Reinforced Functions — chips display ──────────────────────────────────"""

if old_wire in text:
    text = text.replace(old_wire, new_wire)
    changes += 1; print("✅ 4: next plants wired into renderResults()")
else: print("❌ 4: renderResults anchor not found")

f.write_text(text)
print(f"\n{changes} patches applied")
