#!/usr/bin/env python3
"""
patch_guild_functions.py
========================
Upgrades Guild Builder with function composition analysis.

Changes:
1. plantIndex now includes plant_function array
2. analyzeGuildFunctions() added to client JS
3. Function Balance section added to HTML
4. Design Actions section added to HTML
5. Old generic suggestions downgraded to Risks
6. CSS added for new sections
"""
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

# ── 1. Add plant_function to plantIndex payload ───────────────────────────────
old = """const plantIndex = plantsData.map((p: any) => ({
  slug: p.slug,
  common_name: p.common_name,
  family: p.family,
  scientific_name: p.scientific_name,
}));"""

new = """const plantIndex = plantsData.map((p: any) => ({
  slug: p.slug,
  common_name: p.common_name,
  family: p.family,
  scientific_name: p.scientific_name,
  plant_function: p.plant_function || [],
}));"""

if old in text:
    text = text.replace(old, new)
    changes += 1; print("✅ 1: plant_function added to plantIndex")
else: print("❌ 1: plantIndex not found")

# ── 2. Add Function Balance + Design Actions HTML sections ────────────────────
old = """      <div class="result-section" id="section-diversity">
        <p class="result-section-title">Family Diversity</p>
        <div class="diversity-grid" id="diversity-grid"></div>
        <div id="diversity-warning" class="diversity-warning" style="display:none"></div>
      </div>"""

new = """      <div class="result-section" id="section-diversity">
        <p class="result-section-title">Family Diversity</p>
        <div class="diversity-grid" id="diversity-grid"></div>
        <div id="diversity-warning" class="diversity-warning" style="display:none"></div>
      </div>

      <div class="result-section" id="section-functions">
        <p class="result-section-title">Function Balance</p>
        <div id="function-balance"></div>
      </div>

      <div class="result-section" id="section-actions">
        <p class="result-section-title">Design Actions</p>
        <div class="actions-list" id="actions-list"></div>
      </div>"""

if old in text:
    text = text.replace(old, new)
    changes += 1; print("✅ 2: Function Balance + Design Actions HTML added")
else: print("❌ 2: diversity section anchor not found")

# ── 3. Add CSS for function sections ─────────────────────────────────────────
old = "  .empty-state { padding: 3rem 0; text-align: center; }"
new = """  .function-balance { display: flex; flex-direction: column; gap: 0.5rem; }
  .fn-row { display: flex; align-items: center; gap: 0.75rem; padding: 0.45rem 0.75rem; background: var(--bark); border: 1px solid rgba(139,184,58,0.1); }
  .fn-row.missing { border-color: rgba(196,85,26,0.3); background: rgba(122,59,30,0.1); }
  .fn-row.weak { border-color: rgba(212,168,67,0.25); background: rgba(212,168,67,0.05); }
  .fn-row.strong { border-color: rgba(139,184,58,0.2); background: rgba(42,61,31,0.2); }
  .fn-row.over { border-color: rgba(184,176,160,0.2); background: rgba(28,24,18,0.4); }
  .fn-name { font-family: 'Space Mono', monospace; font-size: 0.68rem; color: var(--paper); flex: 1; }
  .fn-count { font-family: 'Bebas Neue', sans-serif; font-size: 1rem; line-height: 1; min-width: 1.5rem; text-align: right; }
  .fn-count.zero { color: var(--rust); }
  .fn-count.one { color: var(--straw); }
  .fn-count.good { color: var(--lime); }
  .fn-count.over { color: var(--ash); }
  .fn-badge { font-family: 'Space Mono', monospace; font-size: 0.52rem; letter-spacing: 0.06em; text-transform: uppercase; padding: 0.1rem 0.4rem; border: 1px solid; }
  .fn-badge.missing { color: var(--rust); border-color: rgba(196,85,26,0.4); }
  .fn-badge.weak { color: var(--straw); border-color: rgba(212,168,67,0.4); }
  .fn-badge.balanced { color: var(--lime); border-color: rgba(139,184,58,0.4); }
  .fn-badge.over { color: var(--ash); border-color: rgba(184,176,160,0.3); }
  .fn-bar-wrap { width: 60px; height: 2px; background: rgba(139,184,58,0.1); flex-shrink: 0; }
  .fn-bar { height: 100%; transition: width 0.3s; }
  .actions-list { display: flex; flex-direction: column; gap: 0.4rem; }
  .action-item { font-size: 0.85rem; color: var(--paper); line-height: 1.55; padding: 0.55rem 0.75rem; border-left: 2px solid var(--lime); background: rgba(42,61,31,0.15); }
  .action-item.risk { border-left-color: var(--rust); background: rgba(122,59,30,0.1); color: var(--ash); }
  .action-item.caution { border-left-color: var(--straw); background: rgba(212,168,67,0.06); color: var(--ash); }
  .empty-state { padding: 3rem 0; text-align: center; }"""

