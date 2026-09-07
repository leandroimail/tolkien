# Tolkien — Tutorial

> **Language / Idioma:** English | [Versão em Português](pt-BR/TUTORIAL.md)

Step-by-step guide for setting up and using the Academic Article Production Multi-Agent System.

---

## Prerequisites

Before you start, make sure you have the following installed on your system:

| Requirement | Minimum Version | Notes |
|------------|----------------|-------|
| **Python** | 3.10+ | Check with `python3 --version` |
| **Node.js** | 18+ | Check with `node --version` |
| **git** | Any | For cloning the repository |
| **AI Harness / CLI** | Latest | **Claude Code**, **OpenCode**, **OpenAI Codex**, or **Google Antigravity** |
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

Your prompt will indicate the environment is active. You must activate it every time you run Python-based skills or validation scripts manually.

To deactivate later:

```bash
deactivate
```

---

## Available Templates & Paper Governance

The `templates/` directory provides ready-made starting points:

| File | Purpose |
|------|---------|
| `templates/research_request_form.md` | A structured form matching all fields collected by the `academic-prd` interview. Fill it out offline before starting the pipeline. |
| `templates/systematic_review_protocol.yaml` | A PRISMA-aligned protocol template for systematic literature reviews used by `academic-researcher`. |
| `templates/paper/style-guide.md.template` | Authorial voice, tone, and CEI paragraph discipline guide. |
| `templates/paper/anti-style-guide.md.template` | Catalog of banned AI markers, scope drift, and master's tone flaws. |
| `templates/paper/human-decisions.md.template` | Template to document author-driven methodological decisions. |

### Paper Governance Directory (`resources/`)

In any paper project (`papers/paper-{slug}/`), you can optionally create a `resources/` folder containing:
- `resources/style-guide.md`: Author voice, terminology, register.
- `resources/anti-style-guide.md`: Prohibited clichés and AI tropes.
- `resources/human-decisions.md`: Key research decisions preserving authentic human authorship.

The `writing-agent` and `academic-writer` automatically check for and obey these files when drafting.

---

## Platform Support

tolkien works identically across the major AI coding platforms:

### 1. Claude Code (CLI)
Uses `CLAUDE.md` and reads skills/agents from `.claude/`:
```bash
/academic-orchestrator "Start a new paper about [topic]"
```

### 2. OpenAI Codex CLI & IDE
Uses `AGENTS.md` and natively discovers skills in `.agents/skills/`. Subagent descriptors live in `.codex/agents/*.toml`:
```bash
$academic-orchestrator "Start a new paper about [topic]"
```

### 3. OpenCode
Uses `AGENTS.md` and natively reads `.agents/skills/` and `.opencode/agents/*.md`:
```bash
@academic-orchestrator "Start a new paper about [topic]"
```

### 4. Google Antigravity / Gemini CLI
Natively discovers workspace rules in `AGENTS.md` and discovers all 24 skills under `.agents/skills/` via progressive disclosure. Canonical agents are orchestrated from `.agents/agents/*.md`:
```bash
/academic-orchestrator "Start a new paper about [topic]"
```
You can also invoke any specialized agent or atomic skill directly using standard slash triggers (e.g., `/research-agent`, `/writing-agent`, `/review-agent`, `/academic-prd`, `/academic-plan`, `/academic-data-validator`, `/academic-format-validator`).

---

## Example: Creating a New Paper End-to-End

This walkthrough illustrates the full pipeline execution for an empirical paper.

### 1. Start the Orchestrator

```
/academic-orchestrator "New paper: benchmarking vector databases for RAG applications"
```

### 2. Answer the PRD Interview (Gate G1)

`academic-prd` conducts an interview to establish the paper's foundation: title, research questions, target venue, citation style, and methodology.
After completing, review `papers/paper-vector-rag/prd.md` to clear **Gate G1**.

### 3. Review the Implementation Plan (Gate G2)

The orchestrator invokes `academic-plan` to generate `plan.md`. Review deliverables and acceptance criteria to clear **Gate G2**.

### 4. Literature Research (Phase 2)

