#!/usr/bin/env python3
"""Obsolete one-off: patched old automate.py prompt strings. Pipeline refactor removed that text."""
from pathlib import Path

f = Path("automate.py")
text = f.read_text()
changes = 0

# Fix 1: Replace conflicting generic rule with tighter actionable rule
old1 = ('"- CRITICAL: Generic names (Corn, Beans, Citrus, Oak, Grasses) MUST go here\\n",\n'
        '            "- NEVER force a generic into a specific species slug\\n",\n'
        '            "- NEVER drop valid ecological references — preserve ambiguity\\n\\n",\n')

new1 = ('"- CRITICAL: Only use generic names that are actionable and meaningful to a grower\\n",\n'
        '            "  Valid: Corn, Oak, Sunflower, Clover (clear, useful to planting decisions)\\n",\n'
        '            "  Avoid: Beans, Grasses, Vegetables (too broad to guide decisions)\\n",\n'
        '            "  If a term is too broad: exclude OR move to companion_categories\\n",\n'
        '            "  if it represents a system (e.g. Nitrogen-fixing annuals)\\n",\n'
        '            "- NEVER force a generic into a specific species slug\\n\\n",\n')

if old1 in text:
    text = text.replace(old1, new1)
    changes += 1
    print("Fix 1: tightened generic rule")
else:
    print("Fix 1 NOT FOUND")
    idx = text.find("NEVER force a generic")
    if idx > 0:
        print(repr(text[idx-200:idx+50]))

# Fix 2: Add max 5 cap on companions_unresolved
old2 = ('"- This prevents silent duplication across the system\\n\\n",\n'
        '            "Field 3')

new2 = ('"- This prevents silent duplication across the system\\n",\n'
        '            "LIMIT: Maximum 5 companions_unresolved entries\\n",\n'
        '            "- Prioritize most relevant and actionable plant references first\\n\\n",\n'
        '            "Field 3')

if old2 in text:
    text = text.replace(old2, new2)
    changes += 1
    print("Fix 2: max 5 cap on companions_unresolved")
else:
    print("Fix 2 NOT FOUND")
    idx = text.find("silent duplication")
    if idx > 0:
        print(repr(text[idx-10:idx+100]))

# Fix 3: Add ordering rule
old3 = ('"Minimum: 3 total references across all three fields\\n",\n'
        '            "At least 1 must be a resolved slug when possible\\n",\n'
        '            "DO NOT modify aka fields')

new3 = ('"Minimum: 3 total references across all three fields\\n",\n'
        '            "At least 1 must be a resolved slug when possible\\n",\n'
        '            "ORDERING PRIORITY (applies to all three companion fields):\\n",\n'
        '            "- Most beneficial or strongest relationships first\\n",\n'
        '            "- Most commonly used or recognizable plants first\\n",\n'
        '            "- Lists are sliced for display so ordering is intentional\\n",\n'
        '            "DO NOT modify aka fields')

if old3 in text:
    text = text.replace(old3, new3)
    changes += 1
    print("Fix 3: ordering priority rule added")
else:
    print("Fix 3 NOT FOUND")
    idx = text.find("Minimum: 3 total references")
    if idx > 0:
        print(repr(text[idx-10:idx+200]))

if changes:
    f.write_text(text)
    print(f"\n{changes} fixes applied")
else:
    print("\nNo changes made")
