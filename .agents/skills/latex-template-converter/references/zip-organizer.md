# .zip Template Organizer (Detailed Workflow)

## Table of Contents
1. [Extract and Identify](#extract-and-identify)
2. [Diagnose Issues](#diagnose-issues)
3. [Output Directory Structure](#output-directory-structure)
4. [Clean main.tex](#clean-maintex)
5. [Create Section Files](#create-section-files)
6. [Handle Dependencies](#handle-dependencies)
7. [Generate README](#generate-readme)
8. [Error Handling](#error-handling)

---

## Extract and Identify

```bash
# Extract
unzip -q template.zip -d /tmp/latex-template-temp
cd /tmp/latex-template-temp

# List all relevant files
find . -type f \( -name "*.tex" -o -name "*.sty" -o -name "*.cls" -o -name "*.bib" \)

# Find main file (contains \documentclass)
grep -rl "\\\\documentclass" . --include="*.tex"
```

**Common main file names:** `main.tex`, `paper.tex`, `document.tex`, `sample-sigconf.tex`, `template.tex`

If multiple candidates, present list to user and ask which is the main file.

**Detect document class:**
```bash
grep "\\documentclass" main.tex
```

**Detect anonymous mode:**
```bash
grep -i "anonymous\|review\|blind" main.tex
```

---

## Diagnose Issues

Present these findings to the user before executing cleanup:

**1. Structural issues:**
- Multi-level directory nesting
- `.tex` files scattered across subdirectories
- Unclear which file is the main entry point

**2. Redundant content:**
- Files with `sample`, `example`, `demo`, `test` in name
- Heavy instructional comments in `.tex` source (`% If you use ...`, `% Please do not ...`)
- Long example sections that should be replaced with actual content
- Dummy author information and affiliations

**3. Dependency issues:**
- `.sty`/`.cls` files referenced but missing
- Image paths broken (absolute paths or wrong relative paths)
- `.bib` file missing or in unexpected location

---

## Output Directory Structure

```
output/
├── main.tex            # Cleaned main file
├── references.bib      # Bibliography
├── text/
│   ├── 01-introduction.tex
│   ├── 02-related-work.tex
│   ├── 03-method.tex
│   ├── 04-experiments.tex
│   └── 05-conclusion.tex
├── figures/            # All image files
├── tables/
│   └── example-table.tex   # Placeholder (prevents Overleaf from deleting empty dir)
└── styles/             # All .sty and .cls files
```

**Create directories:**
```bash
mkdir -p output/{text,figures,tables,styles}
```

---

## Clean main.tex

**Keep in main.tex:**
- `\documentclass[...]{...}` — preserve exactly as-is
- All required `\usepackage` declarations (venue packages, math, etc.)
- Core configuration (anonymous mode, `\settopmatter`, etc.)
- Metadata commands (`\title`, `\author`, `\affiliation`)
- `\begin{abstract}...\end{abstract}` (with TODO placeholder)
- `\begin{document}` / `\end{document}`
- `\maketitle`
- `\input{text/...}` for each section
- Bibliography commands

**Remove from main.tex:**
- Example section content (replace with `\input{text/...}`)
- Verbose instructional comments (keep only structural comments)
- Example author/title information (replace with placeholders)

**Template for cleaned main.tex** (ACM example, adapt documentclass for other venues):
```latex
\documentclass[sigconf]{acmart}  % Original documentclass — do not change

%% Required packages (keep original)

%% Title and author information
\title{Your Paper Title}
\author{Author Name}
\affiliation{%
  \institution{University Name}
  \city{City}
  \country{Country}
}
\email{author@university.edu}

%% CCS Concepts (ACM only)
\begin{CCSXML}
<ccs2012>
  <concept>
    <concept_id>...</concept_id>
    <concept_desc>...</concept_desc>
    <concept_significance>500</concept_significance>
  </concept>
</ccs2012>
\end{CCSXML}
\ccsdesc[500]{...}
\keywords{keyword1, keyword2}

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

\bibliographystyle{ACM-Reference-Format}
\bibliography{references}

\end{document}
```

---

## Create Section Files

Each file in `text/` contains **only** section content starting with `\section{...}`.
No `\begin{document}`, no `\usepackage`, no document-level commands.

```latex
% text/01-introduction.tex
\section{Introduction}
% TODO: Write introduction
```

```latex
% text/02-related-work.tex
\section{Related Work}
% TODO: Write related work
```

Adapt section names to venue conventions (e.g., "Background" instead of "Related Work"
for some venues, "Evaluation" instead of "Experiments" for systems papers).

---

## Handle Dependencies

```bash
# Copy style files (preserve subdirectory structure for multi-file styles)
find /tmp/latex-template-temp -type f \( -name "*.sty" -o -name "*.cls" \) \
  -exec cp --parents {} output/styles/ \;

# Copy images
find /tmp/latex-template-temp -type f \
  \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.pdf" -o -name "*.eps" \) \
  -exec cp {} output/figures/ \;

# Copy bibliography files
find /tmp/latex-template-temp -name "*.bib" -exec cp {} output/ \;
# Rename to references.bib if needed
```

**Update image paths in main.tex** if original used absolute or nested paths:
- Change `\includegraphics{../images/fig1.png}` → `\includegraphics{figures/fig1.png}`

---

## Generate README

Use WebFetch on the conference URL (if provided) to extract submission requirements.

**README template:**
```markdown
# [Conference Name] Submission Template

## Template Information
- Conference: [name]
- Website: [URL]
- Document class: [from \documentclass]

## Submission Requirements
- Page limit: [from website or template]
- Layout: [two-column / single-column]
- Font size: [10pt/11pt]
- Anonymous submission: [yes/no]

## Overleaf Setup
1. Create new project on Overleaf
2. Upload entire `output/` directory contents
3. Set compiler to [pdflatex / xelatex]
4. Set main file to `main.tex`
5. Click Recompile

## File Structure
- `main.tex` — Start here, main entry point
- `text/` — Section files, edit these
- `figures/` — Place your images here
- `tables/` — Place your tables here
- `styles/` — Venue style files (do not modify)
- `references.bib` — Add bibliography entries here

## Adding Content
- Images: `\includegraphics[width=0.8\linewidth]{figures/your-image.pdf}`
- Citations: Add to `references.bib`, cite with `\cite{key}`
- Sections: Edit files in `text/` directory
```

---

## Error Handling

| Scenario | Handling |
|---|---|
| Main file not found | List all `.tex` files, ask user to identify main |
| Multiple `\documentclass` found | Present candidates, ask user to confirm |
| Missing `.sty`/`.cls` | Warn user, list missing files, suggest `tlmgr install` |
| Broken image paths | Fix paths relative to output directory |
| Conference URL inaccessible | Use template comments as fallback, mark fields as [To confirm] |
| `.zip` extraction fails | Ask user to verify file integrity |

---

## Cleanup

```bash
rm -rf /tmp/latex-template-temp
```
