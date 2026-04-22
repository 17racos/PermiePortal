#!/usr/bin/env python3
"""
patch_phase5_5.py
=================
Phase 5.5 — Zone-Aware Candidate Filtering:
1. zone_min/zone_max added to plantIndex
2. userZone state variable (default 9)
3. getZoneFit() function
4. Zone filtering + microclimate penalty in generator
5. zoneFit stored on suggestion candidates
6. Microclimate badge in suggestion UI
7. Microclimate explanation appended
8. CSS for zone badge
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

# ── 1. Add zone_min/zone_max to plantIndex ────────────────────────────────────
patch(
    """  layers: p.layers || [],
  growth_habit: p.growth_habit || '',
}));""",
    """  layers: p.layers || [],
  growth_habit: p.growth_habit || '',
  zone_min: p.zone_min ?? null,
  zone_max: p.zone_max ?? null,
}));""",
    "1: zone_min/zone_max added to plantIndex"
)

# ── 2. Add userZone + getZoneFit() after guild state ─────────────────────────
patch(
    "// ── Guild state ───────────────────────────────────────────────────────────────\nlet guild = [];",
    """// ── Guild state ───────────────────────────────────────────────────────────────
let guild = [];
let userZone = 9; // default — will be UI-driven in future phase

// ── Zone compatibility ────────────────────────────────────────────────────────
function getZoneFit(p, zone) {
  const min = p.zone_min;
  const max = p.zone_max;
  if (min === null || min === undefined || max === null || max === undefined) return 'unknown';
  if (zone >= min && zone <= max)           return 'fit';
  if (zone >= min - 1 && zone <= max + 1)  return 'microclimate';
  return 'out';
}""",
    "2: userZone + getZoneFit() added"
)

# ── 3. Zone filter + microclimate penalty in generator iterative loop ─────────
patch(
    """      const score = scorePlant(p, generated);
      if (score <= 0) continue;""",
    """      const zoneFit = getZoneFit(p, userZone);
      if (zoneFit === 'out') continue;
      let score = scorePlant(p, generated);
      if (zoneFit === 'microclimate') score -= 1.0;
      if (score <= 0) continue;""",
    "3: zone filter + microclimate penalty in generator iterative loop"
)

# ── 4. Zone filter in pickBestForRole (anchor phase) ─────────────────────────
patch(
    """      // Skip specialty plants for food_production
      if (goalKey === 'food_production' && p.food_role === 'specialty') continue;
      // Food Production anchor filter: skip support-heavy edibles + exclusions""",
    """      // Skip specialty plants for food_production
      if (goalKey === 'food_production' && p.food_role === 'specialty') continue;
      // Zone filter
      if (getZoneFit(p, userZone) === 'out') continue;
      // Food Production anchor filter: skip support-heavy edibles + exclusions""",
    "4: zone filter in pickBestForRole"
)

# ── 5. Zone filter + penalty in getNextBestPlants iterative loop ──────────────
patch(
    """    const pestReasons = [];
    if (sharedPestCount === 0 && pests.size > 0)
      pestReasons.push('No shared pest pressure \u2014 clean addition');
    else if (sharedPestCount <= 2 && pests.size > 0)
      pestReasons.push('Low shared pest overlap \u2014 minimal risk');""",
    """    // Zone fit for suggestions
    const zoneFit = getZoneFit(p, userZone);
    if (zoneFit === 'out') continue;

    const pestReasons = [];
    if (sharedPestCount === 0 && pests.size > 0)
      pestReasons.push('No shared pest pressure \u2014 clean addition');
    else if (sharedPestCount <= 2 && pests.size > 0)
      pestReasons.push('Low shared pest overlap \u2014 minimal risk');""",
    "5: zone filter in getNextBestPlants"
)

# ── 6. Store zoneFit on suggestion candidates ─────────────────────────────────
patch(
    """    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      explanations, score: Math.round(score * 10) / 10,
      _hasMissing: hasMissing, _hasNewFamily: hasNewFamily,
      _sharedPests: sharedPestCount,
    });""",
    """    // Microclimate explanation
    if (zoneFit === 'microclimate') {
      explanations.push('May require microclimate support — consider heat retention, wind protection, or canopy cover.');
    }

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      explanations, score: Math.round(score * 10) / 10,
      _hasMissing: hasMissing, _hasNewFamily: hasNewFamily,
      _sharedPests: sharedPestCount,
      zoneFit,
    });""",
    "6: zoneFit stored + microclimate explanation added to candidates"
)

# ── 7. Add zone badge to suggestion UI ───────────────────────────────────────
patch(
    """              <div class="next-plant-name">${p.name}${p.intent ? ` <span class="intent-badge ${p.intent}">${intentLabels[p.intent] || p.intent}</span>` : ''}</div>""",
    """              <div class="next-plant-name">${p.name}${p.intent ? ` <span class="intent-badge ${p.intent}">${intentLabels[p.intent] || p.intent}</span>` : ''}${p.zoneFit === 'microclimate' ? ' <span class="zone-badge micro">microclimate</span>' : ''}</div>""",
    "7: microclimate badge in suggestion UI"
)

# ── 8. Add zone badge CSS ─────────────────────────────────────────────────────
patch(
    "  .intent-badge.fills_gap { color: var(--rust); border-color: rgba(196,85,26,0.4); }",
    """  .zone-badge { font-family: 'Space Mono', monospace; font-size: 0.52rem; letter-spacing: 0.05em; text-transform: uppercase; padding: 0.1rem 0.35rem; border: 1px solid rgba(212,168,67,0.4); color: var(--straw); margin-left: 0.35rem; vertical-align: middle; }
  .intent-badge.fills_gap { color: var(--rust); border-color: rgba(196,85,26,0.4); }""",
    "8: zone badge CSS added"
)

f.write_text(text)
print(f"\n{changes} patches applied")
