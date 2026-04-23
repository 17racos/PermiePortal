#!/usr/bin/env python3
"""
patch_slug_astro.py
===================
Patches src/pages/plants/[slug].astro to render:
  - companions_unresolved → "Also mentioned" plain text list (max 5)
  - companion_categories  → "Ecological Context" filtered to type:system (max 4)

Run from project root:
  python3 patch_slug_astro.py
  python3 patch_slug_astro.py --check   # verify patch applied
"""

import argparse
from pathlib import Path

TEMPLATE = Path("src/pages/plants/[slug].astro")

# ── PATCH 1: Frontmatter additions ────────────────────────────────────────────

OLD_FRONTMATTER = "const companions = plant.companions || [];"

NEW_FRONTMATTER = """const companions = plant.companions || [];

// Unresolved companions — valid plant references not yet in database
const companionsUnresolved = (plant.companions_unresolved || [])
  .filter((c: any) => {
    const name = typeof c === 'string' ? c : c?.name || '';
    return name && name !== 'NEEDS_DATA';
  })
  .slice(0, 5);

// Companion categories — ecological context entries, system type only
const companionCategories = (plant.companion_categories || [])
  .filter((c: any) => c?.type === 'system' && c?.name)
  .slice(0, 4);"""


# ── PATCH 2: CSS additions ─────────────────────────────────────────────────────

OLD_CSS = """  /* COMPANIONS */
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
  .companion-list { list-style: none; display: flex; flex-direction: column; gap: 0.4rem; }
  .companion-list li { font-family: 'Space Mono', monospace; font-size: 0.78rem; padding: 0.4rem 0.75rem; background: rgba(42,61,31,0.4); border-left: 2px solid var(--leaf); color: var(--paper); }
  .cautions-list li { background: rgba(122,59,30,0.2); border-left-color: var(--rust); }"""

NEW_CSS = """  /* COMPANIONS */
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
  .companion-list { list-style: none; display: flex; flex-direction: column; gap: 0.4rem; }
  .companion-list li { font-family: 'Space Mono', monospace; font-size: 0.78rem; padding: 0.4rem 0.75rem; background: rgba(42,61,31,0.4); border-left: 2px solid var(--leaf); color: var(--paper); }
  .cautions-list li { background: rgba(122,59,30,0.2); border-left-color: var(--rust); }
  .unresolved-companions { margin-top: 1.25rem; }
  .unresolved-label { font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ash); opacity: 0.7; margin-bottom: 0.4rem; }
  .unresolved-list li { background: rgba(28,24,18,0.5); border-left-color: rgba(184,176,160,0.3); color: var(--ash); font-style: italic; }
  .unresolved-note { font-family: 'Space Mono', monospace; font-size: 0.55rem; letter-spacing: 0.08em; color: var(--ash); opacity: 0.45; margin-top: 0.4rem; }
  .ecological-context { margin-top: 1.5rem; }
  .context-list li { background: rgba(28,24,18,0.4); border-left-color: rgba(143,184,58,0.25); color: var(--ash); font-size: 0.73rem; }"""


# ── PATCH 3: Companion section HTML ───────────────────────────────────────────

OLD_COMPANION_SECTION = """  <!-- COMPANION PLANTING -->
  {(companions.length > 0 || cautions.length > 0) && (
    <div class="section">
      <p class="section-label">Companion Planting</p>
      <div class="two-col">
        <div>
          <div class="section-title">Good Neighbors</div>
          {companions.length > 0 ? (
            <ul class="companion-list">
              {companions.map((c: any) => <li>{typeof c === "string" ? c : <a href={`/plants/${c.slug}`}>{c.name}</a>}</li>)}
            </ul>
          ) : (
            <p class="empty-state">No companion data yet.</p>
          )}
        </div>
        {cautions.length > 0 && (
          <div>
            <div class="section-title">Cautions</div>
            <ul class="companion-list cautions-list">
              {cautions.map((a: string) => <li>{a}</li>)}
            </ul>
          </div>
        )}
      </div>
    </div>
  )}"""