`research-agent` runs `academic-researcher` against OpenAlex API, extracting relevant works into:
- `papers/paper-vector-rag/research/literature.md`
- `papers/paper-vector-rag/research/references.bib`

### 5. Outline Approval (Phase 3 → Gate G3)

`writing-agent` runs `academic-writer` (outline mode) to create `draft/outline.md` with section allocation, primary themes, and draft Scope Cards. Approve to clear **Gate G3**.

### 6. Full-Text Drafting with Scope Cards & CEI (Phase 4)

`writing-agent` drafts each section sequentially:
1. **Scope Cards**: Every section begins with a mandatory `<!-- SCOPE_CARD ... -->` setting the strict Level of Analysis.
2. **Motivation Triggers & CEI**: Every paragraph follows the Claim → Evidence → Interpretation pattern and justifies design choices using the 6 Motivation Triggers.
3. **Figures & EDA**: `academic-media` generates publication-quality visual elements in `output/figures/`.

### 7. Citation & Data Integrity Gates (Phases 5 & 5.5 → Gates G4 & G4.5)

- **Gate G4 (Citation↔Bibliography)**: `review-agent` runs `academic-citation-manager` and `academic-bibliography-manager`. Confirms 0 orphan citations and 0 phantom entries in `review/citation-report.md`.
- **Gate G4.5 (Data Integrity Gate)**: `data-validation-agent` runs `academic-data-validator` (`data_congruence_gate.py`). Verifies float two-way integrity (Table/Figure defined vs referenced), table arithmetic, and text-data congruence in `review/data-congruence-report.md`.

### 8. Humanization & Writing Quality Audit (Phase 6)

- `academic-humanizer` performs local per-section passes and a transversal global pass.
- `academic-writing-reviewer` executes a deterministic audit:
  ```bash
  python .agents/skills/academic-writing-reviewer/scripts/audit_writing.py \
    papers/paper-vector-rag/draft \
    --output papers/paper-vector-rag/review/writing-review-report.md
  ```
  Audits AI markers (`AIM`), repetitions (`REP`), metric tensions (`NUM`), and unglossed jargon (`JAR-01`).

### 9. 6-D Peer Review & Continuous Revision Loop (Phase 7 → Gate G5)

`review-agent` runs `academic-reviewer`, simulating a 5-persona panel (EIC + 3 reviewers + Devil's Advocate).
Dimension 5 directly incorporates findings from `writing-review-report.md`.
- **Loop**: If any gate fails or review score < 65, the Continuous Revision Loop rewrites affected sections with `writing-agent` and re-audits until **Complete Approval**.

### 10. Output Format Gate & Document Export (Phase 8)

`format-validation-agent` executes `academic-format-validator` (`validate_formats.py`) ensuring zero markdown syntax errors, clean LaTeX compilation, and valid Word (.docx) schemas.
`paper-generator-agent` produces the deliverables in `output/`:
- `output/paper.tex` / `output/paper.pdf`
- `output/paper.docx`

### 11. Process Documentation (Phase 9)

The orchestrator compiles `process-record.md`, logging all human checkpoints, gate results, and revision history.

---

## Troubleshooting

### `ModuleNotFoundError` when a Python script runs

The virtual environment is not active. Run:

```bash
source .venv/bin/activate
```

### Citation Gate fails with orphan or phantom citations

Run the standalone gate check:

```bash
python .agents/skills/academic-citation-manager/scripts/citation_gate.py \
  papers/paper-{slug}/draft papers/paper-{slug}/research/references.bib
```

Ensure all citations in draft match BibTeX keys, and all keys in `.bib` are cited.

### Data Congruence Gate reports orphan or dangling floats

Run:

```bash
python .agents/skills/academic-data-validator/scripts/check_float_integrity.py papers/paper-{slug}/draft
```

Ensure every Table and Figure defined in `07-tables.md` or `08-figure-legends.md` is referenced in the text, and every mention in prose matches a defined float.

### Output Format Gate reports errors

Run:

```bash
python .agents/skills/academic-format-validator/scripts/validate_formats.py papers/paper-{slug}
```

Examine `review/format-validation-report.md` for specific formatting or compilation errors.
