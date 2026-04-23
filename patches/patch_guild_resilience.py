#!/usr/bin/env python3
"""
patch_guild_resilience.py
=========================
Phase 1.5 — refactors function analysis from penalty-based to resilience-aware.

Key changes:
- CORE_ROLES split into FOUNDATIONAL_ROLES + CONTEXTUAL_ROLES
- Overlap in support functions is now POSITIVE (reinforced), not penalized
- "weak" warnings removed — 1 plant covering a role is presence, not weakness
- dominant_functions only fires at guild >= 5 AND >70% saturation
- Badge language: missing / present / reinforced / contextual / dominant
- Design actions: missing-role actions + positive reinforcement notes
"""
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

# ── 1. Replace logic block ─────────────────────────────────────────────────────
OLD_LOGIC = """const CORE_ROLES = [
  'Nitrogen Fixer',
  'Ground Cover',
  'Pollinator',
  'Mulcher',
  'Dynamic Accumulator',
  'Shade Provider',
  'Pest Management',
  'Erosion Control',
];

function analyzeGuildFunctions(slugs) {
  const n = slugs.length;
  if (n === 0) return null;

  // Count each core role across guild plants
  const counts = {};
  for (const role of CORE_ROLES) counts[role] = 0;

  for (const slug of slugs) {
    const p = plantBySlug[slug];
    if (!p) continue;
    for (const fn of (p.plant_function || [])) {
      if (counts.hasOwnProperty(fn)) counts[fn]++;
    }
  }

  const missing         = CORE_ROLES.filter(r => counts[r] === 0);
  const weak            = CORE_ROLES.filter(r => counts[r] === 1);
  const balanced        = CORE_ROLES.filter(r => counts[r] >= 2 && counts[r] / n <= 0.5);
  const overrepresented = CORE_ROLES.filter(r => counts[r] >= 3 || (n >= 3 && counts[r] / n > 0.5));

  // Generate specific actions
  const actions = [];

  for (const role of missing) {
    const msgs = {
      'Nitrogen Fixer':      'Add a Nitrogen Fixer to improve soil fertility and feed neighboring plants.',
      'Ground Cover':        'Add Ground Cover to protect soil, retain moisture, and suppress weeds.',
      'Pollinator':          'Add a Pollinator plant to support beneficial insects and improve yields.',
      'Mulcher':             'Add a Mulcher to generate biomass and build soil organic matter.',
      'Dynamic Accumulator': 'Add a Dynamic Accumulator to mine deep minerals and cycle nutrients.',
      'Shade Provider':      'Add a Shade Provider to create microclimate and protect understory plants.',
      'Pest Management':     'Add a Pest Management plant to deter or confuse pest pressure.',
      'Erosion Control':     'Add an Erosion Control plant to stabilize soil on slopes or bare areas.',
    };
    actions.push({ type: 'action', text: msgs[role] || `Add a ${role} to complete this guild function.` });
  }

  for (const role of weak) {
    actions.push({ type: 'caution', text: `Only 1 plant serving as ${role} — consider adding a second for resilience.` });
  }

  for (const role of overrepresented) {
    actions.push({ type: 'risk', text: `${counts[role]} plants serving as ${role} — consider diversifying guild roles.` });
  }

  if (actions.length === 0) {
    actions.push({ type: 'action', text: 'Core functional roles are well represented across the guild.' });
  }

  return { counts, missing, weak, balanced, overrepresented, actions };
}"""

