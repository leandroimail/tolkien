---
name: academic-humanizer
description: >
  Register adjustment, humanization, and naturalization of academic writing.
  Removes typical AI markers while maintaining academic rigor.
  Supports multiple languages (EN, PT-BR, FI) with disciplinary conventions.
  Trigger: /academic-humanizer, "humanize", "adjust register",
  "naturalize writing", "humanize text", "remove AI feel".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "1.0"
  depends_on: "academic-writer"
---

# Virtualenv

Note: Python scripts for this skill must be executed within the project's virtual environment.
Activate the environment with:

```bash
source .venv/bin/activate
```

Alternatively, use `uv run python -B ...` with the `.venv` active.

# Academic Humanizer

Humanization and naturalization of academic writing. Removes the artificiality of AI-generated text while maintaining academic register, technical terminology, and factual integrity. Consolidates best practices for humanize, humanize-academic-writing, and finnish-humanizer.

## When To Use

- Academic text sounds "too perfect," mechanical, or repetitive
- Paragraphs look like a template with uniform structure
- Transitions are all "Furthermore/Moreover/Additionally"
- Language is excessively abstract without concrete examples
- After the `academic-writer` draft and before the final review
- When the author wants to adjust the academic register by discipline

## When Not To Use

- To draft the article from scratch → use `academic-writer`
- For academic review/peer review → use `academic-reviewer`
- To use an external humanization API → consult HumanizerAI API directly

## Prerequisites

1. **Complete Draft or Section** — `draft/*.md`
2. Information about discipline and target language (from `prd.md`)

## Method

### Step 1: Analyze — Detect AI Patterns

Identify problematic patterns in the text:

#### 5 Main Categories

| # | Pattern | Detection |
|---|--------|----------|
| 1 | **Rhythm Uniformity** | All sentences with ~same length (15-20 words) |
| 2 | **Formulaic Transitions** | Moreover/Furthermore/Additionally at the start of sentences |
| 3 | **Abstract Scaffolding** | "various aspects," "in terms of," "multiple factors" |
| 4 | **Generic Academic Tone** | Lack of critical engagement with sources, no author voice |
| 5 | **Voice Erasure** | "it can be argued...", "it is important to note..." |

#### Quantitative Metrics

- **Sentence Length Variance**: must be > 30%
- **Type-Token Ratio (TTR)**: vocabulary diversity
- **Transition Word Density**: < 5% of sentences
- **Passive Voice %**: appropriate for the discipline
- **Consecutive Similarity**: adjacent sentences should not be structurally identical

### Step 2: Rewrite with Targeted Strategies

#### Strategy 1: Vary Sentence Rhythm (Burstiness)
- Mix: short (5-10 words) + medium (15-20) + long (25-35)
- Before: "This study examines X. The research focuses on Y. The analysis considers Z."
- After: "This study examines X's impact on Y, considering factors from identity formation to civic engagement."

#### Strategy 2: Eliminate Abstract Scaffolding
- Replace "various aspects" → specific named concepts
- Replace "in terms of" → direct relationship
- Replace "it is important to note" → DELETE (start with the content)

#### Strategy 3: Natural Transitions
- Remove: Furthermore, Moreover, Additionally, It is important to note
- Use: direct logical flow, "This pattern echoes...", "Building on..."
- Rule: if deleting the transition doesn't change the meaning, delete it

#### Strategy 4: Ground in Specificity
- Replace "research has shown" → "Patel et al. (2022) surveyed 814 nurses"
- Replace "various studies" → "Four longitudinal cohort studies (totaling 23,000 participants)"
- Replace "the field" → concrete named domain

#### Strategy 5: Restore Author Voice
- Replace "it can be argued" → "We argue"
- Replace "it was found" → "We found" / "The analysis reveals"
- Use first person when the discipline allows

### Step 3: Present with Rationale

For each modified paragraph:
```
**Original:** [original text]
**Revised:** [humanized text]
**Rationale:** Removed 3x "Moreover" transitions, varied sentence length (8, 24, 15 words),
     replaced "various studies" with a specific citation (Smith 2022).
```

## Language-Specific Considerations

### English
- Prefer common over complex: "use" not "utilize"
- Field-specific terminology is fine — don't over-simplify
- Active voice default, passive in Methods when appropriate

### Portuguese (BR)
- Preserve formal Brazilian academic register
- Remove excessive "Além disso/Ademais/Outrossim"
- Keep technical terms in English when it's the field norm
- ABNT: third-person register is standard

### Finnish (FI)
- Suoruus (directness): say it and move on
- Partikkelit: -han/-hän, -pa/-pä, kyllä, vaan — keep text natural
- Do not overstate enthusiasm — "Ihan hyvä" is a compliment

## Guardrails

- **DO NOT change meaning** — only form, never factual content
- **DO NOT add information** — do not invent citations or data
- **DO NOT over-simplify** — naturalizing ≠ infantilizing
- **Preserve citations** — every reference remains intact
- **Respect register** — formal text stays formal
- **DO NOT casualize** — academic writing must remain academic

## Self-Review

### Deterministic
- [ ] 0 new factual information introduced (only form adjustments)
- [ ] All citations preserved intact
- [ ] Sentence length variance > 30%
- [ ] < 2 hedging words per paragraph
- [ ] 0 instances of Furthermore/Moreover/Additionally

### Agentic
- Verify that academic tone was preserved by discipline
- Confirm that technical terminology was not altered
- Verify that the text sounds natural for the target language

## References

- `references/ai-patterns.md` — complete list of 26 detectable AI patterns
- `references/language-specific.md` — conventions by language
