#!/usr/bin/env python3
"""
Validate BibTeX file for required fields per entry type.
Usage: python validate_bib.py research/references.bib [--fix] [--report review/bibliography-report.md]
"""
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

REQUIRED_FIELDS = {
    "article": {"author", "title", "journal", "year", "volume", "pages"},
    "inproceedings": {"author", "title", "booktitle", "year"},
    "book": {"title", "publisher", "year"},  # author OR editor
    "misc": {"author", "title", "year", "url"},
    "incollection": {"author", "title", "booktitle", "publisher", "year"},
    "phdthesis": {"author", "title", "school", "year"},
    "mastersthesis": {"author", "title", "school", "year"},
    "techreport": {"author", "title", "institution", "year"},
}


def parse_bibtex(content: str) -> list[dict]:
    """Parse BibTeX content into list of entry dicts."""
    entries = []
    # Match @type{key, ... }
    pattern = re.compile(
        r"@(\w+)\s*\{([^,]+),\s*(.*?)\n\}",
        re.DOTALL,
    )
    for match in pattern.finditer(content):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)

        fields = {}
        field_pattern = re.compile(r"(\w+)\s*=\s*[{\"](.*?)[}\"]", re.DOTALL)
        for field_match in field_pattern.finditer(body):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2).strip()
            fields[field_name] = field_value

        entries.append({
            "type": entry_type,
            "key": key,
            "fields": fields,
            "raw": match.group(0),
        })
    return entries


def validate_entry(entry: dict) -> list[str]:
    """Validate a single BibTeX entry. Returns list of issues."""
    issues = []
    entry_type = entry["type"]
    key = entry["key"]
    fields = entry["fields"]

    if entry_type not in REQUIRED_FIELDS:
        issues.append(f"[{key}] Unknown entry type: @{entry_type}")
        return issues

    required = REQUIRED_FIELDS[entry_type]

    # Special case: book requires author OR editor
    if entry_type == "book":
        if "author" not in fields and "editor" not in fields:
            issues.append(f"[{key}] @book requires 'author' or 'editor'")
        check_fields = required - {"author"}  # already checked
    else:
        check_fields = required

    for field in check_fields:
        if field not in fields or not fields[field].strip():
            issues.append(f"[{key}] Missing required field: {field}")

    # Validate year is 4 digits
    if "year" in fields:
        year = fields["year"].strip()
        if not re.match(r"^\d{4}$", year):
            issues.append(f"[{key}] Invalid year format: '{year}' (expected YYYY)")

    # Check pages format for articles
    if entry_type == "article" and "pages" in fields:
        pages = fields["pages"]
        if "-" in pages and "--" not in pages:
            issues.append(f"[{key}] Pages should use '--' (double dash): '{pages}'")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate BibTeX file")
    parser.add_argument("bibfile", help="Path to .bib file")
    parser.add_argument("--report", help="Output report file path")
    args = parser.parse_args()

    bib_path = Path(args.bibfile)
    if not bib_path.exists():
        print(f"ERROR: File not found: {bib_path}")
        sys.exit(1)

    content = bib_path.read_text(encoding="utf-8")
    entries = parse_bibtex(content)

    if not entries:
        print("WARNING: No BibTeX entries found in file.")
        sys.exit(1)

    all_issues = []
    stats = defaultdict(int)

    for entry in entries:
        stats[entry["type"]] += 1
        issues = validate_entry(entry)
        all_issues.extend(issues)

    # Report
    print(f"\n{'='*60}")
    print(f"BibTeX Validation Report: {bib_path.name}")
    print(f"{'='*60}")
    print(f"Total entries: {len(entries)}")
    for etype, count in sorted(stats.items()):
        print(f"  @{etype}: {count}")
    print(f"\nIssues found: {len(all_issues)}")

    if all_issues:
        print(f"\n{'─'*60}")
        for issue in all_issues:
            print(f"  ❌ {issue}")
        print(f"{'─'*60}")
        print(f"\nResult: ❌ FAIL — {len(all_issues)} issues to resolve")
    else:
        print(f"\nResult: ✅ PASS — all entries valid")

    # Write report if requested
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# Bibliography Validation Report\n\n")
            f.write(f"**File**: `{bib_path}`\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Total entries**: {len(entries)}\n")
            for etype, count in sorted(stats.items()):
                f.write(f"  - @{etype}: {count}\n")
            f.write(f"- **Issues found**: {len(all_issues)}\n")
            f.write(f"- **Status**: {'✅ PASS' if not all_issues else '❌ FAIL'}\n\n")
            if all_issues:
                f.write(f"## Issues\n\n")
                for issue in all_issues:
                    f.write(f"- {issue}\n")
        print(f"\nReport written to: {report_path}")

    sys.exit(1 if all_issues else 0)


if __name__ == "__main__":
    main()
