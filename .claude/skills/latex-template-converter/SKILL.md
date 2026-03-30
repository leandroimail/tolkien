---
name: latex-template-converter
description: >
  Converts and adapts LaTeX documents to conference and publication templates. Use when
  the user needs to organize a .zip template downloaded from a conference website, migrate
  an existing paper to a different template (ACM acmart, IEEE IEEEtran, NeurIPS, ICLR,
  AAAI, CVPR, KDD, Springer LNCS, ICML), configure anonymous/blind review mode for
  submission, validate template compliance before submitting, or prepare an Overleaf-ready
  structure. Also triggers for: "convert to ACM format", "change template to NeurIPS",
  "organize conference template", "prepare for submission", "set up blind review",
  "clean up zip template", "migrate paper to ICML", "Overleaf template", acmart, IEEEtran,
  neurips_2025, iclr2025, aaai25, llncs, nonacm, sigconf. Applies a deterministic
  4-gate self-review (structure → compliance → compile → PDF) before delivering output.
compatibility: >
  Requires pdflatex or xelatex (TeX Live). WebFetch available for extracting conference
  submission requirements from URLs. Python 3 for validation scripts.
allowed-tools: Read, Glob, Grep, Bash(unzip *), Bash(find *), Bash(mkdir *), Bash(cp *), Bash(bash *), Bash(pdflatex *), Bash(xelatex *), Bash(latexmk *), Bash(python *)
argument-hint: "[template.zip | main.tex] [--target-venue VENUE] [--mode anonymous|camera-ready]"
metadata:
  category: latex
  tags: [latex, template, conference, acm, ieee, neurips, icml, iclr, aaai, cvpr, kdd, springer, overleaf, submission]
  version: "1.0"
---

# LaTeX Template Converter

Converts and adapts LaTeX documents to conference and publication templates. Validates
structural and formatting compliance before delivering any output.

## When To Use

- Organizing a messy `.zip` conference template into clean Overleaf-ready structure
- Migrating an existing paper from one template to another (e.g., NeurIPS → ICML)
- Setting up a venue template from scratch (ACM, IEEE, NeurIPS, ICLR, AAAI, Springer)
- Configuring anonymous/blind review submission mode
- Validating that a paper meets venue formatting requirements before submission

## When Not To Use

- Writing or editing paper content → use `latex` skill
- Compiling a document that already has the correct template → use `latex` skill
- Deep content review (grammar, logic, bibliography audit) → use `latex` skill

## Inputs

- `.zip` file path (for Workflow A) OR `.tex` file path (for Workflow B)
- Target venue name or conference URL (for submission requirements)
- Submission mode: `anonymous` (blind review) or `camera-ready`
- Optional: conference link for extracting official requirements via WebFetch

## Workflow A: Organize Conference Template .zip

Use when the user provides a `.zip` from an official conference website.

### Step 1: Extract and Analyze

```bash
unzip -q template.zip -d /tmp/latex-template-temp
find /tmp/latex-template-temp -type f \( -name "*.tex" -o -name "*.sty" -o -name "*.cls" -o -name "*.bib" \)
```

Identify: main file (contains `\documentclass`), `.sty`/`.cls` files, `.bib` files, images.

```bash
# Find main file
grep -l "\\\\documentclass" /tmp/latex-template-temp/*.tex
```

### Step 2: Diagnose and Present Issues

Present to user before proceeding:
- Disorganized nesting (`.tex` files scattered across directories)
- Redundant content (files named `sample-*`, `example-*`, `demo-*`)
- Excessive instructional comments in source
- Dependency issues (missing `.sty`/`.cls`)

### Step 3: Collect Conference Information

Ask the user for:
1. Conference submission URL (preferred — extract requirements via WebFetch)
2. Conference name (fallback)
3. Special requirements (page limits, anonymity, supplementary rules)

### Step 4: Confirm Cleanup Plan

Present the plan and wait for user confirmation before executing.

### Step 5: Execute Cleanup

```bash
mkdir -p output/{text,figures,tables,styles}
```

**main.tex structure after cleanup:**

```latex
\documentclass[...]{...}  % Original template documentclass — keep unchanged

%% Required packages (keep original declarations)

\title{Your Paper Title}
\author{Author Name}
\affiliation{...}

\begin{abstract}
% TODO: Write abstract
\end{abstract}

\begin{document}
\maketitle

\input{text/01-introduction}
\input{text/02-related-work}
\input{text/03-method}
\input{text/04-experiments}
\input{text/05-conclusion}

\bibliographystyle{...}
\bibliography{references}
\end{document}
```

**Section files** (`text/01-introduction.tex`, etc.) contain only `\section{...}` and content.
No `\begin{document}` or document-level wrappers in section files.

**Copy files:**
```bash
# Style files
find /tmp/latex-template-temp -name "*.sty" -o -name "*.cls" | xargs -I{} cp {} output/styles/

# Images
find /tmp/latex-template-temp -name "*.png" -o -name "*.jpg" -o -name "*.pdf" | xargs -I{} cp {} output/figures/

# Bibliography
find /tmp/latex-template-temp -name "*.bib" | xargs -I{} cp {} output/
```

