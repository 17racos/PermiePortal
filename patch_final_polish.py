#!/usr/bin/env python3
"""
patch_final_polish.py
=====================
Final language polish pass:
1. Conditional family phrasing (only "X-heavy" when dominantFamilyRatio >= 0.5)
2. Explanation variety (3 rotation templates for family + pest)
3. Dominant function tone fix (strength-first, not penalty)
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

# ── 1. Add dominantFamilyRatio to buildExplanations signature ─────────────────
patch(
    """  function buildExplanations(
    fns, family, pests, sharedPestCount,
    hasMissing, missingReasons, hasNewFamily, familyReasons,
    domFamily, gPests, pestOcc
  ) {""",
    """  function buildExplanations(
    fns, family, pests, sharedPestCount,
    hasMissing, missingReasons, hasNewFamily, familyReasons,
    domFamily, gPests, pestOcc, domFamilyRatio, candidateIndex
  ) {""",
    "1: signature updated with domFamilyRatio + candidateIndex"
)

# ── 2. Replace family diversity explanation block with conditional phrasing ───
patch(
    """    // Priority 2: adds_diversity — CAUSE: dominance → EFFECT: reduced vulnerability
    if (hasNewFamily && explanations.length < 2 && family) {
      const famLabel = family.charAt(0).toUpperCase() + family.slice(1);
      if (domFamily) {
        const domLabel = domFamily.charAt(0).toUpperCase() + domFamily.slice(1);
        explanations.push(
          `Introduces ${famLabel}, which breaks the shared pest vulnerability of your ${domLabel}-heavy guild.`
        );
      } else {
        explanations.push(`Introduces ${famLabel}, adding new family diversity that reduces cross-species pest transfer.`);
      }
    }""",
    """    // Priority 2: adds_diversity — conditional family phrasing + rotation
    if (hasNewFamily && explanations.length < 2 && family) {
      const famLabel = family.charAt(0).toUpperCase() + family.slice(1);
      const isHeavy  = domFamily && domFamilyRatio >= 0.5;
      const domLabel = domFamily ? domFamily.charAt(0).toUpperCase() + domFamily.slice(1) : null;
      const idx      = (candidateIndex || 0) % 3;
      if (isHeavy) {
        // Conditional "heavy" phrasing — only when truly dominant
        const heavyVariants = [
          `Introduces ${famLabel}, breaking shared pest pressure in your ${domLabel}-heavy guild.`,
          `Adds ${famLabel} diversity, reducing structural similarity in your ${domLabel}-concentrated guild.`,
          `Diversifies with ${famLabel}, helping isolate pest pathways from your ${domLabel}-heavy base.`,
        ];
        explanations.push(heavyVariants[idx]);
      } else {
        const diverseVariants = [
          `Introduces ${famLabel}, widening ecological diversity across your guild.`,
          `Adds a new plant family (${famLabel}), reducing structural similarity between plants.`,
          `Diversifies your guild with ${famLabel}, helping break shared vulnerability patterns.`,
        ];
        explanations.push(diverseVariants[idx]);
      }
    }""",
    "2: conditional family phrasing + 3-variant rotation"
)

# ── 3. Replace pest explanation block with varied phrasing ────────────────────
patch(
    """    // Priority 3: reduces_risk — top pests sorted by occurrence
    if (explanations.length < 2 && sharedPestCount === 0 && pests.size > 0) {
      const topPests = Array.from(gPests)
        .sort((a, b) => (pestOcc[b] || 0) - (pestOcc[a] || 0))
        .slice(0, 2);
      if (topPests.length > 0) {
        explanations.push(
          `Shares no pests with your guild, reducing the risk of ${topPests.join(' and ')} spreading between plants.`
        );
      } else {
        explanations.push('Shares no pest pressure with your current guild — a clean addition.');
      }
    } else if (explanations.length === 0 && sharedPestCount <= 2 && pests.size > 0) {
      explanations.push('Low pest overlap with your guild — minimal risk of amplifying existing pest pressure.');
    }""",
    """    // Priority 3: reduces_risk — top pests sorted by occurrence, varied phrasing
    if (explanations.length < 2 && sharedPestCount === 0 && pests.size > 0) {
      const topPests = Array.from(gPests)
        .sort((a, b) => (pestOcc[b] || 0) - (pestOcc[a] || 0))
        .slice(0, 2);
      const idx = (candidateIndex || 0) % 3;
      if (topPests.length > 0) {
        const pestVariants = [
          `Shares no pests with your guild, reducing the risk of ${topPests.join(' and ')} spreading between plants.`,
          `Avoids all current pest overlap — isolating pressure from ${topPests.join(' and ')}.`,
          `Does not share pest pathways with your current plants, keeping ${topPests.join(' and ')} contained.`,
        ];
        explanations.push(pestVariants[idx]);
      } else {
        explanations.push('Shares no pest pressure with your current guild — a clean addition.');
      }
    } else if (explanations.length === 0 && sharedPestCount <= 2 && pests.size > 0) {
      explanations.push('Low pest overlap with your guild — minimal risk of amplifying existing pest pressure.');
    }""",
    "3: pest explanation variety (3 rotation variants)"
)

# ── 4. Update call site to pass dominantFamilyRatio and candidate index ───────
patch(
    """    const explanations = buildExplanations(
      fns, family, pests, sharedPestCount,
      hasMissing, missingReasons, hasNewFamily, familyReasons,
      dominantFamily, guildPests, pestOccurrence
    );""",
    """    const explanations = buildExplanations(
      fns, family, pests, sharedPestCount,
      hasMissing, missingReasons, hasNewFamily, familyReasons,
      dominantFamily, guildPests, pestOccurrence,
      dominantFamilyRatio, candidates.length
    );""",
    "4: call site passes dominantFamilyRatio + candidate index"
)

# ── 5. Fix dominant function tone (strength-first, not penalty) ───────────────
patch(
    """const dominantMsgs = {
    'Nitrogen Fixer':  'Nitrogen-fixing plants dominate this guild — ensure other roles are not crowded out.',
    'Ground Cover':    'Ground cover plants dominate — check that taller layers are represented.',
    'Pollinator':      'Pollinator plants dominate — consider structural diversity across layers.',
    'Mulcher':         'Mulch producers dominate — ensure food-producing and support layers are present.',
    'Pest Management': 'Pest management plants dominate — check for balance with productive layers.',
  };""",
    """const dominantMsgs = {
    'Nitrogen Fixer':  'Nitrogen-fixing support is very strong — next additions should complement with productive or support roles.',
    'Ground Cover':    'Ground cover is well saturated — consider adding height and structural diversity to complement it.',
    'Pollinator':      'Pollinator support is very strong — consider adding structural or risk-reduction diversity next.',
    'Mulcher':         'Mulch production is strong — consider adding complementary roles to balance the system.',
    'Pest Management': 'Pest management is well covered — focus next additions on structural or productive roles.',
  };""",
    "5: dominant function tone changed to strength-first framing"
)

f.write_text(text)
print(f"\n{changes} patches applied")
