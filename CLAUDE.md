# Academic Article Production Multi-Agent System (tolkien)

The **Academic Article Production Multi-Agent System (tolkien)** is a powerful multi-agent framework designed to support the complete production cycle of academic and scientific papers, running natively on **Claude Code CLI** via the `.claude/` configuration directory.

## Core Methodology: Academic SDD

tolkien follows an adapted **Spec-Driven Development (SDD)** approach for scientific writing. The process is strictly sequential and traceable:

1. **Academic PRD** (`prd.md`): Defines the "what" (research questions, constraints, style).
2. **Implementation Plan** (`plan.md`): Translation of the PRD into a step-by-step roadmap.
3. **Execution Pipeline**: Sequential drafting, research, and validation with mandatory human checkpoints.

---

## Agents

Agents are high-level coordinators that orchestrate multiple skills to achieve specific goals. Invoke them directly in the Claude Code prompt using their trigger phrases.

| Agent | Purpose | Primary Triggers |
| :--- | :--- | :--- |
| **`academic-orchestrator`** | **Master Coordinator**. Executes the full 10-phase pipeline and manages gates. | `/academic-orchestrator`, `"start academic pipeline"`, `/status`, `"write full article"` |
| **`research-agent`** | Specializes in literature search, triage, and bibliography synthesis. | `/research-agent`, `"search literature"`, `"find papers about"`, `"research for paper"` |
| **`writing-agent`** | Focused on full-text drafting and scientific media (figures/EDA) generation. | `/writing-agent`, `"write section"`, `"draft article"`, `"write and humanize"` |
| **`review-agent`** | Conducts 6-dimension peer review and validates citation consistency. | `/review-agent`, `"review article"`, `"peer review"`, `"verify citations"` |
| **`data-validation-agent`** | Validates congruence of the text with the data presented (numbers vs tables/figures); runs the Data Integrity Gate (G4.5). | `/data-validation-agent`, `"validate data congruence"`, `"check data integrity"` |
| **`format-validation-agent`** | Always-on formatting validation across Markdown, LaTeX and Word (.docx); runs the Output Format Gate. | `/format-validation-agent`, `"validate formatting"`, `"check format"`, `"validate docx"` |
| **`paper-generator-agent`** | Converts the reviewed draft into a finalized PDF/DOCX using LaTeX or Word. | `/paper-generator`, `"generate final paper"`, `"compile LaTeX"`, `"export paper"` |
| **`web-browser-search-agent`** | Web search and browser automation for grey literature, full-text retrieval, and DOI checks. | `/web-browser-search`, `"search the web"`, `"browse URL"`, `"validate DOI online"` |

---

## Specialized Skills

Skills are atomic capabilities that perform specific tasks within the pipeline. All skills are defined under `.claude/skills/` and invoked via `/skill-name` in Claude Code.

### Pipeline Skills
- **`academic-prd`**: Conducts a setup interview to define article requirements. (`/academic-prd`)
- **`academic-plan`**: Generates a detailed implementation plan from a PRD. (`/academic-plan`)
- **`academic-researcher`**: Systematic search using the OpenAlex API. (`/academic-researcher`)
- **`academic-writer`**: Drafts sections (IMRaD or thematic) with field-specific register, Scope Cards, and CEI architecture. (`/academic-writer`)
- **`academic-citation-manager`**: Validates in-text citations against the bibliography. (`/academic-citation-manager`)
- **`academic-bibliography-manager`**: Manages and enriches `.bib` files via OpenAlex. (`/academic-bibliography-manager`)
- **`academic-data-validator`**: Validates congruence of text with the data presented — numbers vs tables/figures, internal consistency, float integrity (Data Integrity Gate G4.5). (`/academic-data-validator`)
- **`academic-format-validator`**: Always-on formatting validation for Markdown, LaTeX and Word (.docx) — the Output Format Gate. (`/academic-format-validator`)
- **`academic-writing-reviewer`**: Read-only writing quality auditor and prose critic for academic papers. Detects AI markers, cross-section repetition, scope drift, unmotivated claims, and narrative tensions; feeds Dimension 5 of the 6-D review. (`/academic-writing-reviewer`, `"audit writing"`, `"check prose quality"`)
- **`academic-reviewer`**: Simulates a reviewer panel for deep 6-dimension artifact evaluation. (`/academic-reviewer`)
- **`academic-humanizer`**: Adjusts tone and removes AI-writing markers (local and global passes). (`/academic-humanizer`)
- **`academic-media`**: Generates publication-quality figures, schematics, and EDA. (`/academic-media`)

