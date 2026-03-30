---
name: academic-reviewer
description: >
  Full academic review of the article in 5 dimensions with multiple perspectives.
  Supports full review, re-review (post-revision verification), quick assessment, and
  focused review. Simulates a reviewer panel with Editor-in-Chief + 3 reviewers + Devil's Advocate.
  Trigger: /academic-reviewer, "review article", "peer review", "evaluate paper",
  "review paper", "critique paper", "verify revision".
allowed-tools: [Read, Write, Edit, Bash, Grep]
metadata:
  version: "1.0"
  depends_on: "academic-writer, academic-citation-manager, academic-bibliography-manager"
---

# Academic Reviewer

Multi-perspective academic review simulating a full peer review process. Consolidates logic from academic-paper-reviewer (5-reviewer panel), scientific-validation (methodological rigor), and scientific-manuscript-review (IMRaD quality).

## When To Use

- Full review of an article before submission
- Post-revision verification (re-review) to confirm that corrections were addressed
- Quick quality assessment of a paper
- Review focused on a specific dimension (methodology, argumentation, etc.)

## When Not To Use

- To draft the article → use `academic-writer`
- To validate citations/bibliography → use `academic-citation-manager` + `academic-bibliography-manager`
- To humanize text → use `academic-humanizer`

## Prerequisites

1. **Complete Draft** — `draft/*.md` (all sections)
2. **`prd.md`** — for discipline context and objectives
3. **Citation↔Bibliography Gate** — must be ✅ PASS before review

## Modes

| Mode | Trigger | Output |
|------|---------|--------|
| `full` | "full review" | 5 reports + Editorial Decision + Revision Roadmap |
| `re-review` | "verify revision" | Response checklist + decision |
| `quick` | "quick assessment" | Checklist + main issues (15 min) |
| `focused` | "review methodology" | Report focused on specific dimensions |

## Method

### Phase 0: Field Analysis & Persona Configuration

1. Read full paper
2. Identify: discipline, paradigm, typology, maturity
3. Configure 5 reviewer personas dynamically:
   - **EIC**: editorial fit, originality, relevance
   - **R1 (Methodology)**: design, statistical validity, reproducibility
   - **R2 (Domain)**: literature coverage, theoretical framework, contribution
   - **R3 (Perspective)**: interdisciplinary connections, practical impact
   - **Devil's Advocate**: counter-arguments, fallacies, confirmation bias

### Phase 1: Parallel 5-D Review

Each reviewer evaluates independently (without cross-referencing):

#### 5 Assessment Dimensions

| # | Dimension | Weight | Primary Evaluator |
|---|----------|------|-------------------|
| 1 | Scientific Rigor | 25% | R1 (Methodology) |
| 2 | Argumentative Coherence | 20% | R2 (Domain) + Devil's Advocate |
| 3 | Bibliographic Integrity | 20% | R2 (Domain) |
| 4 | Writing Quality | 20% | EIC + R3 |
| 5 | Format Compliance | 15% | EIC |

#### Scoring Scale (0-100)

| Range | Descriptor |
|-------|-----------|
| 90-100 | Exceptional — publication-ready |
| 75-89 | Strong — minor revisions needed |
| 60-74 | Adequate — significant revisions needed |
| 40-59 | Weak — major revisions or restructuring |
| 0-39 | Inadequate — fundamental problems |

### Phase 2: Editorial Synthesis & Decision

The editorial_synthesizer consolidates the 5 reports:
1. Identify consensus (4+ reviewers agree) vs. divergence
2. Arbitrate disputed questions
3. CRITICAL issues from Devil's Advocate block Accept

#### Decision Verdicts

| Verdict | Criteria |
|---------|----------|
| **Accept** | Score ≥ 80, 0 CRITICAL issues, no Devil's Advocate blocks |
| **Minor Revision** | Score 65-79, issues addressable in 1 round |
| **Major Revision** | Score 50-64, restructuring needed |
| **Reject** | Score < 50, fundamental problems |

### Phase 2.5: Revision Coaching (Socratic)

If Decision = Minor/Major Revision:
1. Identify the 3 most important questions
2. Socratic guide: "After reading the comments, what surprised you the most?"
3. Help prioritize revisions
4. Generate prioritized Revision Roadmap

## Re-Review Mode

For post-revision verification:

```
Input: Revision Roadmap + revised manuscript
Process:
  For each item in the Roadmap:
    Priority 1 (Required): FULLY_ADDRESSED | PARTIALLY | NOT_ADDRESSED | MADE_WORSE
    Priority 2 (Suggested): ≥ 80% must have a response
    Priority 3 (Nice): Verify but does not block
Output: Verification Report + New Decision
```

## Self-Review

### Deterministic
- [ ] Each reviewer covers a different perspective (no duplicate criticisms)
- [ ] Editorial decision based on reports (no fabrication)
- [ ] Every weakness has a concrete suggestion for improvement
- [ ] Devil's Advocate CRITICAL issues reflected in the decision

### Agentic
- Internal consistency of the report
- Balance between strengths and weaknesses
- Professional and constructive tone

## Output

```markdown
### Review Report
- **Overall Score**: N/100
- **Dimension Scores**: [Rigor: N | Coherence: N | Bibliography: N | Writing: N | Format: N]
- **Verdict**: Accept | Minor Revision | Major Revision | Reject
- **Critical Issues**: N items
- **Revision Roadmap**:
  - Priority 1 (Required): items
  - Priority 2 (Suggested): items
  - Priority 3 (Nice-to-fix): items
```

## References

- `references/review-criteria.md` — framework of criteria by paper type
- `references/scoring-rubrics.md` — 0-100 rubrics with descriptors
- `references/devils-advocate.md` — Devil's Advocate protocol
