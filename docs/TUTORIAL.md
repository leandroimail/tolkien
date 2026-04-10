# Tolkien — Tutorial

Step-by-step guide for setting up and using the Academic Article Production Multi-Agent System.

---

## Prerequisites

Before you start, make sure you have the following installed on your system:

| Requirement | Minimum Version | Notes |
|------------|----------------|-------|
| **Python** | 3.8+ | Check with `python3 --version` |
| **Node.js** | 16+ | Check with `node --version` |
| **git** | Any | For cloning the repository |
| **Claude Code CLI** or **OpenCode** | Latest | Install one of these AI coding tools |
| **Homebrew** (macOS) or **apt-get** (Linux) | — | Used by the install script to set up system deps |

---

## Installation

### Step 1 — Clone the Repository

```bash
git clone https://gitlab.com/leandroimail/tolkien.git
cd tolkien
```

### Step 2 — Run the Dependency Installer

The install script sets up all system packages, Node.js packages, browser automation tools, and the Python virtual environment in a single run.

```bash
bash resources/install_skills_deps.sh
```

**What the script installs:**

| Category | Packages |
|----------|---------|
| System (macOS) | Tesseract OCR, Poppler, TinyTeX, LibreOffice |
| System (Linux) | `tesseract-ocr`, `poppler-utils`, `libreoffice`, `chromium` |
| Node.js (npm) | `docx`, `agent-browser`, `@playwright/cli` |
| Playwright | Chromium browser |
| Python (.venv) | `pyyaml`, `requests`, `pandas`, `matplotlib`, `pypdf`, `pdfplumber`, `reportlab`, `pillow`, `pytesseract`, `pdf2image`, `defusedxml`, `duckduckgo-search` |

The script creates a Python virtual environment at `.venv/` in the project root.

### Step 3 — Activate the Virtual Environment

```bash
source .venv/bin/activate
```

Your prompt will change to indicate the environment is active. You must activate it every time you open a new terminal session and want to run Python-based skills manually.

To deactivate later:

```bash
deactivate
```

> **Note:** When you invoke skills through Claude Code or OpenCode, the tools manage the environment automatically. Manual activation is only needed if you run Python scripts directly.

---

## Available Templates

The `templates/` directory provides ready-made starting points you can use before or alongside the pipeline:

| File | Purpose |
|------|---------|
| `templates/research_request_form.md` | A structured form that maps to all fields collected by the `academic-prd` interview. Fill it out offline before starting the pipeline to have your answers ready. Covers: paper type, research questions, target venue, citation style, inclusion/exclusion criteria, and expected structure. |
| `templates/systematic_review_protocol.yaml` | A PRISMA-aligned protocol template for systematic literature reviews. Pre-populates the structure required by `academic-researcher` for systematic review papers. |

To use the form as a reference during the PRD interview:

```bash
# Open the form in a separate window before invoking the orchestrator
cat templates/research_request_form.md
```

---

## Using tolkien with Claude Code

### Starting a New Paper Project

Open Claude Code in the tolkien directory and invoke the orchestrator:

```
/academic-orchestrator "Start a new research article about multi-agent systems in healthcare"
```

The orchestrator will:
1. Invoke `academic-prd` to run a structured PRD interview
2. Ask you ~10 questions to define the paper's requirements
3. Pause at **Gate G1** for your review of `prd.md`
4. After approval, generate `plan.md` and pause at **Gate G2**
5. Continue automatically through each phase, pausing at each gate

### Invoking Individual Agents

You can invoke any agent directly by trigger phrase if you want to run a specific phase:

```
# Run only the literature research phase
/research-agent "Search for papers about retrieval-augmented generation"

# Write or revise sections
/writing-agent "Draft the methodology section"

# Run peer review
/review-agent "Review the full article"

# Compile the final PDF
/paper-generator "Generate final paper"
```

### Invoking Individual Skills

For fine-grained control, use skills directly:

```bash
# Generate only the PRD (no full pipeline)
/academic-prd

# Validate citations against the bibliography
/academic-citation-manager

# Compile LaTeX manually
/latex

# Search OpenAlex for papers
/academic-researcher
```

---

## Using tolkien with OpenCode

The workflow is identical to Claude Code. tolkien stores its OpenCode configuration under `.agents/` (instead of `.claude/`), which OpenCode reads automatically.

### Starting a New Paper Project (OpenCode)

Open OpenCode in the tolkien directory:

```
@academic-orchestrator Start a new research article about federated learning in IoT
```

Or use the natural language triggers:

```
start academic pipeline for a paper about federated learning in IoT
write full article on transformer-based summarization
```

### Invoking Individual Agents (OpenCode)

```
@research-agent search literature on knowledge graph embeddings
@writing-agent draft the results section
@review-agent review full article
@paper-generator generate final paper
```

