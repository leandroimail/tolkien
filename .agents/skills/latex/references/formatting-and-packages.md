# Formatting and Packages Reference

## Table of Contents
1. [Special Character Escaping](#special-character-escaping)
2. [Critical Package Dependencies](#critical-package-dependencies)
3. [Standard Preamble](#standard-preamble)
4. [Venue Format Specs](#venue-format-specs)
5. [Pre-Submission Format Checker](#pre-submission-format-checker)
6. [Common Formatting Fixes](#common-formatting-fixes)

---

## Special Character Escaping

Always escape in text mode:

| Character | Escaped Form |
|---|---|
| `%` | `\%` |
| `$` | `\$` |
| `&` | `\&` |
| `#` | `\#` |
| `_` | `\_` |
| `{` | `\{` |
| `}` | `\}` |
| `~` | `\textasciitilde` |
| `^` | `\textasciicircum` |

**Angle brackets (common silent error):** Raw `<` and `>` in T1 encoding render as
inverted question marks (¡ ¿) — the document compiles but the PDF is wrong.

```latex
% WRONG — compiles but renders as garbage
temperature <5°C

% CORRECT
temperature $<$5°C
% or
temperature \textless{}5°C
```

**Date ranges** use en-dash (double hyphen): `2019--2025`

**Ellipsis**: `\ldots` not `...`

## Critical Package Dependencies

Missing these packages causes `Undefined control sequence` — always include:

| Command | Required Package |
|---|---|
| `\rowcolor{}` | `\usepackage{colortbl}` |
| `\begin{figure}[H]` | `\usepackage{float}` |
| `\checkmark` | `\usepackage{amssymb}` |
| `\rowcolors{}{}{}` | `\usepackage[table]{xcolor}` |
| `\url{}` in .bib with natbib | `\usepackage{url}` |
| `\toprule`, `\midrule` | `\usepackage{booktabs}` |
| `\SI{}{}`  | `\usepackage{siunitx}` |
| `\cref{}` | `\usepackage{cleveref}` |
| `\begin{algorithm}` | `\usepackage{algorithm}` + `\usepackage{algorithmic}` |
| `\begin{algorithm2e}` | `\usepackage[ruled]{algorithm2e}` |
| `\usepackage[hidelinks]{hyperref}` | Disables colored boxes around links and citations |

**hyperref**: Fine for normal documents. Use `[hidelinks]` to avoid green/red boxes in professional PDFs. Avoid in PDF-to-LaTeX conversions with theorem environments.


## Standard Preamble

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage[hidelinks]{hyperref}

\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{float}        % for [H] float placement
```

## Venue Format Specs

| Venue | Document Class | Columns | Font | Page Limit | Notes |
|---|---|---|---|---|---|
| IEEE (general) | `IEEEtran` | 2 | 10pt | varies | Use `\IEEEpeerreviewmaketitle` |
| ACM (conferences) | `acmart` with `sigconf` | 2 | 9pt | 10–12pp | CCS concepts required |
| NeurIPS | `neurips_2025` | 1 | 10pt | 9pp + refs | Anonymous blind review |
| ICML | `icml2025` | 2 | 10pt | 9pp + refs | Anonymous blind review |
| ICLR | `iclr2025_conference` | 1 | 10pt | 10pp + refs | Anonymous blind review |
| AAAI | `aaai25` | 2 | 10pt | 8pp + refs | Strict page limit |
| Springer LNCS | `llncs` | 1 | 10pt | varies | `\institute{}` required |
| CVPR/ICCV | `cvpr` | 2 | 10pt | 8pp + refs | Anonymous blind review |
| KDD (ACM) | `acmart` with `sigconf` | 2 | 9pt | 10pp + refs | Requires `nonacm` for anonymous |

For full template setup and anonymous submission configuration → use `latex-template-converter`.

## Pre-Submission Format Checker

```bash
python latex_checker.py main.tex --venue neurips --check-anon
```

Checks: word count, required sections, TODO markers, anonymization, mismatched
environments, content stats.

```bash
# Auto-fix after checking
python latex_checker.py main.tex --venue neurips --fix
# Writes to main_fixed.tex

# Clean special characters
python clean_latex.py --input main.tex --output main_cleaned.tex
# Flags: --dry-run, --tables-only
```

## Common Formatting Fixes

**Float placement issues:**
```latex
% Too many "h" placements causing floats to bunch up
\begin{figure}[htbp]   % preferred over [h] alone
% Or force exact placement (requires float package)
\begin{figure}[H]
\end{figure}

**Large Figures & Legibility:**
If large stacked subfigures (e.g., comparing many charts) are pushed to the end of the document:
1. **Split them**: Re-structure from one `figure` with multiple `subfigure`s into individual `figure[H]` environments.
2. **Deterministic Placement**: Using `[H]` from the `float` package ensures they appear immediately after their reference paragraph, preventing "figure orphans" at the end of the paper.
3. **Width Tuning**: A width of `0.85\textwidth` is typically optimal for legibility in single-column templates while allowing for text flow between figures if split.


**Overfull hbox:**
```latex
% Add \sloppy locally or use \emergencystretch
{\emergencystretch=3em \par}
% Or break long URLs
\usepackage{url}
\Urlmuskip=0mu plus 1mu
```

**Bibliography style by venue:**
- IEEE: `\bibliographystyle{IEEEtran}`
- ACM: `\bibliographystyle{ACM-Reference-Format}`
- NeurIPS/ICML/ICLR: `\bibliographystyle{plainnat}` or venue-specific
- Springer LNCS: `\bibliographystyle{splncs04}`
