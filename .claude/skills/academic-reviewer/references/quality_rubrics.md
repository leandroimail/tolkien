# Quality Rubrics for Academic Paper Review

## Purpose

Provides calibrated scoring rubrics for the **6 canonical review dimensions** used by
all reviewers (EIC, R1, R2, R3, Devil's Advocate). Ensures consistent, reproducible
scoring across different papers and review sessions.

> **Single source of truth.** The dimensions and weights below match exactly the
> table in `SKILL.md` (Phase 1) and `review_criteria_framework.md`. All three use a
> single **0–100 scale**. Do not introduce a separate 1–5 scale.

## Scoring Scale

All dimensions scored 0–100. The final weighted score determines the editorial decision.

## Canonical Dimensions & Weights

| # | Dimension | Weight |
|---|-----------|--------|
| 1 | Scientific Rigor & Methodology | 25% |
| 2 | Data & Results Integrity | 20% |
| 3 | Originality & Contribution | 15% |
| 4 | Argument & Evidence Coherence | 15% |
| 5 | Writing Quality | 15% |
| 6 | Format & Bibliographic Compliance | 10% |

Weights sum to 100.

## Decision Mapping

| Weighted Average | Decision |
|-----------------|----------|
| >= 80 | Accept |
| 65-79 | Minor Revision |
| 50-64 | Major Revision |
| < 50 | Reject |

---

## Dimension 1: Scientific Rigor & Methodology (Weight: 25%)

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Research design perfectly aligned with RQ; all validity threats addressed; appropriate statistical methods with power analysis; transparent reporting (all EQUATOR items); reproducible |
| 75-89 | Strong | Sound design with minor gaps; most validity threats addressed; appropriate methods with minor reporting omissions; largely reproducible |
| 60-74 | Adequate | Acceptable design but some validity concerns; methods appropriate but justification lacking; some reporting gaps (missing effect sizes, CIs) |
| 45-59 | Weak | Design has significant flaws; method choice questionable; multiple reporting gaps; reproducibility doubtful |
| < 45 | Insufficient | Fundamental design flaws that invalidate findings; inappropriate methods; results cannot be trusted |

## Dimension 2: Data & Results Integrity (Weight: 20%)

Scored together with the deterministic **Data Integrity Gate (G4.5)** of the
`academic-data-validator` skill. **A BLOCKING gate failure caps this dimension at
≤ 50** (and blocks the pipeline). A PASS-with-warnings leaves scoring to qualitative
judgement on residual issues.

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Every number in prose matches its table/figure; full internal consistency (Ns, totals, %); all floats defined ⇄ referenced; captions accurate; every quantitative claim traceable to shown evidence with correct direction; figure data verifiable (sidecars present) |
| 75-89 | Strong | All key numbers congruent; minor precision/rounding variance only; floats and references resolve; claims well-supported |
| 60-74 | Adequate | Main results congruent but minor discrepancies (a stray number, one unreferenced float, one `manual-verify` figure) that do not change conclusions |
| 45-59 | Weak | Several text↔table/figure mismatches OR internal inconsistencies (Ns/%) OR claims whose direction is not clearly supported by the data |
| < 45 | Insufficient | Numbers in text contradict the tables/figures; results not reproducible from what is shown; conclusions not supported by the presented data |

## Dimension 3: Originality & Contribution (Weight: 15%)

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Novel theoretical framework supported by evidence; opens a new research direction; implications span 3+ fields; no prior work addresses this exact question |
| 75-89 | Strong | Novel methodology OR novel application of existing theory to a new context; clear contribution beyond incremental extension; implications for 2+ fields |
| 60-74 | Adequate | Extends an existing framework with new data, population, or context; contribution clear but incremental; single-field implications |
| 45-59 | Weak | Replicates an existing study with minor variations; contribution marginal; the "so what?" question not convincingly answered |
| < 45 | Insufficient | No discernible original contribution; duplicates existing work without justification; purely descriptive without analytical insight |

## Dimension 4: Argument & Evidence Coherence (Weight: 15%)

Merges argument coherence with evidence sufficiency. Co-owned by R2 and the Devil's Advocate.

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Crystal-clear flow problem → gap → RQ → method → findings → implications; every section builds on the previous; no logical jumps; counterarguments pre-empted; evidence sufficiently supports all claims |
| 75-89 | Strong | Clear flow with minor gaps; most transitions well-handled; argument generally persuasive; evidence adequate for main claims |
| 60-74 | Adequate | Main argument visible but some sections disconnected; occasional logical jumps; most claims supported, a few need more evidence |
| 45-59 | Weak | Argument structure unclear; significant logical gaps; conclusions overreach evidence; key claims under-supported |
| < 45 | Insufficient | No coherent argument; sections appear unrelated; conclusions do not follow from evidence; circular reasoning |

## Dimension 5: Writing Quality (Weight: 15%)

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Professional academic prose; precise terminology; excellent paragraph structure; zero grammatical errors; appropriate register throughout |
| 75-89 | Strong | Good academic writing; minor stylistic inconsistencies; few grammatical issues; terminology mostly precise |
| 60-74 | Adequate | Acceptable writing but room for improvement; some verbose passages; occasional imprecise terminology; some grammar issues |
| 45-59 | Weak | Below journal standards; frequent verbose/unclear passages; terminology inconsistent; multiple grammar issues |
| < 45 | Insufficient | Unacceptable writing quality; incomprehensible passages; severe grammar problems; not suitable for peer review |

## Dimension 6: Format & Bibliographic Compliance (Weight: 10%)

Scored together with the **Citation↔Bibliography Gate (G4)** (`academic-citation-manager`
+ `academic-bibliography-manager`) and the **Output Format Gate** (`academic-format-validator`).
A BLOCKING gate failure caps this dimension at ≤ 50.

| Score Range | Descriptor | Behavioral Indicators |
|------------|------------|----------------------|
| 90-100 | Exceptional | Flawless template/venue compliance; all citations resolve both ways; complete .bib entries; figures/tables formatted to spec; document compiles/validates cleanly (md/tex/docx) |
| 75-89 | Strong | Minor formatting/citation issues only; bibliography complete; compiles/validates with non-critical warnings |
| 60-74 | Adequate | Some formatting gaps or a few incomplete .bib entries; resolvable in one pass |
| 45-59 | Weak | Multiple orphan/ghost citations OR incomplete bibliography OR format gate failures |
| < 45 | Insufficient | Pervasive citation/format problems; does not compile/validate; not submission-ready |

---

## Aggregation Formula

```
Final Score =
  (Rigor       × 0.25) +
  (DataIntegrity × 0.20) +
  (Originality × 0.15) +
  (Coherence   × 0.15) +
  (Writing     × 0.15) +
  (Format      × 0.10)
```

---

## Calibration Notes

- Scores should reflect the paper's quality relative to the target journal's standards.
- A "75" for Nature is not equivalent to "75" for a regional journal.
- When in doubt, err toward the middle of a range.
- Reviewers should explicitly state which range descriptor best matches, then fine-tune within that range.
- If two dimensions are at odds (e.g., excellent methodology but weak writing), do NOT average down — report both scores honestly.
- **Gate override**: any single dimension governed by a BLOCKING gate that FAILS is
  capped at ≤ 50 and forces at least Major Revision regardless of the weighted average.
- A Devil's Advocate **Critical** issue blocks Accept regardless of the numeric total.