if old in text:
    text = text.replace(old, new)
    changes += 1; print("✅ 3: CSS added for function sections")
else: print("❌ 3: CSS anchor not found")

# ── 4. Add analyzeGuildFunctions() and wire it into renderResults() ───────────
# Insert the function definition after scoreGuild() and before renderGuild()
old = "// ── Render ────────────────────────────────────────────────────────────────────"
new = """// ── Function analysis ────────────────────────────────────────────────────────
const CORE_ROLES = [
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
}

// ── Render ────────────────────────────────────────────────────────────────────"""

if old in text:
    text = text.replace(old, new)
    changes += 1; print("✅ 4: analyzeGuildFunctions() added")
else: print("❌ 4: render anchor not found")

# ── 5. Wire function analysis into renderResults() ───────────────────────────
# Insert after diversity warning block (end of renderResults)
old = """  if (divWarning) {
    divWarn.textContent = '⚠️ ' + divWarning;
    divWarn.style.display = 'block';
  } else {
    divWarn.style.display = 'none';
  }
}"""

new = """  if (divWarning) {
    divWarn.textContent = '⚠️ ' + divWarning;
    divWarn.style.display = 'block';
  } else {
    divWarn.style.display = 'none';
  }

  // ── Function analysis ──────────────────────────────────────────────────────
  const fnAnalysis = analyzeGuildFunctions(guild);
  const fnBalance  = document.getElementById('function-balance');
  const actionsList = document.getElementById('actions-list');

  if (fnAnalysis) {
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
  }
}"""

if old in text:
    text = text.replace(old, new)
    changes += 1; print("✅ 5: function analysis wired into renderResults()")
else: print("❌ 5: diversity warning block not found")

# ── 6. Downgrade old generic suggestions to Risks in renderResults ────────────
old = """  // Suggestions + warnings
  const suggEl = document.getElementById('suggestions-list');
  suggEl.innerHTML = '';
  for (const w of r.warnings) {
    const li = document.createElement('div');
    li.className = 'suggestion-item warning';
    li.textContent = '⚠️ ' + w;
    suggEl.appendChild(li);
  }
  for (const s of r.suggestions) {
    const li = document.createElement('div');
    li.className = 'suggestion-item';
    li.textContent = '💡 ' + s;
    suggEl.appendChild(li);
  }"""

new = """  // Risks (formerly suggestions + warnings — now ecological risk signals only)
  const suggEl = document.getElementById('suggestions-list');
  suggEl.innerHTML = '';
  for (const w of r.warnings) {
    const li = document.createElement('div');
    li.className = 'suggestion-item warning';
    li.textContent = '⚠️ ' + w;
    suggEl.appendChild(li);
  }
  // Only show pest/family risk suggestions — functional actions moved to Design Actions
  for (const s of r.suggestions) {
    if (s.includes('Lamiaceae') || s.includes('family') || s.includes('families') || s.includes('balanced')) {
      const li = document.createElement('div');
      li.className = 'suggestion-item';
      li.textContent = '→ ' + s;
      suggEl.appendChild(li);
    }
  }"""

if old in text:
    text = text.replace(old, new)
    changes += 1; print("✅ 6: suggestions section refined to risks only")
else: print("❌ 6: suggestions block not found")

f.write_text(text)
print(f"\n{changes} patches applied")
