#!/usr/bin/env python3
"""
patch_phase3_final.py
=====================
Final Phase 3 fixes:
1. Remove scope dependencies from buildExplanations() — pass all vars explicitly
2. Fix top pest selection (sort by occurrence, not random)
3. Improve explanation templates (CAUSE → EFFECT structure)
4. Prevent weak explanations (return [] if no real signal)
Updates BOTH guild-checker.astro and src/lib/nextPlant.js
"""
from pathlib import Path

changes = 0

def patch_by_position(path, old_str, new_str, label):
    global changes
    text = path.read_text()
    if old_str in text:
        path.write_text(text.replace(old_str, new_str))
        changes += 1
        print(f"✅ {label}")
    else:
        print(f"❌ {label} — not found")

fc  = Path("src/pages/guild-checker.astro")
lib = Path("src/lib/nextPlant.js")

# ── 1. Replace buildExplanations() with explicit params + improved templates ──
OLD_FN = """  // ── Context-aware explanation builder ────────────────────────────────────
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
  }"""

NEW_FN = """  // ── Context-aware explanation builder (no hidden scope deps) ───────────────
  // All variables passed explicitly — no closure over outer vars
  function buildExplanations(
    fns, family, pests, sharedPestCount,
    hasMissing, missingReasons, hasNewFamily, familyReasons,
    domFamily, gPests, pestOcc
  ) {
    const explanations = [];

    // Priority 1: fills_gap — CAUSE: missing role → EFFECT: what it does in THIS guild
    if (hasMissing) {
      const role = missingReasons[0]?.replace('Adds missing ', '').replace(' function', '') || '';
      const roleMap = {
        'Ground Cover':    `Adds Ground Cover, protecting exposed soil and reducing moisture loss between your existing plants.`,
        'Pollinator':      `Adds Pollinator support, attracting beneficial insects that improve fruit and seed set across your guild.`,
        'Pest Management': `Adds Pest Management, helping confuse and deter insects that currently have no disruption in your guild.`,
        'Mulcher':         `Adds a Mulcher, generating biomass that feeds soil biology and reduces bare-ground evaporation.`,
        'Nitrogen Fixer':  `Adds a Nitrogen Fixer, feeding soil nitrogen through root nodules to support neighboring plants.`,
      };
      explanations.push(roleMap[role] || `Fills a missing ${role} role in your guild.`);
    }

    // Priority 2: adds_diversity — CAUSE: family dominance → EFFECT: reduced shared vulnerability
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
    }

    // Priority 3: reduces_risk — CAUSE: low overlap → EFFECT: named pests less likely to spread
    if (explanations.length < 2 && sharedPestCount === 0 && pests.size > 0) {
      // Sort by occurrence to get most common guild pests
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
    }

    // Prevent weak explanations: return empty if no real signal
    if (explanations.length === 0) return [];
    if (!hasMissing && !hasNewFamily && sharedPestCount > 2) return [];

    return explanations.slice(0, 2);
  }"""

patch_by_position(fc, OLD_FN, NEW_FN, "astro: buildExplanations() rewritten with explicit params + improved templates")

# ── 2. Update call site to pass dominantFamily, guildPests, pestOccurrence ────
# Also need pestOccurrence to be built before the candidates loop
# First: add pestOccurrence build before "const candidates = [];"

OLD_CANDIDATES = "  const candidates = [];\n\n  // ── Context-aware explanation builder"
NEW_CANDIDATES = """  // Build pestOccurrence for top-pest sorting in explanations
  const pestOccurrence = {};
  for (const slug of currentSlugs) {
    for (const pest of (plantToPests[slug] || new Set())) {
      pestOccurrence[pest] = (pestOccurrence[pest] || 0) + 1;
    }
  }

  const candidates = [];

  // ── Context-aware explanation builder"""

patch_by_position(fc, OLD_CANDIDATES, NEW_CANDIDATES,
                  "astro: pestOccurrence built before candidates loop")

# ── 3. Update call site to pass all 3 new params ─────────────────────────────
OLD_CALL = """    const explanations = buildExplanations(
      fns, family, pests, sharedPestCount,
      hasMissing, missingReasons, hasNewFamily, familyReasons
    );"""

NEW_CALL = """    const explanations = buildExplanations(
      fns, family, pests, sharedPestCount,
      hasMissing, missingReasons, hasNewFamily, familyReasons,
      dominantFamily, guildPests, pestOccurrence
    );"""

patch_by_position(fc, OLD_CALL, NEW_CALL, "astro: call site updated with explicit params")

# ── 4. Update src/lib/nextPlant.js with same improvements ────────────────────
if lib.exists():
    ltext = lib.read_text()

    LIB_OLD_EXPLAIN = """    // Build context-aware explanations
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
    if (explanations.length === 0) continue;"""

    LIB_NEW_EXPLAIN = """    // Build context-aware explanations (explicit params, no hidden scope)
    const explanations = [];
    if (hasMissing) {
      const role = missingReasons[0]?.replace('Adds missing ','').replace(' function','') || '';
      const roleMap = {
        'Ground Cover':    'Adds Ground Cover, protecting exposed soil and reducing moisture loss between your existing plants.',
        'Pollinator':      'Adds Pollinator support, attracting beneficial insects that improve fruit and seed set across your guild.',
        'Pest Management': 'Adds Pest Management, helping confuse and deter insects that currently have no disruption in your guild.',
        'Mulcher':         'Adds a Mulcher, generating biomass that feeds soil biology and reduces bare-ground evaporation.',
        'Nitrogen Fixer':  'Adds a Nitrogen Fixer, feeding soil nitrogen through root nodules to support neighboring plants.',
      };
      explanations.push(roleMap[role] || `Fills a missing ${role} role in your guild.`);
    }
    if (hasNewFamily && explanations.length < 2 && family) {
      const famLabel = family.charAt(0).toUpperCase() + family.slice(1);
      if (dominantFamily) {
        const domLabel = dominantFamily.charAt(0).toUpperCase() + dominantFamily.slice(1);
        explanations.push(`Introduces ${famLabel}, which breaks the shared pest vulnerability of your ${domLabel}-heavy guild.`);
      } else {
        explanations.push(`Introduces ${famLabel}, adding new family diversity that reduces cross-species pest transfer.`);
      }
    }
    if (explanations.length < 2 && sharedPestCount === 0 && pests.size > 0) {
      // Build pestOccurrence for top-pest sorting
      const pestOcc = {};
      for (const slug of currentGuildSlugs) {
        for (const pest of (plantToPests[slug] || new Set())) {
          pestOcc[pest] = (pestOcc[pest] || 0) + 1;
        }
      }
      const topPests = Array.from(guildPests)
        .sort((a, b) => (pestOcc[b] || 0) - (pestOcc[a] || 0))
        .slice(0, 2);
      if (topPests.length > 0) {
        explanations.push(`Shares no pests with your guild, reducing the risk of ${topPests.join(' and ')} spreading between plants.`);
      } else {
        explanations.push('Shares no pest pressure with your current guild — a clean addition.');
      }
    } else if (explanations.length === 0 && sharedPestCount <= 2 && pests.size > 0) {
      explanations.push('Low pest overlap with your guild — minimal risk of amplifying existing pest pressure.');
    }
    if (explanations.length === 0) continue;
    if (!hasMissing && !hasNewFamily && sharedPestCount > 2) continue;"""

    patch_by_position(lib, LIB_OLD_EXPLAIN, LIB_NEW_EXPLAIN,
                      "lib: explanations updated with explicit params + improved templates")

print(f"\n{changes} changes applied")
