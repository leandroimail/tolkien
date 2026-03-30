#!/usr/bin/env python3
"""
Check BibTeX file for duplicate entries by DOI or title similarity.
Usage: python check_bib_duplicates.py research/references.bib
"""
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher


def parse_bibtex(content: str) -> list[dict]:
    """Parse BibTeX content into list of entry dicts."""
    entries = []
    pattern = re.compile(r"@(\w+)\s*\{([^,]+),\s*(.*?)\n\}", re.DOTALL)
    for match in pattern.finditer(content):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)
        fields = {}
        field_pattern = re.compile(r"(\w+)\s*=\s*[{\"](.*?)[}\"]", re.DOTALL)
        for fm in field_pattern.finditer(body):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        entries.append({"type": entry_type, "key": key, "fields": fields})
    return entries


def normalize_title(title: str) -> str:
    """Normalize title for comparison."""
    title = title.lower()
    title = re.sub(r"[{}\\]", "", title)
    title = re.sub(r"[^a-z0-9\s]", "", title)
    return " ".join(title.split())


def find_duplicates(entries: list[dict]) -> list[tuple]:
    """Find duplicate entries by DOI or title similarity."""
    duplicates = []

    # Check DOI duplicates
    doi_map: dict[str, list[str]] = {}
    for entry in entries:
        doi = entry["fields"].get("doi", "").strip().lower()
        if doi:
            doi_map.setdefault(doi, []).append(entry["key"])

    for doi, keys in doi_map.items():
        if len(keys) > 1:
            duplicates.append(("DOI", doi, keys))

    # Check title similarity
    for i, e1 in enumerate(entries):
        t1 = normalize_title(e1["fields"].get("title", ""))
        if not t1:
            continue
        for e2 in entries[i + 1:]:
            t2 = normalize_title(e2["fields"].get("title", ""))
            if not t2:
                continue
            ratio = SequenceMatcher(None, t1, t2).ratio()
            if ratio >= 0.90:
                duplicates.append((
                    f"Title similarity ({ratio:.0%})",
                    f"'{e1['fields'].get('title', '')[:60]}...'",
                    [e1["key"], e2["key"]],
                ))

    return duplicates


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_bib_duplicates.py <bib_file>")
        sys.exit(1)

    bib_path = Path(sys.argv[1])
    if not bib_path.exists():
        print(f"ERROR: File not found: {bib_path}")
        sys.exit(1)

    content = bib_path.read_text(encoding="utf-8")
    entries = parse_bibtex(content)
    duplicates = find_duplicates(entries)

    print(f"\n{'='*60}")
    print(f"Duplicate Check: {bib_path.name}")
    print(f"{'='*60}")
    print(f"Total entries: {len(entries)}")
    print(f"Duplicates found: {len(duplicates)}")

    if duplicates:
        print(f"\n{'─'*60}")
        for dup_type, value, keys in duplicates:
            print(f"  ⚠️  {dup_type}: {value}")
            print(f"      Keys: {', '.join(keys)}")
        print(f"{'─'*60}")
        print(f"\nResult: ❌ FAIL — {len(duplicates)} duplicate groups found")
    else:
        print(f"\nResult: ✅ PASS — no duplicates found")

    sys.exit(1 if duplicates else 0)


if __name__ == "__main__":
    main()