### Tool Skills
- **`latex`**: Full LaTeX compilation, formatting, and error resolution. (`/latex`)
- **`latex-template-converter`**: Adapts documents to conference-specific templates. (`/latex-template-converter`)
- **`pdf`**: PDF text/table extraction, merging, splitting, watermarking, and creation. (`/pdf`)
- **`docx`**: Word document creation, editing, and formatting. (`/docx`)
- **`xlsx`**: Spreadsheet reading, editing, and formula computation. (`/xlsx`)
- **`web-search`**: Web search returning ranked results with snippets and URLs. (`/web-search`)
- **`web-browser-search`**: Unified search and page interaction. (`/web-browser-search`)
- **`duckducksearch`**: DuckDuckGo search with filters. (`/duckducksearch`)
- **`agent-browser`**: Browser automation and extraction. (`/agent-browser`)
- **`playwright-cli`**: Playwright browser automation and testing. (`/playwright-cli`)
- **`creating-skills`**: Framework for developing, validating, and deploying agent skills. (`/creating-skills`)
- **`multi-ide-artifacts`**: Cross-IDE artifact design, synchronization, and migration. (`/multi-ide-artifacts`)

---

## The 10-Phase Sequential Pipeline

tolkien ensures quality through a structured flow with **mandatory Gates (Checkpoints)**:

1. **Phase 0-1 (The Map)**: PRD Generation → Implementation Plan [Gate G1 & G2]
2. **Phase 2-3 (The Foundation)**: Literature Research → Outline & Architecture [Gate G3]
3. **Phase 4-5 (The Draft)**: Section Drafting (Scope Cards & CEI) → Citation & Bib Cross-Validation [Gate G4] → Data Integrity [Gate G4.5]
4. **Phase 6-7 (The Quality)**: Humanization (Local & Global) → Writing Quality Audit (`academic-writing-reviewer`) → Full 6-D Peer Review [Gate G5]
5. **Phase 8-9 (The Finalized Output)**: Output Formatting (LaTeX/PDF/DOCX) [Output Format Gate — always-on] → Process Documentation.

> **Always-on validation.** The Data Integrity Gate (G4.5) and the Output Format Gate are
> non-skippable. The Output Format Gate also runs automatically via a hook in every harness
> (Claude Code `.claude/settings.json`; Codex `.codex/hooks.json`; OpenCode `.opencode/plugins/`).

> **Continuous Revision Loop.** After an article is drafted, validation and review **always**
> run, and their output **always feeds rewriting**. Phases 5–7 form a loop:
> *write → validate (G4, G4.5) → 6-D review (G5) → rewrite/correct (writing-agent) → re-review*,
> repeating until **Complete Approval**: G4 PASS **and** G4.5 PASS **and** Output Format Gate
> PASS **and** review verdict = Accept (0 unresolved Devil's Advocate CRITICAL, all Priority-1
> Roadmap items FULLY_ADDRESSED). The orchestrator does not advance to final output before then.
> After 3 loops without approval it pauses at a human checkpoint (continue / restructure / stop).
> Owned by `academic-orchestrator`, routing findings to `data-validation-agent`,
> `format-validation-agent`, `review-agent`, and `writing-agent`.

---

## Project Structure

Each article project MUST be created within one of the following root directories:
- `projects/`
- `papers/`
- `.projects/`
- `.papers/`

