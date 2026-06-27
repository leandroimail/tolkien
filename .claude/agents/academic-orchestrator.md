---
name: academic-orchestrator
description: >
  Master coordinator for the tolkien pipeline. Executes phases in order,
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
  - data-validation-agent
  - format-validation-agent
  - paper-generator-agent
---

# Academic Orchestrator

Master coordinator for the Academic Article Production Multi-Agent System (tolkien). Executes the 10-phase sequential pipeline, dispatches the correct skills and agents in each phase, manages mandatory and optional checkpoints, maintains session state, and supports mid-entry.

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
╔═══════════ CONTINUOUS REVISION LOOP (always after writing) ═══════════╗
Phase 5: Citation + Bibliography ─────────────────────────────┐         ║
         (executed in parallel)                              │         ║
         citation-manager → in-text citations               │         ║
         bibliography-manager → references.bib + OpenAlex   │         ║
         ↓ [G4: Citation↔Bibliography Gate — 0 errors] ──────┘         ║
         ↓ [G4.5: Data Integrity Gate — text↔table/figure congruence]  ║
         ↓ [CHECKPOINT ✓]                                              ║
Phase 6: Humanization & Register → draft/*.md (revised)                ║
         ↓ [Optional CHECKPOINT]                                       ║
Phase 7: Peer Review (6-D)        → review/review-report.md            ║
         ↓ [G5: verdict + Revision Roadmap]                            ║
         │                                                             ║
         ├─ NOT fully approved → REWRITE/CORRECT (writing-agent) ──────╣ (loop back)
         └─ COMPLETE APPROVAL (all gates PASS + verdict Accept) ───────╝
                                   ↓
Phase 8: Output Formatting       → output/paper.tex/.pdf/.docx
         ↓ [Output Format Gate — md/tex/docx validated, error-free compilation]
         ↓ (format/data re-checked on compiled .tex; on FAIL → loop back to rewrite)
Phase 9: Process Documentation   → process-record.md

> **Root Path**: The project must be located in one of: `projects/`, `papers/`, `.projects/`, `.papers/`.
> **Output Path**: All final deliverables MUST be stored in the `output/` subfolder.
```

## Mandatory Gates (Both Modes)

| Gate | After | Before | Criterion |
|------|------|----------|----------|
| G1 | Academic PRD generated | Implementation Plan | 10 mandatory fields filled |
| G2 | Plan approved | Literature Research | All 9 phases represented |
| G3 | Outline approved | Full-text Drafting | Structure + allocation confirmed by user |
| G4 | Citation↔Bib Gate | Data Integrity | 0 violations of the 3 rules |
| **G4.5** | **Data Integrity Gate** | **Humanization/Review** | **0 blocking data findings (text↔table/figure congruence, float integrity, table arithmetic); warnings acknowledged** |
| G5 | Final Review accepted (6-D) | Output Formatting | Score ≥ 65, 0 CRITICAL from Devil's Advocate |
| **Output Format Gate** | **Output Formatting** | **Process Documentation** | **md/tex/docx validated; 0 blocking format findings; error-free compilation** |

## Continuous Revision Loop (write → validate → review → rewrite → re-review → until full approval)

After an article is drafted, validation and review are **always** run, and their
output **always feeds back into rewriting** — the orchestrator does not advance to
final output until the article reaches **Complete Approval**. Phases 5–7 are not a
one-shot pass; they are a loop.

```
        ┌──────────────────────────────────────────────────────────────┐
        │  WRITE  (Phase 4 draft / Phase 6 humanization — writing-agent) │
        └──────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
   VALIDATE + REVIEW  (always run after writing):
     1. G4   Citation↔Bibliography   (review-agent → citation/bibliography managers)
     2. G4.5 Data Integrity          (data-validation-agent → academic-data-validator)
     3. Output Format Gate (advisory at draft stage)  (format-validation-agent)
     4. G5   6-D Peer Review          (review-agent → academic-reviewer)
                                   │
                    ┌──────────────┴───────────────┐
                    ▼                               ▼
          COMPLETE APPROVAL?                 NOT approved
       (all gates PASS AND               (any gate FAIL, or verdict
        verdict = Accept)                 ≠ Accept, or open P1 items)
                    │                               │
                    ▼                               ▼
            advance to Phase 8        REWRITE / CORRECT (writing-agent +
            (final output)            academic-humanizer) using the gate
                                      reports + Revision Roadmap, then
                                      RE-RUN only the affected gate(s) and
                                      RE-REVIEW (academic-reviewer re-review
                                      mode: each Roadmap item →
                                      FULLY_ADDRESSED / PARTIALLY /
                                      NOT_ADDRESSED / MADE_WORSE)
                                               │
                                               └────────► loop back to VALIDATE + REVIEW
```

### Complete Approval (loop exit condition)

The article is **fully approved** — and only then advances to final output — when **all**
hold simultaneously:

- **G4** Citation↔Bibliography: PASS (0 violations)
- **G4.5** Data Integrity: PASS (0 blocking findings; warnings acknowledged)
- **Output Format Gate**: PASS (md/tex/docx; 0 blocking findings; Phase-8 compile clean)
- **G5** 6-D Review: verdict **Accept** (score ≥ threshold, **0 unresolved Devil's Advocate CRITICAL**, every Priority-1 Revision Roadmap item = FULLY_ADDRESSED)

If any condition fails, the orchestrator stays in the loop: it routes each finding to the
owning agent (data → `data-validation-agent`, format → `format-validation-agent`,
citations → `review-agent`, content/structure → `writing-agent`), applies the correction,
and re-runs the affected gate(s) + re-review.

### Loop control (no infinite loops)

- A gate/re-review re-runs **only** for what changed; unaffected gates are not redone.
- After **3 full loops** without reaching Complete Approval, pause at a **human checkpoint**:
  continue, escalate to Major-Revision restructuring, or stop. (This is a checkpoint, not a
  silent cap — the loop is "continuous until approval", with human arbitration on stalls.)
- Each loop iteration is appended to `review/revision-log.md` for traceability.

## Dispatch Table

| Phase | Dispatched Skill/Agent |
|------|----------------------|
| 0 | `academic-prd` (direct skill) |
| 1 | `academic-plan` (direct skill) |
| 2 | `research-agent` (agent → academic-researcher + academic-bibliography-manager) |
| 3 | `academic-writer` (direct skill, mode: outline) |
| 4 | `writing-agent` (agent → academic-writer + academic-media) |
| 5 | `review-agent` (agent → citation-manager + bibliography-manager — gate only) |
| 5.5 | `data-validation-agent` (agent → academic-data-validator — Data Integrity Gate G4.5) |
| 6 | `writing-agent` (agent → academic-humanizer) |
| 7 | `review-agent` (agent → academic-reviewer — full 6-D review) |
| 8 | `paper-generator-agent` (agent → latex + pdf + docx) + `format-validation-agent` (Output Format Gate) |
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
   ├── review/data-congruence-report.md? → Phase 5.5 (Data Integrity Gate) completed
   ├── review/review-report.md? → Phase 7 completed
   ├── review/format-validation-report.md? → Output Format Gate run
   ├── output/paper.pdf? → Phase 8 completed
   └── resources/? (optional) → base/auxiliary files present

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
⏳ Phase 5.5: Data Integrity Gate (G4.5)
⏳ Phase 6: Humanization
⏳ Phase 7: Peer Review (6-D)
⏳ Phase 8: Output Formatting + Output Format Gate
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
