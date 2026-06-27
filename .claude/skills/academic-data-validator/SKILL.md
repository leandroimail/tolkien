---
name: academic-data-validator
description: >
  Deterministic Data Integrity Gate (G4.5): validates the congruence between the
  text and the data presented — numbers in the prose vs tables/figures, internal
  numeric consistency (Ns, totals, percentages), and two-way Table/Figure
  reference integrity. Produces a reconciliation worksheet for the qualitative
  congruence pass. Trigger: /academic-data-validator, "validate data congruence",
  "check data integrity", "data congruence gate", "verify results vs tables".
allowed-tools: [Read, Write, Edit, Bash, Grep]
metadata:
  version: "1.0"
  depends_on: ["academic-citation-manager", "academic-reviewer", "academic-media"]
---

# Virtualenv

Note: Python scripts for this skill must be executed within the project's virtual environment.

```bash
source .venv/bin/activate
```

Alternatively, use `uv run python -B ...` with the `.venv` active. All scripts are
**stdlib-only** and have no third-party dependencies.

# Academic Data Validator

Validates the **congruence of the text with the data presented** in the article.
It is the engine behind the **Data Integrity Gate (G4.5)** and feeds **Dimension 2
(Data & Results Integrity)** of `academic-reviewer`. It combines a deterministic
gate (what a script can prove) with a reconciliation worksheet that hands the
remaining semantic checks to the reviewer/LLM.

## When To Use

- Before peer review, to confirm the numbers in the prose match the tables/figures.
- To check internal numeric consistency (Ns, totals, percentages) across sections.
- To verify every Table/Figure is both defined and referenced (no orphan/dangling floats).
- To produce the `data-congruence-report.md` consumed by the reviewer.

## When Not To Use

- To validate citations/bibliography → use `academic-citation-manager` + `academic-bibliography-manager`.
- To validate document formatting (md/tex/docx) → use `academic-format-validator`.
- To draft the text → use `academic-writer`.

## Prerequisites

1. **Draft** — `draft/*.md` (and/or `*.tex` if already compiled).
2. **`prd.md`** — for expected units / sample sizes (optional context).
3. **Figures** — ideally with a data sidecar (`figures/<stem>.{csv,json}` or the
   generating `.py`); see `references/figure-sidecar-convention.md`.

## Method

### Phase 1: Numeric Inventory

Extract every numeric value from prose and tables, tagged with file, line,
section, unit and kind (int/float/percent/ratio/year/word). Word numbers
("eleven") and locale decimals (`0,80`, `4.701`) are normalized.

```bash
python scripts/extract_numeric_inventory.py draft/ --json
```

### Phase 2: Float Integrity Gate (two-way, BLOCKING)

```
RULE A: ∀ Table/Figure defined (caption / \label) → referenced in the prose
        Violation = ORPHAN FLOAT
RULE B: ∀ Table/Figure referenced in the prose → defined (caption / \label)
        Violation = DANGLING REFERENCE
EXPECTED: 0 violations · BLOCKING
```

```bash
python scripts/check_float_integrity.py draft/
```

### Phase 3: Table Arithmetic (BLOCKING on contradiction)

For tables that exist: a labeled Total/Sum row equals the sum of its components;
percentage columns sum to ~100. A hard contradiction is BLOCKING.

```bash
python scripts/check_table_arithmetic.py draft/
```

### Phase 4: Data Integrity Gate + Reconciliation Worksheet

Orchestrates Phases 1–3, builds the cross-section reconciliation worksheet, flags
warnings (summary-only numbers, precision variance, inverted ratios, figure
`manual-verify`), writes the report, and returns the gate exit code.

```bash
python scripts/data_congruence_gate.py <project_dir>
# → writes review/data-congruence-report.md ; exit 0 = PASS/PASS-with-warnings, 1 = FAIL
```

### Phase 5: Agentic Congruence Pass (not automatable)

Using the worksheet, the reviewer/LLM MUST:
- Confirm each cross-section number cluster refers to the **same** quantity.
- Verify each quantitative claim's **direction** matches the table/figure
  (e.g., "accuracy improved" ↔ the value actually rose).
- Map each headline claim to a shown data point, table cell, figure, or citation.
- Resolve every `manual-verify` figure against its source data.

## Two-tier Gate Semantics

| Tier | Findings | Effect |
|------|----------|--------|
| **BLOCKING** (exit 1) | orphan/dangling floats; table total mismatch | Pipeline blocked; Dimension 2 capped ≤ 50 |
| **WARNING** (exit 0) | summary-only numbers; precision variance; inverted ratio; figure `manual-verify` | Surfaced for adjudication; must be acknowledged, never silently passed |

## Pipeline Placement

- **G4.5 — Data Integrity Gate**: after G4 (Citation↔Bib), before Humanization/Review
  (Phase 5→6). Runs the prose + markdown-table tier on the draft.
- **Re-run in Phase 8**: the float/figure/table tier is re-executed against the
  compiled `.tex` (where `\label`/`\ref` fully exist). This timing split is
  intentional — markdown drafts rarely carry `\label`s.

## Self-Review

### Deterministic
- [ ] Float Integrity Gate: 0 orphan and 0 dangling floats.
- [ ] Table arithmetic: 0 total/percentage contradictions.
- [ ] `review/data-congruence-report.md` written with worksheet + exit code.

### Agentic
- [ ] Every cross-section cluster adjudicated (same quantity? direction correct?).
- [ ] Every `manual-verify` figure resolved or explicitly deferred.

## Output

```markdown
# Data Congruence Report (Gate G4.5)
- **Gate result**: ✅ PASS | ⚠️ PASS (with warnings) | ❌ FAIL
- **Numeric tokens analyzed**: N
- **Floats**: D defined / R referenced
- **Blocking findings**: N (list)
- **Warnings**: N (list)
- **Reconciliation worksheet**: cross-section clusters + summary-only + precision variance
```

## References

- `references/numeric-normalization.md` — number normalization rules (word↔digit, %, locale, tolerance)
- `references/figure-sidecar-convention.md` — making figure numbers verifiable

## Related

- `academic-reviewer` — Dimension 2 scores this gate's output qualitatively.
- `academic-media` — should emit figure data sidecars so figure numbers are verifiable.
