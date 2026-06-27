# Review Criteria Framework — Structured Review Criteria Framework

This document defines the universal criteria for academic paper review and the
type-specific criteria differentiated by paper type. All reviewer personas share
this framework.

> **Scale & dimensions.** This framework uses the **single 0–100 scale** and the
> **6 canonical dimensions** defined in `quality_rubrics.md` and `SKILL.md`. The
> legacy 1–5 scale and its separate decision mapping have been removed to keep one
> source of truth. The full 0–100 descriptors live in `quality_rubrics.md`; this
> document focuses on (1) what each dimension evaluates, (2) paper-type-specific
> criteria, and (3) reviewer pitfalls.

---

## 1. Universal Review Dimensions (6 canonical)

| # | Dimension | Weight | What it evaluates |
|---|-----------|--------|-------------------|
| 1 | Scientific Rigor & Methodology | 25% | Research design, statistical validity, controls, reproducibility, transparent reporting |
| 2 | **Data & Results Integrity** | 20% | Congruence of prose numbers with tables/figures; internal numeric consistency (Ns, totals, %); float integrity; claim→evidence traceability with correct direction |
| 3 | Originality & Contribution | 15% | Novelty, research gap filled, significance/impact of the contribution |
| 4 | Argument & Evidence Coherence | 15% | Logical flow, sufficiency of evidence for claims, handling of counterarguments |
| 5 | Writing Quality | 15% | Clarity, precision, academic register, grammar |
| 6 | Format & Bibliographic Compliance | 10% | Template/venue compliance, citation↔bibliography integrity, literature integration |

> For the 0–100 band descriptors of each dimension, see `quality_rubrics.md`.
> Significance/impact and literature integration are folded into Dimensions 3 and 6
> respectively and are reported narratively in the editorial synthesis.

---

## 2. Paper Type-Specific Criteria

Beyond the universal dimensions, apply the focus areas matching the paper type.
These are **qualitative** checks that inform the relevant dimension scores
(especially Dimensions 1 and 2).

### 2.1 Empirical Research

| Additional Focus | Review Question |
|---------------------|-------------|
| Research hypothesis clarity | Are hypotheses testable and consistent with theory? |
| Variable operational definitions | Are independent/dependent/control variable definitions precise? |
| Internal validity | Are confounding variables controlled? |
| External validity | Are results generalizable? |
| Statistical reporting completeness | Effect sizes, confidence intervals, assumption testing reported? |
| **Data congruence** | Do the reported numbers match the tables/figures, and do conclusions stay within what the data supports? *(feeds Dimension 2)* |

### 2.2 Theoretical/Conceptual Paper

| Additional Focus | Review Question |
|---------------------|-------------|
| Conceptual definition precision | Are core concepts clearly delineated? |
| Argument logic structure | Is the premise → inference → conclusion chain complete? |
| Counterargument handling | Are opposing viewpoints considered and addressed? |
| Theoretical novelty | Does it truly advance theoretical development? |
| Testability | Can the theory generate testable propositions? |

### 2.3 Literature Review / Meta-analysis

| Additional Focus | Review Question |
|---------------------|-------------|
| Search strategy | Comprehensive and reproducible (PRISMA compliance)? |
| Inclusion/exclusion criteria | Clear, reasonable, consistently applied? |
| Bias risk assessment | Is bias risk of included studies assessed? |
| Heterogeneity handling | Is statistical/conceptual heterogeneity handled? |
| Synthesis method | Critical synthesis beyond simple vote counting? |
| Publication bias | Assessed and discussed? |
| **Data congruence** | Do pooled estimates/forest-plot values match the text? *(feeds Dimension 2)* |

### 2.4 Case Study

| Additional Focus | Review Question |
|---------------------|-------------|
| Case selection justification | Why this case? What does it represent? |
| Theoretical vs convenience sampling | Is case selection theoretically grounded? |
| Triangulation | Are multiple data sources used? |
| Context description thickness | Is thick description sufficient? |
| Analysis transferability | Are results transferable to other contexts? |
| Researcher reflexivity | Is the researcher's relationship with the case reflected upon? |

### 2.5 Policy Analysis / Policy Brief

| Additional Focus | Review Question |
|---------------------|-------------|
| Policy problem definition | Clearly defined and evidence-supported? |
| Stakeholder analysis | Are key stakeholders identified? |
| Policy option analysis | Are multiple options proposed and compared? |
| Feasibility assessment | Are recommendations practically feasible? |
| Evidence quality | Are recommendations based on reliable evidence? |
| Unintended consequences | Are unintended impacts considered? |

---

## 3. Common Review Pitfalls

### Biases Reviewers Should Avoid

| Pitfall | Description | How to Avoid |
|---------|-------------|--------------|
| **Hypercriticism** | Overblowing minor issues, ignoring overall contribution | Affirm strengths first, then issues; distinguish major from minor |
| **Confirmation Bias** | Only finding evidence supporting pre-existing views | Deliberately seek the paper's merits and counterexamples to your own views |
| **Preference Projection** | Requiring authors to use "my method" | Ask "can this method answer the question?" not "what would I do?" |
| **Paradigm Bias** | Judging qualitative work by quantitative standards (or vice versa) | Use criteria matching the paper's research paradigm |
| **Prestige Bias** | Relaxing standards due to author's institution | Focus on the quality of the paper itself |
| **Novelty Bias** | Undervaluing replication studies | Acknowledge the role of replication in science |
| **Length Bias** | Long = good, short = sloppy | Evaluate content density, not page count |
| **Language Discrimination** | Undervaluing research due to non-native imperfections | Distinguish "language needs polishing" from "research quality is poor" |

### Principles of Constructive Feedback

1. **Specific, not vague**: "The causal inference in Section 3, paragraph 2 lacks control variables" beats "methodology has problems".
2. **Problem + reason + suggestion**: every criticism states "what", "why", and "how to fix".
3. **Distinguish required from suggested**: which changes are mandatory, which are "nice to have".
4. **Acknowledge uncertainty**: "I'm not sure whether this analysis accounts for X" is more accurate than "the author ignored X".
5. **Respect the author**: even if quality is poor, the author invested effort.

---

## 4. Scoring Aggregation

Scoring uses the canonical 0–100 weighted formula (see `quality_rubrics.md`):

```
Final Score =
  Scientific Rigor & Methodology   (25%) +
  Data & Results Integrity         (20%) +
  Originality & Contribution       (15%) +
  Argument & Evidence Coherence    (15%) +
  Writing Quality                  (15%) +
  Format & Bibliographic Compliance(10%)
```

### Score-to-Decision Mapping

| Weighted Total (0–100) | Recommended Decision |
|------------------------|----------------------|
| >= 80 | Accept |
| 65–79 | Minor Revision |
| 50–64 | Major Revision |
| < 50 | Reject |

For the full decision criteria, matrix, and special situations, see
`editorial_decision_standards.md`.

**Important reminders**:
- A single dimension governed by a BLOCKING gate that FAILS is capped at ≤ 50 and
  forces at least Major Revision, regardless of the weighted average.
- A Devil's Advocate **Critical** issue blocks Accept regardless of the total.
- The specific content of reviewer comments matters more than the numbers.
