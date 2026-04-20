#!/usr/bin/env python3
"""
patch_guild_builder.py
======================
Evolves /guild-checker into Guild Builder:
1. Renames copy (title, eyebrow, nav, empty state, labels)
2. Adds Family Diversity section (wires analyzeDiversity logic in client JS)
3. Reframes score display as "Guild Health"
4. Improves empty state for 0 and 1 plant states
5. Adds diversity CSS

Minimal patch — no logic rewrite, no new files.
"""
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

# ── 1. Meta title + description ───────────────────────────────────────────────
old = ('  title="Guild Checker — Design Resilient Plant Guilds | PermiePortal"\n'
       '  description="Add plants to your guild and instantly see pest overlap, family diversity, and ecological risk score based on 1,043 plants and 9,779 relationships."')
new = ('  title="Guild Builder — Design Resilient Plant Guilds | PermiePortal"\n'
       '  description="Build a resilient plant guild with live ecological feedback — pest overlap, family diversity, and risk scored from 1,043 plants and 9,779 relationships."')
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 1: meta updated")
else: print("❌ 1: meta not found")

# ── 2. Nav link label ─────────────────────────────────────────────────────────
old = '    <li><a href="/guild-checker" class="active">Guild Checker</a></li>'
new = '    <li><a href="/guild-checker" class="active">Guild Builder</a></li>'
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 2: nav label updated")
else: print("❌ 2: nav label not found")

# ── 3. Page header copy ───────────────────────────────────────────────────────
old = ('  <p class="page-eyebrow">Ecological Design Tool</p>\n'
       '  <h1 class="page-title">Guild Checker</h1>\n'
       '  <p class="page-desc">\n'
       '    Add plants to see pest overlap, family diversity, and ecological risk — scored from 1,043 plants and 9,779 relationships.\n'
       '  </p>')
new = ('  <p class="page-eyebrow">Ecological Design Tool</p>\n'
       '  <h1 class="page-title">Guild Builder</h1>\n'
       '  <p class="page-desc">\n'
       '    Add plants and watch live ecological feedback update as you build — family diversity, pest overlap, and resilience scored from 1,043 plants and 9,779 relationships.\n'
       '  </p>')
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 3: header copy updated")
else: print("❌ 3: header copy not found")

# ── 4. Left panel search label ────────────────────────────────────────────────
old = '    <p class="panel-label">Search Plants</p>'
new = '    <p class="panel-label">Add Plants to Your Guild</p>'
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 4: search label updated")
else: print("❌ 4: search label not found")

# ── 5. Search placeholder ────────────────────────────────────────────────────
old = '        placeholder="Type a plant name..."'
new = '        placeholder="Search by common name..."'
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 5: placeholder updated")
else: print("❌ 5: placeholder not found")

# ── 6. Empty guild slot text ──────────────────────────────────────────────────
old = '      <div class="guild-empty" id="guild-empty">Add plants above to start building your guild</div>'
new = '      <div class="guild-empty" id="guild-empty">Search for plants above — your guild starts here</div>'
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 6: empty guild text updated")
else: print("❌ 6: empty guild text not found")

# ── 7. Score panel label ──────────────────────────────────────────────────────
old = '        <p class="panel-label">Risk Score</p>'
new = '        <p class="panel-label">Guild Health</p>'
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 7: score label updated")
else: print("❌ 7: score label not found")

# ── 8. Analysis section title ─────────────────────────────────────────────────
old = '        <p class="result-section-title">Analysis</p>'
new = '        <p class="result-section-title">Design Feedback</p>'
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 8: analysis title updated")
else: print("❌ 8: analysis title not found")

# ── 9. Families section title ────────────────────────────────────────────────
old = '        <p class="result-section-title">Families in Guild</p>'
new = '        <p class="result-section-title">Family Composition</p>'
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 9: families title updated")
else: print("❌ 9: families title not found")

# ── 10. Add Family Diversity section to HTML (after families section) ─────────
old = ('      <div class="result-section" id="section-families">\n'
       '        <p class="result-section-title">Family Composition</p>\n'
       '        <div class="family-list" id="families-list"></div>\n'
       '      </div>\n'
       '    </div>\n'
       '  </div>\n'
       '</div>')
new = ('      <div class="result-section" id="section-families">\n'
       '        <p class="result-section-title">Family Composition</p>\n'
       '        <div class="family-list" id="families-list"></div>\n'
       '      </div>\n'
       '      <div class="result-section" id="section-diversity">\n'
       '        <p class="result-section-title">Family Diversity</p>\n'
       '        <div class="diversity-grid" id="diversity-grid"></div>\n'
       '        <div id="diversity-warning" class="diversity-warning" style="display:none"></div>\n'
       '      </div>\n'
       '    </div>\n'
       '  </div>\n'
       '</div>')
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 10: Family Diversity section added to HTML")
else: print("❌ 10: families section anchor not found")