Create `output/tables/example-table.tex` as placeholder (Overleaf deletes empty dirs).

### Step 6: Generate README

Use WebFetch on the conference URL (if provided) to extract:
- Page limits, font size, column format
- Anonymity requirements
- Compilation requirements (engine, special packages)
- Submission deadlines

Generate README with: template info, submission requirements, file structure description,
Overleaf upload steps, common operations (adding figures, tables, references).

---

## Workflow B: Migrate Paper to Different Template

Use when the user has an existing paper and wants to change the conference template.

### Step 1: Identify Source and Target Templates

Determine current `\documentclass` and target venue. Read [references/venues.md](references/venues.md) for target specs.

### Step 2: Adapt Document Class and Preamble

Replace `\documentclass[...]{...}` with target venue class and options.
- Remove source-venue-specific packages not needed by target
- Add target-venue-specific packages and configurations
- Adjust bibliography style for target venue

### Step 3: Adapt Venue-Specific Sections

- **ACM**: Add CCS concepts (`\begin{CCSXML}...`) and `\ccsdesc`, `\keywords`
- **IEEE**: Add `\IEEEpeerreviewmaketitle`, adjust `\author` to `\IEEEauthorblockN`
- **NeurIPS/ICML/ICLR**: Configure anonymous mode, adjust abstract position
- **Springer LNCS**: Add `\institute{}`, adjust author format

### Step 4: Configure Submission Mode

```latex
% Anonymous (blind review) — NeurIPS example
\usepackage[final]{neurips_2025}  % or 'preprint' for arXiv

% Anonymous — ICML example
\usepackage[accepted]{icml2025}

% Anonymous — KDD/ACM (nonacm removes footnotes)
\documentclass[sigconf,anonymous,review,nonacm]{acmart}
\settopmatter{printacmref=false}
\setcopyright{none}
\acmConference[]{}{}{}

% Camera-ready — KDD/ACM (restore metadata)
\documentclass[sigconf]{acmart}
\settopmatter{printacmref=true}
\setcopyright{acmcopyright}
\acmConference[KDD '26]{...}{...}{...}
```

---

## Self-Review Protocol

**Apply all 4 gates before delivering. Do not skip.**

### Gate 1 — Structure

```
□ \documentclass matches target venue class and options
□ All required sections present for venue
□ \input{} or \include{} paths resolve correctly
□ .sty/.cls files from venue present in project (styles/ dir or root)
□ Section files contain only section content (no \begin{document})
□ Abstract in correct position for venue (preamble vs. body)
```

### Gate 2 — Venue Compliance

```
□ Anonymous/review mode set correctly for submission type
□ Author information removed/anonymized (blind review)
□ hidelinks option used for hyperref (professional PDF look)
□ TODOs and placeholder text removed

□ Venue-specific metadata present:
  - ACM: \begin{CCSXML}, \ccsdesc, \keywords
  - IEEE: \IEEEpeerreviewmaketitle
  - NeurIPS/ICML: correct package option (final/preprint/accepted)
□ Bibliography style matches venue
□ Font size and page layout match venue requirements
→ Fix all non-compliance before Gate 3
```

### Gate 3 — Compile

```
□ Run: bash $SKILL_DIR/scripts/compile_latex.sh main.tex --verbose
□   or: latexmk -pdf main.tex
□ Exit code 0
□ No critical errors (undefined control sequences, missing .sty)
□ Run: uv run python -B $SKILL_DIR/scripts/validate_latex.py main.tex
□ Venue-specific style warnings documented if non-critical
→ Fix compilation errors before Gate 4
```

### Gate 4 — PDF Review

```
□ Run: bash $SKILL_DIR/scripts/compile_latex.sh main.tex --preview
□ View all preview pages
□ Column layout correct (two-column / single-column per venue)
□ Figures and tables placed near references (no "orphans" at end of doc)
  - Split large stacked figures if necessary for better placement flow
□ Header/footer absent for anonymous, present for camera-ready

□ Page count within venue limit
□ References formatted correctly for venue style
□ No garbled characters or missing fonts
→ Only deliver after Gate 4 passes
```

## Output

- Organized directory structure ready for Overleaf upload
- Compiled PDF confirming template compiles successfully
- README with venue requirements and usage guide
- List of any TODOs requiring user action (e.g., fill abstract, add author info)

## Reference Map

- **Venue Specs**: [references/venues.md](references/venues.md) — detailed specs per conference
- **.zip Organizer**: [references/zip-organizer.md](references/zip-organizer.md) — detailed cleanup steps
- **Template Migration**: [references/template-migration.md](references/template-migration.md) — migration patterns per venue
- **Validation Checklist**: [references/validation-checklist.md](references/validation-checklist.md) — expanded 4-gate checklist

## Scripts Index

Scripts are in `$SKILL_DIR/scripts/` (Claude Code) or `<skill_path>/scripts/` (other IDEs).

| Script | Purpose |
|---|---|
| `compile_latex.sh` | Compile .tex → PDF with `--preview` flag for PNG page review |
| `validate_latex.py` | Structural LaTeX validation before compilation |
