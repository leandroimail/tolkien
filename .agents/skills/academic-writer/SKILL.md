---
name: academic-writer
description: >
  Full writing of academic articles section by section, following an approved outline.
  Consolidates best practices for scientific writing, human academic register, and
  IMRaD/review/case-study structures.
  Trigger: /academic-writer, "write section", "write article", "write introduction",
  "write paper", "draft manuscript", "write methodology", "write discussion".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "1.0"
  depends_on: "academic-prd, academic-plan, academic-researcher"
---

# Academic Writer

Writing of academic articles with publishable quality, section by section. Consolidates best practices from scientific-writing, academic-paper, academic-writing, academic-writing-style, and scientific-paper into a unified skill.

## When To Use

- Drafting any section of an academic paper (abstract, introduction, methods, results, discussion, conclusion)
- Following IMRaD, systematic review, case study, or thematic structures
- Producing fluid academic prose without bullet points in the final output
- Adjusting academic register by discipline (STEM, social sciences, humanities)

## When Not To Use

- To search for literature → use `academic-researcher`
- To validate in-text citations → use `academic-citation-manager`
- To review a finished article → use `academic-reviewer`
- To humanize already written text → use `academic-humanizer`
- To generate figures/diagrams → use `academic-media`

## Prerequisites

1. **`prd.md`** — type of paper, discipline, citation format, language
2. **`draft/outline.md`** — approved structure with word count allocation
3. **`research/literature.md`** — literature synthesis
4. **`research/references.bib`** — available references for citation

## Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| `section` | "write introduction" | Drafts a specific section |
| `full` | "draft full article" | All sections sequentially |
| `continue` | "continue draft" | Resumes from the last point |

## Method: Two-Stage Writing Process

### Stage 1: Outline with Key Points (Structural)

For each section, create an internal outline with:
- Main arguments to present
- Key studies to cite (with years and findings)
- Data and statistics to include
- Logical flow and organization

> This outline is internal scaffolding — it is NOT the final output.

### Stage 2: Conversion to Full Prose

Expand each point into fluid paragraphs:
1. Transform bullets into sentences with subject, verb, and object
2. Integrate citations naturally (narrative vs. parenthetical)
3. Vary sentence structure — avoid monotony
4. Connect paragraphs by content logic, not by "Furthermore/Moreover"

## Writing Quality Standards

### 5 Anti-Patterns to Avoid

| AI Pattern | How to Fix |
|-----------|---------------|
| **Hedging Soup** — stacking "potentially/possibly/may" | Use one precise statement + one precise limitation |
| **Formulaic Transitions** — "Furthermore/Moreover/Additionally" | Let content logic drive connections; use real transitions |
| **Structural Monotony** — same length in every paragraph | Vary length by ≥ 30%; mix short and long paragraphs |
| **Abstraction Fog** — "various studies/the literature suggests" | Name studies: "Patel et al. (2022) found..." |
| **Voice Erasure** — "it can be argued/it was found" | Use active voice: "We argue..." when the discipline allows |

### Self-Audit Per Section

Before presenting any section:
- [ ] Hedging: < 2 hedging words per paragraph
- [ ] Transitions: 0 instances of Furthermore/Moreover/Additionally
- [ ] Structure: No 3 consecutive paragraphs within 10 words of each other
- [ ] Specificity: 0 instances of "various studies" without concrete referent
- [ ] Voice: < 3 instances of "it can be/it was found" per page

## Section-Specific Checkers

| Section | Must Have | Must NOT Have |
|---------|-----------|---------------|
| Introduction | Context + gap + objective + paper structure | Results, interpretations |
| Methods | Design, sample, variables, reproducible protocol | Interpretations of results |
| Results | Facts, data, objective statistics | Interpretation or speculation |
| Discussion | results↔questions connection, comparison with literature | New data not presented in Results |
| Conclusion | Limitations, future work, implications | New data or results |

## Discipline-Aware Register

| Discipline | Voice | Citation Style | Key Features |
|-----------|-------|---------------|--------------|
| STEM | Active for claims, passive acceptable in Methods | Author-date or numbered | Numbered hypotheses, statistical reporting |
| Social Sciences | Active + first person plural | Author-date (APA) | Theoretical framing, effect sizes |
| Humanities | First person singular | Notes or author-date | Close reading, interpretive argument |
| Interdisciplinary | Active + first person plural | Per target journal | Define terms from each field |

## Citation Integration

- **Narrative**: when author identity matters — "Foucault (1975) argued..." 
  - *If ABNT/LaTeX*: Use `\citeonline{foucault1975}`.
- **Parenthetical**: when the finding matters — "rates tripled (Alexander, 2010)"
  - *If ABNT/LaTeX*: Use `\cite{alexander2010}`.
- **Direct quote**: only when wording is the point — definitions, contested phrases (include page numbers, e.g., `\cite[p.~45]{key}`)
- **Synthesis**: to show consensus — "(Lee, 2019; Nakamura, 2020; dos Santos, 2021)"

## Integration with academic-media

When detecting the need for a figure, schematic, or EDA:
```
→ academic-media: {description of the necessary visual element}
```

## Self-Review

### Deterministic
- [ ] ∀ citation uses format `\cite{key}` or `(Author, Year)` as per style
- [ ] Word count ±10% of outline allocation
- [ ] No bullet points in final prose (except Methods: inclusion criteria)
- [ ] Academic register maintained (no colloquial language)

### Agentic
- consistency of terminology across sections
- logical flow of argumentation
- evidence gaps (factual claims without citation)

## References

- `references/imrad-structure.md` — detailed IMRAD guide
- `references/writing-quality-check.md` — anti-AI markers checklist
- `references/discipline-registers.md` — conventions by field
