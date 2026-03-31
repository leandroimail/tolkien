---
name: latex
description: >
  Creates, compiles, formats, and reviews LaTeX documents of any type. Use whenever the
  user needs to write LaTeX, compile .tex to PDF, fix compilation errors, format academic
  papers (IEEE, ACM, NeurIPS, ICML, AAAI, Springer), review grammar/logic/expression in
  papers, create tables with tabularray, audit bibliographic references, review pseudocode
  or algorithm blocks, check figures, reduce AI-writing traces, or prepare a paper for
  submission. Also triggers for: "fix my LaTeX", "compile this tex", "proofread my paper",
  "check my bibliography", "format for IEEE/ACM/NeurIPS", "review my experiments section",
  latexmk, pdflatex, xelatex, tabularray, bibtex, biber, chktex, algorithm2e, algorithmicx.
  Applies a deterministic self-review protocol (code → compile → PDF preview) before
  delivering any output.
compatibility: >
  Requires pdflatex, xelatex, or lualatex (TeX Live recommended). latexmk optional but
  preferred for multi-pass builds. Python 3 and uv for quality audit scripts (uv run
  python -B ensures isolated execution; fallback: python scripts/name.py directly).
allowed-tools: Read, Glob, Grep, Bash(uv *), Bash(python *), Bash(pdflatex *), Bash(xelatex *), Bash(latexmk *), Bash(bibtex *), Bash(biber *), Bash(chktex *), Bash(compile_latex.sh *), Bash(bash *)
argument-hint: "[main.tex] [--module MODULE] [--section SECTION] [--venue VENUE]"
metadata:
  category: latex
  tags: [latex, pdf, academic, ieee, acm, neurips, icml, aaai, compilation, grammar, bibliography, tables, tabularray, figures, pseudocode]
  version: "1.0"
---

# Virtualenv

Note: Python scripts for this skill must be executed within the project's virtual environment.
Activate the environment with:

```bash
source .venv/bin/activate
```

Alternatively, use `uv run python -B ...` with the `.venv` active.

# LaTeX Document Skill

Creates, compiles, formats, and reviews any LaTeX document. Applies a deterministic
self-review protocol before delivering output.

## When To Use

- Writing or editing any LaTeX document (papers, theses, reports, presentations, CVs)
- Compiling `.tex` to PDF and diagnosing build failures
- Reviewing academic papers: grammar, logic, expression, bibliography, figures, pseudocode
- Formatting papers to meet venue requirements (IEEE, ACM, NeurIPS, ICML, AAAI, Springer)
- Creating or migrating tables (tabularray, booktabs, tabularx)
- Auditing references, citations, and cross-references
- Reducing AI-writing traces while preserving LaTeX syntax
- Reviewing experiment sections without rewriting citations or math

## When Not To Use

- Converting an existing paper to a **different conference template** → use `latex-template-converter`
- Organizing a `.zip` template downloaded from a conference website → use `latex-template-converter`
- Deep literature research or fact-finding without a `.tex` file
- DOCX/PDF conversion tasks not involving LaTeX source

## Module Router

Scripts are in `$SKILL_DIR/scripts/` (Claude Code) or `<skill_path>/scripts/` (other IDEs).
Run Python scripts with `uv run python -B` for isolated execution, or `python` directly.

| Module | Use When | Primary Command | Reference |
|---|---|---|---|
| `compile` | Build fails or fresh compile needed | `bash $SKILL_DIR/scripts/compile_latex.sh main.tex --verbose` | [compilation.md](references/compilation.md) |
| `format` | LaTeX or venue formatting review | `uv run python -B $SKILL_DIR/scripts/latex_checker.py main.tex --venue <venue>` | [formatting-and-packages.md](references/formatting-and-packages.md) |
| `bibliography` | Missing citations, unused entries, BibTeX validation | `uv run python -B $SKILL_DIR/scripts/verify_bib.py refs.bib --tex main.tex` | [academic-modules.md](references/academic-modules.md) |
| `grammar` | Grammar and surface-level language fixes | `uv run python -B $SKILL_DIR/scripts/analyze_grammar.py main.tex --section intro` | [academic-modules.md](references/academic-modules.md) |
| `sentences` | Long, dense, hard-to-read sentences | `uv run python -B $SKILL_DIR/scripts/analyze_sentences.py main.tex --section intro` | [academic-modules.md](references/academic-modules.md) |
| `logic` | Weak argument flow, unclear transitions, intro funnel | `uv run python -B $SKILL_DIR/scripts/analyze_logic.py main.tex --section methods` | [academic-modules.md](references/academic-modules.md) |
| `expression` | Academic tone polish without changing claims | `uv run python -B $SKILL_DIR/scripts/improve_expression.py main.tex --section related` | [academic-modules.md](references/academic-modules.md) |
| `figures` | Figure existence, DPI, caption review | `uv run python -B $SKILL_DIR/scripts/check_figures.py main.tex` | [academic-modules.md](references/academic-modules.md) |
| `pseudocode` | IEEE-safe pseudocode, algorithm2e cleanup, caption/label | `uv run python -B $SKILL_DIR/scripts/check_pseudocode.py main.tex --venue ieee` | [academic-modules.md](references/academic-modules.md) |
| `tables` | Create or fix tables with tabularray | (manual edit) | [tables.md](references/tables.md) |
| `experiment` | Experiment design quality, discussion depth | `uv run python -B $SKILL_DIR/scripts/analyze_experiment.py main.tex --section experiments` | [academic-modules.md](references/academic-modules.md) |
| `deai` | Reduce AI-writing traces, preserve LaTeX syntax | `uv run python -B $SKILL_DIR/scripts/deai_check.py main.tex --section introduction` | [academic-modules.md](references/academic-modules.md) |

