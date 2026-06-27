#!/usr/bin/env python3
"""
Numeric inventory extractor for academic drafts (Markdown / LaTeX).

Extracts every numeric value from prose and tables, tagging each with its file,
line, section, surrounding context, unit and kind. This is the shared engine used
by data_congruence_gate.py; it is also runnable standalone for inspection.

Stdlib only — runs under the project .venv without extra dependencies.

Usage:
    python extract_numeric_inventory.py <draft_dir_or_file> [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ── Section detection ───────────────────────────────────────────

_SECTION_KEYWORDS = [
    ("abstract", r"abstract|resumo"),
    ("introduction", r"introduction|introdu"),
    ("related", r"related\s+work|literature\s+review|background|estado\s+da\s+arte|trabalhos\s+relacionados"),
    ("method", r"method|methodology|approach|materials|procedure|m[ée]todo|metodologia"),
    ("experiment", r"experiment|evaluation|implementation|setup|experimento|avalia"),
    ("result", r"result|performance|finding|resultado"),
    ("discussion", r"discussion|analysis|discuss[aã]o|an[áa]lise"),
    ("conclusion", r"conclusion|concluding|final\s+remarks|conclus[aã]o"),
]

_MD_HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*)$")
_TEX_SECTION_RE = re.compile(r"\\(?:sub)*section\*?\{([^}]*)\}")


def _classify_heading(title: str) -> str | None:
    low = title.lower()
    for name, pattern in _SECTION_KEYWORDS:
        if re.search(pattern, low):
            return name
    return None


def split_sections(lines: list[str], is_tex: bool) -> dict[int, str]:
    """Return {line_number: section_name} for every line (1-based)."""
    mapping: dict[int, str] = {}
    current = "preamble"
    in_fence = False
    for i, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if not is_tex and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_fence = not in_fence
            mapping[i] = current
            continue
        if in_fence:
            mapping[i] = current
            continue

        heading_title = None
        if is_tex:
            m = _TEX_SECTION_RE.search(raw)
            if m:
                heading_title = m.group(1)
        else:
            m = _MD_HEADING_RE.match(raw)
            if m:
                heading_title = m.group(2)

        if heading_title is not None:
            name = _classify_heading(heading_title)
            if name:
                current = name
        mapping[i] = current
    return mapping


# ── Number tokenization ─────────────────────────────────────────

# Word numbers commonly used in academic prose (EN + a few PT-BR).
_WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000,
    "um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "quatro": 4,
    "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10,
    "onze": 11, "doze": 12,
}

# Ratio like 30/75 or 442/450.
_RATIO_RE = re.compile(r"(?<![\w/.])(\d{1,7})\s*/\s*(\d{1,7})(?![\w/])")
# Percentage like 92%, 0.80%, 12.5 %.
_PERCENT_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:[.,]\d+)?)\s*%")
# Scientific notation 1.2e-3.
_SCI_RE = re.compile(r"(?<![\w.])([-+]?\d+(?:\.\d+)?[eE][-+]?\d+)")
# Plain numbers with optional thousands separators and decimals.
_NUM_RE = re.compile(r"(?<![\w.,])([-+]?\d{1,3}(?:[,.]\d{3})+(?:[.,]\d+)?|[-+]?\d+(?:[.,]\d+)?)(?![\w])")

_WORD_RE = re.compile(
    r"(?<![\w-])(" + "|".join(sorted(_WORD_NUMBERS, key=len, reverse=True)) + r")(?![\w-])",
    re.IGNORECASE,
)


def _normalize_plain(token: str) -> float | None:
    """Normalize a numeric token to a float, handling locale thousands/decimals."""
    t = token.strip().replace(" ", "")
    if not t:
        return None
    # Both separators present → the last one is the decimal separator.
    if "," in t and "." in t:
        if t.rfind(",") > t.rfind("."):
            t = t.replace(".", "").replace(",", ".")
        else:
            t = t.replace(",", "")
    elif "," in t:
        # Comma as thousands (1,000) vs decimal (0,80): if exactly 3 digits follow
        # the last comma and there is more than one group, treat as thousands.
        parts = t.split(",")
        if len(parts) >= 2 and all(len(p) == 3 for p in parts[1:]) and len(parts[0]) <= 3:
            t = t.replace(",", "")
        else:
            t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def _context(text: str, start: int, end: int, width: int = 50) -> str:
    a = max(0, start - width)
    b = min(len(text), end + width)
    return re.sub(r"\s+", " ", text[a:b]).strip()


def extract_from_text(text: str, file: str, line_no: int, section: str) -> list[dict]:
    """Extract all numeric tokens from a single visible line."""
    found: list[dict] = []
    spans: list[tuple[int, int]] = []

    def overlaps(s: int, e: int) -> bool:
        return any(not (e <= xs or s >= xe) for xs, xe in spans)

    # Order matters: ratios, percents, scientific, then plain, then words.
    for m in _RATIO_RE.finditer(text):
        s, e = m.span()
        num, den = int(m.group(1)), int(m.group(2))
        spans.append((s, e))
        found.append({
            "raw": m.group(0), "value": (num / den if den else None),
            "numerator": num, "denominator": den, "unit": "ratio", "kind": "ratio",
            "file": file, "line": line_no, "section": section,
            "context": _context(text, s, e),
        })
    for m in _PERCENT_RE.finditer(text):
        s, e = m.span()
        if overlaps(s, e):
            continue
        spans.append((s, e))
        val = _normalize_plain(m.group(1))
        found.append({
            "raw": m.group(0), "value": val, "unit": "%", "kind": "percent",
            "file": file, "line": line_no, "section": section,
            "context": _context(text, s, e),
        })
    for m in _SCI_RE.finditer(text):
        s, e = m.span()
        if overlaps(s, e):
            continue
        spans.append((s, e))
        try:
            val = float(m.group(1))
        except ValueError:
            val = None
        found.append({
            "raw": m.group(0), "value": val, "unit": "", "kind": "float",
            "file": file, "line": line_no, "section": section,
            "context": _context(text, s, e),
        })
    for m in _NUM_RE.finditer(text):
        s, e = m.span()
        if overlaps(s, e):
            continue
        spans.append((s, e))
        val = _normalize_plain(m.group(1))
        if val is None:
            continue
        kind = "year" if (val == int(val) and 1900 <= val <= 2099 and "." not in m.group(1) and "," not in m.group(1)) else (
            "int" if val == int(val) else "float")
        found.append({
            "raw": m.group(0), "value": val, "unit": "", "kind": kind,
            "file": file, "line": line_no, "section": section,
            "context": _context(text, s, e),
        })
    for m in _WORD_RE.finditer(text):
        s, e = m.span()
        if overlaps(s, e):
            continue
        spans.append((s, e))
        val = _WORD_NUMBERS[m.group(1).lower()]
        found.append({
            "raw": m.group(0), "value": float(val), "unit": "", "kind": "word-int",
            "file": file, "line": line_no, "section": section,
            "context": _context(text, s, e),
        })
    return found


def _visible_line(raw: str, is_tex: bool) -> str:
    """Lightweight visible-text extraction (keeps numbers, drops markup noise)."""
    if is_tex:
        line = re.sub(r"(?<!\\)%.*", "", raw)
        line = re.sub(r"\\(?:cite\w*|ref|label|eqref|autoref|Cref)\*?(?:\[[^\]]*\])?\{[^}]*\}", " ", line)
        line = re.sub(r"\\[a-zA-Z]+\*?", " ", line)
        line = line.replace("{", " ").replace("}", " ").replace("&", " ")
        return line
    line = re.sub(r"<!--.*?-->", " ", raw)
    line = re.sub(r"`[^`]+`", " ", line)
    return line


def iter_draft_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    files: list[Path] = []
    for ext in ("*.md", "*.markdown", "*.tex"):
        files.extend(sorted(target.rglob(ext)))
    # Skip obvious build artifacts.
    return [f for f in files if not any(p in {".git", "node_modules", ".venv"} for p in f.parts)]


def build_inventory(target: Path) -> list[dict]:
    inventory: list[dict] = []
    for path in iter_draft_files(target):
        is_tex = path.suffix.lower() == ".tex"
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lines = content.split("\n")
        section_map = split_sections(lines, is_tex)
        in_fence = False
        for i, raw in enumerate(lines, 1):
            stripped = raw.strip()
            if not is_tex and (stripped.startswith("```") or stripped.startswith("~~~")):
                in_fence = not in_fence
                continue
            if in_fence or not stripped:
                continue
            visible = _visible_line(raw, is_tex)
            inventory.extend(
                extract_from_text(visible, str(path), i, section_map.get(i, "preamble"))
            )
    return inventory


def main() -> int:
    ap = argparse.ArgumentParser(description="Numeric inventory for academic drafts")
    ap.add_argument("target", type=Path, help="draft directory or file (.md/.tex)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()
    if not args.target.exists():
        print(f"[ERROR] not found: {args.target}", file=sys.stderr)
        return 2
    inv = build_inventory(args.target)
    if args.json:
        print(json.dumps(inv, ensure_ascii=False, indent=2))
    else:
        print(f"Extracted {len(inv)} numeric tokens")
        for item in inv:
            print(f"  [{item['section']:<12}] {item['raw']:>10}  ({item['kind']})  {item['file']}:{item['line']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
