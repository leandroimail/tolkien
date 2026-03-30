# Academic Article Production Multi-Agent System (AAPMAS)

The **Academic Article Production Multi-Agent System (AAPMAS)** is a powerful multi-agent framework designed to support the complete production cycle of academic and scientific papers. It is fully compatible with both **Claude Code** (CLI) and **OpenCode**, using a standardized structure of specialized agents and atomic skills.

## 🚀 Core Methodology: Academic SDD

AAPMAS follows an adapted **Spec-Driven Development (SDD)** approach for scientific writing. The process is strictly sequential and traceable:

1.  **Academic PRD** (`prd.md`): Defines the "what" (research questions, constraints, style).
2.  **Implementation Plan** (`plan.md`): Translation of the PRD into a step-by-step roadmap.
3.  **Execution Pipeline**: Sequential drafting, research, and validation with mandatory human checkpoints.

---

## 🤖 Agents

Agents are high-level coordinators that orchestrate multiple skills to achieve specific goals. They can be invoked directly via their triggers or managed by the Orchestrator.

| Agent | Purpose | Primary Triggers |
| :--- | :--- | :--- |
| **`academic-orchestrator`** | **Master Coordinator**. Executes the full 10-phase pipeline and manages gates. | `/academic-orchestrator`, `"start academic pipeline"`, `/status`, `"write full article"` |
| **`research-agent`** | Specializes in literature search, triage, and bibliography synthesis. | `/research-agent`, `"search literature"`, `"find papers about"`, `"research for paper"` |
| **`writing-agent`** | Focused on full-text drafting and scientific media (figures/EDA) generation. | `/writing-agent`, `"write section"`, `"draft article"`, `"write and humanize"` |
| **`review-agent`** | Conducts 5-dimension peer review and validates citation consistency. | `/review-agent`, `"review article"`, `"peer review"`, `"verify citations"` |
| **`paper-generator-agent`** | Converts the reviewed draft into a finalized PDF/DOCX using LaTeX or Word. | `/paper-generator`, `"generate final paper"`, `"compile LaTeX"`, `"export paper"` |

---

## 🛠️ Specialized Skills

Skills are atomic capabilities that perform specific tasks within the pipeline.

### Pipeline Skills
- **`academic-prd`**: Conducts a setup interview to define article requirements. (`/academic-prd`)
- **`academic-plan`**: Generates a detailed implementation plan from a PRD. (`/academic-plan`)
- **`academic-researcher`**: Systematic search using the OpenAlex API. (`/academic-researcher`)
- **`academic-writer`**: Drafts sections (IMRaD or thematic) with field-specific register. (`/academic-writer`)
- **`academic-citation-manager`**: Validates in-text citations against the bibliography. (`/academic-citation-manager`)
- **`academic-bibliography-manager`**: Manages and enriches `.bib` files via OpenAlex. (`/academic-bibliography-manager`)
- **`academic-reviewer`**: Simulates a reviewer panel for deep artifact evaluation. (`/academic-reviewer`)
- **`academic-humanizer`**: Adjusts tone and removes AI-writing markers. (`/academic-humanizer`)
- **`academic-media`**: Generates publication-quality figures, schematics, and EDA. (`/academic-media`)

### Tool Skills
- **`latex`**: Full LaTeX compilation and formatting support.
- **`latex-template-converter`**: Adapts documents to conference-specific templates.
- **`pdf` / `docx` / `xlsx`**: Comprehensive manipulation of common document formats.

---

## 🛤️ The 10-Phase Sequential Pipeline

AAPMAS ensures quality through a structured flow with **5 Mandatory Gates (Checkpoints)**:

1.  **Phase 0-1 (The Map)**: PRD Generation ➔ Implementation Plan [Gate G1 & G2]
2.  **Phase 2-3 (The Foundation)**: Literature Research ➔ Outline & Architecture [Gate G3]
3.  **Phase 4-5 (The Draft)**: Section Drafting ➔ Citation & Bib Cross-Validation [Gate G4]
4.  **Phase 6-7 (The Quality)**: Humanization ➔ Full 5-D Peer Review [Gate G5]
5.  **Phase 8-9 (The Finalized Output)**: Output Formatting (LaTeX/PDF) ➔ Process Documentation.

---

## 📂 Project Structure

Each article project follows a standardized folder layout to ensure state persistence:

```text
paper-{slug}/
├── prd.md                    ← Paper requirements
├── plan.md                   ← Execution roadmap & checklist
├── research/                 ← Literature, search strategy, and references.bib
├── draft/                    ← Markdown sections (abstract, intro, methods, etc.)
├── review/                   ← Review reports and revision logs
├── output/                   ← Final PDF, LaTeX source, and figures
└── process-record.md         ← Human-AI collaboration history
```

---

## ⚙️ Configuration & Environment

AAPMAS is configured via the following directories:
- **`.agents/`**: Standard configuration for OpenCode.
- **`.claude/`**: Mirror configuration for Claude Code (CLI).

### Prerequisites
To ensure all skills work correctly (especially for LaTeX and Media generation), run the setup script:
`bash resources/install_skills_deps.sh`

### How to use
Simply call the Orchestrator to start a new project or resume an existing one:
> `/academic-orchestrator "Start a new research article about multi-agent systems"`
