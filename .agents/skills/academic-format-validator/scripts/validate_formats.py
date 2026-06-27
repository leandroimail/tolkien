#!/usr/bin/env python3
"""
Output Format Gate — auto-detect artifacts and validate each present format.

Validates Markdown (always), LaTeX (.tex, if present) and Word (.docx, if present),
REUSING the existing latex and docx skill scripts rather than duplicating them.
Aggregates results into review/format-validation-report.md and returns:

    exit 0  → PASS or PASS-with-warnings (no BLOCKING)
    exit 1  → FAIL (one or more BLOCKING)

The absence of a .tex/.docx artifact is "skipped (not present)", never a failure.
Never assumes output/paper.tex — globs broadly under the project root.

Stdlib only (subprocess to the reused scripts). Run under the project .venv.

Usage:
    python validate_formats.py <project_dir> [--require Intro,Methods,Results] [--compile]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from check_markdown import iter_md, lint_file
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from check_markdown import iter_md, lint_file

# Resolve sibling skills relative to THIS file so it works in .claude/ and .agents/.
SKILLS_DIR = Path(__file__).resolve().parents[2]          # …/skills
LATEX_SCRIPTS = SKILLS_DIR / "latex" / "scripts"
DOCX_VALIDATE = SKILLS_DIR / "docx" / "scripts" / "office" / "validate.py"

_SKIP_PARTS = {".git", "node_modules", ".venv", "__pycache__"}
# Vendor/template directory markers to skip during artifact discovery.
_TEMPLATE_MARKERS = ("template", "_latex", "conference_latex", "styles", "sty", "cls")


def _is_skipped(p: Path) -> bool:
    if any(seg in _SKIP_PARTS for seg in p.parts):
        return True
    low = [seg.lower() for seg in p.parts]
    return any(any(mark in seg for mark in _TEMPLATE_MARKERS) for seg in low)


def _discover(root: Path, pattern: str) -> list[Path]:
    return [p for p in sorted(root.rglob(pattern)) if not _is_skipped(p)]


def _artifact_dirs(root: Path) -> list[Path]:
    """Where to look for compiled artifacts (.tex/.docx).

    Scans the canonical ``output/`` directory mandated by the pipeline AND ``draft/``
    (some projects author natively in LaTeX, keeping ``main.tex`` under ``draft/``).
    Vendor/template directories and stale ``output_v*`` siblings are excluded by the
    skip filter. Never assumes a specific filename. Falls back to the project root
    only when neither ``output/`` nor ``draft/`` exists.
    """
    dirs = [root / sub for sub in ("output", "draft") if (root / sub).is_dir()]
    return dirs or [root]


def _run(cmd: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return proc.returncode, (proc.stdout + proc.stderr).strip()
    except FileNotFoundError:
        return 127, "tool/script not found"
    except subprocess.TimeoutExpired:
        return 124, "timed out"


def validate_markdown(root: Path, required: list[str]) -> dict:
    draft_dir = root / "draft" if (root / "draft").is_dir() else root
    files = iter_md(draft_dir)
    findings: list[dict] = []
    for p in files:
        findings.extend(lint_file(p, required))
    return {"format": "markdown", "present": bool(files), "count": len(files), "findings": findings}


def _collect_tex(root: Path) -> list[Path]:
    tex: list[Path] = []
    for d in _artifact_dirs(root):
        cand = sorted(d.glob("*.tex")) if d == root else sorted(d.rglob("*.tex"))
        tex.extend(p for p in cand if not _is_skipped(p) and not p.name.endswith((".sty", ".cls")))
    # Also the project root's top-level .tex (a stray main/fragment), per the
    # documented contract — non-recursive, so stale output_v*/vendor dirs are not gated.
    tex.extend(p for p in sorted(root.glob("*.tex"))
               if not _is_skipped(p) and not p.name.endswith((".sty", ".cls")))
    # De-dup preserving order.
    seen, result = set(), []
    for p in tex:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def validate_latex(root: Path, do_compile: bool, do_lint: bool = False) -> dict:
    targets = _collect_tex(root)
    findings: list[dict] = []
    py = sys.executable

    for tex in targets:
        content = tex.read_text(encoding="utf-8", errors="ignore")
        is_main = "\\documentclass" in content

        if is_main:
            # Authoritative check for a full document is compilation (Phase 8 only).
            if do_compile:
                cscript = LATEX_SCRIPTS / "compile_latex.sh"
                if cscript.exists():
                    rc, out = _run(["bash", str(cscript), str(tex)])
                    if rc != 0:
                        findings.append({"severity": "BLOCKING", "type": "latex_compile",
                                         "file": str(tex), "line": 0,
                                         "message": f"Compilation failed (rc={rc}): {out[-500:]}"})
            # chktex lint is optional/noisy → advisory, opt-in.
            if do_lint:
                cf = LATEX_SCRIPTS / "check_format.py"
                if cf.exists():
                    rc, out = _run([py, str(cf), str(tex)])
                    if rc not in (0, 127):
                        findings.append({"severity": "WARNING", "type": "latex_lint",
                                         "file": str(tex), "line": 0,
                                         "message": f"chktex findings: {out[:400]}"})
            # Figure existence / DPI / caption (advisory).
            fscript = LATEX_SCRIPTS / "check_figures.py"
            if fscript.exists():
                rc, out = _run([py, str(fscript), str(tex)])
                if rc not in (0, 127):
                    findings.append({"severity": "WARNING", "type": "latex_figures",
                                     "file": str(tex), "line": 0,
                                     "message": f"check_figures.py: {out[:400]}"})
        else:
            # Body-only fragment → validate_latex.py is the right structural check.
            vscript = LATEX_SCRIPTS / "validate_latex.py"
            if vscript.exists():
                rc, out = _run([py, str(vscript), str(tex)])
                if rc not in (0, 127):
                    findings.append({"severity": "BLOCKING", "type": "latex_structure",
                                     "file": str(tex), "line": 0,
                                     "message": f"validate_latex.py reported issues:\n{out[:500]}"})
    return {"format": "latex", "present": bool(targets), "count": len(targets), "findings": findings}


def _collect_docx(root: Path) -> list[Path]:
    docx: list[Path] = []
    for d in _artifact_dirs(root):
        cand = sorted(d.glob("*.docx")) if d == root else sorted(d.rglob("*.docx"))
        docx.extend(p for p in cand if not _is_skipped(p) and not p.name.startswith("~$"))
    docx.extend(p for p in sorted(root.glob("*.docx"))
                if not _is_skipped(p) and not p.name.startswith("~$"))
    seen, result = set(), []
    for p in docx:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def validate_docx(root: Path) -> dict:
    docx_files = _collect_docx(root)
    findings: list[dict] = []
    py = sys.executable
    for d in docx_files:
        if DOCX_VALIDATE.exists():
            rc, out = _run([py, str(DOCX_VALIDATE), str(d)])
            if rc == 127:
                findings.append({"severity": "WARNING", "type": "docx_tool_missing",
                                 "file": str(d), "line": 0,
                                 "message": "docx validate.py not available; schema not checked."})
            elif rc != 0:
                findings.append({"severity": "BLOCKING", "type": "docx_schema",
                                 "file": str(d), "line": 0,
                                 "message": f"DOCX schema validation failed:\n{out[:500]}"})
        else:
            findings.append({"severity": "WARNING", "type": "docx_tool_missing",
                             "file": str(d), "line": 0,
                             "message": "docx skill validate.py not found; .docx not validated."})
    return {"format": "docx", "present": bool(docx_files), "count": len(docx_files), "findings": findings}


def run(root: Path, required: list[str], do_compile: bool, do_lint: bool = False) -> dict:
    results = [
        validate_markdown(root, required),
        validate_latex(root, do_compile, do_lint),
        validate_docx(root),
    ]
    all_findings = [f for r in results for f in r["findings"]]
    blocking = [f for f in all_findings if f["severity"] == "BLOCKING"]
    warnings = [f for f in all_findings if f["severity"] == "WARNING"]
    return {"results": results, "blocking": blocking, "warnings": warnings}


def render_report(root: Path, agg: dict) -> str:
    status = "❌ FAIL" if agg["blocking"] else ("⚠️ PASS (with warnings)" if agg["warnings"] else "✅ PASS")
    out = ["# Format Validation Report (Output Format Gate)", "",
           f"- **Gate result**: {status}", ""]
    out.append("| Format | Present | Artifacts | Findings |")
    out.append("|--------|---------|-----------|----------|")
    for r in agg["results"]:
        present = "yes" if r["present"] else "skipped (not present)"
        out.append(f"| {r['format']} | {present} | {r['count']} | {len(r['findings'])} |")
    out.append("")
    if agg["blocking"]:
        out.append("## ❌ Blocking findings (must fix)")
        out.append("")
        for f in agg["blocking"]:
            out.append(f"- **[{f['type']}]** {f['message']}  ({f['file']}:{f['line']})")
        out.append("")
    if agg["warnings"]:
        out.append("## ⚠️ Warnings")
        out.append("")
        for f in agg["warnings"]:
            out.append(f"- **[{f['type']}]** {f['message']}  ({f['file']}:{f['line']})")
        out.append("")
    if not agg["blocking"] and not agg["warnings"]:
        out.append("All present formats validated cleanly.")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Output Format Gate (md/tex/docx)")
    ap.add_argument("target", type=Path, help="project directory (or a single .md/.tex/.docx file)")
    ap.add_argument("--require", default="", help="comma-separated required section names")
    ap.add_argument("--compile", action="store_true", help="run the authoritative LaTeX compile gate")
    ap.add_argument("--lint", action="store_true", help="also run chktex lint on main .tex (noisy)")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    if not args.target.exists():
        print(f"[ERROR] not found: {args.target}", file=sys.stderr)
        return 2
    required = [s for s in args.require.split(",") if s.strip()] if args.require else []

    if args.target.is_file():
        # Validate a single explicit artifact (used by paper-generator-agent).
        suffix = args.target.suffix.lower()
        parent = args.target.parent
        if suffix in (".md", ".markdown"):
            findings = lint_file(args.target, required)
            results = [{"format": "markdown", "present": True, "count": 1, "findings": findings}]
        elif suffix == ".tex":
            results = [validate_latex(parent, args.compile, args.lint)]
        elif suffix == ".docx":
            results = [validate_docx(parent)]
        else:
            print(f"[ERROR] unsupported file type: {suffix}", file=sys.stderr)
            return 2
        all_findings = [f for r in results for f in r["findings"]]
        agg = {"results": results,
               "blocking": [f for f in all_findings if f["severity"] == "BLOCKING"],
               "warnings": [f for f in all_findings if f["severity"] == "WARNING"]}
        root = parent
    else:
        root = args.target
        agg = run(root, required, args.compile, args.lint)
    report = render_report(root, agg)

    out_path = args.out or (root / "review" / "format-validation-report.md")
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Report written: {out_path}")
    except OSError as e:
        print(f"[WARN] could not write report ({e}); printing:\n", file=sys.stderr)
        print(report)

    status = "FAIL" if agg["blocking"] else ("PASS-WITH-WARNINGS" if agg["warnings"] else "PASS")
    print(f"Output Format Gate: {status} "
          f"({len(agg['blocking'])} blocking, {len(agg['warnings'])} warnings)")
    return 1 if agg["blocking"] else 0


if __name__ == "__main__":
    sys.exit(main())
