#!/usr/bin/env python3
"""
patch_phase3_explanations.py
============================
Phase 3 — context-aware explanations replacing generic reasons.
Changes:
1. Adds buildExplanations() helper inside getNextBestPlants()
2. Replaces reasons[] with explanations[] in candidates.push()
3. Updates UI to use .next-plant-explanation CSS class
4. Updates src/lib/nextPlant.js with same logic
"""
from pathlib import Path

changes = 0

def patch(path, old, new, label):
    global changes
    text = path.read_text()
    if old in text:
        path.write_text(text.replace(old, new))
        changes += 1
        print(f"✅ {label}")
    else:
        print(f"❌ {label} — not found")

fc  = Path("src/pages/guild-checker.astro")
lib = Path("src/lib/nextPlant.js")

# ── 1. Add buildExplanations() before candidates loop + replace in push ──────
# Insert explanation builder before "const candidates = [];"
# and update candidates.push to use explanations

OLD_CANDIDATES_INIT = "  const candidates = [];\n  for (const p of plantIndex) {"

NEW_CANDIDATES_INIT = """  const candidates = [];

  // ── Context-aware explanation builder ────────────────────────────────────
  function buildExplanations(fns, family, pests, sharedPestCount,
                             hasMissing, missingReasons, hasNewFamily, familyReasons) {
    const explanations = [];

    // Priority 1: fills_gap — explain missing role in guild context
    if (hasMissing) {
      for (const reason of missingReasons.slice(0, 1)) {
        const role = reason.replace('Adds missing ', '').replace(' function', '');
        const contextMap = {
          'Ground Cover':    'Your guild lacks Ground Cover — this plant helps retain moisture and suppress weeds between your existing species.',
          'Pollinator':      'Your guild has no dedicated Pollinator support — this plant attracts beneficial insects that improve yields across the system.',
          'Pest Management': 'No Pest Management plant exists in your guild — this plant helps confuse or deter insects that threaten neighboring species.',
          'Mulcher':         'Your guild lacks a Mulcher — this plant generates biomass that feeds soil biology and reduces bare-ground moisture loss.',
          'Nitrogen Fixer':  'Your guild is missing a Nitrogen Fixer — this plant feeds soil nitrogen to neighboring plants through root nodules.',
        };
        explanations.push(contextMap[role] || `Your guild is missing ${role} — this plant fills that functional gap.`);
      }
    }

    // Priority 2: adds_diversity — explain family context
    if (hasNewFamily && explanations.length < 2) {
      const domLabel = dominantFamily
        ? dominantFamily.charAt(0).toUpperCase() + dominantFamily.slice(1)
        : null;
      if (domLabel && family) {
        const famLabel = family.charAt(0).toUpperCase() + family.slice(1);
        explanations.push(
          `Your guild is heavy in ${domLabel} — this plant introduces ${famLabel}, reducing shared pest vulnerability across the system.`
        );
      } else if (family) {
        const famLabel = family.charAt(0).toUpperCase() + family.slice(1);
        explanations.push(`Introduces ${famLabel}, adding new family diversity to your guild.`);
      }
    }

    // Priority 3: reduces_risk — explain pest context
    if (explanations.length < 2) {
      if (sharedPestCount === 0 && pests.size > 0) {
        // Mention top shared guild pests if available
        const topGuildPests = Array.from(guildPests).slice(0, 2).join(' and ');
        if (topGuildPests) {
          explanations.push(
            `This plant shares no pests with your guild, reducing risk of ${topGuildPests} spreading between species.`
          );
        } else {
          explanations.push('This plant shares no pest pressure with your current guild — a clean addition.');
        }
      } else if (sharedPestCount <= 2 && pests.size > 0 && explanations.length === 0) {
        explanations.push('Minimal overlap with existing pest pressure — unlikely to amplify current pest issues.');
      }
    }

    return explanations.slice(0, 2);
  }

  for (const p of plantIndex) {"""

patch(fc, OLD_CANDIDATES_INIT, NEW_CANDIDATES_INIT, "astro: buildExplanations() added")

# ── 2. Replace candidates.push to use explanations ───────────────────────────
OLD_PUSH = """    const reasons = [...roleReasons, ...familyReasons, ...pestReasons].slice(0, 3);
    if (reasons.length === 0) continue;

    const hasMissing   = missingReasons.length > 0;
    const hasNewFamily = familyScore > 0;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      reasons, score: Math.round(score * 10) / 10,
      _hasMissing: hasMissing, _hasNewFamily: hasNewFamily,
      _sharedPests: sharedPestCount,
    });"""

