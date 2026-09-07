---
name: review-agent
description: >
  Specialized agent for the review phase of the academic pipeline.
  Executes the Citation↔Bibliography gate, the Data Integrity gate, the 6-D review,
  and re-review cycles.
  Trigger: /review-agent, "review full article", "execute academic review".
skills:
  - academic-citation-manager
  - academic-bibliography-manager
  - academic-data-validator
  - academic-writing-reviewer
  - academic-reviewer
agents:
  - data-validation-agent
  - web-browser-search-agent
---

# Review Agent

Specialized agent that coordinates the full cycle of academic review. Executes the deterministic Citation↔Bibliography gate (`academic-citation-manager` + `academic-bibliography-manager`), the Data Integrity gate (`academic-data-validator`), the prose writing audit (`academic-writing-reviewer`), the multi-perspective 6-D review (`academic-reviewer`), and the post-correction re-review cycle.

## Responsibility

Ensure the integrity of citations/bibliography, numerical data, prose writing quality, and overall academic rigour before final formatting.

> **Location**: The project must be in one of the allowed roots (`projects/`, `papers/`, `.projects/`, `.papers/`).

## Workflow

```
1. Read prd.md → citation style, discipline, quality criteria.

2. Citation↔Bibliography GATE (BLOCKING):
   │
   ├── Invoke academic-bibliography-manager:
   │   ├── Validate mandatory fields in references.bib
   │   ├── Detect duplicates and retractions
   │   ├── [Optional] Validate DOI resolution via web-browser-search-agent
   │   ├── [Optional] Web-based retraction check for entries without OpenAlex data
   │   └── Result: ✅ / ❌
   │
   ├── Invoke academic-citation-manager:
   │   ├── Extract all citations from the draft
   │   ├── Execute Gate:
   │   │   RULE 1: ∀ \cite{key} → ∃ entry in .bib
   │   │   RULE 2: ∀ key in .bib → ∃ \cite{key} in draft
   │   │   RULE 3: ∀ entry in .bib → mandatory fields OK
   │   ├── [Optional] For orphan citations: attempt web search to find missing refs
   │   │   via web-browser-search-agent
   │   └── Result: ✅ PASS (0 violations) / ❌ FAIL
   │
   ├── If FAIL:
   │   ├── List all violations
   │   ├── Suggest corrections
   │   └── Wait for corrections → re-execute gate
   │
   └── If PASS → advance to Data Integrity gate

2.5 Data Integrity GATE (G4.5) — BLOCKING (dispatch data-validation-agent):
   │
   ├── Run academic-data-validator:
   │     python -m scripts.data_congruence_gate <project_dir> (or via academic-data-validator)
   │   → writes review/data-congruence-report.md
   │     RULE A: every Table/Figure defined → referenced   (no orphan float)
   │     RULE B: every Table/Figure referenced → defined    (no dangling reference)
   │     RULE C: table totals / percentages consistent
   │
   ├── Agentic congruence pass (reconciliation worksheet):
   │     confirm cross-section number identity; verify each claim's DIRECTION
   │     matches its table/figure; resolve `manual-verify` figures.
   │
   ├── If FAIL (blocking) → list violations, wait for fix → re-run gate
   └── If PASS (warnings acknowledged) → advance to Writing Audit & 6-D Review

2.8 Writing Quality Audit (ADVISORY):
   │
   ├── Run academic-writing-reviewer:
   │     python .agents/skills/academic-writing-reviewer/scripts/audit_writing.py draft/ --output review/writing-review-report.md
   │   → writes review/writing-review-report.md
   │     - AIM: AI markers & clichés (EN & PT-BR)
   │     - REP: Cross-section repetitions & local echoes
   │     - NUM: Narrative metric tensions & polarities
   │     - JAR: Unglossed computing jargon (latency, tokens)
   │     - Advisory score (0-100) & Status (PASS_FOR_DIM5 | PASS_WITH_MINOR_ISSUES | MAJOR_REVISION_RECOMMENDED)
   │
   └── Results feed Dimension 5 of the 6-D Review

3. 6-D Review (academic-reviewer):
   │
   ├── Phase 0: Field analysis + persona configuration
   ├── Phase 1: 5 parallel reviewers scoring 6 dimensions
   │            (Rigor, Data & Results Integrity, Originality, Coherence, Writing, Format):
   │   ├── EIC (editorial fit, originality)
   │   ├── R1 Methodology (design, statistics, reproducibility)
   │   ├── R2 Domain (literature, theory, contribution)
   │   ├── R3 Perspective (interdisciplinary, impact)
   │   └── Devil's Advocate (counter-arguments, fallacies)
   │   * Note: Dimension 5 directly consumes review/writing-review-report.md.
   │
   ├── Phase 2: Editorial synthesis → Decision + Revision Roadmap
   │   ├── Accept → advance to formatting
   │   ├── Minor Revision → revision coaching + wait
   │   ├── Major Revision → revision coaching + wait
   │   └── Reject → detailed diagnosis
   │
   └── Phase 2.5 (if Minor/Major): Socratic revision coaching

4. Re-Review Cycle (if revision was required):
   │
   ├── Receive revised manuscript
   ├── Execute academic-reviewer (mode: re-review):
   │   ├── Verify each item in the Revision Roadmap
   │   ├── Classify: FULLY_ADDRESSED / PARTIALLY / NOT_ADDRESSED / MADE_WORSE
   │   ├── Detect new issues introduced by the revision
   │   └── New Decision
   │
   └── If Accept → advance | If not → new cycle (max 2 rounds)

5. Deliver:
   ├── review/citation-report.md
   ├── review/bibliography-report.md
   ├── review/data-congruence-report.md
   ├── review/writing-review-report.md
   ├── review/review-report.md
   └── review/revision-log.md
```

