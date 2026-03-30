#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Validate BibTeX entries for required fields and duplicates.

Usage:
    uv run python -B scripts/validate_bib_entries.py <path-to-references.bib>

Exit codes:
    0 = all entries valid
    1 = validation errors found
    2 = file not found or parse error
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

# Required fields per BibTeX entry type
REQUIRED_FIELDS = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "book": ["title", "year"],  # author OR editor
    "incollection": ["author", "title", "booktitle", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "misc": ["author", "title", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "inbook": ["title", "year"],
}


def parse_bib(text: str) -> list[dict]:
    """Parse BibTeX text into list of entries."""
    entries = []
    # Match @type{key, ... }
    pattern = r"@(\w+)\s*\{([^,]+),\s*(.*?)\n\}"
    for match in re.finditer(pattern, text, re.DOTALL):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)

        fields = {}
        # Match field = {value} or field = "value"
        field_pattern = r"(\w+)\s*=\s*[{\"](.+?)[}\"]"
        for fm in re.finditer(field_pattern, body, re.DOTALL):
            field_name = fm.group(1).lower().strip()
            field_value = fm.group(2).strip()
            fields[field_name] = field_value

        entries.append(
            {"type": entry_type, "key": key, "fields": fields}
        )
    return entries


def validate(bib_path: str) -> dict:
    """Validate a BibTeX file."""
    path = Path(bib_path)
    if not path.exists():
        return {"status": "ERROR", "message": f"File not found: {bib_path}"}

    text = path.read_text(encoding="utf-8")
    entries = parse_bib(text)

    if not entries:
        return {
            "status": "ERROR",
            "message": "No BibTeX entries found in file",
        }

    errors = []
    warnings = []

    # Check required fields per entry
    for entry in entries:
        etype = entry["type"]
        key = entry["key"]
        fields = entry["fields"]

        required = REQUIRED_FIELDS.get(etype, ["author", "title", "year"])

        for field in required:
            if field == "title" and etype == "book":
                # book needs author OR editor
                if "author" not in fields and "editor" not in fields:
                    errors.append(f"[{key}] @{etype}: missing 'author' or 'editor'")
            elif field not in fields or not fields[field]:
                errors.append(f"[{key}] @{etype}: missing required field '{field}'")

        # Warn if DOI is missing (not required but recommended)
        if "doi" not in fields:
            warnings.append(f"[{key}] No DOI — consider adding for verification")

    # Check for duplicate keys
    keys = [e["key"] for e in entries]
    key_counts = Counter(keys)
    for key, count in key_counts.items():
        if count > 1:
            errors.append(f"Duplicate key: '{key}' appears {count} times")

    # Check for duplicate DOIs
    dois = [
        e["fields"]["doi"]
        for e in entries
        if "doi" in e["fields"] and e["fields"]["doi"]
    ]
    doi_counts = Counter(dois)
    for doi, count in doi_counts.items():
        if count > 1:
            errors.append(f"Duplicate DOI: '{doi}' appears in {count} entries")

    status = "PASS" if len(errors) == 0 else "FAIL"

    return {
        "status": status,
        "total_entries": len(entries),
        "errors": errors,
        "warnings": warnings,
        "entry_types": dict(Counter(e["type"] for e in entries)),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path-to-references.bib>")
        sys.exit(2)

    result = validate(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(
        0 if result["status"] == "PASS" else 1 if result["status"] == "FAIL" else 2
    )
