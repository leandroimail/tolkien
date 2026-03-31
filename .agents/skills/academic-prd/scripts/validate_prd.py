#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Validate an Academic PRD (prd.md) for completeness and coherence.

Usage:
    uv run python -B scripts/validate_prd.py <path-to-prd.md>

Exit codes:
    0 = all checks pass
    1 = validation errors found
    2 = file not found or parse error
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml")
    sys.exit(2)

MANDATORY_FIELDS = [
    "paper_type",
    "discipline",
    "research_questions",
    "citation_format",
    "output_format",
    "template",
    "support_documents",
    "search_strategy",
    "paper_structure",
    "languages",
]

VALID_PAPER_TYPES = [
    "research article",
    "review",
    "systematic review",
    "meta-analysis",
    "case study",
]

VALID_CITATION_FORMATS = ["APA", "MLA", "Chicago", "IEEE", "Vancouver", "ABNT"]

VALID_STRUCTURES = ["IMRaD", "systematic review", "thematic", "case study"]
VALID_ROOTS = ["projects", "papers", ".projects", ".papers"]


def extract_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter from markdown text."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        print(f"ERROR: YAML parse error: {e}")
        return None


def is_non_empty(value) -> bool:
    """Check if a value is non-empty (not None, not empty string, not empty list)."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and not value.startswith("{")
    if isinstance(value, list):
        return len(value) > 0 and all(
            isinstance(v, str) and not v.startswith("{") for v in value
        )
    if isinstance(value, dict):
        return len(value) > 0
    return True


def validate(prd_path: str) -> dict:
    """Validate a PRD file and return results."""
    path = Path(prd_path)
    if not path.exists():
        return {"status": "ERROR", "message": f"File not found: {prd_path}"}

    text = path.read_text(encoding="utf-8")
    fm = extract_frontmatter(text)
    if fm is None:
        return {"status": "ERROR", "message": "No valid YAML frontmatter found"}

    errors = []
    warnings = []

    # Check file location
    # Expected: root/paper-slug/prd.md
    parts = list(path.resolve().parts)
    # Search for the root in the path
    root_idx = -1
    for i, part in enumerate(parts):
        if part in VALID_ROOTS:
            root_idx = i
            break
    
    if root_idx == -1:
        errors.append(f"PRD file must be inside one of the approved root folders: {VALID_ROOTS}")
    else:
        # Check if there is at least one folder level between root and prd.md
        # parts looks like: (..., root, paper-slug, prd.md)
        if len(parts) - 1 - root_idx < 2:
            errors.append("PRD file must be inside a project-specific subfolder within the root")

    # Check mandatory fields
    for field in MANDATORY_FIELDS:
        if field not in fm:
            errors.append(f"Missing field: {field}")
        elif not is_non_empty(fm.get(field)):
            errors.append(f"Empty field: {field}")

    # Validate paper_type
    pt = fm.get("paper_type", "")
    if isinstance(pt, str) and pt.lower() not in VALID_PAPER_TYPES:
        warnings.append(
            f"Unusual paper_type: '{pt}'. Expected one of: {VALID_PAPER_TYPES}"
        )

    # Validate citation_format
    cf = fm.get("citation_format", "")
    if isinstance(cf, str) and cf not in VALID_CITATION_FORMATS:
        warnings.append(
            f"Unknown citation_format: '{cf}'. Expected one of: {VALID_CITATION_FORMATS}"
        )

    # Validate research_questions
    rq = fm.get("research_questions", [])
    if isinstance(rq, list) and len(rq) == 0:
        errors.append("research_questions must contain at least 1 question")

    # Coherence checks
    cf = fm.get("citation_format", "")
    of = fm.get("output_format", {})
    primary_format = of if isinstance(of, str) else of.get("primary", "") if isinstance(of, dict) else ""

    if cf == "IEEE" and primary_format and "LaTeX" not in primary_format:
        warnings.append(
            "IEEE citation format strongly recommends LaTeX output format"
        )

    pt = fm.get("paper_type", "").lower() if isinstance(fm.get("paper_type"), str) else ""
    ps = fm.get("paper_structure", "").lower() if isinstance(fm.get("paper_structure"), str) else ""

    if pt == "systematic review" and ps != "systematic review":
        errors.append(
            "Systematic review paper_type requires 'systematic review' structure"
        )

    if pt == "meta-analysis" and ps != "systematic review":
        errors.append(
            "Meta-analysis paper_type requires 'systematic review' structure"
        )

    # Template coherence
    tmpl = fm.get("template", {})
    tmpl_file = tmpl.get("file", "none") if isinstance(tmpl, dict) else str(tmpl)
    if tmpl_file and tmpl_file != "none":
        if primary_format == "DOCX" and tmpl_file.endswith((".cls", ".sty")):
            errors.append(
                "LaTeX template file specified but output_format is DOCX — mismatch"
            )

    status = "PASS" if len(errors) == 0 else "FAIL"

    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "fields_checked": len(MANDATORY_FIELDS),
        "fields_present": len(MANDATORY_FIELDS) - len(
            [e for e in errors if "Missing field" in e or "Empty field" in e]
        ),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path-to-prd.md>")
        sys.exit(2)

    result = validate(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1 if result["status"] == "FAIL" else 2)