NEW_LOGIC = """// Foundational roles: warn if missing, celebrate if reinforced
const FOUNDATIONAL_ROLES = [
  'Nitrogen Fixer',
  'Ground Cover',
  'Pollinator',
  'Pest Management',
  'Mulcher',
];

// Contextual roles: show if present, never warn if absent
const CONTEXTUAL_ROLES = [
  'Dynamic Accumulator',
  'Erosion Control',
  'Shade Provider',
];

const ALL_TRACKED_ROLES = [...FOUNDATIONAL_ROLES, ...CONTEXTUAL_ROLES];

function analyzeGuildFunctions(slugs) {
  const n = slugs.length;
  if (n === 0) return null;

  // Count every tracked role across guild plants
  const counts = {};
  for (const role of ALL_TRACKED_ROLES) counts[role] = 0;

  for (const slug of slugs) {
    const p = plantBySlug[slug];
    if (!p) continue;
    for (const fn of (p.plant_function || [])) {
      if (counts.hasOwnProperty(fn)) counts[fn]++;
    }
  }

  // missing_foundational: foundational roles with 0 coverage
  const missingFoundational = FOUNDATIONAL_ROLES.filter(r => counts[r] === 0);

  // present_foundational: foundational roles with >= 1 coverage
  const presentFoundational = FOUNDATIONAL_ROLES.filter(r => counts[r] >= 1);

  // reinforced: ANY tracked role with >= 2 coverage (usually good)
  const reinforced = ALL_TRACKED_ROLES.filter(r => counts[r] >= 2);

  // contextual: contextual roles that are present
  const contextualPresent = CONTEXTUAL_ROLES.filter(r => counts[r] >= 1);

  // dominant: only flag if guild >= 5 AND role > 70% saturation
  // This is rare and intentional — normal overlap is NOT flagged
  const dominant = ALL_TRACKED_ROLES.filter(r =>
    n >= 5 && counts[r] / n > 0.7
  );

  // ── Generate design actions ───────────────────────────────────────────────
  const actions = [];

  // Missing foundational roles — clear actionable gaps
  const missingMsgs = {
    'Nitrogen Fixer':  'Add a Nitrogen Fixer to improve soil fertility and feed neighboring plants.',
    'Ground Cover':    'Add Ground Cover to protect exposed soil, retain moisture, and suppress weeds.',
    'Pollinator':      'Add a Pollinator plant to strengthen beneficial insect activity.',
    'Pest Management': 'Add a Pest Management plant to break insect pressure and confuse pest navigation.',
    'Mulcher':         'Add a Mulcher to generate biomass and build soil organic matter.',
  };
  for (const role of missingFoundational) {
    actions.push({ type: 'action', text: missingMsgs[role] || `Add a ${role} to fill a missing foundational role.` });
  }

  // Dominant functions — only fires in large guilds with extreme saturation
  const dominantMsgs = {
    'Nitrogen Fixer':  'Nitrogen-fixing plants dominate this guild — ensure other roles are not crowded out.',
    'Ground Cover':    'Ground cover plants dominate — check that taller layers are represented.',
    'Pollinator':      'Pollinator plants dominate — consider structural diversity across layers.',
    'Mulcher':         'Mulch producers dominate — ensure food-producing and support layers are present.',
    'Pest Management': 'Pest management plants dominate — check for balance with productive layers.',
  };
  for (const role of dominant) {
    actions.push({ type: 'risk', text: dominantMsgs[role] || `${role} saturates this guild — review overall role balance.` });
  }

  // Positive reinforcement notes for reinforced support functions
  const reinforcedMsgs = {
    'Nitrogen Fixer':      'Nitrogen-fixing support is reinforced — good for long-term soil fertility.',
    'Mulcher':             'Mulch production is reinforced — biomass and soil building are well covered.',
    'Pollinator':          'Pollinator support is reinforced — beneficial insect activity should be strong.',
    'Dynamic Accumulator': 'Dynamic accumulation is reinforced — mineral cycling is well supported.',
    'Erosion Control':     'Erosion control is reinforced — soil stability is well covered.',
    'Ground Cover':        'Ground cover is reinforced — soil protection is strong.',
    'Pest Management':     'Pest management is reinforced — insect disruption is well supported.',
  };
  for (const role of reinforced) {
    if (!dominant.includes(role) && reinforcedMsgs[role]) {
      actions.push({ type: 'positive', text: reinforcedMsgs[role] });
    }
  }

  if (actions.length === 0) {
    actions.push({ type: 'action', text: 'Core foundational roles are well covered — guild looks ecologically balanced.' });
  }

  return {
    counts,
    missingFoundational,
    presentFoundational,
    reinforced,
    contextualPresent,
    dominant,
    actions,
  };
}"""

