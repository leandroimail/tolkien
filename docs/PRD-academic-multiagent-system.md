# Technical PRD: Multi-Agent System for Scientific Article Production (AAPMAS)

**Version:** 1.0
**Date:** 2026-03-29
**Status:** Draft for review

---

## 1. Executive Summary

The **Academic Article Production Multi-Agent System (AAPMAS)** is a multi-agent harness for supporting the production of academic and scientific papers, runnable in **Claude Code** and **OpenCode**. The system follows a **Spec-Driven Development (SDD)** approach adapted to the academic context: the process starts with an **Academic PRD** (paper requirements document), which generates an implementation plan with tasks, and then executes the writing pipeline sequentially with mandatory human confirmation checkpoints.

The system is composed of **atomic skills** (specialized capabilities) and **agents** (configurations that orchestrate those skills). Skills are the building blocks; agents decide which skills to use and in what order.

---

## 2. Problem

Scientific article production is a complex, multidisciplinary process involving literature research, argument structuring, writing, reference management, peer review, and output formatting. Today:

- There is no structured, traceable workflow for this process with AI support
- Existing skills and agents are fragmented, overlapping, and uncoordinated
- There are no deterministic validations ensuring integrity between citations and bibliography
- There are no human confirmation checkpoints between critical stages
- The state of the work-in-progress article is not persisted in a structured way

---

## 3. Objectives

### 3.1 Primary Objectives

- Implement a complete sequential pipeline for scientific article production
- Create consolidated skills with no overlap and clear responsibilities
- Guarantee deterministic validations at each stage (LaTeX compilation, citations, bibliography)
- Implement self-review and agentic review in each skill
- Keep article state in Markdown files per project
- Ensure cross-IDE compatibility: Claude Code (`.claude/skills/`) and OpenCode (`.agents/skills/`)

### 3.2 Out of Scope

- GUI or web interface
- Automatic submission to journals or conferences
- Managing multiple articles simultaneously in a single project
- Integration with external reference managers (Zotero, Mendeley)

---

## 4. Approach: Academic Spec-Driven Development

The system adapts SDD to the academic context:

```
┌─────────────────────────────────────────────────────────────┐
│  ACADEMIC SDD                                               │
│                                                             │
│  [Academic PRD]  →  [Implementation Plan]  →  [Execution]  │
│     prd.md              plan.md + tasks         pipeline    │
│                                                             │
│  Equivalent to:                                             │
│  spec.md          →  implementation steps  →  code/write   │
└─────────────────────────────────────────────────────────────┘
```

**Academic PRD** works as the paper requirements document - it defines what will be written, for whom, and under which constraints.

**Implementation Plan** translates the PRD into sequential tasks with phases, deliverables, and completion criteria.

**Execution** runs the pipeline phase by phase, with mandatory human checkpoints.

---

## 5. System Architecture

### 5.1 Layers

```
┌──────────────────────────────────────────────────────────────┐
│  LAYER 3: AGENTS                                             │
│  academic-orchestrator (auto + interactive)                  │
│  research-agent | writing-agent | review-agent               │
│  paper-generator-agent                                       │
├──────────────────────────────────────────────────────────────┤
│  LAYER 2: PIPELINE SKILLS                                    │
│  academic-prd | academic-plan | academic-researcher          │
│  academic-writer | academic-citation-manager                 │
│  academic-bibliography-manager | academic-reviewer           │
│  academic-humanizer | academic-media                         │
├──────────────────────────────────────────────────────────────┤
│  LAYER 1: TOOL SKILLS (already implemented)                  │
│  latex | latex-template-converter | pdf | docx | xlsx        │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 Sequential Pipeline

```
Phase 0: Academic PRD           → prd.md
         ↓ [CHECKPOINT ✓]
Phase 1: Implementation Plan    → plan.md
         ↓ [CHECKPOINT ✓]
Phase 2: Literature Research    → research/literature.md + references.bib
         ↓ [CHECKPOINT ✓]
Phase 3: Outline & Architecture → draft/outline.md
         ↓ [CHECKPOINT ✓]
