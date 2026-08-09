"""Diff ways static assets against the lines template to find stock leftovers."""

import filecmp
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # web-sdk
WAYS = ROOT / "apps" / "ways" / "static" / "assets"
LINES = ROOT / "apps" / "lines" / "static" / "assets"

identical, different, ways_only = [], [], []
for path in sorted(WAYS.rglob("*")):
    if not path.is_file():
        continue
    rel = path.relative_to(WAYS)
    other = LINES / rel
    if "backup" in str(rel).lower():
        continue
    if not other.exists():
        ways_only.append(str(rel))
    elif filecmp.cmp(path, other, shallow=False):
        identical.append(str(rel))
    else:
        different.append(str(rel))

print("== IDENTICAL to template (stock leftovers) ==")
for p in identical:
    print("  ", p)
print(f"\n== DIFFERENT from template ({len(different)}) ==")
for p in different:
    print("  ", p)
print(f"\n== WAYS-ONLY (new for this game) ({len(ways_only)}) ==")
for p in ways_only:
    print("  ", p)
