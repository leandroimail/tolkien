#!/usr/bin/env python3
"""
Float (Table/Figure) integrity checker — the two-way rule applied to floats.

Mirrors the Citation↔Bibliography gate: every Table/Figure that is DEFINED
(captioned / \\label'd) must be REFERENCED in the prose, and every Table/Figure
REFERENCED in the prose must be DEFINED. Violations of either direction are
BLOCKING.

Works on Markdown (caption lines + inline "Table N"/"Figure N" references) and
LaTeX (\\label / \\ref / \\caption inside table/figure environments).

Stdlib only. Runnable standalone or imported by data_congruence_gate.py.

Usage:
    python check_float_integrity.py <draft_dir_or_file>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from extract_numeric_inventory import iter_draft_files
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from extract_numeric_inventory import iter_draft_files

# ── Markdown patterns ───────────────────────────────────────────
# A caption line STARTS (after optional emphasis/list markers) with the float id.
_MD_CAPTION_RE = re.compile(
    r"^\s{0,3}(?:>?\s*)?(?:\*\*|__|\*|_)?\s*"
    r"(Table|Tab\.?|Figure|Fig\.?|Tabela|Figura)\s*0*(\d+)\b",
    re.IGNORECASE,
)
# Any inline mention of a float.
_FLOAT_MENTION_RE = re.compile(
    r"\b(Table|Tab\.?|Figure|Fig\.?|Tabela|Figura)\s*0*(\d+)\b",
    re.IGNORECASE,
)

# ── LaTeX patterns ──────────────────────────────────────────────
_TEX_LABEL_RE = re.compile(r"\\label\{((?:tab|fig|table|figure)[:_][^}]+)\}", re.IGNORECASE)
_TEX_REF_RE = re.compile(r"\\(?:ref|autoref|Cref|cref|eqref)\{((?:tab|fig|table|figure)[:_][^}]+)\}", re.IGNORECASE)


def _kind(word: str) -> str:
    w = word.lower()
    return "figure" if w.startswith(("fig", "figura")) else "table"


def analyze_markdown(content: str) -> dict:
    lines = content.split("\n")
    defined: dict[str, int] = {}      # "table:1" -> line
    referenced: dict[str, int] = {}   # "table:1" -> first ref line
    in_fence = False
    for i, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        cap = _MD_CAPTION_RE.match(raw)
        cap_span = cap.span() if cap else None
        if cap:
            key = f"{_kind(cap.group(1))}:{int(cap.group(2))}"
            defined.setdefault(key, i)
        # All other mentions on the line are references (skip the caption span).
        for m in _FLOAT_MENTION_RE.finditer(raw):
            if cap_span and m.start() < cap_span[1]:
                continue
            key = f"{_kind(m.group(1))}:{int(m.group(2))}"
            referenced.setdefault(key, i)
    return {"defined": defined, "referenced": referenced}


def analyze_latex(content: str) -> dict:
    defined: dict[str, int] = {}
    referenced: dict[str, int] = {}
    for i, raw in enumerate(content.split("\n"), 1):
        for m in _TEX_LABEL_RE.finditer(raw):
            defined.setdefault(m.group(1).lower(), i)
        for m in _TEX_REF_RE.finditer(raw):
            referenced.setdefault(m.group(1).lower(), i)
    return {"defined": defined, "referenced": referenced}


def check(target: Path) -> dict:
    findings: list[dict] = []
    totals = {"defined": 0, "referenced": 0}
    for path in iter_draft_files(target):
        content = path.read_text(encoding="utf-8", errors="ignore")
        data = analyze_latex(content) if path.suffix.lower() == ".tex" else analyze_markdown(content)
        defined, referenced = data["defined"], data["referenced"]
        totals["defined"] += len(defined)
        totals["referenced"] += len(referenced)

        for key, line in defined.items():
            if key not in referenced:
                findings.append({
                    "severity": "BLOCKING", "type": "orphan_float", "key": key,
                    "file": str(path), "line": line,
                    "message": f"{key} is defined/captioned but never referenced in the prose.",
                })
        for key, line in referenced.items():
            if key not in defined:
                findings.append({
                    "severity": "BLOCKING", "type": "dangling_reference", "key": key,
                    "file": str(path), "line": line,
                    "message": f"{key} is referenced in the prose but has no caption/definition.",
                })
    return {"findings": findings, "totals": totals}


def main() -> int:
    ap = argparse.ArgumentParser(description="Table/Figure two-way integrity check")
    ap.add_argument("target", type=Path, help="draft directory or file")
    args = ap.parse_args()
    if not args.target.exists():
        print(f"[ERROR] not found: {args.target}", file=sys.stderr)
        return 2
    result = check(args.target)
    blocking = [f for f in result["findings"] if f["severity"] == "BLOCKING"]
    print(f"Floats defined: {result['totals']['defined']} | referenced: {result['totals']['referenced']}")
    for f in result["findings"]:
        print(f"  [{f['severity']}] {f['type']}: {f['message']} ({f['file']}:{f['line']})")
    if not result["findings"]:
        print("  No float-integrity issues detected.")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
