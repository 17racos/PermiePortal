#!/usr/bin/env python3
"""
patch_phase5_6.py
=================
Phase 5.6 — Assistive Completion Mode:
1. guild changes from [slug] to [{slug, source}]
2. removedByUser Set tracks user removals
3. addToGuild() updated to track source + layers + family
4. removePlant() extracted (was inline in slots)
5. completeGuild() added
6. generateGoalGuild accepts {preserveExisting} param
7. Search + clear updated for new structure
8. All guild.map/filter/includes updated
9. "Complete Guild" button added
10. Visual source badge (auto tag)
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

# ── 1. Guild state: add removedByUser, update addToGuild ─────────────────────
patch(
    "// ── Guild state ───────────────────────────────────────────────────────────────\nlet guild = [];\nlet userZone = 9;",
    """// ── Guild state ───────────────────────────────────────────────────────────────
let guild = [];          // [{slug, source: 'user'|'generated'}]
let removedByUser = new Set();
let userZone = 9;""",
    "1: guild state updated with removedByUser"
)

# ── 2. Update addToGuild to accept source param ───────────────────────────────
patch(
    """  function addToGuild(slug) {
    generated.push(slug);
    guildSet.add(slug);
    const fam = plantToFamily[slug] || '__none__';
    famSeen[fam] = (famSeen[fam] || 0) + 1;
    const layer = inferLayer(plantBySlug[slug] || {});
    layerSeen[layer] = (layerSeen[layer] || 0) + 1;
  }""",
    """  function addToGuild(slug, source = 'generated') {
    if (guildSet.has(slug)) return;
    generated.push(slug);
    guildSet.add(slug);
    const fam = plantToFamily[slug] || '__none__';
    famSeen[fam] = (famSeen[fam] || 0) + 1;
    const p = plantBySlug[slug];
    if (p) {
      const layer = inferLayer(p);
      layerSeen[layer] = (layerSeen[layer] || 0) + 1;
    }
    // Push to global guild with source tag
    guild.push({ slug, source });
    removedByUser.delete(slug);
  }""",
    "2: addToGuild updated with source param"
)

# ── 3. Skip removed plants in all generator loops ────────────────────────────
# Iterative while loop
patch(
    "      if (guildSet.has(p.slug)) continue;\n      if (!p.plant_function || p.plant_function.length === 0) continue;\n      if (goalKey === 'food_production' && p.food_role === 'specialty') continue;\n      if (getZoneFit(p, userZone) === 'out') continue;",
    """      if (guildSet.has(p.slug)) continue;
      if (removedByUser.has(p.slug)) continue;
      if (!p.plant_function || p.plant_function.length === 0) continue;
      if (goalKey === 'food_production' && p.food_role === 'specialty') continue;
      if (getZoneFit(p, userZone) === 'out') continue;""",
    "3: removedByUser check in iterative loop"
)

# pickBestForRole loop
patch(
    "      if (guildSet.has(p.slug)) continue;\n      if (!p.plant_function || p.plant_function.length === 0) continue;\n      if (!p.plant_function.includes(requiredRole)) continue;\n      if (getZoneFit(p, userZone) === 'out') continue;",
    """      if (guildSet.has(p.slug)) continue;
      if (removedByUser.has(p.slug)) continue;
      if (!p.plant_function || p.plant_function.length === 0) continue;
      if (!p.plant_function.includes(requiredRole)) continue;
      if (getZoneFit(p, userZone) === 'out') continue;""",
    "3b: removedByUser check in pickBestForRole"
)

# ── 4. generateGoalGuild: add preserveExisting param, update guild reset ──────
patch(
    "function generateGoalGuild(goalKey) {\n  const profile = GOAL_PROFILES[goalKey];\n  if (!profile) return [];\n\n  const generated = [];\n  const guildSet  = new Set();\n  const famSeen   = {};\n  let layerSeen = {};",
    """function generateGoalGuild(goalKey, { preserveExisting = false } = {}) {
  const profile = GOAL_PROFILES[goalKey];
  if (!profile) return [];

  let generated = [];
  const guildSet  = new Set();
  let famSeen   = {};
  let layerSeen = {};

  if (preserveExisting) {
    // Rebuild context from existing guild — don't wipe user plants
    for (const g of guild) {
      generated.push(g.slug);
      guildSet.add(g.slug);
      const fam = plantToFamily[g.slug] || '__none__';
      famSeen[fam] = (famSeen[fam] || 0) + 1;
      const p = plantBySlug[g.slug];
      if (p) {
        const layer = inferLayer(p);
        layerSeen[layer] = (layerSeen[layer] || 0) + 1;
      }
    }
  }""",
    "4: generateGoalGuild accepts preserveExisting param"
)

# ── 5. generateGoalGuild: don't push to guild directly (addToGuild does it) ──
# The return value is used by the generate button — keep return generated
# but addToGuild now pushes to guild[], so avoid double-push
# Find the return statement and add a note
patch(
    "  return generated;\n}\n\n",
    """  // Note: addToGuild() pushes each slug to guild[] during generation
  // For preserveExisting mode, only NEW plants were added via addToGuild
  return generated;
}