NEW_PUSH = """    const hasMissing   = missingReasons.length > 0;
    const hasNewFamily = familyScore > 0;

    // Build context-aware explanations (replaces generic reasons)
    const explanations = buildExplanations(
      fns, family, pests, sharedPestCount,
      hasMissing, missingReasons, hasNewFamily, familyReasons
    );
    if (explanations.length === 0) continue;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      explanations, score: Math.round(score * 10) / 10,
      _hasMissing: hasMissing, _hasNewFamily: hasNewFamily,
      _sharedPests: sharedPestCount,
    });"""

patch(fc, OLD_PUSH, NEW_PUSH, "astro: candidates.push uses explanations")

# ── 3. Update UI render to use explanations + new CSS class ──────────────────
OLD_UI = """          <div class="next-plant-reasons">
            ${p.reasons.map(r => `<span class="next-plant-reason">${r}</span>`).join('')}
          </div>"""

NEW_UI = """          <div class="next-plant-explanations">
            ${(p.explanations || []).map(e => `<span class="next-plant-explanation">${e}</span>`).join('')}
          </div>"""

patch(fc, OLD_UI, NEW_UI, "astro: UI uses explanations + new CSS class")

# ── 4. Update CSS: add explanation style, keep reason for backward compat ─────
OLD_CSS = "  .next-plant-reason { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); padding: 0.1rem 0.45rem; border: 1px solid rgba(139,184,58,0.2); background: rgba(42,61,31,0.2); }"

NEW_CSS = """  .next-plant-reason { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--ash); padding: 0.1rem 0.45rem; border: 1px solid rgba(139,184,58,0.2); background: rgba(42,61,31,0.2); }
  .next-plant-explanations { display: flex; flex-direction: column; gap: 0.3rem; margin-top: 0.3rem; }
  .next-plant-explanation { font-size: 0.78rem; color: var(--ash); line-height: 1.55; font-style: italic; }"""

patch(fc, OLD_CSS, NEW_CSS, "astro: explanation CSS added")

# ── 5. Update src/lib/nextPlant.js with same logic ───────────────────────────
if lib.exists():
    ltext = lib.read_text()

    LIB_OLD_PUSH = """    const reasons = [...roleReasons, ...familyReasons, ...pestReasons].slice(0, 3);
    if (reasons.length === 0) continue;

    const hasMissing   = missingReasons.length > 0;
    const hasNewFamily = familyScore > 0;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      reasons, score: Math.round(score * 10) / 10,
      _hasMissing: hasMissing, _hasNewFamily: hasNewFamily,
      _sharedPests: sharedPestCount,
    });"""

    LIB_NEW_PUSH = """    const hasMissing   = missingReasons.length > 0;
    const hasNewFamily = familyScore > 0;

    // Build context-aware explanations
    const explanations = [];
    if (hasMissing) {
      const role = missingReasons[0]?.replace('Adds missing ','').replace(' function','') || '';
      const ctxMap = {
        'Ground Cover':    'Your guild lacks Ground Cover — this plant helps retain moisture and suppress weeds between existing species.',
        'Pollinator':      'Your guild has no dedicated Pollinator support — this plant attracts beneficial insects that improve yields.',
        'Pest Management': 'No Pest Management plant exists in your guild — this plant helps confuse or deter insects threatening neighbors.',
        'Mulcher':         'Your guild lacks a Mulcher — this plant generates biomass that feeds soil biology.',
        'Nitrogen Fixer':  'Your guild is missing a Nitrogen Fixer — this plant feeds soil nitrogen through root nodules.',
      };
      explanations.push(ctxMap[role] || `Your guild is missing ${role} — this plant fills that functional gap.`);
    }
    if (hasNewFamily && explanations.length < 2 && family) {
      const famLabel = family.charAt(0).toUpperCase() + family.slice(1);
      explanations.push(`Introduces ${famLabel}, adding new family diversity to reduce shared pest vulnerability.`);
    }
    if (explanations.length === 0 && sharedPestCount === 0 && pests.size > 0) {
      explanations.push('This plant shares no pest pressure with your current guild — a clean addition.');
    }
    if (explanations.length === 0) continue;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      explanations, score: Math.round(score * 10) / 10,
      _hasMissing: hasMissing, _hasNewFamily: hasNewFamily,
      _sharedPests: sharedPestCount,
    });"""

    patch(lib, LIB_OLD_PUSH, LIB_NEW_PUSH, "lib: explanations added")

print(f"\n{changes} changes applied")
