# Pest Organic Controls Rewrite

Rewrite the `control_methods` section for every pest YAML file in `src/seeds/pests/`.
Skip: pests-data.yml and pests-data.yml.bak

## The Problem With Current Controls

Current controls read like a generic checklist. They tell users WHAT to do but not:
- WHEN to do it (timing in the pest lifecycle)
- HOW to actually do it (real instructions, not "apply neem oil")
- WHAT to try first vs last resort
- WHAT NOT to do (common mistakes that backfire)
- WHY it works (so users understand, not just follow instructions)

## Voice

Same as descriptions — write for a curious 10-year-old AND a frustrated first-time gardener.
Plain language. Real instructions. No filler. Honest about what works and what does not.

## Gold Standard Example — Aphids

Read src/seeds/pests/aphids-data.yml for the complete example of what ALL controls should look like.

Key elements that make it work:
- biological_controls: Tells user to WAIT before acting. Explains WHY not to buy ladybugs.
  Gives specific plants to grow to attract beneficials.
- preventive_methods: Explains the actual mechanism (nitrogen = soft growth = aphid food).
  Makes the lifecycle concrete (born pregnant, thousands in a week).
- cultural_practices: Specific companion plants with WHY they work. Trap crop concept explained.
  Lifecycle timing so user knows when to check.
- mechanical_physical: Honest about limitations. Tells user when to escalate and why.
- organic_sprays: Gives the actual DIY recipe. Names real products. Explains contact vs systemic.
  Tells user WHEN to spray (dusk) and WHY. Warns about harming beneficials.

## Rules For Every Pest

biological_controls:
- Name specific predators and how to ATTRACT them, not just "introduce them"
- Warn against buying beneficial insects commercially if that applies
- Give specific plants to grow nearby to support beneficials
- Tell user when to wait vs when to act

preventive_methods:
- Explain the underlying mechanism — WHY does this pest thrive?
- Make it actionable: what specific conditions favor this pest?
- Give early warning signs before infestation gets bad
- No "balanced watering and fertilization" without explaining what that means

cultural_practices:
- Specific companion plant names with functional reason
- Lifecycle information — how fast does this pest reproduce? What interrupts it?
- Rotation or spacing advice where relevant

mechanical_physical:
- Real instructions, not "hand pick"
- Honest about when it works and when it does not
- When to escalate beyond mechanical methods

organic_sprays:
- DIY recipes where possible (insecticidal soap = castile soap + water)
- Specific timing (when to apply relative to pest lifecycle and beneficial activity)
- Contact vs systemic distinction where relevant
- What NOT to spray near (flowers, beneficial habitat)
- Realistic expectations — what will this actually achieve?

## Format

Keep valid YAML. Use >- block scalar for multi-sentence fields.
Keep all other fields exactly as they are.
Only rewrite the 5 control_methods sub-fields.

## Process

Work alphabetically through all pest files.
After every 25 files run: python3 validate.py --summary
Fix any YAML errors before continuing.

When ALL files are done:
  ./sync.sh
  git add -A
  git commit -m "Rewrite pest controls — actionable, accessible, lifecycle-aware"
