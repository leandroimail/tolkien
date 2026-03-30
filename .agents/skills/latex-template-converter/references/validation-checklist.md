# Template Validation Checklist (Expanded 4-Gate)

## Table of Contents
1. [Gate 1 — Structure Validation](#gate-1--structure-validation)
2. [Gate 2 — Venue Compliance Validation](#gate-2--venue-compliance-validation)
3. [Gate 3 — Compilation Validation](#gate-3--compilation-validation)
4. [Gate 4 — PDF Review](#gate-4--pdf-review)
5. [Final Delivery Gate](#final-delivery-gate)

Expanded version of the self-review protocol in SKILL.md. Use when thorough validation
is needed before final delivery.

---

## Gate 1 — Structure Validation

### Document Organization

- [ ] `\documentclass` matches target venue class and options exactly
- [ ] All `\usepackage` declarations for venue-required packages present
- [ ] No packages from source venue that conflict with target venue
- [ ] Main file only: no section content directly in `main.tex` (use `\input{}`)
- [ ] All `\input{path}` or `\include{path}` files exist at specified paths
- [ ] Bibliography file referenced in `\bibliography{refs}` or `\addbibresource{refs.bib}` exists
- [ ] Venue `.sty`/`.cls` files present (in `styles/` or project root)

### Section Structure

- [ ] All required sections present for academic paper: Introduction, Related Work, Method/Approach, Experiments/Evaluation, Conclusion
- [ ] Abstract present and correctly positioned for target venue
- [ ] Section files (in `text/`) contain only `\section{}` and content — no `\begin{document}` or `\usepackage`
- [ ] Logical section numbering (no gaps, no duplicate section names)

---

## Gate 2 — Venue Compliance Validation

### Anonymous Submission Requirements

- [ ] Author names removed or replaced with "Anonymous Author(s)"
- [ ] Author affiliations removed or anonymized
- [ ] Email addresses removed
- [ ] Self-identifying acknowledgments removed or anonymized
- [ ] Self-citations handled per venue policy (anonymized or removed)
- [ ] Anonymous mode option set in documentclass or package

### Venue-Specific Metadata

**ACM venues:**
- [ ] `\begin{CCSXML}...\end{CCSXML}` present with valid concept IDs
- [ ] `\ccsdesc[...]{}` matching CCS XML entries
- [ ] `\keywords{...}` present
- [ ] For anonymous: `nonacm` option, `\settopmatter{printacmref=false}`, `\setcopyright{none}`, cleared `\acmConference`

**IEEE venues:**
- [ ] `\IEEEpeerreviewmaketitle` added after `\maketitle` (for double-blind)
- [ ] `\begin{IEEEkeywords}...\end{IEEEkeywords}` present

**NeurIPS:**
- [ ] Correct package option: default (anonymous) or `final`/`preprint`
- [ ] NeurIPS paper checklist appendix present (required since 2022)

**ICML:**
- [ ] `icml2025` package option correct for submission type
- [ ] Author format uses `\icmlauthor{}{}` and `\icmlaffiliation{}{}`

**Springer LNCS:**
- [ ] `\titlerunning{}` and `\authorrunning{}` present
- [ ] `\institute{}` present with all author institutions

### Content Compliance

- [ ] No `% TODO` markers remaining
- [ ] No placeholder text (`[AUTHOR]`, `[CITATION NEEDED]`, `[FIG]`, `[TBD]`)
- [ ] No broken `\ref{}` or `\cite{}` keys (all resolve to defined labels/bib entries)
- [ ] Page count within venue limit (count manually or compile and check PDF)

### Bibliography Compliance

- [ ] `\bibliographystyle{}` matches venue requirement
- [ ] Bibliography compiles (bibtex/biber runs without critical errors)
- [ ] No `??` citation markers (means bib not compiled or key missing)

---

## Gate 3 — Compilation Validation

```bash
# Run full compilation
latexmk -pdf main.tex

# Check exit code
echo "Exit code: $?"

# Check for critical errors in log
grep -n "^!" main.log | head -20

# Check for undefined references
grep "Warning.*Reference.*undefined\|Warning.*Citation.*undefined" main.log
```

### Compilation Pass/Fail Criteria

- [ ] Exit code 0 (no fatal errors)
- [ ] No `Undefined control sequence` errors
- [ ] No `File not found` errors
- [ ] No `Missing \begin{document}` errors
- [ ] `\ref{}` and `\cite{}` warnings: 0 (all resolved after multi-pass)
- [ ] Package conflicts resolved

**Acceptable warnings (do not block):**
- Overfull hbox < 10pt
- Font substitution warnings
- Unused bibliography entries (in venue-provided example .bib)
- Package version warnings

---

## Gate 4 — PDF Review

```bash
# Generate page previews
bash compile_latex.sh main.tex --preview
```

### Visual Verification Checklist

- [ ] Column layout correct: two-column (ACM, IEEE, ICML, AAAI, CVPR) or one-column (NeurIPS, ICLR, LNCS)
- [ ] Page header matches venue format
  - Anonymous: no author names in header
  - Camera-ready: correct conference name and authors
- [ ] Page footer: conference info (camera-ready) or absent (anonymous)
- [ ] Font renders correctly (no missing glyphs, no tofu squares)
- [ ] No garbled characters from unescaped special characters
- [ ] Figures present and correctly sized
- [ ] Tables render without overflow
- [ ] Section numbering correct (no `0.1` or `0.1.1` from wrong base class)
- [ ] Bibliography renders in correct venue style
- [ ] Page count: count PDF pages, verify within venue limit

### Page Count Verification

| Venue | Main Content | References |
|---|---|---|
| NeurIPS | 9 pages | Unlimited, not counted |
| ICML | 9 pages | Unlimited, not counted |
| ICLR | 10 pages | Unlimited, not counted |
| ACM (KDD/CHI) | 10–12 pages | Counted in total |
| IEEE (most) | Varies | Counted in total |
| AAAI | 8 pages | Counted in total |
| CVPR | 8 pages | Unlimited, not counted |
| Springer LNCS | Varies | Counted in total |

---

## Final Delivery Gate

```
All 4 gates passed?

Gate 1 ✓ Structure valid
Gate 2 ✓ Venue compliant
Gate 3 ✓ Compiles cleanly (exit code 0)
Gate 4 ✓ PDF visually correct

→ Deliver to user with:
   - Compiled PDF
   - Organized directory structure
   - README with submission instructions
   - List of remaining TODOs (abstract, content, acknowledgments)
```