Inside the chosen root, a subfolder with the project or paper name (slug) MUST be created. All generated files MUST be stored in an `output/` subfolder within the project's directory.

```text
{root}/paper-{slug}/
├── prd.md                    ← Paper requirements
├── plan.md                   ← Execution roadmap & checklist
├── research/                 ← Literature, search strategy, and references.bib
├── draft/                    ← Markdown sections (abstract, intro, methods, etc.)
├── review/                   ← Review reports and revision logs
├── output/                   ← ALL generated deliverables (PDF, LaTeX, etc.)
├── resources/                ← (OPTIONAL) Base/auxiliary files provided by researcher
└── process-record.md         ← Human-AI collaboration history
```

> **About `resources/`**: This is an **optional** directory for base and auxiliary files. It is not mandatory — the pipeline works without it. Use it to store: reference guidelines (e.g. `style-guide.md`, `anti-style-guide.md`, `human-decisions.md`), raw data, pre-existing documents, or any researcher-provided material that aids paper construction.

---

## Configuration & Environment

tolkien for Claude Code is configured via the **`.claude/`** directory and root `CLAUDE.md`:
- **`.claude/skills/`**: All specialized Agent Skills (`SKILL.md`, scripts, and references).
- **`.claude/agents/`**: Claude Code custom subagents (`.md` files).
- **`.claude/settings.json`**: Hooks and behavioral configuration for the Claude Code harness.

### Project Root Directory Structure

```
tolkien/
├── .claude/                    ← Claude Code configuration (this harness)
│   ├── agents/                 ← Claude subagents (.md)
│   ├── skills/                 ← Claude skills (.claude/skills/*/SKILL.md)
│   └── settings.json           ← Claude Code hooks and validation settings
├── .agents/                    ← Canonical configuration (Codex, OpenCode, Antigravity)
│   ├── agents/                 ← Canonical agent descriptors (.md)
│   └── skills/                 ← Atomic Agent Skills (SKILL.md, scripts, references)
├── .codex/                     ← OpenAI Codex configuration
│   ├── agents/                 ← Codex subagent descriptors (.toml)
│   └── hooks.json              ← Codex lifecycle hooks
├── .opencode/                  ← OpenCode configuration
│   ├── agents/                 ← OpenCode subagent descriptors (.md)
│   └── plugins/                ← OpenCode validation plugins (.js)
├── resources/                  ← Installation scripts and dependencies
│   ├── install_skills_deps.sh  ← Main dependency installer (run this first)
│   └── requirements_skills.txt  ← Python package list
├── templates/                  ← Ready-to-use templates for paper projects
│   ├── research_request_form.md ← Structured form for PRD interview
│   └── systematic_review_protocol.yaml ← PRISMA-aligned protocol template
├── .venv/                      ← Python virtual environment (created by install script)
├── docs/                       ← System documentation
├── papers/                     ← Paper projects (one subdirectory per project)
├── projects/                   ← Alternative root for paper projects
├── AGENTS.md                   ← Canonical rules & system documentation
└── CLAUDE.md                   ← Claude Code root instructions (this file)
```

### Prerequisites

To ensure all skills work correctly (especially for LaTeX, PDF, and Media generation), run the setup script from the repository root:

```bash
bash resources/install_skills_deps.sh
```

The script creates or updates the Python virtual environment at `.venv` and installs the required Python packages there.

### Virtual Environment

Before running any Python-based skill scripts manually, activate the virtual environment:

```bash
source .venv/bin/activate
```

When the environment is active, `python` and `pip` refer to the project-local `.venv`. If you open a new terminal session, activate `.venv` again before running scripts or skills that depend on Python packages.

To leave the environment:

```bash
deactivate
```

### How to Use

Call the Orchestrator in the Claude Code prompt to start a new project or resume an existing one:

```
/academic-orchestrator "Start a new research article about multi-agent systems"
```