if OLD_LOGIC in text:
    text = text.replace(OLD_LOGIC, NEW_LOGIC)
    changes += 1; print("✅ 1: logic block replaced with resilience-aware version")
else:
    print("❌ 1: logic block not found")

# ── 2. Replace render block ────────────────────────────────────────────────────
OLD_RENDER = """  if (fnAnalysis) {
    // Render function balance rows
    fnBalance.innerHTML = '<div class="function-balance">' +
      CORE_ROLES.map(role => {
        const count   = fnAnalysis.counts[role];
        const isMissing = count === 0;
        const isWeak    = count === 1;
        const isOver    = fnAnalysis.overrepresented.includes(role);
        const rowClass  = isMissing ? 'missing' : isOver ? 'over' : isWeak ? 'weak' : 'strong';
        const cntClass  = isMissing ? 'zero' : isOver ? 'over' : isWeak ? 'one' : 'good';
        const badge     = isMissing ? 'missing' : isOver ? 'over' : isWeak ? 'weak' : 'balanced';
        const badgeTxt  = isMissing ? 'missing' : isOver ? 'excess' : isWeak ? 'weak' : 'ok';
        const barW      = Math.min(100, Math.round((count / guild.length) * 100));
        const barColor  = isMissing ? 'var(--rust)' : isOver ? 'var(--ash)' : isWeak ? 'var(--straw)' : 'var(--lime)';
        return `<div class="fn-row ${rowClass}">
          <span class="fn-name">${role}</span>
          <div class="fn-bar-wrap"><div class="fn-bar" style="width:${barW}%;background:${barColor}"></div></div>
          <span class="fn-count ${cntClass}">${count}</span>
          <span class="fn-badge ${badge}">${badgeTxt}</span>
        </div>`;
      }).join('') + '</div>';

    // Render design actions
    actionsList.innerHTML = '';
    for (const a of fnAnalysis.actions) {
      const el = document.createElement('div');
      el.className = `action-item ${a.type === 'action' ? '' : a.type}`.trim();
      const icon = a.type === 'risk' ? '⚠️' : a.type === 'caution' ? '💛' : '→';
      el.textContent = icon + ' ' + a.text;
      actionsList.appendChild(el);
    }
  }"""

