#!/usr/bin/env python3
"""
patch_next_v2_2.py
==================
Phase 2.2 — intent-aware suggestion behavior:
1. "No suggestion needed" state when guild is balanced
2. Improvement threshold filter (score >= topScore * 0.6)
3. Intent tag on each suggestion (fills_gap / adds_diversity / reduces_risk)
4. UI intent badge display
5. Empty state messaging
Updates BOTH guild-checker.astro and src/lib/nextPlant.js
"""
from pathlib import Path

# ── 1. Patch getNextBestPlants filter block in guild-checker.astro ────────────
fc = Path("src/pages/guild-checker.astro")
text = fc.read_text()

OLD_FILTER = """  // Family diversity filter: max 2 per family in final results
  const familySeen = {};
  const filtered = [];
  for (const c of candidates) {
    const fam = c.family || '__none__';
    familySeen[fam] = (familySeen[fam] || 0) + 1;
    if (familySeen[fam] <= 2) filtered.push(c);
    if (filtered.length >= limit) break;
  }
  // Strip internal sort metadata before returning
  return filtered.map(({ _hasMissing, _hasNewFamily, _sharedPests, ...rest }) => rest);
}"""

NEW_FILTER = """  // ── Balanced guild check — return empty if no improvements needed ──────────
  const familyDiversity = guildFamilies.size / n;
  const guildPestArr    = Array.from(guildPests);
  // (pestOverlap estimate: shared pests / total — approximate without full scoring)
  const dominantFamilyRatio = n > 0 ? (Object.values(familyCounts).sort((a,b)=>b-a)[0]||0)/n : 0;
  if (
    missingRoles.length === 0 &&
    familyDiversity >= 0.75 &&
    dominantFamilyRatio <= 0.5 &&
    candidates.length > 0 &&
    candidates[0].score < 3.0
  ) {
    return []; // guild is well-balanced, no additions needed
  }

  // ── Improvement threshold: only keep candidates within 60% of top score ──
  const topScore = candidates[0]?.score || 0;
  const threshold = topScore * 0.6;
  const aboveThreshold = candidates.filter(c => c.score >= threshold);

  // ── Intent tag: primary reason for suggestion ─────────────────────────────
  const tagged = aboveThreshold.map(c => ({
    ...c,
    intent: c._hasMissing   ? 'fills_gap'
          : c._hasNewFamily ? 'adds_diversity'
          :                   'reduces_risk',
  }));

  // ── Family diversity filter: max 2 per family in final results ────────────
  const familySeen = {};
  const filtered = [];
  for (const c of tagged) {
    const fam = c.family || '__none__';
    familySeen[fam] = (familySeen[fam] || 0) + 1;
    if (familySeen[fam] <= 2) filtered.push(c);
    if (filtered.length >= limit) break;
  }

  // Strip internal sort metadata before returning
  return filtered.map(({ _hasMissing, _hasNewFamily, _sharedPests, ...rest }) => rest);
}"""

if OLD_FILTER in text:
    text = text.replace(OLD_FILTER, NEW_FILTER)
    print("✅ 1: filter block updated with balanced check + intent tags")
else:
    print("❌ 1: filter block not found")

# ── 2. Patch UI render to show intent badge and empty state ───────────────────
OLD_UI = """const suggestions = getNextBestPlants(guild, 5);
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
        </a>"""

NEW_UI = """const suggestions = getNextBestPlants(guild, 5);
    const intentLabels = {
      fills_gap:      'fills gap',
      adds_diversity: 'adds diversity',
      reduces_risk:   'reduces risk',
    };
    if (suggestions.length === 0) {
      nextNote.textContent = '';
      nextList.innerHTML = '<div class="next-balanced-state">' +
        '<span class="next-balanced-icon">✓</span>' +
        '<div>' +
          '<div class="next-balanced-title">Guild is well-balanced</div>' +
          '<div class="next-balanced-sub">Further additions may increase complexity without improving resilience.</div>' +
        '</div>' +
      '</div>';
      nextSection.style.display = 'block';
    } else if (suggestions.length > 0) {
      nextNote.textContent = 'Plants scored by role coverage, family diversity, and pest overlap with your current guild.';
      nextList.innerHTML = suggestions.map(p => `
        <a href="/plants/${p.slug}" class="next-plant-card" target="_blank">
          <div class="next-plant-header">
            <div>
              <div class="next-plant-name">${p.name}${p.intent ? ` <span class="intent-badge ${p.intent}">${intentLabels[p.intent] || p.intent}</span>` : ''}</div>
              ${p.family ? `<div class="next-plant-family">${p.family}</div>` : ''}
            </div>
            <div class="next-plant-score">${p.score}</div>
          </div>
          <div class="next-plant-reasons">
            ${p.reasons.map(r => `<span class="next-plant-reason">${r}</span>`).join('')}
          </div>
        </a>"""

