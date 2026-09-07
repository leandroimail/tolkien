# Tutorial: Producing a Scientific Article from Scratch with tolkien

This tutorial provides a complete end-to-end walkthrough to conceive, research, structure, draft, validate, and export a scientific paper using **tolkien**, advancing safely through the 7 quality gates until final acceptance.

> **Language / Idioma:** English | [Versão em Português](../pt-BR/tutoriais/produzindo-artigo-do-zero.md)

---

## 1. Learning Objectives

By the end of this lesson, you will have produced a fully audited scientific manuscript:
- Requirements and research questions formalized in `prd.md` (Gate G1).
- Execution roadmap and operational checklist in `plan.md` (Gate G2).
- Validated, deduplicated literature base in `references.bib`.
- Approved modular structure with Scope Cards in `outline.md` (Gate G3).
- Substantive draft with CEI architecture and zero orphan citations (Gate G4).
- 100% mathematical congruence between prose numbers and tables/figures (Gate G4.5).
- Simulated peer review panel report with composite score $\ge 65/100$ and zero critical issues (Gate G5).
- Clean manuscript exported to Word (.docx) or LaTeX (.pdf) passing the `Output Format Gate`.

---

## 2. Prerequisites

Before starting, ensure your environment meets the following requirements:

1. **Python 3.10 or higher:**
   ```bash
   python3 --version
   ```
2. **tolkien dependencies installed in the virtual environment:**
   Run the bootstrap script from the repository root:
   ```bash
   bash resources/install_skills_deps.sh
   source .venv/bin/activate
   ```
3. **AI Harness configured:**
   tolkien runs natively in your chosen environment:
   - **Google Antigravity** (with `.agents/`)
   - **Claude Code CLI** (with `.claude/`)
   - **OpenAI Codex** (with `.codex/`)
   - **OpenCode** (with `.opencode/`)

---

## 3. Step-by-Step Walkthrough

### Step 1: Initialize the Paper Project

Choose a unique identifier (*slug*) for your paper (for example, `paper-neural-robustness`). Create the directory structure under `papers/`:

```bash
mkdir -p papers/paper-neural-robustness/{research,draft,review,output,resources}
```

> **Checkpoint:** Verify the directories by running:
> ```bash
> ls -d papers/paper-neural-robustness/*/
> ```
> The output should list: `draft/`, `output/`, `research/`, `resources/`, `review/`.

---

### Step 2: Requirements Interview — Academic PRD (Phase 0)

Start by activating the orchestrator or PRD skill:
> `/academic-prd "Configure a new paper on adversarial robustness in neural networks"`

Answer the interactive interview prompts:
- Primary research questions.
- Target venue (e.g., IEEE Transactions, Elsevier, Springer, ACM).
- Paper type (empirical, systematic review, theoretical).
- Available data or experimental code.

The agent synthesizes requirements into `papers/paper-neural-robustness/prd.md`.

> **Checkpoint (Gate G1):** Review `papers/paper-neural-robustness/prd.md`, examine scope, and approve by typing:
> `"Approve PRD"` or `"Gate G1 approved"`.

---

### Step 3: Implementation Plan Generation (Phase 1)

With the PRD validated, generate the operational roadmap:
> `/academic-plan`

The agent reads `prd.md` and generates `papers/paper-neural-robustness/plan.md`, detailing tasks, deliverables, and acceptance criteria for all phases.

> **Checkpoint (Gate G2):** Review the task sequence in `plan.md`. Confirm by typing:
> `"Implementation plan approved"`.

---

### Step 4: Literature Research and Curation (Phase 2)

Activate the research agent to query academic literature:
> `/research-agent "Search literature on adversarial training and certified robustness"`

The agent queries the OpenAlex API, resolves DOIs, and produces two artifacts:
1. `papers/paper-neural-robustness/research/literature.md` (analytical synthesis).
2. `papers/paper-neural-robustness/research/references.bib` (cleaned, enriched BibTeX file).

> **Checkpoint:** Inspect the `.bib` file by running:
> ```bash
> head -n 25 papers/paper-neural-robustness/research/references.bib
> ```
> Verify that entries include complete fields (`author`, `title`, `journal`/`booktitle`, `year`, `doi`).

---

### Step 5: Section Structuring and Scope Cards (Phase 3)

Ask the writing agent to outline the manuscript:
> `/writing-agent "Create paper outline with Scope Cards per section"`

The agent generates `papers/paper-neural-robustness/outline.md`. Each section includes a mandatory **Scope Card**:

```markdown
<!-- SCOPE CARD
section: 01-introduction
core_claim: Traditional adversarial training degrades under large-scale distribution shifts.
required_citations: [Goodfellow2015, Madry2018]
excluded_topics: [Convex optimization convergence proofs]
connection: Sets the stage for theoretical foundations in 02-theory.
-->
```

> **Checkpoint (Gate G3):** Ensure each section has clearly delineated boundaries and confirm by typing:
> `"Outline and Scope Cards approved"`.

---

### Step 6: Modular Section Drafting with CEI Architecture (Phase 4)

With the structure approved, initiate section drafting:
> `/writing-agent "Draft all manuscript sections"`

The `writing-agent` drafts sections sequentially under `papers/paper-neural-robustness/draft/`:
- `00-abstract.md`
- `01-introduction.md`
- `02-theory.md`
- `03-methodology.md`
- `04-findings.md`
- `05-discussion.md`
- `06-conclusion.md`
- `07-tables.md`
- `08-figure-legends.md`