NEW_RENDER = """  if (fnAnalysis) {
    // ── Function Balance — three grouped sections ────────────────────────────
    const n = guild.length;
    let balanceHTML = '<div class="function-balance">';

    // Section 1: Foundational roles (all shown — missing highlighted)
    balanceHTML += '<div class="fn-section-label">Foundational</div>';
    for (const role of FOUNDATIONAL_ROLES) {
      const count     = fnAnalysis.counts[role];
      const isMissing = count === 0;
      const isReinf   = count >= 2;
      const isDom     = fnAnalysis.dominant.includes(role);
      const rowClass  = isMissing ? 'missing' : isDom ? 'over' : isReinf ? 'strong' : 'strong';
      const cntClass  = isMissing ? 'zero' : 'good';
      const badge     = isMissing ? 'missing' : isDom ? 'dominant' : isReinf ? 'reinforced' : 'present';
      const badgeTxt  = isMissing ? 'missing' : isDom ? 'dominant' : isReinf ? 'reinforced' : 'present';
      const barW      = Math.min(100, n > 0 ? Math.round((count / n) * 100) : 0);
      const barColor  = isMissing ? 'var(--rust)' : isDom ? 'var(--straw)' : 'var(--lime)';
      balanceHTML += `<div class="fn-row ${rowClass}">
        <span class="fn-name">${role}</span>
        <div class="fn-bar-wrap"><div class="fn-bar" style="width:${barW}%;background:${barColor}"></div></div>
        <span class="fn-count ${cntClass}">${count}</span>
        <span class="fn-badge ${badge}">${badgeTxt}</span>
      </div>`;
    }

    // Section 2: Contextual roles (only shown if present)
    const ctxPresent = CONTEXTUAL_ROLES.filter(r => fnAnalysis.counts[r] > 0);
    if (ctxPresent.length > 0) {
      balanceHTML += '<div class="fn-section-label" style="margin-top:0.75rem">Contextual</div>';
      for (const role of ctxPresent) {
        const count   = fnAnalysis.counts[role];
        const isReinf = count >= 2;
        const barW    = Math.min(100, n > 0 ? Math.round((count / n) * 100) : 0);
        balanceHTML += `<div class="fn-row strong">
          <span class="fn-name">${role}</span>
          <div class="fn-bar-wrap"><div class="fn-bar" style="width:${barW}%;background:var(--lime)"></div></div>
          <span class="fn-count good">${count}</span>
          <span class="fn-badge ${isReinf ? 'reinforced' : 'contextual'}">${isReinf ? 'reinforced' : 'contextual'}</span>
        </div>`;
      }
    }

    balanceHTML += '</div>';
    fnBalance.innerHTML = balanceHTML;

    // ── Design Actions ────────────────────────────────────────────────────────
    actionsList.innerHTML = '';
    for (const a of fnAnalysis.actions) {
      const el = document.createElement('div');
      const typeMap = { action: '', risk: 'risk', caution: 'caution', positive: 'positive' };
      el.className = `action-item ${typeMap[a.type] || ''}`.trim();
      const icon = a.type === 'risk' ? '⚠️' : a.type === 'positive' ? '✓' : '→';
      el.textContent = icon + ' ' + a.text;
      actionsList.appendChild(el);
    }
  }"""

if OLD_RENDER in text:
    text = text.replace(OLD_RENDER, NEW_RENDER)
    changes += 1; print("✅ 2: render block updated with grouped sections")
else:
    print("❌ 2: render block not found")

# ── 3. Update CSS — add missing badge types, section labels, positive style ───
OLD_CSS = """  .fn-badge.missing { color: var(--rust); border-color: rgba(196,85,26,0.4); }
  .fn-badge.weak { color: var(--straw); border-color: rgba(212,168,67,0.4); }
  .fn-badge.balanced { color: var(--lime); border-color: rgba(139,184,58,0.4); }
  .fn-badge.over { color: var(--ash); border-color: rgba(184,176,160,0.3); }"""

NEW_CSS = """  .fn-badge.missing { color: var(--rust); border-color: rgba(196,85,26,0.4); }
  .fn-badge.present { color: var(--lime); border-color: rgba(139,184,58,0.3); }
  .fn-badge.reinforced { color: var(--lime); border-color: rgba(139,184,58,0.5); background: rgba(42,61,31,0.3); }
  .fn-badge.contextual { color: var(--ash); border-color: rgba(184,176,160,0.25); }
  .fn-badge.dominant { color: var(--straw); border-color: rgba(212,168,67,0.4); }
  .fn-section-label { font-family: 'Space Mono', monospace; font-size: 0.55rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--ash); opacity: 0.6; margin-bottom: 0.3rem; margin-top: 0.1rem; }
  .action-item.positive { border-left-color: var(--lime); background: rgba(42,61,31,0.2); color: var(--ash); }"""

if OLD_CSS in text:
    text = text.replace(OLD_CSS, NEW_CSS)
    changes += 1; print("✅ 3: CSS updated with new badge types and section labels")
else:
    print("❌ 3: CSS not found")

f.write_text(text)
print(f"\n{changes} patches applied")
