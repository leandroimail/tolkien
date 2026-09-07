---
name: academic-reviewer
description: >
  Full academic review of the article in 6 dimensions with multiple perspectives.
  Supports full review, re-review (post-revision verification), quick assessment, and
  focused review. Simulates a reviewer panel with Editor-in-Chief + 3 reviewers + Devil's Advocate.
  Trigger: /academic-reviewer, "review article", "peer review", "evaluate paper",
  "review paper", "critique paper", "verify revision".
allowed-tools: [Read, Write, Edit, Bash, Grep]
metadata:
  version: "1.0"
  depends_on: "academic-writer, academic-citation-manager, academic-bibliography-manager"
---

# Virtualenv

Note: Python scripts for this skill must be executed within the project's virtual environment.
Activate the environment with:

```bash
source .venv/bin/activate
```

Alternatively, use `uv run python -B ...` with the `.venv` active.

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

### Phase 1: Parallel 6-D Review

Each reviewer evaluates independently (without cross-referencing).

#### 6 Assessment Dimensions (canonical — single 0-100 scale)

> This table is the **single source of truth** for dimensions and weights. The
> rubrics in `references/quality_rubrics.md` and `references/review_criteria_framework.md`
> use exactly these six dimensions and weights. Weights sum to 100.

| # | Dimension | Weight | Primary Evaluator |
|---|----------|------|-------------------|
| 1 | Scientific Rigor & Methodology | 25% | R1 (Methodology) |
| 2 | **Data & Results Integrity** | 20% | R1 (Methodology) + Devil's Advocate |
| 3 | Originality & Contribution | 15% | EIC + R2 (Domain) |
| 4 | Argument & Evidence Coherence | 15% | R2 (Domain) + Devil's Advocate |
| 5 | Writing Quality | 15% | EIC + R3 |
| 6 | Format & Bibliographic Compliance | 10% | EIC |

#### Dimension 2 — Data & Results Integrity (mandatory checklist)

This dimension is **new and mandatory**. Every reviewer pass MUST run the
deterministic **Data Integrity Gate (G4.5)** via the `academic-data-validator`
skill, then score the dimension qualitatively. Verify, item by item:

- [ ] **Text ↔ table/figure congruence**: every numeric value stated in the prose
      (abstract, results, discussion, conclusion) matches the value shown in the
      table/figure it refers to.
- [ ] **Internal numeric consistency**: sample sizes (N), totals, sub-totals and
      percentages are consistent across sections; percentages sum to ~100; ratios
      (e.g., `442/450`) are arithmetically valid (numerator ≤ denominator).
- [ ] **Float integrity (two-way)**: every Table/Figure is both defined and
      referenced in the text; no orphan floats, no dangling references.
- [ ] **Caption accuracy**: each table/figure caption matches the content it labels.
- [ ] **Claim → evidence traceability**: each quantitative or comparative claim
      ("improved", "outperforms", "increased") is traceable to a shown data point,
      table cell, figure, or cited source — and the stated direction matches the data.
- [ ] **Figure data verifiability**: where a figure carries numbers, a source-data
      sidecar (`figures/<stem>.{csv,json}` or the generating script) exists; if
      absent, flag `manual-verify` — never assume congruence silently.

**Gate linkage**: if the Data Integrity Gate (G4.5) returns a BLOCKING failure,
Dimension 2 is capped at ≤ 50 and the pipeline is blocked until corrected. A
PASS-with-warnings leaves the score to qualitative judgement on residual issues.

#### Dimension 5 — Writing Quality & Style (mandatory advisory audit)

This dimension consumes the findings from **`academic-writing-reviewer`** (`review/writing-review-report.md`).
The reviewers (EIC + R3) MUST inspect the advisory score and findings:
- [ ] **AI markers & cliches**: 0 unresolved Tier 1 markers (delve, underscores, pivotal, etc.).
- [ ] **Redundancy & repetition**: 0 unresolved cross-section duplicates (REP-01); sentence echoes addressed.
- [ ] **Scope discipline**: strict alignment with Section Scope Cards (no conflating agent team with whole firm).
- [ ] **Motivation & explanation**: all 6 Motivation Triggers addressed with clear causal mechanisms; no uninterpreted data dumps (CEI rule followed).
- [ ] **Audience jargon calibration**: all specialized computing terms (latency, tokens, context window) glossed at first use for management/interdisciplinary readers.
- [ ] **Author voice**: no "master's student" insecurity or excessive hedging; assertive scholarly stance.

**Advisory linkage**: if `academic-writing-reviewer` issues `MAJOR_REVISION_RECOMMENDED` (advisory score < 70 or CRITICAL findings present), Dimension 5 is capped at ≤ 60, triggering a revision loop.


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
- **Overall Score**: N/100  (weighted: Rigor×0.25 + Data×0.20 + Originality×0.15 + Coherence×0.15 + Writing×0.15 + Format×0.10)
- **Dimension Scores**: [Rigor: N | Data Integrity: N | Originality: N | Coherence: N | Writing: N | Format: N]
- **Gate Results**: [Citation↔Bib (G4): PASS/FAIL | Data Integrity (G4.5): PASS/WARN/FAIL]
- **Verdict**: Accept | Minor Revision | Major Revision | Reject
- **Critical Issues**: N items
- **Data Integrity Findings**: N blocking, N warnings (see review/data-congruence-report.md)
- **Revision Roadmap**:
  - Priority 1 (Required): items
  - Priority 2 (Suggested): items
  - Priority 3 (Nice-to-fix): items
```

## Automated Checks (optional, rule-based backstop)

Rule-based analyzers run on the Markdown drafts (or `.tex`/`.typ` if present) to
surface coherence, methodology, experiment and writing issues before the
qualitative pass. They require `scripts/parsers.py` (which now includes a
`MarkdownParser`). Run them from the project root with the venv active:

```bash
source .venv/bin/activate
SKILL=.claude/skills/academic-reviewer/scripts
for f in draft/*.md; do
  python "$SKILL/analyze_logic.py"      "$f" --cross-section
  python "$SKILL/analyze_experiment.py" "$f"
  python "$SKILL/analyze_grammar.py"    "$f"
  python "$SKILL/analyze_sentences.py"  "$f"
done
```

These checks are advisory and feed the qualitative dimensions; they do not
replace the deterministic gates (Citation↔Bib G4, Data Integrity G4.5).

## References

- `references/review_criteria_framework.md` — framework of criteria by paper type (0-100 scale)
- `references/quality_rubrics.md` — 0-100 rubrics with descriptors for the 6 canonical dimensions
- `references/editorial_decision_standards.md` — Accept/Minor/Major/Reject criteria + decision matrix
- `references/devils-advocate.md` — Devil's Advocate protocol
- `references/rubric_scientific_manuscript.json` — meta-rubric for the *quality of the review itself* (1-5 scale, threshold 3.5; orthogonal to the manuscript rubric — do not merge)

## Related Validators

- **`academic-writing-reviewer`** — deterministic and NYT-mode writing audit: AI markers, cross-section repetition, scope drift, unmotivated claims, unglossed jargon. Feeds Dimension 5.
- **`academic-data-validator`** — deterministic Data Integrity Gate (G4.5): text↔table/figure
  congruence, internal numeric consistency, float integrity. Feeds Dimension 2.
- **`academic-citation-manager`** + **`academic-bibliography-manager`** — Citation↔Bibliography Gate (G4). Feeds Dimension 6.
- **`academic-format-validator`** — Output Format Gate: Markdown/LaTeX/DOCX formatting. Feeds Dimension 6.

