from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

def patch(old, new, label):
    global text, changes
    if old in text:
        text = text.replace(old, new, 1)
        changes += 1
        print(f"✅ {label}")
    else:
        print(f"❌ {label}")

# 1. Add Why narrative function
patch(
"// ── Guild Pattern Recognition (Phase 5) ──────────────────────────────────────",
"""// ── Why This Guild Works narrative ───────────────────────────────────────────
function generateWhyNarrative(fnAnalysis, r) {
  const c = fnAnalysis.counts;
  const pests = r.sharedPests || [];
  const results = [];

  if ((c['Nitrogen Fixer'] || 0) > 0 && (c['Mulcher'] || 0) > 0) {
    results.push('This system helps feed itself — nitrogen-fixing plants and biomass producers build fertility with fewer outside inputs.');
  } else if ((c['Nitrogen Fixer'] || 0) > 0) {
    results.push('Nitrogen-fixing plants help feed nearby plants and reduce dependence on added fertilizer.');
  } else if ((c['Mulcher'] || 0) > 0) {
    results.push('Biomass-producing plants add organic matter that feeds soil life over time.');
  }

  if ((c['Ground Cover'] || 0) > 0) {
    results.push('Groundcover plants protect exposed soil, hold moisture, and reduce weed pressure.');
  }

  const hasPoll = (c['Pollinator'] || 0) > 0;
  const hasPest = (c['Pest Management'] || 0) > 0;
  if (hasPoll && hasPest) {
    results.push('Pollinator-supporting and pest-disrupting plants help attract beneficial insects while making it harder for pests to move through the system.');
  } else if (hasPoll) {
    results.push('Pollinator plants support fruit set, seed production, and beneficial insect activity.');
  } else if (hasPest) {
    results.push('Pest-management plants help confuse, repel, or interrupt pest pressure naturally.');
  }

  if ((c['Shade Provider'] || 0) > 0 || r.resilience > 70) {
    results.push('Layered structure gives the guild more stability by spreading growth across canopy, shrub, vine, herb, and ground layers.');
  }

  if ((c['Dynamic Accumulator'] || 0) > 0) {
    results.push('Dynamic accumulator plants help cycle nutrients by pulling them from deeper soil and returning them through leaf drop, chop-and-drop, or dieback.');
  }

  if (pests.length > 0 && r.breakdown.pestOverlap < 40) {
    results.push('Some shared pest pressure exists, but the guild spreads risk across different plants instead of relying on one crop.');
  }

  if (fnAnalysis.reinforced.length >= 3) {
    results.push('Several key jobs are backed up by more than one plant, so the system is less dependent on any single species.');
  }

  return results.slice(0, 5);
}

// ── Guild Pattern Recognition (Phase 5) ──────────────────────────────────────""",
"Added generateWhyNarrative()"
)

# 2. Add Why section before System Pattern
patch(
"""      <div class="result-section" id="section-pattern" style="display:none">
        <p class="result-section-title">System Pattern</p>
        <div id="pattern-display"></div>
      </div>

      <div class="result-section" id="section-suggestions">""",
"""      <div class="result-section" id="section-why" style="display:none">
        <p class="result-section-title">Why This Guild Works</p>
        <ul class="why-list" id="why-list"></ul>
      </div>

      <div class="result-section" id="section-pattern" style="display:none">
        <p class="result-section-title">System Pattern</p>
        <div id="pattern-display"></div>
      </div>

      <div class="result-section" id="section-suggestions">""",
"Added Why This Guild Works section"
)

# 3. Add CSS
patch(
"  .pattern-primary {",
"""  .why-list { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.6rem; }
  .why-list li { font-size: 0.88rem; color: var(--ash); line-height: 1.7; padding-left: 1.1rem; position: relative; }
  .why-list li::before { content: '→'; position: absolute; left: 0; color: var(--lime); font-family: 'Space Mono', monospace; font-size: 0.72rem; top: 0.18rem; }
  .pattern-primary {""",
"Added why-list CSS"
)

# 4. Wire into renderResults
patch(
"""  // ── System Pattern ────────────────────────────────────────────────────────
  const patternSection  = document.getElementById('section-pattern');
  const patternDisplay  = document.getElementById('pattern-display');""",
"""  // ── Why This Guild Works ─────────────────────────────────────────────────
  const whySection = document.getElementById('section-why');
  const whyList    = document.getElementById('why-list');

  if (fnAnalysis && r) {
    const whyPoints = generateWhyNarrative(fnAnalysis, r);
    if (whyPoints.length > 0) {
      whyList.innerHTML = whyPoints.map(p => `<li>${p}</li>`).join('');
      whySection.style.display = 'block';
    } else {
      whySection.style.display = 'none';
    }
  }

  // ── System Pattern ────────────────────────────────────────────────────────
  const patternSection  = document.getElementById('section-pattern');
  const patternDisplay  = document.getElementById('pattern-display');""",
"Wired Why This Guild Works into renderResults"
)

f.write_text(text)
print(f"\\n{changes} patches applied")