NEW_COMPANION_SECTION = """  <!-- COMPANION PLANTING -->
  {(companions.length > 0 || cautions.length > 0 || companionsUnresolved.length > 0 || companionCategories.length > 0) && (
    <div class="section">
      <p class="section-label">Companion Planting</p>
      <div class="two-col">
        <div>
          <div class="section-title">Good Neighbors</div>
          {companions.length > 0 ? (
            <ul class="companion-list">
              {companions.map((c: any) => <li>{typeof c === "string" ? c : <a href={`/plants/${c.slug}`}>{c.name}</a>}</li>)}
            </ul>
          ) : (
            <p class="empty-state">No companion data yet.</p>
          )}

          {companionsUnresolved.length > 0 && (
            <div class="unresolved-companions">
              <p class="unresolved-label">Also mentioned as companions:</p>
              <ul class="companion-list unresolved-list">
                {companionsUnresolved.map((c: any) => (
                  <li>{typeof c === 'string' ? c : c.name}</li>
                ))}
              </ul>
              <p class="unresolved-note">Not yet profiled in PermiePortal</p>
            </div>
          )}
        </div>

        <div>
          {cautions.length > 0 && (
            <div>
              <div class="section-title">Cautions</div>
              <ul class="companion-list cautions-list">
                {cautions.map((a: string) => <li>{a}</li>)}
              </ul>
            </div>
          )}

          {companionCategories.length > 0 && (
            <div class="ecological-context">
              <div class="section-title">Ecological Context</div>
              <ul class="companion-list context-list">
                {companionCategories.map((c: any) => (
                  <li>{c.name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  )}"""


def check(text):
    """Check which patches are already applied."""
    results = {
        'frontmatter': NEW_FRONTMATTER.split('\n')[2] in text,
        'css':         'unresolved-companions' in text,
        'html':        'companionsUnresolved.length > 0' in text,
    }
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true',
                        help='Check patch status without modifying')
    args = parser.parse_args()

    if not TEMPLATE.exists():
        print(f"❌ Template not found: {TEMPLATE}")
        return

    text = TEMPLATE.read_text(encoding='utf-8')
    status = check(text)

    if args.check:
        print(f"Patch status for {TEMPLATE}:")
        for k, v in status.items():
            print(f"  {'✅' if v else '❌'} {k}")
        return

    changes = 0

    # Patch 1: Frontmatter
    if not status['frontmatter']:
        if OLD_FRONTMATTER in text:
            text = text.replace(OLD_FRONTMATTER, NEW_FRONTMATTER)
            changes += 1
            print("✅ Patch 1: frontmatter additions applied")
        else:
            print("❌ Patch 1: frontmatter anchor not found")
    else:
        print("⏭️  Patch 1: frontmatter already applied")

    # Patch 2: CSS
    if not status['css']:
        if OLD_CSS in text:
            text = text.replace(OLD_CSS, NEW_CSS)
            changes += 1
            print("✅ Patch 2: CSS additions applied")
        else:
            print("❌ Patch 2: CSS anchor not found")
    else:
        print("⏭️  Patch 2: CSS already applied")

    # Patch 3: HTML
    if not status['html']:
        if OLD_COMPANION_SECTION in text:
            text = text.replace(OLD_COMPANION_SECTION, NEW_COMPANION_SECTION)
            changes += 1
            print("✅ Patch 3: companion HTML section updated")
        else:
            print("❌ Patch 3: companion HTML anchor not found")
            # Show context to help diagnose
            idx = text.find('COMPANION PLANTING')
            if idx > 0:
                print(f"   Found 'COMPANION PLANTING' at char {idx}")
                print(f"   Context: {repr(text[idx:idx+100])}")
    else:
        print("⏭️  Patch 3: HTML already applied")

    if changes > 0:
        TEMPLATE.write_text(text, encoding='utf-8')
        print(f"\n✅ {changes} patch(es) applied to {TEMPLATE}")
        print("   Run: npm run dev — check /plants/moringa or /plants/banana")
    else:
        print("\n  No changes made")


if __name__ == '__main__':
    main()
