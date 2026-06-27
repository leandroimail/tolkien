#!/usr/bin/env python3
"""
Data Integrity Gate (G4.5) — orchestrator for the academic-data-validator skill.

Runs the deterministic checks (numeric inventory, float integrity, table
arithmetic), builds a cross-section "reconciliation worksheet" for the agentic
(LLM) pass to adjudicate, writes review/data-congruence-report.md, and returns:

    exit 0  → PASS or PASS-with-warnings (no BLOCKING findings)
    exit 1  → FAIL (one or more BLOCKING findings)

Deterministic BLOCKING findings: orphan/dangling floats, table total mismatches.
Everything else (cross-section precision variance, summary-only numbers,
manual-verify figures, percent anomalies) is a WARNING surfaced for human/LLM
adjudication — never a silent pass.

Stdlib only.

Usage:
    python data_congruence_gate.py <project_dir|draft_dir|file> [--out PATH]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from extract_numeric_inventory import build_inventory
    from check_float_integrity import check as check_floats
    from check_table_arithmetic import check as check_tables
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from extract_numeric_inventory import build_inventory
    from check_float_integrity import check as check_floats
    from check_table_arithmetic import check as check_tables

_BODY_SECTIONS = {"introduction", "related", "method", "experiment", "result", "discussion"}


def _resolve_paths(target: Path) -> tuple[Path, Path]:
    """Return (scan_target, project_root). project_root holds review/."""
    if target.is_file():
        # .../<root>/draft/file.md → root is two up; else file.parent.
        if target.parent.name == "draft":
            return target, target.parent.parent
        return target, target.parent
    if (target / "draft").is_dir():
        return target / "draft", target
    if target.name == "draft":
        return target, target.parent
    return target, target


def _cluster(inventory: list[dict]) -> dict:
    """Group numeric tokens by rounded value; build cross-section clusters."""
    clusters: dict[float, list[dict]] = {}
    for item in inventory:
        v = item.get("value")
        if v is None:
            continue
        # Skip trivially common small integers and years to reduce noise.
        if item["kind"] == "year":
            continue
        key = round(v, 4)
        clusters.setdefault(key, []).append(item)
    return clusters


def build_worksheet(inventory: list[dict]) -> tuple[list[str], list[dict]]:
    """Return (markdown_lines, warnings)."""
    clusters = _cluster(inventory)
    lines: list[str] = []
    warnings: list[dict] = []

    # Cross-section clusters: same value in 2+ distinct sections.
    cross = []
    for value, items in clusters.items():
        secs = {it["section"] for it in items}
        if len(secs) >= 2 and abs(value) >= 1:
            cross.append((value, items, secs))
    cross.sort(key=lambda x: (-len(x[2]), -x[0]))

    if cross:
        lines.append("#### Cross-section number clusters (verify identity + arithmetic)")
        lines.append("")
        lines.append("| Value | Sections | Occurrences |")
        lines.append("|-------|----------|-------------|")
        for value, items, secs in cross[:40]:
            raws = ", ".join(sorted({it["raw"] for it in items}))
            lines.append(f"| {value:g} | {', '.join(sorted(secs))} | {raws} |")
        lines.append("")

    # Summary-only numbers: salient value in abstract/conclusion but no body section.
    summary_only = []
    for value, items in clusters.items():
        if abs(value) < 2:
            continue
        secs = {it["section"] for it in items}
        if (secs & {"abstract", "conclusion"}) and not (secs & _BODY_SECTIONS):
            summary_only.append((value, items, secs))
    if summary_only:
        lines.append("#### Summary-only numbers (stated in abstract/conclusion, not found in body)")
        lines.append("")
        for value, items, secs in sorted(summary_only, key=lambda x: -x[0])[:30]:
            ex = items[0]
            warnings.append({
                "severity": "WARNING", "type": "summary_only_number",
                "file": ex["file"], "line": ex["line"],
                "message": f"Value {ex['raw']} appears in {', '.join(sorted(secs))} but not in the body — verify it traces to a result.",
            })
            lines.append(f"- **{ex['raw']}** ({', '.join(sorted(secs))}) — _{ex['context']}_")
        lines.append("")

    # Precision-variance pairs: distinct cluster values within 2% relative.
    values = sorted(v for v in clusters if abs(v) >= 1)
    pv_seen = set()
    pv_lines = []
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            a, b = values[i], values[j]
            if a == b:
                continue
            if b - a > a * 0.02:
                break
            denom = max(abs(a), abs(b)) or 1
            if abs(a - b) / denom <= 0.02:
                sa = {it["section"] for it in clusters[a]}
                sb = {it["section"] for it in clusters[b]}
                if sa | sb and (sa != sb or len(sa) > 1):
                    keypair = (a, b)
                    if keypair in pv_seen:
                        continue
                    pv_seen.add(keypair)
                    ra = clusters[a][0]["raw"]
                    rb = clusters[b][0]["raw"]
                    pv_lines.append(f"- `{ra}` vs `{rb}` (sections: {', '.join(sorted(sa | sb))})")
                    warnings.append({
                        "severity": "WARNING", "type": "precision_variance",
                        "file": clusters[a][0]["file"], "line": clusters[a][0]["line"],
                        "message": f"Possible precision/rounding variance: {ra} vs {rb}.",
                    })
    if pv_lines:
        lines.append("#### Possible precision / rounding variance (same quantity stated differently?)")
        lines.append("")
        lines.extend(pv_lines[:30])
        lines.append("")

    # Ratio sanity: numerator should usually not exceed denominator.
    for item in inventory:
        if item.get("kind") == "ratio" and item.get("numerator") is not None:
            if item["numerator"] > item["denominator"]:
                warnings.append({
                    "severity": "WARNING", "type": "ratio_inverted",
                    "file": item["file"], "line": item["line"],
                    "message": f"Ratio {item['raw']} has numerator > denominator — verify it is intended.",
                })
    return lines, warnings


def _figure_manual_verify(project_root: Path, inventory: list[dict]) -> list[dict]:
    """Flag figure-referencing numeric claims when no figure data sidecar exists."""
    warnings: list[dict] = []
    fig_dirs = [p for p in project_root.rglob("figures") if p.is_dir()]
    if not fig_dirs:
        fig_dirs = [project_root]
    has_sidecar = any(
        any(d.rglob(ext)) for d in fig_dirs for ext in ("*.csv", "*.json")
    ) or any(d.rglob("*.py") for d in fig_dirs)
    images = [p for d in fig_dirs for ext in ("*.png", "*.jpg", "*.jpeg", "*.eps", "*.pdf", "*.svg")
              for p in d.rglob(ext)]
    if images and not has_sidecar:
        warnings.append({
            "severity": "WARNING", "type": "figure_manual_verify",
            "file": str(fig_dirs[0]), "line": 0,
            "message": (f"{len(images)} figure image(s) found with no data sidecar "
                        "(figures/<stem>.{csv,json} or .py). Numbers shown inside figures "
                        "cannot be auto-verified — mark for manual verification."),
        })
    return warnings


def run(target: Path) -> dict:
    scan_target, project_root = _resolve_paths(target)
    inventory = build_inventory(scan_target)
    floats = check_floats(scan_target)
    tables = check_tables(scan_target)
    worksheet_lines, ws_warnings = build_worksheet(inventory)
    fig_warnings = _figure_manual_verify(project_root, inventory)

    findings = floats["findings"] + tables["findings"] + ws_warnings + fig_warnings
    blocking = [f for f in findings if f.get("severity") == "BLOCKING"]
    warnings = [f for f in findings if f.get("severity") == "WARNING"]
    return {
        "project_root": project_root, "scan_target": scan_target,
        "inventory_count": len(inventory),
        "float_totals": floats["totals"], "table_count": tables["table_count"],
        "blocking": blocking, "warnings": warnings,
        "worksheet_lines": worksheet_lines,
    }


def render_report(result: dict) -> str:
    status = "❌ FAIL" if result["blocking"] else ("⚠️ PASS (with warnings)" if result["warnings"] else "✅ PASS")
    out = []
    out.append("# Data Congruence Report (Gate G4.5)")
    out.append("")
    out.append(f"- **Gate result**: {status}")
    out.append(f"- **Numeric tokens analyzed**: {result['inventory_count']}")
    out.append(f"- **Floats**: {result['float_totals']['defined']} defined / {result['float_totals']['referenced']} referenced")
    out.append(f"- **Tables parsed**: {result['table_count']}")
    out.append(f"- **Blocking findings**: {len(result['blocking'])}")
    out.append(f"- **Warnings**: {len(result['warnings'])}")
    out.append("")
    out.append("> Deterministic gate. BLOCKING findings must be fixed before the pipeline "
               "advances. WARNINGs require human/LLM adjudication using the reconciliation "
               "worksheet below — they are never silently passed.")
    out.append("")

    if result["blocking"]:
        out.append("## ❌ Blocking findings (must fix)")
        out.append("")
        for f in result["blocking"]:
            loc = f"{f.get('file','')}:{f.get('line','')}"
            out.append(f"- **[{f['type']}]** {f['message']}  ({loc})")
        out.append("")

    if result["warnings"]:
        out.append("## ⚠️ Warnings (adjudicate)")
        out.append("")
        for f in result["warnings"]:
            loc = f"{f.get('file','')}:{f.get('line','')}"
            out.append(f"- **[{f['type']}]** {f['message']}  ({loc})")
        out.append("")

    out.append("## Reconciliation worksheet (for the agentic congruence pass)")
    out.append("")
    out.append("The script proposes candidate-equal numbers across sections; it does NOT "
               "assert semantic identity. The reviewer/LLM must confirm each cluster refers "
               "to the same quantity and that the stated direction matches the data, then "
               "cross-check against tables/figures.")
    out.append("")
    if result["worksheet_lines"]:
        out.extend(result["worksheet_lines"])
    else:
        out.append("_No multi-section numeric clusters detected._")
    out.append("")
    out.append("## Agentic checks still required (not automatable)")
    out.append("")
    out.append("- [ ] Confirm each cross-section cluster refers to the SAME quantity.")
    out.append("- [ ] Verify every quantitative claim's DIRECTION matches the table/figure "
               "(e.g., \"improved\" ↔ the number actually rose).")
    out.append("- [ ] Map each headline claim to a shown data point, table cell, figure, or citation.")
    out.append("- [ ] Resolve every `manual-verify` figure against its source data.")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Data Integrity Gate (G4.5)")
    ap.add_argument("target", type=Path, help="project dir, draft dir, or single file")
    ap.add_argument("--out", type=Path, default=None, help="report path (default: <root>/review/data-congruence-report.md)")
    args = ap.parse_args()
    if not args.target.exists():
        print(f"[ERROR] not found: {args.target}", file=sys.stderr)
        return 2

    result = run(args.target)
    report = render_report(result)

    out_path = args.out or (result["project_root"] / "review" / "data-congruence-report.md")
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Report written: {out_path}")
    except OSError as e:
        print(f"[WARN] could not write report ({e}); printing to stdout:\n", file=sys.stderr)
        print(report)

    status = "FAIL" if result["blocking"] else ("PASS-WITH-WARNINGS" if result["warnings"] else "PASS")
    print(f"Data Integrity Gate: {status} "
          f"({len(result['blocking'])} blocking, {len(result['warnings'])} warnings)")
    return 1 if result["blocking"] else 0


if __name__ == "__main__":
    sys.exit(main())