Phase 4: Full-text Drafting     → draft/*.md (section by section)
         ↓ [CHECKPOINT ✓]
Phase 5: Citation + Bibliography ────────────────────────────┐
         (runs in parallel)                                 │
         citation-manager → in-text citations               │
         bibliography-manager → references.bib + OpenAlex  │
         ↓ [GATE: cross-validation citation↔bibliography]   ┘
         ↓ [CHECKPOINT ✓]
Phase 6: Humanization & Register → draft/*.md (revised)
         ↓ [CHECKPOINT ✓]
Phase 7: Peer Review             → review/review-report.md
         ↓ [review + re-review if needed]
         ↓ [CHECKPOINT ✓]
Phase 8: Output Formatting       → output/paper.tex/.pdf/.docx
         ↓ [CHECKPOINT ✓]
Phase 9: Process Documentation   → process-record.md
```

### 5.3 State Structure (Markdown)

Each article has a project folder with the following structure:

```
paper-{slug}/
├── prd.md                    ← Academic PRD (paper requirements)
├── plan.md                   ← Implementation plan + tasks
├── research/
│   ├── literature.md         ← sources found, triage, synthesis
│   ├── search-strategy.md    ← search strategy, inclusion/exclusion criteria
│   └── references.bib        ← BibTeX (source of truth for references)
├── draft/
│   ├── outline.md            ← approved structure, word allocation
│   ├── introduction.md
│   ├── methodology.md
│   ├── results.md
│   ├── discussion.md
│   ├── conclusion.md
│   └── abstract.md
├── review/
│   ├── review-report.md      ← 5-dimension review
│   └── revision-log.md       ← revision history
├── output/
│   ├── paper.tex
│   ├── paper.pdf
│   └── paper.docx
└── process-record.md         ← human-AI process documentation
```

---

## 6. Skill Specification

### 6.1 Complete Inventory

| # | Skill | Status | Absorbs (legacy) | Layer |
|---|---|---|---|---|
| 1 | `academic-prd` | **CREATE** | - | Meta |
| 2 | `academic-plan` | **CREATE** | - | Meta |
| 3 | `academic-researcher` | **CONSOLIDATE** | academic-researcher, academic-deep-research, openalex-paper-search | Pipeline |
| 4 | `academic-writer` | **CONSOLIDATE** | academic-writing, academic-writing-style, scientific-writing, academic-paper, scientific-paper | Pipeline |
| 5 | `academic-citation-manager` | **CONSOLIDATE** | citation-anchoring, citation-audit, citation-validator, citation-management | Pipeline |
| 6 | `academic-bibliography-manager` | **CONSOLIDATE** | citation-bibliography-generator, openalex-database | Pipeline |
| 7 | `academic-reviewer` | **CONSOLIDATE** | academic-paper-reviewer, scientific-validation, scientific-manuscript-review | Pipeline |
| 8 | `academic-humanizer` | **CONSOLIDATE** | humanize, humanize-academic-writing, finnish-humanizer | Pipeline |
| 9 | `academic-media` | **CONSOLIDATE** | scientific-eda, scientific-paper-figure-generator, scientific-schematics | Support |
| 10 | `latex` | ✅ READY | latex-build, latex-document, latex-paper-en, latex-pdf-compiler, latex-tables, latex-formatting | Tool |
| 11 | `latex-template-converter` | ✅ READY | latex-conference-template-organizer | Tool |
| 12 | `pdf` | ✅ READY | - | Tool |
| 13 | `docx` | ✅ READY | - | Tool |
| 14 | `xlsx` | ✅ READY | - | Tool |
| - | `scientific-email-polishing` | KEEP (utility) | - | Utility |

### 6.2 Skill: `academic-prd`

**Purpose:** Conduct a setup interview with the user and generate the article `prd.md`.

**Inspiration:** SDD `spec.md` - define the *what* before the *how*.

**Trigger:** `/academic-prd`, "create academic PRD", "configure article", "start pipeline"

**Required inputs (through interview):**
1. Paper type (research article, review, case study, systematic review, meta-analysis)
2. Discipline / field (e.g., medicine, engineering, psychology)
3. Research questions and primary objectives
4. Citation style (APA, MLA, Chicago, IEEE, Vancouver, ABNT)
5. Output format (LaTeX, DOCX, PDF, Markdown)
6. Conference/publication template (if applicable)
7. Supporting documents (guidelines, templates, reference papers)
8. Search strategy (keywords, databases, inclusion/exclusion criteria)
9. Paper structure (IMRaD, thematic, other)
10. Language(s) (main paper + bilingual abstract if needed)

**Outputs:**
- `prd.md` - article requirements document with all decisions recorded
- Decision summary printed in the terminal for confirmation

**Technique:** Uses BDD to formalize requirements:
```gherkin
Given a defined paper type and discipline,
When the user provides the required details,
Then the system generates a structured outline that follows field conventions.
```

**Deterministic validations:**
- Check that all 10 required fields are filled
- Check coherence: e.g. IEEE format requires LaTeX; ABNT allows DOCX
- Warn if a conference template is specified without a template file

**Self-review:** The agent rereads the generated `prd.md` and checks completeness before delivery.

**Checkpoint:** Mandatory - the user must confirm the `prd.md` before proceeding.

---

### 6.3 Skill: `academic-plan`

**Purpose:** Read `prd.md` and generate `plan.md` with phases, tasks, deliverables, and completion criteria.

**Trigger:** `/academic-plan`, "generate plan", "create article tasks"

**Inputs:** `prd.md` (required)

**Outputs:**
- `plan.md` - complete plan with numbered phases, per-phase tasks, deliverables, and acceptance criteria
- Tasks formatted as a Markdown checklist: `- [ ] Task`

**`plan.md` structure:**
```markdown
# Implementation Plan: {paper title}
## Phase 2: Literature Research
### Tasks
- [ ] Define search strategy
- [ ] Run OpenAlex search with keywords: {PRD keywords}
- [ ] Screen sources using criteria: {PRD criteria}
- [ ] Synthesize N primary sources
### Deliverable: research/literature.md + research/references.bib
### Completion criterion: N screened sources, validated .bib
```

**Deterministic validations:**
- Check that all 9 pipeline phases are represented in the plan
- Check that plan deliverables match the expected folder structure

**Self-review:** The agent verifies PRD coverage in the plan before delivery.

**Checkpoint:** Mandatory - the user confirms the plan before execution.

---

### 6.4 Skill: `academic-researcher`

**Purpose:** Systematic literature search, source triage, and bibliographic synthesis.

**Absorbed sources:** academic-researcher, academic-deep-research, openalex-paper-search

**OpenAlex integration (internal dependency):**
- Search by keywords, DOI, author, institution
- Keyless API: `curl "https://api.openalex.org/works?search={query}&mailto={email}"`
- Filter by year, type, open access, and impact factor (FWCI)
- Export metadata to BibTeX

**Trigger:** `/academic-researcher`, "search literature", "find papers about"

**Modes:**
- `socratic` - dialogue to refine the research question before searching
- `full` - complete systematic search with screening and synthesis
- `quick` - fast search for the N most relevant papers

**Inputs:** `prd.md`, keywords, inclusion/exclusion criteria

**Outputs:**
- `research/literature.md` - sources found + triage + synthesis
- `research/search-strategy.md` - documented strategy
- `research/references.bib` - raw BibTeX (to be validated by the bibliography manager)

**Deterministic validations:**
- Check that each exported entry has required fields: `author`, `title`, `year`, `journal/booktitle`
- Check that there are no duplicate entries (by DOI)
- Count N sources found vs. the minimum N defined in the PRD

**Self-review:** The agent evaluates thematic coverage of the literature against the PRD research questions.

**Agentic review:** The agent generates a gap report: "PRD question X does not have enough sources - suggest additional search?"

**Checkpoint:** Optional (interactive) or automatic (auto).

---

### 6.5 Skill: `academic-writer`

**Purpose:** Full article drafting, section by section, following the approved outline.

**Absorbed sources:** academic-writing, academic-writing-style, scientific-writing, academic-paper, scientific-paper

> **Consolidation note:** `scientific-paper` and `academic-paper` will be analyzed to remove duplicates. Antagonistic practices (e.g. different approaches to introductions) will be resolved in favor of best practices in the field. The consolidated skill should cover both research articles and reviews.

**Trigger:** `/academic-writer`, "write section", "draft article", "write introduction"

**Modes:**
- `section` - drafts a specific section
- `full` - drafts the entire article section by section with checkpoints between sections
- `continue` - continues an existing draft from `draft/outline.md`

**Inputs:** `prd.md`, `draft/outline.md`, `research/literature.md`, `research/references.bib`

**Outputs:** `draft/*.md` - one section per file

**Supported structures:**
- IMRaD (Introduction, Methods, Results, Discussion)
- Systematic review (Introduction, Methods, Results, Discussion, Conclusion)
- Thematic (free-form sections defined in the PRD)
- Case study

**Per-section checkers:**
- Introduction: includes context + gap + objective + paper structure
- Methods: includes design, sample/dataset, variables, reproducible protocol
- Results: contains no interpretation (facts and data only)
- Discussion: connects results to the research questions
- Conclusion: introduces no new data, includes limitations and future work

**Self-review:** After each section, the agent checks:
1. Does the section satisfy the approved outline?
2. Are all citations referenced as `[KEY]` or `\cite{key}`?
3. Is the academic register maintained (no colloquial language)?
4. Does the word count match the outline allocation?

**Agentic review:** After the full draft, the agent performs a cross-sectional review:
- Terminology consistency across sections
- Logical flow of argumentation
- Evidence gaps (claims without citations)

**Integration with `academic-media`:** When the writer detects a need for a figure/schematic/EDA, it emits an explicit call: `→ academic-media: {description of the required visual element}`

**Checkpoint:** Mandatory after the outline; optional after each section (interactive mode).

---

### 6.6 Skill: `academic-citation-manager`

**Purpose:** Manage and validate in-text citations - format, completeness, and consistency.

**Absorbed sources:** citation-anchoring, citation-audit, citation-validator, citation-management

**Trigger:** `/academic-citation-manager`, "check citations", "format in-text references"

**Responsibilities:**
- Track all occurrences of `\cite{key}` / `(Author, Year)` in the draft
- Validate citation format according to the PRD style (APA, IEEE, ABNT, etc.)
- Identify orphan citations (present in text but missing from `.bib`)
- Identify ghost citations (present in `.bib` but not cited in text)

**Cross-validation gate (with bibliography-manager):**
```
VERIFY: For every citation in the draft -> a matching entry exists in references.bib
VERIFY: For every entry in references.bib -> it is cited at least once in the draft
RESULT: ✅ Consistent | ❌ N inconsistencies found
```

**Outputs:**
- Validation report: `review/citation-report.md`
- Draft with corrected citations

**Deterministic validations:**
- Count unique citations vs. `.bib` entries
- Check style-specific formatting (e.g. APA: `(Author, Year)`, IEEE: `[N]`)
- Detect duplicates: same work cited with different keys

**Self-review:** The agent reruns the gate after corrections to confirm zero inconsistencies.

**Checkpoint:** Cross-validation gate is a mandatory checkpoint before review.

---

### 6.7 Skill: `academic-bibliography-manager`

**Purpose:** Manage and validate `references.bib` - completeness, format, and OpenAlex enrichment.

**Absorbed sources:** citation-bibliography-generator, openalex-database

**OpenAlex integration (internal dependency):**
- Resolve DOI -> complete metadata -> BibTeX
- Check article existence and retraction via `is_retracted`
- Enrich incomplete entries with OpenAlex data

**Trigger:** `/academic-bibliography-manager`, "validate bibliography", "generate BibTeX", "resolve DOI"

**Responsibilities:**
- Validate completeness of each BibTeX entry (required fields by type)
- Enrich incomplete entries via OpenAlex
- Detect and remove duplicates
- Format output according to the PRD style

**Required fields by BibTeX type:**
```
@article:       author, title, journal, year, volume, pages
@inproceedings:  author, title, booktitle, year
@book:           author/editor, title, publisher, year
@misc:           author, title, year, url, note (access)
```

**Outputs:**
- `research/references.bib` - validated and enriched
- Validation report: `review/bibliography-report.md`

**Deterministic validations:**
```bash
# Check required fields in each entry
python scripts/validate_bib.py research/references.bib

# Check duplicates by DOI
python scripts/check_bib_duplicates.py research/references.bib
```

**Self-review:** The agent rereads the entire `.bib` file and checks that zero entries are missing required fields.

**Checkpoint:** Runs before the cross-validation gate with the citation manager.

---

### 6.8 Skill: `academic-reviewer`

**Purpose:** Complete academic review of the article in 5 dimensions.

**Absorbed sources:** academic-paper-reviewer, scientific-validation, scientific-manuscript-review

**Trigger:** `/academic-reviewer`, "review article", "peer review", "evaluate paper"

**Review dimensions (5-D):**
1. **Scientific rigor** - methodology, reproducibility, statistical validity
2. **Argument coherence** - logical flow, claim-evidence chains
3. **Bibliographic integrity** - literature coverage, adequate citations
4. **Writing quality** - clarity, cohesion, academic register
5. **Format compliance** - adherence to the PRD template/style

**Modes:**
- `full` - full review across all 5 dimensions
- `focused` - review focused on specific dimensions (post-revision)
- `quick` - quick checklist before submission

**Outputs:**
- `review/review-report.md` - detailed report with scores per dimension and suggestions
- `review/revision-log.md` - revision history

**Self-review:** The agent checks internal consistency of the report before delivery.

**Agentic review:** A second pass after user revisions - checks whether the raised issues were addressed.

**Checkpoint:** Mandatory after the full review; mandatory after post-correction re-review.

---

### 6.9 Skill: `academic-humanizer`

**Purpose:** Adjust register, humanize, and naturalize academic writing.

**Absorbed sources:** humanize, humanize-academic-writing, finnish-humanizer

**Trigger:** `/academic-humanizer`, "humanize", "adjust register", "naturalize writing"

**Responsibilities:**
- Keep academic register while removing the artificial feel of AI-generated text
- Adapt tone to the discipline and paper type
- Preserve technical terminology
- Ensure voice consistency across the document

**Self-review:** The agent checks that no new factual information was introduced (only form changes).

**Checkpoint:** Optional - run before the final review or after the reviewer pass.

---

### 6.10 Skill: `academic-media`

**Purpose:** Create figures, schematics, diagrams, and exploratory data analyses for academic papers. It can be invoked by the writer or used independently.

**Absorbed sources:** scientific-eda, scientific-paper-figure-generator, scientific-schematics

**Trigger:** `/academic-media`, "create figure", "generate schematic", "exploratory analysis", "EDA"

**Modes:**
- `figure` - generate result figures (charts, plots)
- `schematic` - generate conceptual diagrams and workflows
- `eda` - run exploratory data analysis and generate visualizations

**Outputs:** Image files in `output/figures/` + generation code in `output/figures/scripts/`

**Deterministic validations:**
- Check that generated figures have caption, label, and a reference in the text (`\ref{fig:X}`)
- Check minimum resolution for publication (300 DPI)

**Self-review:** The agent checks that the figure matches the visual style of the template specified in the PRD.

**Integration:** Can be called directly (`/academic-media figure "description"`) or via the writer.

---

## 7. Agent Specification

### 7.1 Agent: `academic-orchestrator`

**Purpose:** Master coordinator of the pipeline - executes phases in order, dispatches the right skills, manages checkpoints, and maintains session state.

**Reference:** Based on `academic-pipeline v2.7` (`.agents_old/skills/academic-pipeline/skill.md`)

**Trigger:** `/academic-orchestrator`, "start academic pipeline", "write full article"

**Two operating modes:**

```
AUTO MODE
─────────
Runs the full pipeline automatically.
Pauses ONLY at mandatory checkpoints (5 gates).
Best for: users who want the final result with minimal intervention.

INTERACTIVE MODE (default)
──────────────────────────
Requests human confirmation at EACH phase.
Allows adjustments, feedback, and redirection between phases.
Best for: users who want full control, first-time use of the system.
```

**Mandatory checkpoints (both modes):**

| Gate | After | Before |
|---|---|---|
| G1 | Academic PRD generated | Implementation Plan |
| G2 | Implementation Plan approved | Literature Research |
| G3 | Outline approved | Full-text Drafting |
| G4 | Citation↔Bibliography gate (0 errors) | Humanization/Review |
| G5 | Final review accepted | Output Formatting |

**Optional checkpoints (interactive mode):**
- After literature review
- After each drafted section
- After humanization
- Before exporting the final format

**Orchestrator capabilities:**
- Detect the current project phase (mid-entry)
- Read `plan.md` to track progress
- Update checklist items in `plan.md` after each phase
- Generate `process-record.md` at the end with session history
- Handle mid-pipeline entry: "I already have the draft, I want review"

**Status dashboard** (available at any time with `/status`):
```
Pipeline Status: Paper "{title}"
─────────────────────────────────
✅ Phase 0: Academic PRD        (2026-03-29)
✅ Phase 1: Implementation Plan (2026-03-29)
🔄 Phase 2: Literature Research  (in progress)
   ├── ✅ Initial search: 47 papers
   ├── 🔄 Screening: 32/47
   └── ⏳ Synthesis: pending
⏳ Phase 3: Outline
...
```

**Skills used:**
- All pipeline skills (Layer 2)
- Tool skills as needed (Layer 1)

---

### 7.2 Agent: `research-agent`

**Purpose:** Specialized agent for the research phase - can be used independently of the orchestrator.

**Skills used:** `academic-researcher` + `academic-bibliography-manager`

**Trigger:** Invoked by the orchestrator in Phase 2, or directly by the user.

**Responsibility:** Produce validated `literature.md` + `references.bib` ready for the writer.

---

### 7.3 Agent: `writing-agent`

**Purpose:** Specialized agent for drafting - coordinates writer + media.

**Skills used:** `academic-writer` + `academic-media` (when needed) + `academic-humanizer`

**Trigger:** Invoked by the orchestrator in Phases 4-6, or directly by the user.

---

### 7.4 Agent: `review-agent`

**Purpose:** Specialized agent for review - executes the full review cycle.

**Skills used:** `academic-citation-manager` + `academic-bibliography-manager` + `academic-reviewer`

**Cycle:**
1. Citation↔Bibliography gate (deterministic)
2. 5-D review
3. Waits for corrections
4. Focused re-review

**Trigger:** Invoked by the orchestrator in Phases 5-7, or directly by the user for an existing paper.

---

### 7.5 Agent: `paper-generator-agent`

**Purpose:** Specialized agent for final paper generation in publishable format - converts the reviewed draft into compiled LaTeX, producing the final academic PDF.

**Skills used:** `latex` + `latex-template-converter` + `pdf`

**Trigger:** `/paper-generator`, "generate final paper", "compile LaTeX", "generate paper PDF", "export paper". Invoked by the orchestrator in Phase 8 (Output Formatting).

**Internal pipeline:**

```
1. Consolidate the draft
   ├── Read draft/*.md (all approved sections)
   ├── Assemble order: abstract -> introduction -> methodology
   │   -> results -> discussion -> conclusion
   └── Verify that all required sections exist

2. Select and configure the LaTeX template
   ├── Read prd.md -> identify conference/publication template
   ├── If a template is specified: invoke latex-template-converter
   │   to organize and configure the template
   └── If no template: use a standard academic LaTeX structure

3. Generate paper.tex
   ├── Convert Markdown content -> LaTeX
   │   ├── Sections -> \section{}, \subsection{}
   │   ├── Figures -> \includegraphics{} + \caption{} + \label{}
   │   ├── Tables -> tabular/booktabs environment
   │   ├── Equations -> equation/align environments
   │   └── Citations [KEY] -> \cite{key}
   ├── Insert references.bib via \bibliography{}
   ├── Configure \bibliographystyle{} according to the PRD style
   └── Write output/paper.tex

4. Compile LaTeX -> PDF
   ├── Run pdflatex (2 passes for cross-references)
   ├── Run bibtex / biber for the bibliography
   ├── Run pdflatex (2 final passes)
   └── Verify: compile without errors -> output/paper.pdf

5. Validate the generated PDF
   ├── Verify that paper.pdf exists and is not corrupted
   ├── Verify page count (>= 1)
   ├── Verify that all sections appear in the PDF
   └── Verify that bibliographic references were resolved

6. Optional DOCX generation
   └── If prd.md specifies DOCX as an additional output:
       invoke the docx skill to generate output/paper.docx
```

**Inputs:**
- `prd.md` - requirements (template, citation style, output format, language)
- `draft/*.md` - all paper sections reviewed and approved
- `research/references.bib` - bibliography validated by the review-agent
- `output/figures/` - images and figures generated by academic-media
- LaTeX template (if specified in the PRD)

**Outputs:**
- `output/paper.tex` - complete compilable LaTeX source
- `output/paper.pdf` - final PDF generated by pdflatex/xelatex
- `output/paper.docx` - Word version (optional, if specified in the PRD)
- `output/compilation-log.txt` - full compilation log for diagnostics

**Deterministic validations (LaTeX gate):**
```bash
# Compilation must finish with exit code 0
pdflatex -interaction=nonstopmode output/paper.tex
echo "Exit code: $?"   # must be 0

# PDF must exist and have size > 0
test -s output/paper.pdf && echo "PDF OK" || echo "PDF MISSING"

# Check for critical errors in the log
grep -c "! " output/compilation-log.txt  # must be 0

# Check for unresolved reference warnings
grep "Citation .* undefined" output/compilation-log.txt  # must be empty
grep "Reference .* undefined" output/compilation-log.txt # must be empty
```

**LaTeX gate (blocking):**
```
VERIFY: pdflatex compilation finishes with exit code 0
VERIFY: output/paper.pdf generated with size > 0
VERIFY: 0 critical errors in the log (lines starting with "! ")
VERIFY: 0 unresolved citations in the log
RESULT: ✅ Paper generated | ❌ Compilation failed - show errors and wait for correction
```

**Compilation error handling:**

| Error | Common cause | Agent action |
|---|---|---|
| `! Undefined control sequence` | Invalid LaTeX command in the draft | Identify the line and suggest a fix |
| `Citation X undefined` | Key does not exist in the .bib | Invoke academic-bibliography-manager to resolve it |
| `File X.sty not found` | LaTeX package not installed | List missing packages and instruct installation |
| `Overfull \hbox` | Line too long | Fix automatically (line breaks, hyphenation) |
| `Missing $ inserted` | Formula outside math mode | Identify and fix delimiters |

**Self-review:**
1. The agent checks that the generated PDF contains all sections expected in the outline
2. The agent checks page count vs. the PRD limit (if specified)
3. The agent checks that PDF metadata (title, author) is correct
4. The agent checks that all figures rendered correctly (no "??" placeholders in the PDF)

**Checkpoint:** The LaTeX gate is a mandatory checkpoint (G5.5) - the pipeline does not move to Process Documentation if compilation fails.

---

## 8. Integration Requirements

### 8.1 OpenAlex

OpenAlex exists as an **internal dependency** of two skills - it is not a standalone skill:

| Skill | OpenAlex use | Type of use |
|---|---|---|
| `academic-researcher` | Literature search by keywords, filters, citations | Search |
| `academic-bibliography-manager` | DOI resolution -> metadata -> BibTeX, retraction check | Enrichment |

**Base configuration (both skills):**
```bash
# Polite pool: 10 req/s with email
BASE_URL="https://api.openalex.org"
MAILTO="user@institution.edu"  # configurable in the PRD

# Example: resolve DOI
curl -s "${BASE_URL}/works/https://doi.org/10.1038/nature12345?mailto=${MAILTO}"
```

### 8.2 Citation ↔ Bibliography Gate

Cross-cutting business rule executed by `review-agent` before moving on to review:

```
RULE 1: For every key in \cite{key} in the draft -> there is an entry @{type}{key,...} in references.bib
RULE 2: For every key in references.bib -> there is at least 1 \cite{key} in the draft
RULE 3: For every entry in references.bib -> required fields by type are filled

EXPECTED RESULT: 0 violations of RULE 1, RULE 2, RULE 3
BLOCKING: Yes - pipeline does not advance if result != 0 violations
```

### 8.3 Deterministic Validations by Phase

| Phase | Validation | Blocking |
|---|---|---|
| PRD | 10 required fields filled | Yes |
| Plan | All 9 phases represented | Yes |
| Research | Minimum number of sources, .bib without duplicates | Yes |
| Drafting | Section checkers (see §6.5) | Partial |
| Citation | Citation↔Bibliography gate | Yes |
| LaTeX | Compile without errors (`pdflatex`) | Yes |
| PDF | Visual formatting check | No (alert only) |

---

## 9. Skill Creation Standard

### 9.1 Normative Reference: `creating-skills`

**Every creation, consolidation, or modification of a skill in AAPMAS must follow the concepts, principles, and specifications defined in the `creating-skills` skill** (`.claude/skills/creating-skills/` and `.agents/skills/creating-skills/`).

This skill is the **normative reference** for any skill implementation work in this project. It is not optional.

### 9.2 Mandatory Principles (extracted from `creating-skills`)

**1. Conciseness - context is a shared resource**
- Include only what the agent does not already know by default
- Ask for each line: "Does Claude need this? Does it already know it?"
- Focus on what is unique to the academic domain and the specific workflow

**2. Progressive Disclosure (3 loading levels)**

| Level | When it loads | Cost | Content |
|---|---|---|---|
| L1: Metadata | Always (startup) | ~100 tokens | YAML `name` + `description` |
| L2: Instructions | When the skill triggers | < 5,000 tokens | `skill.md` body |
| L3: Resources | On demand | Unlimited | `scripts/`, `references/`, `assets/` |

Rules:
- `skill.md` must have **fewer than 500 lines**
- Detailed content goes into `references/`
- References must be **one level deep** - no nested chains

**3. Appropriate Degrees of Freedom**
- High freedom (text guidance): multiple valid approaches
- Medium freedom (pseudocode/templates): a preferred pattern exists
- Low freedom (exact code): only one correct form

**4. Skill Directory Structure**

```
{skill-name}/
├── skill.md          ← main instruction (< 500 lines)
├── references/       ← detailed documentation on demand
│   └── *.md
├── scripts/          ← executable scripts (checkers, validators)
│   └── *.py / *.sh
└── assets/           ← templates, examples, static artifacts
    └── *
```

**5. Required Frontmatter**

```yaml
---
name: {skill-name}
description: >
  {precise description of when to use - trigger keywords}
  {include example phrases that trigger the skill}
allowed-tools: [Read, Write, Edit, Bash, ...]
metadata:
  version: "1.0"
  depends_on: "{dependent skills, separated by commas}"
---
```

**6. Required Sections in `skill.md`**
- `## When To Use` - explicit triggers
- `## When Not To Use` - clear exclusions to avoid incorrect activation
- `## Prerequisites` - what to gather before running
- Self-review protocol (deterministic + agentic)

**7. Rules for Consolidating Legacy Skills**
- Analyze every skill to be absorbed before consolidating
- Remove duplicates - if two skills teach the same thing, keep only the better version
- Remove antagonisms - if two skills have contradictory approaches, decide which one prevails and document why
- Keep the best deterministic practices from each absorbed skill
- Do not copy content Claude already knows (context overload)

**8. Validation Before Deployment**
Every new skill must be validated against the `creating-skills` criteria before being considered ready:
- Complete and correct frontmatter
- Well-defined triggers (no ambiguity)
- `skill.md` within the 500-line limit
- Scripts in `scripts/` if there is deterministic logic
- Tested in Claude Code AND OpenCode

### 9.3 Application to AAPMAS

For each skill listed in the Roadmap (§14), the implementation process is:

```
1. Read all legacy skills to be absorbed (see §15)
2. Identify: duplicates, antagonisms, best practices
3. Decide: what to keep, what to discard, what to unify
4. Implement following creating-skills (structure, frontmatter, limits)
5. Put deterministic validations in scripts/
6. Put extensive content in references/
7. Validate against creating-skills before finalizing
8. Synchronize .claude/skills/ ↔ .agents/skills/ via multi-ide-artifacts
```

---

## 11. Cross-IDE Compatibility

### 11.1 File Structure

```
.claude/skills/          ← Claude Code
.agents/skills/          ← OpenCode

Both must contain the same skills with the same content.
Use multi-ide-artifacts for synchronization and conversion.
```

### 11.2 Skill Format

All skills must follow the pattern defined in `creating-skills`:

```markdown
---
name: {skill-name}
description: {trigger description - when to use, keywords}
allowed-tools: [Read, Write, Edit, Bash, ...]
metadata:
  version: "1.0"
  depends_on: "{dependent skills}"
---

# {Skill Name}
...
```

### 11.3 Command Compatibility

All Bash scripts inside skills must be compatible with:
- macOS (zsh/bash) - `brew`-based dependencies
- Linux (bash) - `apt`/`pip`-based dependencies

Detection pattern:
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
else
  # Linux
fi
```

---

## 12. Self-Review Protocol

Each skill must implement self-review at two levels:

### Level 1: Deterministic Self-Review
- Automated checkers (scripts, counts, format validations)
- Binary result: ✅ / ❌
- Examples: LaTeX compilation, BibTeX field counts, citation↔bib gate

### Level 2: Agentic Self-Review
- The agent rereads its own output and evaluates quality
- Result: quality report with improvement suggestions
- Examples: thematic coverage of the literature, argumentative coherence of the draft

**Agentic self-review template:**
```
### Self-Review: {phase name}
- Completeness: {N/N criteria met}
- Quality: {qualitative assessment}
- Attention points: {list of items for human verification}
- Recommendation: ✅ Proceed | ⚠️ Review before proceeding
```

---

## 13. Acceptance Criteria (BDD)

```gherkin
Feature: Complete Pipeline

  Scenario: Creating an article from scratch
    Given a user starts /academic-orchestrator
    When they complete the setup interview
    Then prd.md is generated with 10 required fields filled
    And the user must confirm the prd.md before proceeding

  Scenario: Citation↔Bibliography validation
    Given a complete draft with citations
    And a references.bib with entries
    When the review-agent runs the validation gate
    Then every \cite{key} in the draft must have a matching entry in the .bib
    And every entry in the .bib must be cited in the draft
    And the pipeline does NOT advance if there are violations

  Scenario: LaTeX compilation
    Given output/paper.tex generated
    When the latex skill runs pdflatex
    Then it must compile without errors
    And it must generate a readable output/paper.pdf
    And the pipeline does NOT advance if there are compilation errors

  Scenario: Cross-IDE compatibility
    Given a skill created in .claude/skills/
    When multi-ide-artifacts synchronizes
    Then the same skill must exist in .agents/skills/
    And both versions must behave the same way

  Scenario: Mid-entry into the pipeline
    Given a paper already has a draft in draft/*.md
    When the user starts /academic-orchestrator
    Then the orchestrator detects the current phase
    And offers to continue from the correct phase
    And does not reprocess phases that are already complete
```

---

## 14. Implementation Roadmap

### Priority 1 - Meta-Skill Foundation (no dependencies)
1. `academic-prd` - foundation of the entire pipeline
2. `academic-plan` - depends only on `prd.md`

### Priority 2 - Research Skills
3. `academic-researcher` - consolidation + OpenAlex integration
4. `academic-bibliography-manager` - consolidation + OpenAlex DOI resolution

### Priority 3 - Writing Skills
5. `academic-writer` - major consolidation, requires duplicate analysis
6. `academic-citation-manager` - consolidation + deterministic gate
7. `academic-media` - consolidation, used as a dependency by the writer

### Priority 4 - Review and Quality Skills
8. `academic-reviewer` - consolidation
9. `academic-humanizer` - consolidation

### Priority 5 - Agents
10. `review-agent` - uses skills 4, 6, 8 (all ready)
11. `research-agent` - uses skills 3, 4 (ready)
12. `writing-agent` - uses skills 5, 7, 9 (ready)
13. `paper-generator-agent` - uses latex, latex-template-converter, pdf (all ready)
14. `academic-orchestrator` - uses all agents and skills (last)

### Priority 6 - Cross-IDE Sync
15. Synchronize `.claude/skills/` ↔ `.agents/skills/` via `multi-ide-artifacts`

---

## 15. Legacy Skill References

For implementing each skill, consult the following legacy skills in `.agents_old/skills/`:

| Skill to create | Read before implementing |
|---|---|
| `academic-prd` | `academic-pipeline/skill.md` (workflow section), `skills.md` (PRD section) |
| `academic-plan` | `academic-pipeline/skill.md` (stages and deliverables) |
| `academic-researcher` | `academic-researcher/`, `academic-deep-research/`, `openalex-paper-search/` |
| `academic-writer` | `academic-writing/`, `academic-writing-style/`, `scientific-writing/`, `academic-paper/`, `scientific-paper/` |
| `academic-citation-manager` | `citation-anchoring/`, `citation-audit/`, `citation-validator/`, `citation-management/` |
| `academic-bibliography-manager` | `citation-bibliography-generator/`, `openalex-database/` |
| `academic-reviewer` | `academic-paper-reviewer/`, `scientific-validation/`, `scientific-manuscript-review/` |
| `academic-humanizer` | `humanize/`, `humanize-academic-writing/`, `finnish-humanizer/` |
| `academic-media` | `scientific-eda/`, `scientific-paper-figure-generator/`, `scientific-schematics/` |
| `academic-orchestrator` | `academic-pipeline/skill.md` (orchestration structure and checkpoints) |
| `paper-generator-agent` | `latex/skill.md`, `latex-template-converter/skill.md`, `pdf/skill.md` (ready tool skills) |

---

## 16. Glossary

| Term | Definition |
|---|---|
| **Academic PRD** | Paper requirements document (equivalent to spec.md in SDD) |
| **SDD** | Spec-Driven Development - development approach guided by specification |
| **Gate** | Blocking validation that prevents pipeline progress if criteria are not met |
| **Checkpoint** | Mandatory or optional human confirmation point |
| **Deterministic self-review** | Automated verification with a binary result (script/count) |
| **Agentic self-review** | Qualitative evaluation of the agent's own output |
| **Citation↔Bibliography Gate** | Cross-validation between in-text citations and .bib entries |
| **Mid-entry** | Entering the pipeline at a phase other than the initial one |
| **AAPMAS** | Academic Article Production Multi-Agent System - system name |
