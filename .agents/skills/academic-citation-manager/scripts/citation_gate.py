#!/usr/bin/env python3
"""
Citation↔Bibliography Gate: deterministic cross-validation.
Checks that every \cite{key} in draft exists in .bib and vice-versa.
Usage: python citation_gate.py <draft_dir> <bib_file>
"""
import re
import sys
from pathlib import Path


def extract_cite_keys_from_drafts(draft_dir: Path) -> dict[str, list[tuple[str, int]]]:
    """Extract all citation keys from draft markdown files.
    Returns: {key: [(filename, line_number), ...]}
    """
    keys: dict[str, list[tuple[str, int]]] = {}

    for md_file in sorted(draft_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), 1):
            # Match \cite{key} or \cite{key1, key2}
            for match in re.finditer(r"\\cite\{([^}]+)\}", line):
                raw_keys = match.group(1)
                for k in raw_keys.split(","):
                    k = k.strip()
                    if k:
                        keys.setdefault(k, []).append((md_file.name, line_num))

            # Match (Author, Year) style — basic pattern
            for match in re.finditer(r"\[([A-Z][a-zA-Z]+\d{4}[a-z]?)\]", line):
                k = match.group(1)
                keys.setdefault(k, []).append((md_file.name, line_num))

    return keys


def extract_bib_keys(bib_path: Path) -> set[str]:
    """Extract all entry keys from BibTeX file."""
    content = bib_path.read_text(encoding="utf-8")
    keys = set()
    for match in re.finditer(r"@\w+\s*\{([^,]+),", content):
        keys.add(match.group(1).strip())
    return keys


def run_gate(draft_dir: Path, bib_path: Path) -> dict:
    """Run the Citation↔Bibliography gate."""
    cite_keys = extract_cite_keys_from_drafts(draft_dir)
    bib_keys = extract_bib_keys(bib_path)

    draft_key_set = set(cite_keys.keys())

    # RULE 1: Every cite key must exist in .bib
    orphan_citations = draft_key_set - bib_keys

    # RULE 2: Every .bib key must be cited at least once
    phantom_citations = bib_keys - draft_key_set

    return {
        "draft_keys": len(draft_key_set),
        "bib_keys": len(bib_keys),
        "orphan_citations": sorted(orphan_citations),
        "phantom_citations": sorted(phantom_citations),
        "cite_locations": cite_keys,
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python citation_gate.py <draft_dir> <bib_file>")
        sys.exit(1)

    draft_dir = Path(sys.argv[1])
    bib_path = Path(sys.argv[2])

    if not draft_dir.is_dir():
        print(f"ERROR: Draft directory not found: {draft_dir}")
        sys.exit(1)
    if not bib_path.exists():
        print(f"ERROR: BibTeX file not found: {bib_path}")
        sys.exit(1)

    result = run_gate(draft_dir, bib_path)
    total_violations = len(result["orphan_citations"]) + len(result["phantom_citations"])

    print(f"\n{'='*60}")
    print(f"Citation↔Bibliography Gate")
    print(f"{'='*60}")
    print(f"Citations in draft: {result['draft_keys']} unique keys")
    print(f"Entries in .bib:    {result['bib_keys']} entries")

    if result["orphan_citations"]:
        print(f"\n⚠️  RULE 1 VIOLATIONS — Orphan citations (in text, not in .bib):")
        for key in result["orphan_citations"]:
            locations = result["cite_locations"].get(key, [])
            loc_str = ", ".join(f"{f}:{l}" for f, l in locations[:3])
            print(f"    ❌ {key} — found at: {loc_str}")

    if result["phantom_citations"]:
        print(f"\n⚠️  RULE 2 VIOLATIONS — Phantom citations (in .bib, not in text):")
        for key in result["phantom_citations"]:
            print(f"    ❌ {key}")

    print(f"\n{'─'*60}")
    if total_violations == 0:
        print(f"Result: ✅ GATE PASS — 0 violations")
    else:
        print(f"Result: ❌ GATE FAIL — {total_violations} violations")
        print(f"   Orphan citations: {len(result['orphan_citations'])}")
        print(f"   Phantom citations: {len(result['phantom_citations'])}")
        print(f"\n⛔ BLOQUEANTE: Pipeline cannot advance until all violations are resolved.")

    sys.exit(1 if total_violations else 0)


if __name__ == "__main__":
    main()
