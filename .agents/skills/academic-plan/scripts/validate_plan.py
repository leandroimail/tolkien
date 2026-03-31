#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Validate an Implementation Plan (plan.md) for completeness.

Usage:
    uv run python -B scripts/validate_plan.py <path-to-plan.md>

Exit codes:
    0 = all checks pass
    1 = validation errors found
    2 = file not found or parse error
"""

import json
import re
import sys
from pathlib import Path

REQUIRED_PHASES = [
    "Phase 0",
    "Phase 1",
    "Phase 2",
    "Phase 3",
    "Phase 4",
    "Phase 5",
    "Phase 6",
    "Phase 7",
    "Phase 8",
    "Phase 9",
]

EXPECTED_DELIVERABLES = [
    "prd.md",
    "plan.md",
    "research/literature.md",
    "research/references.bib",
    "draft/outline.md",
    "draft/",
    "review/review-report.md",
    "output/paper.tex",
    "output/paper.pdf",
    "process-record.md",
]

MANDATORY_GATES = ["G3", "G4", "G5"]
VALID_ROOTS = ["projects", "papers", ".projects", ".papers"]

REQUIRED_SECTIONS_PER_PHASE = ["Tasks", "Deliverable", "Acceptance Criteria"]


def validate(plan_path: str) -> dict:
    """Validate a plan.md file and return results."""
    path = Path(plan_path)
    if not path.exists():
        return {"status": "ERROR", "message": f"File not found: {plan_path}"}

    text = path.read_text(encoding="utf-8")
    errors = []
    warnings = []

    # Check file location
    # Expected: root/paper-slug/plan.md
    parts = list(path.resolve().parts)
    root_idx = -1
    for i, part in enumerate(parts):
        if part in VALID_ROOTS:
            root_idx = i
            break
            
    if root_idx == -1:
        errors.append(f"Plan file must be inside one of the approved root folders: {VALID_ROOTS}")
    else:
        # Check if there is at least one folder level between root and plan.md
        if len(parts) - 1 - root_idx < 2:
            errors.append("Plan file must be inside a project-specific subfolder within the root")

    # Check all 9 phases are present (Phase 0 through Phase 9)
    phases_found = []
    for phase in REQUIRED_PHASES:
        # Match "## Phase N" with any suffix
        pattern = rf"##\s+{re.escape(phase)}"
        if re.search(pattern, text):
            phases_found.append(phase)
        else:
            errors.append(f"Missing phase: {phase}")

    # Check expected deliverables are mentioned and follow structural rules
    for deliverable in EXPECTED_DELIVERABLES:
        if deliverable not in text:
            warnings.append(f"Expected deliverable not found in plan: {deliverable}")
        elif deliverable.startswith("output/") and deliverable not in text: # This is partly redundant but good for clarity
            errors.append(f"Missing mandatory output deliverable: {deliverable}")

    # Check mandatory gates
    for gate in MANDATORY_GATES:
        if gate not in text:
            errors.append(f"Missing mandatory gate: {gate}")

    # Check each found phase has tasks
    phase_sections = re.split(r"(?=##\s+Phase \d)", text)
    for section in phase_sections:
        phase_match = re.match(r"##\s+(Phase \d+)", section)
        if not phase_match:
            continue
        phase_name = phase_match.group(1)

        has_tasks = bool(re.search(r"- \[[ x]\]", section))
        has_deliverable = bool(
            re.search(r"(?:Deliverable|Deliverable)", section, re.IGNORECASE)
        )
        has_criteria = bool(
            re.search(r"(?:Acceptance Criteria|Criteria)", section, re.IGNORECASE)
        )

        if not has_tasks:
            warnings.append(f"{phase_name}: No task checkboxes found")
        if not has_deliverable:
            warnings.append(f"{phase_name}: No deliverables section found")
        if not has_criteria:
            warnings.append(f"{phase_name}: No acceptance criteria found")

    # Check checkpoints exist
    checkpoint_count = len(re.findall(r"(?:Checkpoint|GATE|⏸)", text, re.IGNORECASE))
    if checkpoint_count < 3:
        warnings.append(
            f"Only {checkpoint_count} checkpoints found (expected ≥ 5 for full pipeline)"
        )

    status = "PASS" if len(errors) == 0 else "FAIL"

    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "phases_found": len(phases_found),
        "phases_expected": len(REQUIRED_PHASES),
        "gates_present": [g for g in MANDATORY_GATES if g in text],
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path-to-plan.md>")
        sys.exit(2)

    result = validate(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(
        0 if result["status"] == "PASS" else 1 if result["status"] == "FAIL" else 2
    )
