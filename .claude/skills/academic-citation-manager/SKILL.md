---
name: academic-citation-manager
description: >
  Management and validation of in-text citations — format, completeness, consistency,
  and cross-validation with references.bib (Citation↔Bibliography gate).
  Trigger: /academic-citation-manager, "verify citations", "format citations",
  "citation audit", "check citations", "citation gate".
allowed-tools: [Read, Write, Edit, Bash, Grep]
metadata:
  version: "1.0"
  depends_on: "academic-bibliography-manager"
---

# Virtualenv

Note: Python scripts for this skill must be executed within the project's virtual environment.
Activate the environment with:

```bash
source .venv/bin/activate
```

Alternatively, use `uv run python -B ...` with the `.venv` active.

# Academic Citation Manager

Management and validation of in-text citations in the academic paper draft. Responsible for the deterministic Citation↔Bibliography gate that blocks the pipeline if inconsistencies are found.

## When To Use

- Tracking all `\cite{key}` or `(Author, Year)` citations in the draft
- Validating citation format according to PRD style
- Identifying orphan citations (in text but no entry in `.bib`)
- Identifying ghost citations (in `.bib` but not cited in text)
- Executing the Citation↔Bibliography gate before review
- Detecting duplicate keys citing the same work

## When Not To Use

- To validate `.bib` fields → use `academic-bibliography-manager`
- To search for new papers → use `academic-researcher`
- To draft the text → use `academic-writer`

## Prerequisites

1. **Complete Draft** — `draft/*.md` (all sections)
2. **`research/references.bib`** — validated by bibliography-manager
3. **`prd.md`** — to identify citation style (APA, IEEE, ABNT, etc.)

## Method

### Phase 1: Citation Extraction

Scan all `draft/*.md` files and extract:
- All occurrences of `\cite{key}`, `\citeonline{key}`, `\citeauthor{key}`, `\nocite{key}` (LaTeX styles, particularly `abntex2` commands)
- All occurrences of `(Author, Year)` or `[N]` (inline text)
- Exact position: file, line, context

```bash
python scripts/extract_citations.py draft/
```

### Phase 2: .bib Key Extraction

Parse `research/references.bib` and extract all citation keys.

### Phase 3: Citation↔Bibliography Gate (BLOCKING)

```
RULE 1: ∀ key in \cite{key} or \citeonline{key} in draft → ∃ entry @{type}{key,...} in references.bib
         Violation = ORPHAN CITATION

RULE 2: ∀ key in references.bib → ∃ at least 1 \cite{key} or \citeonline{key} in draft
         Violation = GHOST CITATION

RULE 3: ∀ entry in references.bib → mandatory fields by type filled
         Violation = INCOMPLETE ENTRY

EXPECTED RESULT: 0 violations
BLOCKING: Yes — pipeline does not advance if result ≠ 0
```

```bash
python scripts/citation_gate.py draft/ research/references.bib
```

### Phase 4: Format Validation

By citation style:

| Style | In-Text Format | Example | LaTeX Commands |
|--------|----------------|---------|-----------------|
| APA | (Author, Year) | (Smith, 2023) | `\cite{}` / `\parencite{}` |
| IEEE | [N] | [1] | `\cite{}` |
| Vancouver | (N) | (1) | `\cite{}` |
| ABNT / ABNT 2 | (AUTHOR, Year) | (SILVA, 2023) | `\cite{}` for indirect, `\citeonline{}` for direct |
| Chicago | (Author Year) | (Smith 2023) | `\cite{}` / footnotes |

**Special note for ABNT (Associação Brasileira de Normas Técnicas):**
When generating or validating LaTeX for ABNT:
- Ensure the `abntex2cite` package is assumed.
- Ensure all indirect citations (at the end of ideas) use `\cite{key}` (which renders as `(AUTHOR, Year)`).
- Ensure all direct/narrative citations (part of the text) use `\citeonline{key}` (which renders as `Author (Year)`).

### Phase 5: Problem Detection

- **Citation Duplicate**: same work cited with different keys
- **Excessive Self-citation**: > 15% of citations are from the same author
- **Unbalanced Citations**: disproportionate concentration in one section
- **Old Citations**: > 50% of sources are over 10 years old (flag, non-blocking)

### Phase 6: Correction and Reporting

1. Automatically correct issues when possible
2. Generate report: `review/citation-report.md`

## Self-Review

### Deterministic
- [ ] Citation↔Bibliography Gate: 0 violations of the 3 rules
- [ ] 100% of citations in the correct format for the PRD style
- [ ] 0 duplicate keys referencing the same work

### Agentic
- Re-execute gate after corrections to confirm 0 inconsistencies
- Verify citation distribution across sections

## Output

```markdown
### Citation Validation Report
- **Citations in draft**: N unique keys
- **Entries in .bib**: M entries
- **Orphan citations** (in text, not in .bib): N → list
- **Phantom citations** (in .bib, not in text): N → list
- **Format violations**: N → list with corrections
- **Gate result**: ✅ PASS (0 violations) | ❌ FAIL (N violations)
```

## References

- `references/citation-formats.md` — guide to formats by style
- `references/citation-quality.md` — bibliographic quality metrics