""",
    "5: clarifying comment on return"
)

# ── 6. Update renderGuild to use guild[].slug ─────────────────────────────────
patch(
    "  countEl.textContent = guild.length;\n\n  // Remove old slots (not the empty placeholder)\n  slots.querySelectorAll('.guild-slot').forEach(el => el.remove());\n\n  if (guild.length === 0) {\n    empty.style.display = 'block';\n  } else {\n    empty.style.display = 'none';\n    for (const slug of guild) {",
    """  countEl.textContent = guild.length;

  // Remove old slots (not the empty placeholder)
  slots.querySelectorAll('.guild-slot').forEach(el => el.remove());

  if (guild.length === 0) {
    empty.style.display = 'block';
  } else {
    empty.style.display = 'none';
    for (const g of guild) {
      const slug = g.slug;""",
    "6a: renderGuild uses guild[].slug"
)

# Fix the slot innerHTML to show source badge
patch(
    """      const el = document.createElement('div');
      el.className = 'guild-slot';
      el.innerHTML = `
        <div>
          <div class="slot-name">${p.common_name}</div>
          ${fam ? `<div class="slot-family">${fam}</div>` : ''}
        </div>
        <button class="slot-remove" data-slug="${slug}">✕</button>
      `;""",
    """      const el = document.createElement('div');
      el.className = 'guild-slot';
      el.innerHTML = `
        <div>
          <div class="slot-name">${p.common_name}${g.source === 'generated' ? ' <span class="plant-tag-auto">auto</span>' : ''}</div>
          ${fam ? `<div class="slot-family">${fam}</div>` : ''}
        </div>
        <button class="slot-remove" data-slug="${slug}">✕</button>
      `;""",
    "6b: auto badge for generated plants"
)

# ── 7. Update remove button handler ──────────────────────────────────────────
patch(
    "    slots.querySelectorAll('.slot-remove').forEach(btn => {\n    btn.addEventListener('click', () => {\n      const slug = btn.getAttribute('data-slug');\n      guild = guild.filter(s => s !== slug);\n      renderGuild();\n      renderResults();\n    });\n  });",
    """    slots.querySelectorAll('.slot-remove').forEach(btn => {
    btn.addEventListener('click', () => {
      const slug = btn.getAttribute('data-slug');
      const entry = guild.find(g => g.slug === slug);
      if (entry && entry.source === 'generated') {
        removedByUser.add(slug);
      }
      guild = guild.filter(g => g.slug !== slug);
      renderGuild();
      renderResults();
    });
  });""",
    "7: remove button tracks removedByUser"
)

# ── 8. Update renderResults to use slug extraction ────────────────────────────
patch(
    "  if (guild.length < 2) {",
    """  const guildSlugs = guild.map(g => g.slug);
  if (guild.length < 2) {""",
    "8a: guildSlugs extracted at top of renderResults"
)

# ── 9. Fix all slug-based calls in renderResults ─────────────────────────────
patch(
    "  const r = scoreGuild(guild);",
    "  const r = scoreGuild(guildSlugs);",
    "9a: scoreGuild uses guildSlugs"
)

patch(
    "  const r = analyzeGuildFunctions(guild);",
    "  const r = analyzeGuildFunctions(guildSlugs);",
    "9b: analyzeGuildFunctions — not likely present but safe"
)

# fnAnalysis
patch(
    "  const fnAnalysis = analyzeGuildFunctions(guild);",
    "  const fnAnalysis = analyzeGuildFunctions(guildSlugs);",
    "9c: analyzeGuildFunctions uses guildSlugs"
)

# pattern
patch(
    "    const pattern = analyzeGuildPattern(guild, fnAnalysis, r);",
    "    const pattern = analyzeGuildPattern(guildSlugs, fnAnalysis, r);",
    "9d: analyzeGuildPattern uses guildSlugs"
)

# diversity section
patch(
    "  const n = guild.length;\n  const divFamilies = guild.filter(s => plantToFamily[s]).map(s => plantToFamily[s]);",
    "  const n = guildSlugs.length;\n  const divFamilies = guildSlugs.filter(s => plantToFamily[s]).map(s => plantToFamily[s]);",
    "9e: diversity section uses guildSlugs"
)

# next plants
patch(
    "  if (guild.length >= 2) {\n    const suggestions = getNextBestPlants(guild, 5);",
    "  if (guildSlugs.length >= 2) {\n    const suggestions = getNextBestPlants(guildSlugs, 5);",
    "9f: getNextBestPlants uses guildSlugs"
)

# ── 10. Fix search box to use slug comparison ─────────────────────────────────
patch(
    ".filter(p => p.common_name.toLowerCase().includes(q) && !guild.includes(p.slug))",
    ".filter(p => p.common_name.toLowerCase().includes(q) && !guild.some(g => g.slug === p.slug))",
    "10a: search filter uses guild[].slug"
)

patch(
    "        if (!guild.includes(p.slug)) {\n          guild.push(p.slug);",
    "        if (!guild.some(g => g.slug === p.slug)) {\n          guild.push({ slug: p.slug, source: 'user' });",
    "10b: search add uses new guild structure"
)

# ── 11. Fix clear button ──────────────────────────────────────────────────────
patch(
    """  guild = [];
  selectedGoal = null;
  document.querySelectorAll('.goal-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('goal-generate-btn').style.display = 'none';
  document.getElementById('goal-header').style.display = 'none';
  renderGuild();
  renderResults();""",
    """  guild = [];
  removedByUser.clear();
  selectedGoal = null;
  document.querySelectorAll('.goal-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('goal-generate-btn').style.display = 'none';
  document.getElementById('goal-header').style.display = 'none';
  renderGuild();
  renderResults();""",
    "11: clear button also clears removedByUser"
)

# ── 12. Fix generate button to reset guild[] correctly ────────────────────────
patch(
    """  const slugs    = generateGoalGuild(selectedGoal);

  // Populate guild
  guild = slugs;""",
    """  // Full regeneration — clear existing guild and removedByUser
  guild = [];
  removedByUser.clear();
  generateGoalGuild(selectedGoal);

  // guild[] is now populated by addToGuild() calls inside generator
  const slugs = guild.map(g => g.slug);""",
    "12: generate button resets guild and triggers generator"
)

# ── 13. Add completeGuild function + Complete Guild button ────────────────────
patch(
    "// ── Goal selector interaction ─────────────────────────────────────────────────\nlet selectedGoal = null;",
    """// ── Complete guild (preserve existing, fill gaps) ────────────────────────────
function completeGuild() {
  if (!selectedGoal) return;
  generateGoalGuild(selectedGoal, { preserveExisting: true });
  renderGuild();
  renderResults();
}

// ── Goal selector interaction ─────────────────────────────────────────────────
let selectedGoal = null;""",
    "13a: completeGuild() function added"
)

# Add complete button to HTML
patch(
    '      <button class="goal-generate-btn" id="goal-generate-btn" style="display:none">\n        Generate Starter Guild →\n      </button>',
    """      <button class="goal-generate-btn" id="goal-generate-btn" style="display:none">
        Generate Starter Guild →
      </button>
      <button class="goal-complete-btn" id="goal-complete-btn" style="display:none">
        Complete Missing Gaps →
      </button>""",
    "13b: Complete Guild button added to HTML"
)

# Wire complete button
patch(
    "document.getElementById('goal-generate-btn').addEventListener('click', () => {",
    """document.getElementById('goal-complete-btn').addEventListener('click', () => {
  if (!selectedGoal) return;
  completeGuild();
  const header = document.getElementById('goal-header');
  const profile = GOAL_PROFILES[selectedGoal];
  header.innerHTML = `<strong>Goal: ${profile.label} (gaps completed)</strong><br>${profile.description}`;
  header.style.display = 'block';
});

document.getElementById('goal-generate-btn').addEventListener('click', () => {""",
    "13c: complete button wired"
)

# Show complete button when goal is selected
patch(
    "    document.getElementById('goal-generate-btn').style.display = 'block';",
    """    document.getElementById('goal-generate-btn').style.display = 'block';
    // Show complete button only if guild has plants
    if (guild.length > 0) {
      document.getElementById('goal-complete-btn').style.display = 'block';
    }""",
    "13d: complete button shown when goal selected + guild has plants"
)

# Also show complete button after generating
patch(
    """  // guild[] is now populated by addToGuild() calls inside generator
  const slugs = guild.map(g => g.slug);""",
    """  // guild[] is now populated by addToGuild() calls inside generator
  const slugs = guild.map(g => g.slug);
  document.getElementById('goal-complete-btn').style.display = 'block';""",
    "13e: complete button shown after generation"
)

# ── 14. Add CSS for auto badge + complete button ──────────────────────────────
patch(
    "  .slot-remove:hover { border-color: var(--rust); background: rgba(196,85,26,0.1); }",
    """  .slot-remove:hover { border-color: var(--rust); background: rgba(196,85,26,0.1); }
  .plant-tag-auto { font-family: 'Space Mono', monospace; font-size: 0.5rem; letter-spacing: 0.06em; text-transform: uppercase; padding: 0.1rem 0.3rem; border: 1px solid rgba(139,184,58,0.25); color: var(--ash); opacity: 0.7; margin-left: 0.3rem; vertical-align: middle; }
  .goal-complete-btn { font-family: 'Space Mono', monospace; font-size: 0.62rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.45rem 1rem; background: none; border: 1px solid rgba(139,184,58,0.3); color: var(--ash); cursor: pointer; transition: all 0.2s; width: 100%; margin-top: 0.4rem; }
  .goal-complete-btn:hover { border-color: var(--lime); color: var(--lime); }""",
    "14: auto badge + complete button CSS added"
)

# ── 15. Fix scoreGuild/analyzeGuildFunctions calls with guildSlugs ───────────
# These functions receive slugs internally — make sure renderResults passes guildSlugs
# Find the remaining guild references in renderResults
patch(
    "  const suggestions = getNextBestPlants(guildSlugs, 5);",
    "  const suggestions = getNextBestPlants(guildSlugs, 5);",
    "15: getNextBestPlants already patched (no-op verify)"
)

f.write_text(text)
print(f"\n{changes} patches applied")