# ── 11. Add CSS for diversity section ────────────────────────────────────────
old = '  .empty-state { padding: 3rem 0; text-align: center; }'
new = ('  .diversity-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.6rem; margin-bottom: 0.75rem; }\n'
       '  .diversity-stat { background: var(--bark); border: 1px solid rgba(139,184,58,0.12); padding: 0.7rem 0.9rem; }\n'
       '  .diversity-stat-value { font-family: \'Bebas Neue\', sans-serif; font-size: 1.4rem; color: var(--lime); line-height: 1; }\n'
       '  .diversity-stat-key { font-family: \'Space Mono\', monospace; font-size: 0.56rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ash); margin-top: 0.2rem; }\n'
       '  .diversity-warning { font-size: 0.82rem; color: var(--straw); line-height: 1.55; padding: 0.5rem 0.75rem; border-left: 2px solid var(--straw); background: rgba(212,168,67,0.06); }\n'
       '  .empty-state { padding: 3rem 0; text-align: center; }')
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 11: diversity CSS added")
else: print("❌ 11: empty-state CSS anchor not found")

# ── 12. Update JS empty state rendering to handle 0 vs 1 plant ───────────────
old = ("  if (guild.length < 2) {\n"
       "    emptyState.style.display = 'block';\n"
       "    results.style.display    = 'none';\n"
       "    return;\n"
       "  }")
new = ("  if (guild.length < 2) {\n"
       "    emptyState.style.display = 'block';\n"
       "    results.style.display    = 'none';\n"
       "    // Update empty state message based on guild size\n"
       "    const emptyText = emptyState.querySelector('.empty-state-text');\n"
       "    if (emptyText) {\n"
       "      if (guild.length === 0) {\n"
       "        emptyText.innerHTML = 'Start building — search for a plant above<br>and add it to your guild';\n"
       "      } else {\n"
       "        emptyText.innerHTML = 'Add at least one more plant<br>to see live ecological feedback';\n"
       "      }\n"
       "    }\n"
       "    return;\n"
       "  }")
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 12: empty state JS updated for 0/1 plant states")
else: print("❌ 12: empty state JS anchor not found")

# ── 13. Wire analyzeDiversity in JS renderResults() ──────────────────────────
# Insert after the families rendering block
old = ("  // Families\n"
       "  const famEl = document.getElementById('families-list');\n"
       "  famEl.innerHTML = '';\n"
       "  for (const f of r.dominantFamilies) {\n"
       "    const tag = document.createElement('span');\n"
       "    tag.className = 'family-tag';\n"
       "    tag.textContent = f;\n"
       "    famEl.appendChild(tag);\n"
       "  }\n"
       "}")
new = ("  // Families\n"
       "  const famEl = document.getElementById('families-list');\n"
       "  famEl.innerHTML = '';\n"
       "  for (const f of r.dominantFamilies) {\n"
       "    const tag = document.createElement('span');\n"
       "    tag.className = 'family-tag';\n"
       "    tag.textContent = f;\n"
       "    famEl.appendChild(tag);\n"
       "  }\n"
       "\n"
       "  // Family Diversity (analyzeDiversity logic inlined — same data source)\n"
       "  const divGrid = document.getElementById('diversity-grid');\n"
       "  const divWarn = document.getElementById('diversity-warning');\n"
       "  const n = guild.length;\n"
       "  const divFamilies = guild.filter(s => plantToFamily[s]).map(s => plantToFamily[s]);\n"
       "  const divCounts = {};\n"
       "  for (const f of divFamilies) divCounts[f] = (divCounts[f] || 0) + 1;\n"
       "  const uniqueFams = Object.keys(divCounts).length;\n"
       "  const divScore = Math.round((Math.min(1, uniqueFams / n)) * 100);\n"
       "  const domFamEntry = Object.entries(divCounts).sort((a,b) => b[1]-a[1])[0];\n"
       "  const domFam = domFamEntry?.[0] || '—';\n"
       "  const domCount = domFamEntry?.[1] || 0;\n"
       "  const domRatio = domCount / n;\n"
       "  divGrid.innerHTML = `\n"
       "    <div class='diversity-stat'><div class='diversity-stat-value'>${uniqueFams}</div><div class='diversity-stat-key'>Unique Families</div></div>\n"
       "    <div class='diversity-stat'><div class='diversity-stat-value'>${divScore}%</div><div class='diversity-stat-key'>Diversity Score</div></div>\n"
       "    <div class='diversity-stat'><div class='diversity-stat-value'>${n}</div><div class='diversity-stat-key'>Total Plants</div></div>\n"
       "    <div class='diversity-stat'><div class='diversity-stat-value' style='font-size:0.95rem;padding-top:0.2rem'>${domFam}</div><div class='diversity-stat-key'>Dominant Family</div></div>\n"
       "  `;\n"
       "  // Warning\n"
       "  let divWarning = null;\n"
       "  if (domRatio > 0.5) {\n"
       "    divWarning = `${domFam} is ${Math.round(domRatio*100)}% of your guild — consider adding plants from other families.`;\n"
       "  } else if (uniqueFams < 3) {\n"
       "    divWarning = `Only ${uniqueFams} ${uniqueFams === 1 ? 'family' : 'families'} — aim for 3 or more for ecological resilience.`;\n"
       "  }\n"
       "  if (divWarning) {\n"
       "    divWarn.textContent = '⚠️ ' + divWarning;\n"
       "    divWarn.style.display = 'block';\n"
       "  } else {\n"
       "    divWarn.style.display = 'none';\n"
       "  }\n"
       "}")
if old in text:
    text = text.replace(old, new); changes += 1; print("✅ 13: analyzeDiversity wired in JS")
else: print("❌ 13: families JS block not found")

f.write_text(text)
print(f"\n{changes} patches applied")