if OLD_UI in text:
    text = text.replace(OLD_UI, NEW_UI)
    print("✅ 2: UI render updated with intent badge + balanced empty state")
else:
    print("❌ 2: UI render block not found")

# ── 3. Add CSS for intent badges and balanced state ───────────────────────────
OLD_CSS = "  .next-plant-reason { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); padding: 0.1rem 0.45rem; border: 1px solid rgba(139,184,58,0.2); background: rgba(42,61,31,0.2); }"

NEW_CSS = """  .next-plant-reason { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); padding: 0.1rem 0.45rem; border: 1px solid rgba(139,184,58,0.2); background: rgba(42,61,31,0.2); }
  .intent-badge { font-family: 'Space Mono', monospace; font-size: 0.52rem; letter-spacing: 0.05em; text-transform: uppercase; padding: 0.1rem 0.35rem; border: 1px solid; vertical-align: middle; margin-left: 0.35rem; }
  .intent-badge.fills_gap { color: var(--rust); border-color: rgba(196,85,26,0.4); }
  .intent-badge.adds_diversity { color: var(--lime); border-color: rgba(139,184,58,0.35); }
  .intent-badge.reduces_risk { color: var(--straw); border-color: rgba(212,168,67,0.35); }
  .next-balanced-state { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem 0; }
  .next-balanced-icon { font-size: 1.1rem; color: var(--lime); line-height: 1.4; flex-shrink: 0; }
  .next-balanced-title { font-family: 'Space Mono', monospace; font-size: 0.72rem; color: var(--lime); margin-bottom: 0.25rem; }
  .next-balanced-sub { font-size: 0.78rem; color: var(--ash); font-style: italic; line-height: 1.5; }"""

if OLD_CSS in text:
    text = text.replace(OLD_CSS, NEW_CSS)
    print("✅ 3: intent badge + balanced state CSS added")
else:
    print("❌ 3: CSS anchor not found")

fc.write_text(text)

# ── 4. Update src/lib/nextPlant.js filter block ───────────────────────────────
lib = Path("src/lib/nextPlant.js")
if lib.exists():
    ltext = lib.read_text()

    OLD_LIB = """  const familySeen = {};
  const filtered = [];
  for (const c of candidates) {
    const fam = c.family || '__none__';
    familySeen[fam] = (familySeen[fam] || 0) + 1;
    if (familySeen[fam] <= 2) filtered.push(c);
    if (filtered.length >= limit) break;
  }

  return filtered.map(({ _hasMissing, _hasNewFamily, _sharedPests, ...rest }) => rest);
}"""

    NEW_LIB = """  // Balanced guild check
  const familyDiversity = guildFamilies.size / n;
  const dominantFamilyRatio = n > 0 ? (Object.values(familyCounts).sort((a,b)=>b-a)[0]||0)/n : 0;
  if (
    missingRoles.length === 0 &&
    familyDiversity >= 0.75 &&
    dominantFamilyRatio <= 0.5 &&
    candidates.length > 0 &&
    candidates[0].score < 3.0
  ) {
    return [];
  }

  // Improvement threshold
  const topScore = candidates[0]?.score || 0;
  const threshold = topScore * 0.6;
  const aboveThreshold = candidates.filter(c => c.score >= threshold);

  // Intent tagging
  const tagged = aboveThreshold.map(c => ({
    ...c,
    intent: c._hasMissing   ? 'fills_gap'
          : c._hasNewFamily ? 'adds_diversity'
          :                   'reduces_risk',
  }));

  const familySeen = {};
  const filtered = [];
  for (const c of tagged) {
    const fam = c.family || '__none__';
    familySeen[fam] = (familySeen[fam] || 0) + 1;
    if (familySeen[fam] <= 2) filtered.push(c);
    if (filtered.length >= limit) break;
  }

  return filtered.map(({ _hasMissing, _hasNewFamily, _sharedPests, ...rest }) => rest);
}"""

    if OLD_LIB in ltext:
        lib.write_text(ltext.replace(OLD_LIB, NEW_LIB))
        print("✅ 4: src/lib/nextPlant.js filter block updated")
    else:
        print("❌ 4: lib filter block not found")
else:
    print("⏭️  4: src/lib/nextPlant.js not found — skipping")

print("\nDone")