Every substantive paragraph follows the **CEI** (*Claim $\rightarrow$ Evidence $\rightarrow$ Interpretation*) pattern.

> **Checkpoint:** Verify all draft section files exist:
> ```bash
> ls papers/paper-neural-robustness/draft/
> ```

---

### Step 7: Deterministic Citation and Data Validations (Phase 5)

Before peer review, run the automated verification gates:

1. **Gate G4 (Citation ↔ Bibliography Gate):**
   ```bash
   python .agents/skills/academic-citation-manager/scripts/citation_gate.py \
     papers/paper-neural-robustness/draft \
     papers/paper-neural-robustness/research/references.bib
   ```
   *Expected outcome:* `GATE PASS: 0 orphan citations, 0 missing keys.`

2. **Gate G4.5 (Data Integrity Gate):**
   ```bash
   python .agents/skills/academic-data-validator/scripts/data_congruence_gate.py \
     papers/paper-neural-robustness
   ```
   *Expected outcome:* `DATA CONGRUENCE: PASS` (0 discrepancies between text and tables).

> **Checkpoint:** Confirm `review/citation-report.md` and `review/data-congruence-report.md` report zero blocking issues.

---

### Step 8: Humanization and Prose Quality Audit (Phase 6)

Naturalize writing and audit stylistic quality:

1. **Humanization Pass:**
   > `/academic-humanizer "Adjust cadence, senior academic register, and eliminate AI markers in draft"`

2. **Static Prose Audit:**
   ```bash
   python .agents/skills/academic-writing-reviewer/scripts/audit_writing.py \
     papers/paper-neural-robustness/draft \
     --output papers/paper-neural-robustness/review/writing-review-report.md
   ```

> **Checkpoint:** Verify that `writing-review-report.md` attests a score $\ge 70/100$ and status `PASS_FOR_DIM5`.

---

### Step 9: 6-D Peer Review Panel and Revision Loop (Phase 7)

Convene the simulated reviewer panel:
> `/review-agent "Run complete 6-dimension academic peer review"`

The agent simulates the Editor-in-Chief, three specialist reviewers, and the Devil's Advocate, critiquing Rigor, Methodology, Originality, Coherence, Writing, and Compliance.

- **If verdict is `ACCEPT` (Score $\ge 65/100$ and 0 critical issues):** Gate G5 passes.
- **If verdict is `REVISE_AND_RESUBMIT`:** The orchestrator dispatches `writing-agent` to address roadmap items and returns automatically to Step 7.

> **Checkpoint (Gate G5):** Confirm `papers/paper-neural-robustness/review/review-report.md` displays `Verdict: Accept`.

---

### Step 10: Final Deliverables Compilation (Phases 8 & 9)

With all gates cleared, compile the submission deliverables:
> `/paper-generator "Export final paper in Word DOCX and LaTeX PDF with double-blind formatting"`

The agent runs the `Output Format Gate` and compiles final files into `papers/paper-neural-robustness/output/`:
- `output/paper.pdf`
- `output/paper.tex`
- `output/paper.docx`

> **Checkpoint (Output Format Gate):**
> Validate structural integrity:
> ```bash
> python .agents/skills/academic-format-validator/scripts/validate_formats.py \
>   papers/paper-neural-robustness
> ```
> Expected output: `Output Format Gate: PASS (0 blocking, 0 warnings)`.

---

## 4. Expected Final Directory Layout

Upon completing this tutorial, your paper directory will contain:

```text
papers/paper-neural-robustness/
├── prd.md                              ← Approved PRD [Gate G1]
├── plan.md                             ← Completed task roadmap [Gate G2]
├── outline.md                          ← Section structure & Scope Cards [Gate G3]
├── research/
│   ├── literature.md                   ← Literature synthesis via OpenAlex
│   └── references.bib                  ← Enriched BibTeX bibliography
├── draft/
│   ├── 00-abstract.md to 06-conclusion.md ← Prose sections in CEI format
│   ├── 07-tables.md                    ← Study tables
│   └── 08-figure-legends.md            ← Figure captions
├── review/
│   ├── citation-report.md              ← Gate G4 report (0 orphan citations)
│   ├── data-congruence-report.md       ← Gate G4.5 report (100% data congruence)
│   ├── writing-review-report.md        ← Dimension 5 writing quality report
│   ├── review-report.md                ← 6-D review report [Gate G5: Accept]
│   └── format-validation-report.md     ← Output Format Gate report
├── output/
│   ├── paper.pdf                       ← Final compiled PDF
│   ├── paper.tex                       ← Clean LaTeX source
│   ├── paper.docx                      ← Final formatted Word manuscript
│   └── figures/                        ← Vector and raster figures
└── process-record.md                   ← Human-AI collaboration and gate audit log
```

---

## 5. Next Steps

1. **Customize Style Guides:** Add `papers/paper-neural-robustness/resources/style-guide.md` to guide author tone and domain-specific terminology.
2. **Conference Template Adaptation:** Use `latex-template-converter` if migrating to specific conference formats (IEEEtran, ACM sigconf, Springer LNCS, NeurIPS).
3. **Format Hooks:** Keep lifecycle validation hooks enabled in your environment to maintain syntax and structural integrity across every turn.