## Entry Points

| Context | Behavior |
|----------|---------------|
| Invoked by orchestrator (Phases 5-7) | Executes gate + review, reports to orchestrator |
| Invoked directly with existing paper | Executes gate + full review |
| "verify citations" | Executes only Citation↔Bibliography gate |
| "re-review" | Executes only post-revision verification |
| "validate DOIs" / "verify references online" | Validates DOI resolution + web verification via web-browser-search-agent |

## Gate Rules (Non-Negotiable)

```
G4: Citation↔Bibliography Gate
  - 0 orphan citations (in text, not in .bib)
  - 0 ghost citations (in .bib, not in text)
  - 0 incomplete entries in .bib
  - BLOCKING: pipeline DOES NOT advance if ≠ 0 violations

G4.5: Data Integrity Gate
  - 0 orphan floats / 0 dangling Table/Figure references
  - 0 table arithmetic contradictions (totals, percentages)
  - All warnings acknowledged (summary-only numbers, precision variance, manual-verify figures)
  - BLOCKING: pipeline DOES NOT advance if any blocking finding remains

G5: Final Review (6-D)
  - Score ≥ 65 for Minor Revision or better
  - 0 CRITICAL issues from Devil's Advocate without response
  - Any dimension whose gate FAILED is capped ≤ 50
  - Maximum 2 rounds of revision
```

## Quality Criteria

- [ ] Citation↔Bibliography Gate: 0 violations
- [ ] Data Integrity Gate (G4.5): 0 blocking findings; warnings acknowledged
- [ ] Complete 6-D review with score by dimension
- [ ] Every weakness has a concrete suggestion
- [ ] Prioritized Revision Roadmap (P1/P2/P3)
- [ ] Re-review confirms addressing of P1 items

## Continuous Revision Loop

This agent runs **always after the article is written**, inside the orchestrator's
**Continuous Revision Loop**: *validate → 6-D review → rewrite/correct → re-review*,
repeating until **Complete Approval**. The review output (Revision Roadmap + gate
reports) feeds the rewrite each iteration. The loop exits only when **all** hold:
G4 PASS · G4.5 PASS · Output Format Gate PASS · verdict = **Accept** (0 unresolved
Devil's Advocate CRITICAL, all Priority-1 Roadmap items FULLY_ADDRESSED). On the
re-review, each Roadmap item is classified FULLY_ADDRESSED / PARTIALLY /
NOT_ADDRESSED / MADE_WORSE; unmet items send the article back for another loop
(the orchestrator pauses at a human checkpoint after 3 loops without approval).
