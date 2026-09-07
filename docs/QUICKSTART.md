# Quick Start — tolkien in 5 Minutes

> **Language / Idioma:** English | [Versão em Português](pt-BR/QUICKSTART.md)

---

## 5-Minute Crash Course

### 1. Install

Run from the tolkien repository root:

```bash
bash resources/install_skills_deps.sh
source .venv/bin/activate
```

The script installs all system packages (Tesseract, Poppler, TinyTeX, LibreOffice), Node.js packages, Playwright Chromium, and Python dependencies.

The `resources/` directory contains:
- `install_skills_deps.sh` — main installer script
- `requirements_skills.txt` — Python package list

**Templates:** Before starting, you can copy `templates/research_request_form.md` to prepare your paper requirements offline.

### 2. Start a New Paper

In Claude Code, OpenCode, Codex, or Antigravity, run:

```
/academic-orchestrator "Start a new paper about [your topic]"
```

The orchestrator will interview you for ~10 minutes to build `prd.md`, then guide the execution of the pipeline.

### 3. Work Through the Gates

The pipeline enforces mandatory quality checkpoints (Gates) and runs an automated **Continuous Revision Loop** for Phases 5–7:

| Gate | Stage | What to do |
|------|-------|-----------|
| **G1** | After PRD | Review `prd.md`. Confirm all 10 mandatory fields are correct. |
| **G2** | After Plan | Review `plan.md`. Confirm the 9-phase roadmap matches your intent. |
| **G3** | After Outline | Review `draft/outline.md`. Confirm section structure, word budgets, and Scope Cards. |
| **G4** | After Citations | Review `review/citation-report.md`. Ensure 0 orphan citations and 0 phantom entries. |
| **G4.5** | After Data Integrity | Review `review/data-congruence-report.md`. Verify text numbers match tables/figures, float two-way references, and table arithmetic. |
| **G5** | After Peer Review | Review `review/review-report.md`. If score < 65 or Devil's Advocate flags CRITICAL issues, the Continuous Revision Loop rewrites affected sections and re-reviews until complete approval. |
| **Output Format Gate** | After Deliverables | Review `review/format-validation-report.md`. Confirm Markdown, LaTeX, and Word (.docx) compile without errors. |

### 4. Find Your Output

All deliverables land in `output/`:

```
papers/paper-{slug}/output/
├── paper.pdf      # Final compiled PDF
├── paper.tex      # LaTeX source
├── paper.docx     # Word document
└── figures/       # Generated figures and diagrams
```

### Common Pitfalls

- **Forgetting to activate `.venv`** — Python skills will fail. Run `source .venv/bin/activate` first.
- **Skipping gate review** — Gates catch problems early. Read each report in `review/` before approving.
- **Wrong project root** — Paper projects must reside in `projects/`, `papers/`, `.projects/`, or `.papers/`.
- **Stale `references.bib`** — If you add citations to the draft manually, re-run `/academic-bibliography-manager` to enrich and validate the new entries.

### Key Commands at a Glance

```bash
# Full pipeline coordinator (recommended)
/academic-orchestrator "topic"

# Specialized agents
/research-agent          # Literature search, triage & bib synthesis
/writing-agent           # Section drafting (Scope Cards + CEI), humanization & audit
/review-agent            # Citation gate, data integrity gate & 6-D review
/data-validation-agent   # Data Integrity Gate (G4.5)
/format-validation-agent # Always-on Output Format Gate (md/tex/docx)
/paper-generator         # Final LaTeX/PDF/DOCX compilation

# Specialized skills
/academic-prd                    # PRD interview only
/academic-plan                   # Implementation plan generation
/academic-researcher             # OpenAlex literature search
/academic-writer                 # Drafting sections with CEI architecture
/academic-citation-manager       # Citation audit (Gate G4)
/academic-bibliography-manager   # BibTeX validation & enrichment
/academic-data-validator         # Data congruence & float integrity (Gate G4.5)
/academic-writing-reviewer       # Writing quality audit (AIM, REP, NUM, JAR)
/academic-humanizer              # Two-pass AI marker removal
/academic-reviewer               # 6-D peer review panel simulation
/academic-format-validator       # Format validation gate
/latex                           # LaTeX compile & debug
```
