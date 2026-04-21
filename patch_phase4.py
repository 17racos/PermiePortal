#!/usr/bin/env python3
"""
patch_phase4_goal_builder.py
============================
Phase 4 — Goal-Driven Builder:
1. Goal selector UI above search box
2. GOAL_PROFILES config
3. generateGoalGuild() function using existing scoring logic
4. Auto-populate guild + show goal header
5. CSS for goal selector
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

# ── 1. Add goal selector HTML above search ────────────────────────────────────
patch(
    '    <p class="panel-label">Add Plants to Your Guild</p>\n    <div class="search-wrap">',
    """    <div class="goal-selector" id="goal-selector">
      <p class="panel-label">Start with a Goal <span class="goal-optional">(optional)</span></p>
      <div class="goal-buttons">
        <button class="goal-btn" data-goal="food_production">Food Production</button>
        <button class="goal-btn" data-goal="low_maintenance">Low Maintenance</button>
        <button class="goal-btn" data-goal="pest_resistant">Pest Resistant</button>
        <button class="goal-btn" data-goal="pollinator_support">Pollinator Support</button>
        <button class="goal-btn" data-goal="soil_building">Soil Building</button>
      </div>
      <button class="goal-generate-btn" id="goal-generate-btn" style="display:none">
        Generate Starter Guild →
      </button>
    </div>
    <div id="goal-header" style="display:none" class="goal-header"></div>

    <p class="panel-label">Add Plants to Your Guild</p>
    <div class="search-wrap">""",
    "1: goal selector HTML added"
)

# ── 2. Add goal selector CSS ──────────────────────────────────────────────────
patch(
    "  .empty-state { padding: 3rem 0; text-align: center; }",
    """  .goal-selector { margin-bottom: 1.5rem; padding-bottom: 1.25rem; border-bottom: 1px solid rgba(139,184,58,0.1); }
  .goal-optional { font-size: 0.55rem; color: var(--ash); opacity: 0.5; letter-spacing: 0.05em; text-transform: none; font-style: italic; }
  .goal-buttons { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.75rem; }
  .goal-btn { font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 0.06em; text-transform: uppercase; padding: 0.3rem 0.65rem; background: none; border: 1px solid rgba(139,184,58,0.2); color: var(--ash); cursor: pointer; transition: all 0.2s; }
  .goal-btn:hover { border-color: rgba(139,184,58,0.4); color: var(--lime); }
  .goal-btn.active { border-color: var(--lime); color: var(--lime); background: rgba(42,61,31,0.3); }
  .goal-generate-btn { font-family: 'Space Mono', monospace; font-size: 0.62rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.45rem 1rem; background: rgba(42,61,31,0.4); border: 1px solid rgba(139,184,58,0.35); color: var(--lime); cursor: pointer; transition: all 0.2s; width: 100%; }
  .goal-generate-btn:hover { background: rgba(42,61,31,0.6); border-color: var(--lime); }
  .goal-header { font-family: 'Space Mono', monospace; font-size: 0.65rem; color: var(--straw); padding: 0.5rem 0.75rem; border-left: 2px solid var(--straw); background: rgba(212,168,67,0.06); margin-bottom: 1rem; line-height: 1.6; }
  .empty-state { padding: 3rem 0; text-align: center; }""",
    "2: goal selector CSS added"
)

# ── 3. Add GOAL_PROFILES + generateGoalGuild() before renderGuild() ──────────
patch(
    "// ── Render ────────────────────────────────────────────────────────────────────\nfunction renderGuild() {",
    """// ── Goal profiles ────────────────────────────────────────────────────────────
