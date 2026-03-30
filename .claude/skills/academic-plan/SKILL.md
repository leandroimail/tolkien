---
name: academic-plan
description: >
  Reads an approved Academic PRD (prd.md) and generates a structured implementation plan (plan.md) with
  phases, tasks, deliverables, and acceptance criteria for the academic paper pipeline.
  Triggers: /academic-plan, "generate plan", "create article tasks", "plan phases",
  "gerar plano", "criar tasks do artigo".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "1.0"
  depends_on: "academic-prd"
---

# Academic Plan

Generate `plan.md` from an approved `prd.md`. This is **Phase 1** of the pipeline — translating *what* (PRD) into *how* (sequenced tasks with deliverables).

## When To Use

- User has a confirmed `prd.md` and wants to plan the paper writing process
- User invokes `/academic-plan` or says "generate plan", "create tasks"
- After `academic-prd` completes successfully

## When Not To Use

- No `prd.md` exists → use `academic-prd` first
- User wants to start writing immediately → the plan must be approved first
- User wants to modify an existing plan → edit `plan.md` directly

## Prerequisites

- `paper-{slug}/prd.md` must exist and be approved (status: "approved" in frontmatter)
- Read and understand all PRD fields before generating the plan

## Method

### 1. Parse the PRD

Read `prd.md` and extract:
- Paper type and structure → determines which sections to plan
- Search strategy → determines scope of research phase
- Citation format and output format → determines formatting phase requirements
- Template → determines if template conversion is needed
- Languages → determines if bilingual abstract is needed
- Research questions → determines research depth

### 2. Generate Phase-by-Phase Plan

The plan MUST cover all **9 phases** of the pipeline (Phases 0-9). Use the template in [assets/plan-template.md](assets/plan-template.md).

**Phase mapping:**

| Phase | Skill(s) | Key Deliverable |
|-------|----------|----------------|
| 0 | academic-prd | `prd.md` (already done) |
| 1 | academic-plan | `plan.md` (this phase) |
| 2 | academic-researcher | `research/literature.md` + `research/references.bib` |
| 3 | academic-writer (outline) | `draft/outline.md` |
| 4 | academic-writer (full) | `draft/*.md` (all sections) |
| 5 | academic-citation-manager + academic-bibliography-manager | Validated citations + bibliography |
| 6 | academic-humanizer | `draft/*.md` (humanized) |
| 7 | academic-reviewer | `review/review-report.md` |
| 8 | paper-generator-agent | `output/paper.tex` + `output/paper.pdf` |
| 9 | (orchestrator) | `process-record.md` |

### 3. Generate Tasks per Phase

For each phase, create specific, actionable tasks derived from the PRD:

**Phase 2 tasks example (adapt based on PRD):**
```markdown
## Phase 2: Literature Research
### Tasks
- [ ] Define search strategy from PRD keywords: {keywords from prd.md}
- [ ] Execute OpenAlex search with filters: {date range, type, language}
- [ ] Screen results by inclusion criteria: {criteria from prd.md}
- [ ] Synthesize {N minimum} primary sources
- [ ] Export validated BibTeX entries to references.bib
### Deliverables
- `research/literature.md` — sources found + screening + synthesis
- `research/search-strategy.md` — documented strategy
- `research/references.bib` — BibTeX entries
### Acceptance Criteria
- ≥ {N} sources screened and triaged
- references.bib has 0 duplicate DOIs
- All entries have required BibTeX fields
### Checkpoint: User reviews literature before proceeding
```

**Adapt tasks to PRD specifics:**
- Systematic review → add PRISMA flow diagram task, quality assessment task
- Meta-analysis → add effect size extraction task, heterogeneity analysis task
- Case study → add case timeline task, clinical findings task
- If bilingual abstract → add separate translation/writing task in Phase 4
- If specific template → add template setup task in Phase 8

### 4. Set Word Allocations

Based on paper type and any page/word limits from the PRD, allocate words per section:

| Paper Type | Abstract | Intro | Methods | Results | Discussion | Conclusion |
|-----------|---------|-------|---------|---------|-----------|-----------|
| Research (8pg) | 200 | 800 | 1200 | 1500 | 1200 | 500 |
| Review (12pg) | 250 | 1000 | 500 | 3000 | 2000 | 500 |
| Short paper (4pg) | 150 | 400 | 600 | 800 | 600 | 300 |

Adjust based on template page limits. Include allocations in the Phase 4 tasks.

### 5. Validate the Plan

Run validation script:
```bash
uv run python -B scripts/validate_plan.py paper-{slug}/plan.md
```

Checks:
- All 9 phases (0-9) are represented
- Each phase has tasks, deliverables, and acceptance criteria
- Deliverable paths match the expected folder structure
- Checkpoints are marked for mandatory gates (G1-G5)

### 6. Self-Review

Before delivering, verify:
- [ ] All 9 pipeline phases are represented
- [ ] Tasks are specific (include PRD-derived values, not generic placeholders)
- [ ] Word allocations sum to a reasonable total for the paper type
- [ ] Mandatory checkpoints G1-G5 are present
- [ ] Deliverable paths match: `research/`, `draft/`, `review/`, `output/`
- [ ] Plan reflects all PRD constraints (template, language, structure)

**CHECKPOINT: Present plan summary and ask user to confirm before proceeding.**

## Quality Checklist

- [ ] 9/9 phases present
- [ ] `validate_plan.py` returns 0 errors
- [ ] Tasks derived from PRD (not generic)
- [ ] Word allocations realistic for paper type
- [ ] `plan.md` written to `paper-{slug}/plan.md`
- [ ] User confirmed plan

## Outputs

- `paper-{slug}/plan.md` — complete implementation plan with task checklists

## Integration

After confirmation:
- The orchestrator uses `plan.md` to track progress through the pipeline
- Each phase's tasks are checked off as they complete
- `academic-orchestrator` reads `plan.md` for mid-entry detection
