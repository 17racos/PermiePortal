# Pest Description & Characteristics Rewrite

Rewrite the `description` and `characteristics` fields for every pest YAML file in `src/seeds/pests/` (skip `pests-data.yml` and `pests-data.yml.bak`).

## Voice and Tone

Write for TWO readers simultaneously:
1. A curious 10-year-old who found something weird on their plant
2. A frustrated first-time gardener who needs to know what this is RIGHT NOW

Rules:
- Lead with what the grower will actually SEE or NOTICE first — the damage, the bug, the symptom
- No Latin unless it adds real value (scientific name is already in a separate field)
- No "photosynthetic capacity", "voraciously", "defoliation" without plain explanation
- Short sentences. Active voice. Urgency where the pest is serious.
- If it looks like something specific — say so. "Looks like a tiny lobster" beats "elongate with forceps-like cerci"
- Diseases get the same treatment — what does the plant look like when infected? How fast does it spread?

## Target Voice Examples

CURRENT (bad):
  description: Tomato hornworms are large, green caterpillars that feed voraciously on tomato plants. They are easily recognized by their prominent horn-like projection on the rear and their rapid defoliation of leaves.
  characteristics: These caterpillars can reach up to 4 inches in length and display a bright green body with distinct white stripes. Their heavy feeding can quickly strip plants of foliage, reducing photosynthetic capacity and fruit yield.

TARGET (good):
  description: If your tomato plant looks like something took scissors to it overnight, check the stems carefully. Tomato hornworms are huge — up to 4 inches long — and so perfectly green they disappear against leaves. One hornworm can strip a plant in days. The horn on their tail looks scary but does nothing. The real damage is the feeding.
  characteristics: Look for bright green caterpillars with white diagonal stripes and a curved horn at the back end. Check stem junctions and the undersides of branches — they hold still and rely on camouflage. Dark green or black droppings on leaves below mean one is feeding above you. Eggs are small, round, and pale green on leaf undersides.

CURRENT (bad):
  description: Aphids are small, soft-bodied insects that come in various colors such as green, black, yellow, or pink.
  characteristics: Aphids have pear-shaped bodies and are often less than 1/8 inch long. They possess long, slender mouthparts.

TARGET (good):
  description: Aphids are the most common pest in any garden — tiny, soft, and almost always clustered in groups on new growth, flower buds, or stem tips. They suck sap and leave behind sticky honeydew that turns black with sooty mold. A small colony explodes into thousands in a week. The good news: they have more natural enemies than almost any other pest.
  characteristics: Look for clusters of tiny pear-shaped insects — green, black, yellow, pink, or white depending on species — on the newest, softest growth. They barely move when disturbed. Check the undersides of curling or yellowing leaves. Ants farming them is a dead giveaway — ants protect aphid colonies from predators in exchange for the honeydew they produce.

## Format Rules

- description: 3-5 sentences. What the grower notices first, what damage looks like, urgency level.
- characteristics: 3-5 sentences. How to find and identify it in the field. Specific visual cues.
- Keep ALL other fields exactly as they are — only rewrite description and characteristics
- Maintain valid YAML formatting
- Do not add or remove any fields

## Process

Work through ALL pest files in src/seeds/pests/ alphabetically.
Skip: pests-data.yml and pests-data.yml.bak

For each file:
1. Read the current description and characteristics
2. Rewrite both in the target voice
3. Save the file
4. Move to the next

After every 25 files run:
  python3 validate.py --summary

When ALL files are done:
  ./sync.sh
  git add -A
  git commit -m "Rewrite pest descriptions — accessible voice for all ages"
