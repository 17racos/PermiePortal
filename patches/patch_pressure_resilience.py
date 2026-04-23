#!/usr/bin/env python3
"""
patch_pressure_resilience.py
============================
Phase 3.6 — Pressure vs Resilience model:
1. Rename Guild Health → System Pressure
2. Rename Pest Overlap → Shared Pest Exposure
3. Change RISK → PRESSURE in score label
4. Add subtitle under score
5. Add pestMitigationScore calculation + Resilience Factors section
6. Add balancing statement when pressure + mitigation both high
7. Soften pest warning tone
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
        print(f"❌ {label} — not found")

# ── 1. Rename score panel label HTML ─────────────────────────────────────────
patch(
    '        <p class="panel-label">Guild Health</p>',
    '        <p class="panel-label">System Pressure</p>',
    "1: Guild Health → System Pressure"
)

# ── 2. Add subtitle + initial score label text ───────────────────────────────
patch(
    '        <div class="score-label" id="score-label">LOW RISK — RESILIENCE: 100</div>\n        <div class="score-bar-wrap">',
    '        <div class="score-label" id="score-label">LOW PRESSURE — RESILIENCE: 100</div>\n        <p class="score-subtitle">Measures shared pest exposure. Higher values indicate more interaction, not necessarily instability.</p>\n        <div class="score-bar-wrap">',
    "2: subtitle added + LOW RISK → LOW PRESSURE"
)

# ── 3. Rename Pest Overlap card ───────────────────────────────────────────────
patch(
    '          <div class="breakdown-key">Pest Overlap</div>',
    '          <div class="breakdown-key">Shared Pest Exposure</div>',
    "3: Pest Overlap → Shared Pest Exposure"
)

# ── 4. Add Resilience Factors section HTML after breakdown grid ───────────────
patch(
    '      <div class="result-section" id="section-suggestions">',
    """      <div class="result-section" id="section-mitigation">
        <p class="result-section-title">Resilience Factors</p>
        <div class="mitigation-grid" id="mitigation-grid"></div>
      </div>

      <div class="result-section" id="section-suggestions">""",
    "4: Resilience Factors section HTML added"
)

# ── 5. Add CSS for subtitle + mitigation ─────────────────────────────────────
patch(
    "  .score-bar { height: 100%; background: var(--lime); transition: width 0.5s ease, background 0.4s; }",
    """  .score-bar { height: 100%; background: var(--lime); transition: width 0.5s ease, background 0.4s; }
  .score-subtitle { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); opacity: 0.6; margin-top: 0.4rem; line-height: 1.6; max-width: 320px; }
  .mitigation-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; }
  .mitigation-card { background: var(--bark); border: 1px solid rgba(139,184,58,0.12); padding: 0.7rem 0.9rem; }
  .mitigation-value { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; line-height: 1; }
  .mitigation-value.weak { color: var(--rust); }
  .mitigation-value.moderate { color: var(--straw); }
  .mitigation-value.strong { color: var(--lime); }
  .mitigation-key { font-family: 'Space Mono', monospace; font-size: 0.56rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ash); margin-top: 0.2rem; }
  .mitigation-label { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); margin-top: 0.15rem; font-style: italic; }""",
    "5: subtitle + mitigation CSS added"
)

# ── 6. Update score label render JS ──────────────────────────────────────────
patch(
    "  labelEl.textContent = `${r.riskLevel.toUpperCase()} RISK — RESILIENCE: ${r.resilience}`;",
    """  const pressureLabel = r.riskLevel === 'low' ? 'LOW' : r.riskLevel === 'medium' ? 'MODERATE' : 'ELEVATED';
  labelEl.textContent = `${pressureLabel} PRESSURE — RESILIENCE: ${r.resilience}`;""",
    "6: RISK → PRESSURE in score label"
)

# ── 7. Wire pestMitigationScore after breakdown render ───────────────────────
patch(
    """  // Breakdown
  document.getElementById('bd-diversity').textContent = r.breakdown.familyDiversity + '%';
  document.getElementById('bd-overlap').textContent   = r.breakdown.pestOverlap + '%';
  document.getElementById('bd-dominant').textContent  = r.breakdown.dominantRatio + '%';""",
    """  // Breakdown
  document.getElementById('bd-diversity').textContent = r.breakdown.familyDiversity + '%';
  document.getElementById('bd-overlap').textContent   = r.breakdown.pestOverlap + '%';
  document.getElementById('bd-dominant').textContent  = r.breakdown.dominantRatio + '%';

  // Resilience Factors — pestMitigationScore
  const fnCounts = {};
  for (const slug of guild) {
    const p = plantBySlug[slug];
    if (!p) continue;
    for (const fn of (p.plant_function || [])) {
      fnCounts[fn] = (fnCounts[fn] || 0) + 1;
    }
  }
  const famDiv = r.breakdown.familyDiversity / 100;
  const rawMitigation = ((fnCounts['Pest Management'] || 0) * 25)
                      + ((fnCounts['Pollinator'] || 0) * 10)
                      + (famDiv * 30);
  const pestMitigationScore = Math.min(100, Math.round(rawMitigation));
  const mitLabel = pestMitigationScore < 30 ? 'Weak mitigation'
                 : pestMitigationScore < 60 ? 'Moderate mitigation'
                 : 'Strong mitigation';
  const mitClass = pestMitigationScore < 30 ? 'weak'
                 : pestMitigationScore < 60 ? 'moderate' : 'strong';
  const mitGrid = document.getElementById('mitigation-grid');
  mitGrid.innerHTML = `
    <div class="mitigation-card">
      <div class="mitigation-value ${mitClass}">${pestMitigationScore}</div>
      <div class="mitigation-key">Pest Mitigation</div>
      <div class="mitigation-label">${mitLabel}</div>
    </div>
    <div class="mitigation-card">
      <div class="mitigation-value ${mitClass}">${r.resilience}</div>
      <div class="mitigation-key">Resilience Score</div>
      <div class="mitigation-label">${r.resilience >= 75 ? 'Structurally resilient' : r.resilience >= 50 ? 'Moderate resilience' : 'Building resilience'}</div>
    </div>
  `;""",
    "7: pestMitigationScore computed + Resilience Factors rendered"
)

# ── 8. Soften pest warning tone ───────────────────────────────────────────────
patch(
    "warnings.push(`Several pests affect multiple plants — ${dominant} are the dominant shared pressures.`);",
    "warnings.push(`Shared pest pressure detected — ${dominant} affect multiple plants in this guild.`);",
    "8: pest warning tone softened"
)

patch(
    "warnings.push(`Some pest overlap exists — ${dominant} affect multiple guild members.`);",
    "warnings.push(`Some shared pest exposure exists — ${dominant} appear across multiple plants.`);",
    "8b: secondary pest warning tone softened"
)

# ── 9. Add balancing statement when pressure + mitigation both high ───────────
patch(
    """  // Only show pest/family risk suggestions — functional actions moved to Design Actions
  for (const s of r.suggestions) {""",
    """  // Balancing statement when pressure and mitigation are both significant
  if (r.breakdown.pestOverlap > 50 && pestMitigationScore > 50) {
    const li = document.createElement('div');
    li.className = 'suggestion-item';
    li.textContent = '\u2713 Shared pest pressure exists, but mitigation systems are strong \u2014 this guild is likely resilient.';
    suggEl.appendChild(li);
  }

  // Only show pest/family risk suggestions — functional actions moved to Design Actions
  for (const s of r.suggestions) {""",
    "9: balancing statement when pressure + mitigation both high"
)

f.write_text(text)
print(f"\n{changes} patches applied")