---

## Example: Creating a New Paper End-to-End

This example walks you through the complete pipeline for a hypothetical paper on vector database benchmarking.

### 1. Start the Orchestrator

```
/academic-orchestrator "New paper: benchmarking vector databases for RAG applications"
```

### 2. Answer the PRD Interview (Gate G1)

The `academic-prd` skill asks structured questions. Example answers:

| Question | Example Answer |
|---------|---------------|
| Paper type | Experimental research / benchmark study |
| Target venue | SIGMOD 2026 |
| Language | English |
| Research question | Which vector database delivers the best recall-latency tradeoff for RAG workloads? |
| Citation style | IEEE |
| Structure | IMRaD |

After completing the interview, review `papers/paper-vector-rag/prd.md` and approve to pass Gate G1.

### 3. Review the Implementation Plan (Gate G2)

The orchestrator generates `plan.md` automatically. Review the 9-phase plan and approve to pass Gate G2.

### 4. Literature Research (Phase 2)

The orchestrator invokes `research-agent`, which runs `academic-researcher` against the OpenAlex API using your PRD keywords. The output lands in:

```
papers/paper-vector-rag/research/literature.md
papers/paper-vector-rag/research/references.bib
```

### 5. Outline Approval (Phase 3 → Gate G3)

The `academic-writer` skill (outline mode) generates `draft/outline.md` with section headers and word allocations. Review and approve to pass Gate G3.

### 6. Full-text Drafting (Phase 4)

The `writing-agent` drafts each section sequentially. Figures and plots are generated by `academic-media` and saved to `output/figures/`. This is the longest phase.

### 7. Citation Validation (Phase 5 → Gate G4)

`review-agent` runs `academic-citation-manager` and `academic-bibliography-manager`. These tools check that:
- Every `\cite{key}` in the draft has a matching entry in `references.bib`
- Every entry in `references.bib` is cited at least once
- Every BibTeX entry has all mandatory fields

A violation report is written to `review/citation-report.md`. Fix any violations before Gate G4 clears.

### 8. Humanization (Phase 6)

`academic-humanizer` adjusts the register of the draft — removing AI-writing markers while preserving academic rigor and field-specific vocabulary.

### 9. Peer Review (Phase 7 → Gate G5)

`academic-reviewer` simulates a panel of 5 reviewers. The review report lands in `review/review-report.md`. The composite score must be ≥ 65/100 with no CRITICAL issues to pass Gate G5. If the score is below threshold, the orchestrator loops back to the writing phase for revisions.

### 10. Output Generation (Phase 8 → Gate G5.5)

`paper-generator-agent` compiles the LaTeX document and exports PDF and DOCX. All files land in `output/`:

```
papers/paper-vector-rag/output/paper.tex
papers/paper-vector-rag/output/paper.pdf
papers/paper-vector-rag/output/paper.docx
```

Gate G5.5 verifies that `pdflatex` exits with code 0 and all references resolve.

### 11. Process Documentation (Phase 9)

The orchestrator writes `process-record.md` — a log of every decision, gate outcome, and revision in the pipeline run.

---

## Troubleshooting

### `pdflatex: command not found`

TinyTeX was not installed or its bin directory is not in `PATH`. Re-run the install script:

```bash
bash resources/install_skills_deps.sh
```

Or add TinyTeX manually to your shell profile:

```bash
# macOS (Apple Silicon)
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"

# macOS (Intel)
export PATH="$HOME/.TinyTeX/bin/x86_64-darwin:$PATH"

# Linux (x86_64)
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
```

### `ModuleNotFoundError` when a Python skill runs

The virtual environment is not active. Run:

```bash
source .venv/bin/activate
```

If the `.venv/` directory does not exist, re-run:

```bash
bash resources/install_skills_deps.sh
```

### `academic-researcher` returns no results

The OpenAlex API is a public API with rate limits. If you get empty results:
- Wait a few seconds and retry
- Narrow your search keywords in `prd.md`
- OpenAlex does not require an API key, but sending a polite email header is recommended for high-volume use

### Gate is not clearing despite fixing violations

Re-invoke the relevant agent explicitly to re-run the validation:

```
/review-agent "execute academic review"
```

The orchestrator checks gate state based on the latest report file, not a cache.

### LaTeX compilation fails with undefined references

Make sure `references.bib` is in the correct location (`research/references.bib`) and that the LaTeX template includes `\bibliography{../research/references}`. The `latex` skill can diagnose most compilation errors automatically.

### Skills are not recognized in OpenCode

Confirm that `.agents/skills/` and `.agents/agents/` directories exist and contain the skill definitions. Use the `multi-ide-artifacts` skill to re-sync if needed:

```
/multi-ide-artifacts sync claude-to-opencode
```
