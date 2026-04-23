#!/usr/bin/env python3
"""
patch_phase5_pattern.py
=======================
Phase 5 — Guild Pattern Recognition:
1. analyzeGuildPattern() function
2. System Pattern HTML section (between mitigation and suggestions)
3. CSS for pattern display
4. Wire into renderResults()
"""
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

def patch(old, new, label):
    global text, changes
    if old in text:
        text = text.replace(old, new)
        changes += 1
        print(f"✅ {label}")
    else:
        print(f"❌ {label}")

# ── 1. Add System Pattern HTML section ───────────────────────────────────────
patch(
    '      <div class="result-section" id="section-suggestions">',
    """      <div class="result-section" id="section-pattern" style="display:none">
        <p class="result-section-title">System Pattern</p>
        <div id="pattern-display"></div>
      </div>

      <div class="result-section" id="section-suggestions">""",
    "1: System Pattern HTML section added"
)

# ── 2. Add CSS ────────────────────────────────────────────────────────────────
patch(
    "  .mitigation-label { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); margin-top: 0.15rem; font-style: italic; }",
    """  .mitigation-label { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); margin-top: 0.15rem; font-style: italic; }
  .pattern-primary { font-family: 'Space Mono', monospace; font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--lime); margin-bottom: 0.3rem; }
  .pattern-summary { font-size: 0.85rem; color: var(--ash); line-height: 1.6; margin-bottom: 0.5rem; font-style: italic; }
  .pattern-traits { display: flex; flex-wrap: wrap; gap: 0.3rem; }
  .pattern-chip { font-family: 'Space Mono', monospace; font-size: 0.58rem; padding: 0.15rem 0.5rem; border: 1px solid rgba(139,184,58,0.2); color: var(--ash); }""",
    "2: pattern CSS added"
)

# ── 3. Add analyzeGuildPattern() function before renderGuild() ────────────────
patch(
    "// ── Render ────────────────────────────────────────────────────────────────────\nfunction renderGuild() {",
    """// ── Guild Pattern Recognition (Phase 5) ──────────────────────────────────────
function analyzeGuildPattern(guildSlugs, fnAnalysis, r) {
  const counts  = fnAnalysis ? fnAnalysis.counts : {};
  const overlap = r.breakdown.pestOverlap;
  const divPct  = r.breakdown.familyDiversity;

  // ── Layer detection ──────────────────────────────────────────────────────
  const layerSet = new Set();
  for (const slug of guildSlugs) {
    const p = plantBySlug[slug];
    if (p) layerSet.add(inferLayer(p));
  }
  const hasCanopy  = layerSet.has('canopy');
  const hasShrub   = layerSet.has('shrub');
  const hasGround  = layerSet.has('ground') || layerSet.has('root');
  const layerCount = layerSet.size;

  // ── Pattern detection (priority order) ───────────────────────────────────
  let primary = 'balanced';

  // Food Forest: canopy + shrub + ground/root + decent diversity
  if (hasCanopy && hasShrub && hasGround && divPct >= 60) {
    primary = 'food_forest';
  }
  // Soil Builder: nitrogen + mulch + accumulation
  else if ((counts['Nitrogen Fixer'] || 0) >= 2 &&
           (counts['Mulcher'] || 0) >= 2 &&
           (counts['Dynamic Accumulator'] || 0) >= 2) {
    primary = 'soil_builder';
  }
  // Pollinator Hub
  else if ((counts['Pollinator'] || 0) >= 3 ||
           (fnAnalysis && fnAnalysis.dominant && fnAnalysis.dominant.includes('Pollinator'))) {
    primary = 'pollinator_hub';
  }
  // Pest Resistant: strong management + low overlap
  else if ((counts['Pest Management'] || 0) >= 2 && overlap < 40) {
    primary = 'pest_resistant';
  }

  // ── Trait extraction ──────────────────────────────────────────────────────
  const traits = [];
  if (divPct >= 70)                          traits.push('high diversity');
  if (overlap < 30)                          traits.push('low pest pressure');
  if ((counts['Nitrogen Fixer'] || 0) >= 2)  traits.push('nitrogen rich');
  if (layerCount >= 3)                       traits.push('layered structure');
  if ((counts['Pollinator'] || 0) >= 3)      traits.push('pollinator dense');
  if ((counts['Mulcher'] || 0) >= 2 &&
      (counts['Ground Cover'] || 0) >= 2)   traits.push('low input');
  if (r.resilience >= 75)                    traits.push('high resilience');

  // ── Label + summary ───────────────────────────────────────────────────────
  const labels = {
    food_forest:    'Food Forest Starter',
    soil_builder:   'Soil Building System',
    pollinator_hub: 'Pollinator Hub',
    pest_resistant: 'Pest Resistant System',
    balanced:       'Balanced System',
  };

  const summaries = {
    food_forest:    'This guild resembles a young layered food system with structural diversity across canopy, shrub, and ground layers.',
    soil_builder:   'This system is heavily focused on soil building — nitrogen fixation, dynamic accumulation, and biomass production work together.',
    pollinator_hub: 'This guild prioritizes pollinator attraction and beneficial insect habitat with dense flowering support.',
    pest_resistant: 'This guild is structured to minimize shared pest pressure through active disruption and family diversity.',
    balanced:       'This is a balanced system with no dominant ecological specialization — resilient and broadly functional.',
  };

  return {
    primary,
    primaryLabel: labels[primary] || 'Balanced System',
    traits,
    summary: summaries[primary] || summaries.balanced,
  };
}

// ── Render ────────────────────────────────────────────────────────────────────
function renderGuild() {""",
    "3: analyzeGuildPattern() added"
)

# ── 4. Wire pattern into renderResults() — after fnAnalysis block ─────────────
patch(
    "  if (fnAnalysis) {\n    // ── Reinforced Functions — chips display ──────────────────────────────────",
    """  // ── System Pattern ────────────────────────────────────────────────────────
  const patternSection  = document.getElementById('section-pattern');
  const patternDisplay  = document.getElementById('pattern-display');
  if (fnAnalysis && r) {
    const pattern = analyzeGuildPattern(guild, fnAnalysis, r);
    patternDisplay.innerHTML = `
      <div class="pattern-primary">${pattern.primaryLabel}</div>
      <div class="pattern-summary">${pattern.summary}</div>
      <div class="pattern-traits">${pattern.traits.map(t => `<span class="pattern-chip">${t}</span>`).join('')}</div>
    `;
    patternSection.style.display = 'block';
  } else {
    patternSection.style.display = 'none';
  }

  if (fnAnalysis) {
    // ── Reinforced Functions — chips display ──────────────────────────────────""",
    "4: pattern wired into renderResults()"
)

f.write_text(text)
print(f"\n{changes} patches applied")
