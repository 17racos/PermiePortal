from pathlib import Path

file_path = Path("src/pages/guild-checker.astro")
text = file_path.read_text()

old = "if (!improves) continue;"
new = "if (!improves) score -= 2.0;"

if old not in text:
    print("❌ Target line not found. No changes made.")
else:
    text = text.replace(old, new)
    file_path.write_text(text)
    print("✅ Replaced hard gate with weighted penalty.")

print("\nVerify with:")
print("grep -n \"improves\" src/pages/guild-checker.astro")