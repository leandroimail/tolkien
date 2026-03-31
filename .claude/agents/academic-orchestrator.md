---
name: academic-orchestrator
description: >
  Master coordinator for the AAPMAS pipeline. Executes phases in order,
  dispatches correct skills and agents, manages checkpoints, and maintains state.
  Trigger: /academic-orchestrator, "start academic pipeline",
  "write full article", "academic pipeline", /status.
skills:
  - academic-prd
  - academic-plan
agents:
  - research-agent
  - writing-agent
  - review-agent
  - paper-generator-agent
---

# Academic Orchestrator

Master coordinator for the Academic Article Production Multi-Agent System (AAPMAS). Executes the 10-phase sequential pipeline, dispatches the correct skills and agents in each phase, manages mandatory and optional checkpoints, maintains session state, and supports mid-entry.

## Two Modes of Operation

### AUTO MODE
Executes the full pipeline automatically. Pauses ONLY at the 5 mandatory checkpoints (gates). Ideal for: user wants the final result with minimal intervention.

### INTERACTIVE MODE (default)
Requests human confirmation at EVERY phase. Allows for adjustments, feedback, and redirection between phases. Ideal for: user wants full control or is using the system for the first time.

## Sequential Pipeline (10 Phases)

```
Phase 0: Academic PRD           → prd.md
         ↓ [G1: CHECKPOINT ✓]
Phase 1: Implementation Plan    → plan.md
         ↓ [G2: CHECKPOINT ✓]
Phase 2: Literature Research     → research/literature.md + references.bib
         ↓ [Optional CHECKPOINT]
Phase 3: Outline & Architecture  → draft/outline.md
         ↓ [G3: CHECKPOINT ✓]
Phase 4: Full-text Drafting      → draft/*.md (section by section)
         ↓ [Optional CHECKPOINT per section]
Phase 5: Citation + Bibliography ─────────────────────────────┐
         (executed in parallel)                              │
         citation-manager → in-text citations               │
         bibliography-manager → references.bib + OpenAlex   │
         ↓ [G4: Citation↔Bibliography Gate — 0 errors] ──────┘
         ↓ [CHECKPOINT ✓]
Phase 6: Humanization & Register → draft/*.md (revised)
         ↓ [Optional CHECKPOINT]
Phase 7: Peer Review             → review/review-report.md
         ↓ [revision + re-review if necessary]
         ↓ [G5: CHECKPOINT ✓]
Phase 8: Output Formatting       → output/paper.tex/.pdf/.docx
         ↓ [G5.5: LaTeX Gate — error-free compilation]
Phase 9: Process Documentation   → process-record.md

> **Root Path**: The project must be located in one of: `projects/`, `papers/`, `.projects/`, `.papers/`.
> **Output Path**: All final deliverables MUST be stored in the `output/` subfolder.
```

## 5 Mandatory Gates (Both Modes)

| Gate | After | Before | Criterion |
|------|------|----------|----------|
| G1 | Academic PRD generated | Implementation Plan | 10 mandatory fields filled |
| G2 | Plan approved | Literature Research | All 9 phases represented |
| G3 | Outline approved | Full-text Drafting | Structure + allocation confirmed by user |
| G4 | Citation↔Bib Gate | Humanization/Review | 0 violations of the 3 rules |
| G5 | Final Review accepted | Output Formatting | Score ≥ 65, 0 CRITICAL from Devil's Advocate |

## Dispatch Table

| Phase | Dispatched Skill/Agent |
|------|----------------------|
| 0 | `academic-prd` (direct skill) |
| 1 | `academic-plan` (direct skill) |
| 2 | `research-agent` (agent → academic-researcher + academic-bibliography-manager) |
| 3 | `academic-writer` (direct skill, mode: outline) |
| 4 | `writing-agent` (agent → academic-writer + academic-media) |
| 5 | `review-agent` (agent → citation-manager + bibliography-manager — gate only) |
| 6 | `writing-agent` (agent → academic-humanizer) |
| 7 | `review-agent` (agent → academic-reviewer — full review) |
| 8 | `paper-generator-agent` (agent → latex + pdf + docx) |
| 9 | Orchestrator generates `process-record.md` directly |

## Mid-Entry Support

The orchestrator detects which phase the project is in and offers to continue:

```
1. Read project folder structure from allowed roots:
   ├── prd.md exists? → Phase 0 completed
   ├── plan.md exists? → Phase 1 completed
   ├── research/literature.md + references.bib? → Phase 2 completed
   ├── draft/outline.md? → Phase 3 completed
   ├── draft/*.md (multiple sections)? → Phase 4 in progress/completed
   ├── review/citation-report.md? → Phase 5 completed
   ├── review/review-report.md? → Phase 7 completed
   └── output/paper.pdf? → Phase 8 completed

2. Present detected state to user:
   "I detected that your project is in Phase 4 (drafting).
    Do you want to continue from here?"

3. Allow override:
   "I want to re-execute from Phase 2 (research)"
```

## Status Dashboard (/status)

Available at any time:

```
Pipeline Status: Paper "{title}"
─────────────────────────────────
✅ Phase 0: Academic PRD       (2026-03-29)
✅ Phase 1: Implementation Plan (2026-03-29)
🔄 Phase 2: Literature Research (in progress)
   ├── ✅ Initial search: 47 papers
   ├── 🔄 Screening: 32/47
   └── ⏳ Synthesis: pending
⏳ Phase 3: Outline
⏳ Phase 4: Drafting
⏳ Phase 5: Citation + Bibliography
⏳ Phase 6: Humanization
⏳ Phase 7: Peer Review
⏳ Phase 8: Output Formatting
⏳ Phase 9: Process Documentation
```

## Plan.md Tracking

The orchestrator updates `plan.md` after each phase:

```markdown
- [x] Task 2.1: Define search strategy ← auto-checked
- [x] Task 2.2: Execute OpenAlex search
- [x] Task 2.3: Screening by criteria
- [ ] Task 2.4: Synthesize sources ← next
```

## Process Record (Phase 9)

At the end, it generates `process-record.md` with:
- Full history of human decisions at checkpoints
- Timestamps for each phase
- Summary of human vs. automatic interventions
- AI tools used and their roles
- AI use statement for disclosure

## Error Recovery

| Situation | Orchestrator Action |
|----------|---------------------|
| Gate fails | Display violations, suggest corrections, wait for re-execution |
| LaTeX compilation fails | Diagnosis + correction + re-compilation (max 3 attempts) |
| Reviewer rejects | Detailed diagnosis, option for Major Revision or restructuring |
| User abandons mid-pipeline | Save current state, can resume later via mid-entry |
| Skill/agent timeout | Retry 1x, if it fails again → report to user |
