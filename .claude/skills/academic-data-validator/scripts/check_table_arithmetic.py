#!/usr/bin/env python3
"""
Table arithmetic checker.

For tables that actually exist in the draft, verify simple, hard arithmetic that
must hold regardless of domain:
  - a row/column labeled "Total"/"Sum"/"Soma" equals the sum of its components;
  - a column of percentages sums to ~100 (±1);
These are BLOCKING when contradicted (the data shown is internally inconsistent).

Supports Markdown pipe tables and LaTeX tabular. If no parseable table is found,
the script reports nothing and exits 0 (absence of tables is not a failure).

Stdlib only. Runnable standalone or imported by data_congruence_gate.py.

Usage:
    python check_table_arithmetic.py <draft_dir_or_file> [--tol 1.0]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from extract_numeric_inventory import _normalize_plain, iter_draft_files
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from extract_numeric_inventory import _normalize_plain, iter_draft_files

_TOTAL_RE = re.compile(r"\b(total|sum|soma|overall|geral)\b", re.IGNORECASE)
_PCT_CELL_RE = re.compile(r"\d+(?:[.,]\d+)?\s*%")


def _cell_number(cell: str):
    cell = cell.strip()
    is_pct = bool(_PCT_CELL_RE.search(cell))
    m = re.search(r"[-+]?\d[\d.,]*", cell)
    if not m:
        return None, is_pct
    return _normalize_plain(m.group(0)), is_pct


def _parse_markdown_tables(content: str) -> list[list[list[str]]]:
    """Return a list of tables; each table is a list of rows; each row a list of cells."""
    tables = []
    rows: list[list[str]] = []
    in_fence = False
    for raw in content.split("\n"):
        s = raw.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            if rows:
                tables.append(rows)
                rows = []
            continue
        if in_fence:
            continue
        if s.startswith("|") and s.count("|") >= 2:
            cells = [c.strip() for c in s.strip("|").split("|")]
            # Skip separator rows like |---|---|
            if all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in cells if c):
                continue
            rows.append(cells)
        else:
            if rows:
                tables.append(rows)
                rows = []
    if rows:
        tables.append(rows)
    return tables


def _parse_latex_tables(content: str) -> list[list[list[str]]]:
    tables = []
    for block in re.findall(r"\\begin\{tabular\}.*?\\end\{tabular\}", content, re.DOTALL):
        rows = []
        body = re.sub(r"\\begin\{tabular\}(?:\{[^}]*\})?", "", block)
        body = body.replace("\\end{tabular}", "")
        for line in body.split("\\\\"):
            line = re.sub(r"\\hline|\\toprule|\\midrule|\\bottomrule", "", line)
            if "&" not in line:
                continue
            cells = [c.strip() for c in line.split("&")]
            if any(c for c in cells):
                rows.append(cells)
        if rows:
            tables.append(rows)
    return tables


def _check_table(rows: list[list[str]], tol: float, file: str, idx: int) -> list[dict]:
    findings: list[dict] = []
    if len(rows) < 2:
        return findings
    ncols = max(len(r) for r in rows)

    # Column-wise numeric matrices.
    cols: list[list] = [[] for _ in range(ncols)]
    pct_flags = [False] * ncols
    for r in rows:
        for c in range(ncols):
            cell = r[c] if c < len(r) else ""
            val, is_pct = _cell_number(cell)
            cols[c].append(val)
            if is_pct:
                pct_flags[c] = True

    # Percentage columns should sum to ~100 (exclude a "total" row if present).
    total_row_idx = next(
        (ri for ri, r in enumerate(rows) if r and _TOTAL_RE.search(" ".join(r[:1]))), None)
    for c in range(ncols):
        if not pct_flags[c]:
            continue
        vals = [(ri, v) for ri, v in enumerate(cols[c]) if v is not None and ri != total_row_idx and ri != 0]
        s = sum(v for _, v in vals)
        if len(vals) >= 2 and not (100 - tol <= s <= 100 + tol) and not (s <= tol):
            findings.append({
                "severity": "WARNING", "type": "percent_sum",
                "file": file, "table": idx,
                "message": f"Column {c + 1} percentages sum to {s:.2f}%, expected ~100%.",
            })

    # Total row: sum of component rows equals the labeled total.
    if total_row_idx is not None:
        for c in range(1, ncols):
            comp = [cols[c][ri] for ri in range(len(rows))
                    if ri != total_row_idx and ri != 0 and cols[c][ri] is not None]
            total_val = cols[c][total_row_idx]
            if total_val is not None and len(comp) >= 2:
                ssum = sum(comp)
                if abs(ssum - total_val) > max(tol, abs(total_val) * 0.001):
                    findings.append({
                        "severity": "BLOCKING", "type": "total_mismatch",
                        "file": file, "table": idx,
                        "message": (f"Column {c + 1}: components sum to {ssum:g} "
                                    f"but the Total row states {total_val:g}."),
                    })
    return findings


def check(target: Path, tol: float = 1.0) -> dict:
    findings: list[dict] = []
    table_count = 0
    for path in iter_draft_files(target):
        content = path.read_text(encoding="utf-8", errors="ignore")
        tables = (_parse_latex_tables(content) if path.suffix.lower() == ".tex"
                  else _parse_markdown_tables(content))
        for idx, rows in enumerate(tables, 1):
            table_count += 1
            findings.extend(_check_table(rows, tol, str(path), idx))
    return {"findings": findings, "table_count": table_count}


def main() -> int:
    ap = argparse.ArgumentParser(description="Table arithmetic consistency check")
    ap.add_argument("target", type=Path)
    ap.add_argument("--tol", type=float, default=1.0, help="absolute tolerance")
    args = ap.parse_args()
    if not args.target.exists():
        print(f"[ERROR] not found: {args.target}", file=sys.stderr)
        return 2
    result = check(args.target, args.tol)
    print(f"Tables parsed: {result['table_count']}")
    for f in result["findings"]:
        print(f"  [{f['severity']}] {f['type']}: {f['message']} ({f['file']} table {f['table']})")
    if not result["findings"]:
        print("  No table-arithmetic issues detected.")
    return 1 if any(f["severity"] == "BLOCKING" for f in result["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