## Inputs

- Path to main `.tex` file (or content of file in conversation)
- Optional: target module (`--module <module>`)
- Optional: target section (`--section <section>`)
- Optional: venue (`--venue ieee|acm|neurips|icml|aaai|springer`)
- Optional: bibliography `.bib` file path

If module is ambiguous, infer from the user's request. Ask only for the `.tex` path when missing.

## Self-Review Protocol

**Apply these 3 gates to every document before delivering output. Do not skip gates.**

### Gate 1 — Code Review (before compiling)

```
□ No unclosed environments (\begin{X} has matching \end{X})
□ All packages declared for every command used
  - \rowcolor → \usepackage{colortbl}
  - \begin{figure}[H] → \usepackage{float}
  - \checkmark → \usepackage{amssymb}
□ For professional PDFs, prefer \usepackage[hidelinks]{hyperref}

□ Special characters escaped in text mode: % $ & # _ { } ~ ^
□ Angle brackets in text mode use math mode: $<$ $>$ or \textless \textgreater
  (NOT raw < > — they render as inverted question marks in T1 encoding)
□ All \cite{key} keys exist in .bib; all \ref{label} have a \label{label}
□ Math environments consistent (no $ inside align/equation environments)
□ Date ranges use en-dash: 2019--2025
→ Fix all issues before Gate 2
```

### Gate 2 — Compile

```
□ Run: bash $SKILL_DIR/scripts/compile_latex.sh main.tex --verbose
□   or: latexmk -pdf main.tex
□ Exit code 0
□ No critical errors in .log (undefined control sequences, missing files)
□ Warnings about overfull hbox > 10pt investigated
□ Run lint: bash $SKILL_DIR/scripts/latex_lint.sh main.tex (optional but recommended)
→ Fix compilation errors before Gate 3. Tolerate minor warnings.
```

### Gate 3 — PDF Review

```
□ Run: bash $SKILL_DIR/scripts/compile_latex.sh main.tex --preview
□ View all PNG previews
□ Layout matches expectations (margins, columns, font sizes)
□ No garbled characters or missing glyphs
□ Figures and tables render correctly (near their first mention)
  - If large stacked figures are pushed to the end, split them into individual figure[H] environments

□ No text cut off by severe overfull hbox
□ References show as [1] not [?], citations resolved
→ Only deliver to user after Gate 3 passes
```

## Output Contract

- Return findings in LaTeX diff-comment style: `% MODULE (Line N) [Severity] [Priority]: Issue`
- Severity: `ERROR` (blocks compilation), `WARNING` (degrades quality), `INFO` (suggestion)
- Priority: `HIGH`, `MEDIUM`, `LOW`
- Report exact command used and exit code when a script fails
- Preserve `\cite{}`, `\ref{}`, `\label{}`, custom macros, and math unless user asks for edits

## Workflow

1. Identify the smallest matching module from the user's request
2. Read only the reference file for that module
3. Run the module script or perform manual review
4. Apply Self-Review Gates 1–3
5. Report issues, fixes, and blockers in LaTeX diff-comment format
6. For a different concern, switch modules rather than overloading one run

## Safety Boundaries

- Never invent citations, metrics, baselines, or experimental results
- Never rewrite bibliography keys, `\ref{}`, `\label{}`, or math by default
- Treat prose rewrites as proposals; keep source-preserving checks separate
- Do not run multiple parallel compile commands before TeX Live is installed
  (risk of dpkg lock contention if auto-installation is triggered)

## Reference Map

- **Compilation**: [references/compilation.md](references/compilation.md) — latexmk, engines, flags, troubleshooting
- **Formatting & Packages**: [references/formatting-and-packages.md](references/formatting-and-packages.md) — venue specs, packages, special chars
- **Tables**: [references/tables.md](references/tables.md) — tabularray patterns, migration from legacy packages
- **Academic Modules**: [references/academic-modules.md](references/academic-modules.md) — bibliography, grammar, logic, figures, pseudocode, experiment, deai
- **Self-Review Checklist**: [references/self-review-checklist.md](references/self-review-checklist.md) — expanded 20+ item checklist

Read only the file matching the active module.

## Scripts Index

All scripts in `scripts/`. Run with `uv run python -B` or `python` directly.

| Script | Purpose |
|---|---|
| `compile_latex.sh` | Compile .tex → PDF with preview, auto engine detection |
| `latex_checker.py` | Pre-submission format check (venue compliance, word count, TODOs) |
| `clean_latex.py` | Fix special/non-UTF8 characters in .tex source |
| `verify_bib.py` | BibTeX integrity: missing fields, unused entries, key consistency |
| `check_figures.py` | Figure existence, extension, DPI, caption/label quality |
| `analyze_grammar.py` | Grammar and surface-level language analysis |
| `analyze_sentences.py` | Long and dense sentence detection |
| `analyze_logic.py` | Argument flow, transitions, intro funnel quality |
| `improve_expression.py` | Academic tone polish without changing claims |
| `check_pseudocode.py` | IEEE-safe pseudocode, algorithm2e cleanup |
| `analyze_experiment.py` | Experiment design, discussion depth, conclusion completeness |
| `deai_check.py` | Detect and flag AI-writing traces |
| `optimize_title.py` | Generate/compare/optimize paper titles |
| `translate_academic.py` | Chinese→English academic translation helper |
| `check_format.py` | chktex wrapper with enhanced reporting |
| `validate_latex.py` | Structural validation before compilation |
| `latex_lint.sh` | LaTeX linting with chktex |
| `latex_wordcount.sh` | Word count in .tex file |
| `latex_package_check.sh` | Check package availability before compiling |

**Examples**: See `examples/` for complete request-to-command walkthroughs.