const GOAL_PROFILES = {
  food_production: {
    label: 'Food Production',
    description: 'Prioritizes edible species with soil support and structural resilience.',
    targetRoles: ['Edible', 'Ground Cover', 'Nitrogen Fixer', 'Mulcher'],
    avoidOverweight: ['Ornamental'],
    preferredGuildSize: 6,
  },
  low_maintenance: {
    label: 'Low Maintenance',
    description: 'Self-sustaining ground cover, mulch, and pest deterrence with minimal input.',
    targetRoles: ['Ground Cover', 'Mulcher', 'Pest Management', 'Pollinator'],
    avoidOverweight: ['Edible'],
    preferredGuildSize: 5,
  },
  pest_resistant: {
    label: 'Pest Resistant',
    description: 'Strong pest disruption, pollinator support, and family diversity to reduce shared pressure.',
    targetRoles: ['Pest Management', 'Pollinator', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 6,
  },
  pollinator_support: {
    label: 'Pollinator Support',
    description: 'Dense pollinator habitat with pest deterrence and ground-level coverage.',
    targetRoles: ['Pollinator', 'Pest Management', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 5,
  },
  soil_building: {
    label: 'Soil Building',
    description: 'Deep soil improvement through nitrogen fixation, dynamic accumulation, and biomass production.',
    targetRoles: ['Nitrogen Fixer', 'Mulcher', 'Dynamic Accumulator', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 6,
  },
};

function generateGoalGuild(goalKey) {
  const profile = GOAL_PROFILES[goalKey];
  if (!profile) return [];

  const generated = [];
  const guildSet  = new Set();
  const famSeen   = {};

  // Score a candidate against the current growing guild + goal profile
  function scorePlant(p, currentSlugs) {
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    // Goal role bonus
    let goalBonus = 0;
    for (const fn of fns) {
      if (profile.targetRoles.includes(fn)) goalBonus += 1.5;
      if (profile.avoidOverweight.length > 0 &&
          profile.avoidOverweight.includes(fn) &&
          !profile.targetRoles.includes(fn)) goalBonus -= 0.5;
    }

    // Family diversity bonus
    const existingFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const familyBonus = (family && !existingFamilies.has(family)) ? 1.0 : 0;

    // Pest overlap penalty
    const guildPests = new Set();
    for (const s of currentSlugs) {
      for (const pest of (plantToPests[s] || new Set())) guildPests.add(pest);
    }
    let sharedPests = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPests++; }
    const pestPenalty = sharedPests * 0.3;

    return goalBonus + familyBonus - pestPenalty;
  }

  // Build guild iteratively
  for (let i = 0; i < profile.preferredGuildSize; i++) {
    let bestSlug  = null;
    let bestScore = -Infinity;

    for (const p of plantIndex) {
      if (guildSet.has(p.slug)) continue;
      if (!p.plant_function || p.plant_function.length === 0) continue;

      // Max 2 per family in generated guild
      const fam = plantToFamily[p.slug] || '__none__';
      if ((famSeen[fam] || 0) >= 2) continue;

      const score = scorePlant(p, generated);
      if (score <= 0 && i > 0) continue; // first plant always gets added

      if (score > bestScore ||
          (score === bestScore && bestSlug && p.slug < bestSlug)) {
        bestScore = score;
        bestSlug  = p.slug;
      }
    }

    if (bestSlug) {
      generated.push(bestSlug);
      guildSet.add(bestSlug);
      const fam = plantToFamily[bestSlug] || '__none__';
      famSeen[fam] = (famSeen[fam] || 0) + 1;
    } else {
      break; // no more good candidates
    }
  }

  return generated;
}

// ── Render ────────────────────────────────────────────────────────────────────
function renderGuild() {""",
    "3: GOAL_PROFILES + generateGoalGuild() added"
)

# ── 4. Wire goal button interaction + generate button in script ───────────────
patch(
    "// ── Search ────────────────────────────────────────────────────────────────────",
    """// ── Goal selector interaction ─────────────────────────────────────────────────
let selectedGoal = null;

document.querySelectorAll('.goal-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.goal-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedGoal = btn.getAttribute('data-goal');
    document.getElementById('goal-generate-btn').style.display = 'block';
  });
});

document.getElementById('goal-generate-btn').addEventListener('click', () => {
  if (!selectedGoal) return;
  const profile  = GOAL_PROFILES[selectedGoal];
  const slugs    = generateGoalGuild(selectedGoal);

  // Populate guild
  guild = slugs;
  renderGuild();
  renderResults();

  // Show goal header
  const header = document.getElementById('goal-header');
  header.innerHTML = `<strong>Goal: ${profile.label}</strong><br>${profile.description}`;
  header.style.display = 'block';
});

// ── Search ────────────────────────────────────────────────────────────────────""",
    "4: goal selector JS interaction wired"
)

# ── 5. Clear goal state when guild is cleared ─────────────────────────────────
patch(
    """document.getElementById('clear-btn').addEventListener('click', () => {
  guild = [];
  renderGuild();
  renderResults();
});""",
    """document.getElementById('clear-btn').addEventListener('click', () => {
  guild = [];
  selectedGoal = null;
  document.querySelectorAll('.goal-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('goal-generate-btn').style.display = 'none';
  document.getElementById('goal-header').style.display = 'none';
  renderGuild();
  renderResults();
});""",
    "5: clear button resets goal state"
)

f.write_text(text)
print(f"\n{changes} patches applied")
