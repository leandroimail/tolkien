#!/usr/bin/env python3
"""
Self-contained structural linter for Markdown drafts.

No external toolchain (no markdownlint/remark/prettier) — stdlib only, runs under
the project .venv. Checks the structural properties that matter for academic
drafts:

  - heading hierarchy (single H1; no skipped levels)
  - fenced code blocks closed
  - YAML frontmatter closed (if opened)
  - pipe tables well-formed (consistent column count; header separator present)
  - local image/link targets resolve on disk
  - required sections present (optional, advisory)

Severities: BLOCKING (structural breakage) and WARNING (style/structure advisory).

Usage:
    python check_markdown.py <file_or_dir> [--require Intro,Methods,Results] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
_PIPE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
_SEP_ROW_RE = re.compile(r"^\s*\|?(?:\s*:?-{1,}:?\s*\|)+\s*:?-{0,}:?\s*\|?\s*$")


def _is_external(target: str) -> bool:
    t = target.strip().lower()
    return t.startswith(("http://", "https://", "mailto:", "ftp://", "#", "data:"))


def lint_file(path: Path, required: list[str]) -> list[dict]:
    findings: list[dict] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")

    # Frontmatter.
    fm_open = False
    body_start = 0
    if lines and lines[0].strip() == "---":
        closed = False
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                closed = True
                body_start = i + 1
                break
        if not closed:
            findings.append({"severity": "BLOCKING", "type": "frontmatter_unclosed",
                             "file": str(path), "line": 1,
                             "message": "YAML frontmatter opened with '---' but never closed."})
        fm_open = closed

    in_fence = False
    fence_marker = ""
    fence_start = 0
    prev_level = 0
    h1_count = 0
    headings_seen: list[str] = []
    table_block: list[tuple[int, str]] = []

    def flush_table(block: list[tuple[int, str]]):
        if len(block) < 1:
            return
        # Expect: header row, separator row, then data rows.
        first_no, first = block[0]
        ncols = first.strip().strip("|").count("|") + 1
        has_sep = len(block) >= 2 and _SEP_ROW_RE.match(block[1][1])
        if not has_sep:
            findings.append({"severity": "WARNING", "type": "table_no_separator",
                             "file": str(path), "line": first_no,
                             "message": "Pipe table has no header separator row (|---|---|)."})
        for ln, row in block:
            cols = row.strip().strip("|").count("|") + 1
            if cols != ncols:
                findings.append({"severity": "WARNING", "type": "table_ragged",
                                 "file": str(path), "line": ln,
                                 "message": f"Table row has {cols} columns; header has {ncols}."})

    for i, raw in enumerate(lines, 1):
        if _FENCE_RE.match(raw):
            marker = _FENCE_RE.match(raw).group(1)
            if not in_fence:
                in_fence, fence_marker, fence_start = True, marker, i
            elif marker == fence_marker:
                in_fence = False
            continue
        if in_fence:
            continue

        # Tables.
        if _PIPE_ROW_RE.match(raw):
            table_block.append((i, raw))
            continue
        elif table_block:
            flush_table(table_block)
            table_block = []

        # Headings.
        m = _HEADING_RE.match(raw)
        if m:
            level = len(m.group(1))
            headings_seen.append(m.group(2).strip())
            if level == 1:
                h1_count += 1
            if prev_level and level > prev_level + 1:
                findings.append({"severity": "WARNING", "type": "heading_skip",
                                 "file": str(path), "line": i,
                                 "message": f"Heading jumps from H{prev_level} to H{level} (skipped a level)."})
            prev_level = level

        # Images (local target must exist).
        for mm in _IMG_RE.finditer(raw):
            tgt = mm.group(1).split()[0].strip("<>")
            if _is_external(tgt):
                continue
            resolved = (path.parent / tgt).resolve()
            if not resolved.exists():
                findings.append({"severity": "BLOCKING", "type": "image_missing",
                                 "file": str(path), "line": i,
                                 "message": f"Image target not found on disk: {tgt}"})
        # Local links (advisory).
        for mm in _LINK_RE.finditer(raw):
            tgt = mm.group(1).split()[0].strip("<>")
            if _is_external(tgt) or tgt.startswith("#"):
                continue
            base = tgt.split("#")[0]
            if not base:
                continue
            resolved = (path.parent / base).resolve()
            if not resolved.exists():
                findings.append({"severity": "WARNING", "type": "link_broken",
                                 "file": str(path), "line": i,
                                 "message": f"Local link target not found: {base}"})

    if table_block:
        flush_table(table_block)
    if in_fence:
        findings.append({"severity": "BLOCKING", "type": "code_fence_unclosed",
                         "file": str(path), "line": fence_start,
                         "message": f"Code fence opened with '{fence_marker}' but never closed."})
    if h1_count > 1:
        findings.append({"severity": "WARNING", "type": "multiple_h1",
                         "file": str(path), "line": 1,
                         "message": f"{h1_count} level-1 headings found; expected a single H1 title."})

    # Required sections (advisory).
    if required:
        joined = " \n ".join(headings_seen).lower()
        for req in required:
            if req.strip() and req.strip().lower() not in joined:
                findings.append({"severity": "WARNING", "type": "missing_section",
                                 "file": str(path), "line": 0,
                                 "message": f"Expected section not found: '{req.strip()}'."})
    _ = fm_open  # reserved for future frontmatter-field checks
    return findings


def iter_md(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return [p for p in sorted(target.rglob("*.md"))
            if not any(seg in {".git", "node_modules", ".venv"} for seg in p.parts)]


def main() -> int:
    ap = argparse.ArgumentParser(description="Markdown structural linter")
    ap.add_argument("target", type=Path)
    ap.add_argument("--require", default="", help="comma-separated required section names")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.target.exists():
        print(f"[ERROR] not found: {args.target}", file=sys.stderr)
        return 2
    required = [s for s in args.require.split(",") if s.strip()] if args.require else []
    all_findings: list[dict] = []
    for p in iter_md(args.target):
        all_findings.extend(lint_file(p, required))
    if args.json:
        print(json.dumps(all_findings, ensure_ascii=False, indent=2))
    else:
        if not all_findings:
            print("Markdown: no structural issues detected.")
        for f in all_findings:
            print(f"  [{f['severity']}] {f['type']}: {f['message']} ({f['file']}:{f['line']})")
    return 1 if any(f["severity"] == "BLOCKING" for f in all_findings) else 0


if __name__ == "__main__":
    sys.exit(main())
