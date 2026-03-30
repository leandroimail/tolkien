# Research Protocol

## Two-Cycle Mandatory Research

Every research theme MUST go through two complete cycles. This prevents superficial coverage and ensures contradicting evidence is found.

### Cycle 1: Landscape Analysis

**Goal:** Understand the broad terrain of the topic.

1. **Broad search** — Use primary keywords with permissive filters
2. **Pattern identification** — What themes emerge? What's consensus? What's contested?
3. **Landmark discovery** — Which papers are highly cited (>100 citations)?
4. **Gap identification** — Which research questions lack coverage?
5. **Keyword refinement** — What new terms appeared that should be searched?

**Output:** List of themes, landmark papers, gaps, refined keywords for Cycle 2.

### Cycle 2: Deep Investigation

**Goal:** Fill gaps, verify claims, find contradictions.

1. **Targeted search** — Use refined keywords from Cycle 1
2. **Citation chain traversal** — Follow `cited_by` and `referenced_works` of landmarks
3. **Contradicting evidence** — Actively search for alternative perspectives
4. **Cross-validation** — Verify key claims across 2-3 independent sources
5. **Recency check** — Search most recent publications (last 2 years)

**Output:** Complete source list, validated findings, documented contradictions.

## Analysis Between Search Rounds

Between every search action, STOP and analyze:

1. **Connect** — How does this finding relate to what we already know?
2. **Evolve** — Has our understanding of the topic changed?
3. **Highlight** — What patterns are emerging across sources?
4. **Address** — Are there contradictions? How do we resolve them?
5. **Narrate** — Maintain a running narrative, not just a list of papers

This prevents the "collect everything, analyze nothing" trap.

## Three Checkpoints (Full Mode)

| Checkpoint | When | What to Present |
|-----------|------|-----------------|
| CP1 | After Socratic phase | Clarified research questions + understanding |
| CP2 | After research plan | Themes, execution plan, expected deliverables |
| CP3 | After synthesis | Full literature review + gap analysis |

In `quick` mode, only CP3 applies.

## Evidence Hierarchy and Confidence

### Hierarchy (highest to lowest)

1. **Systematic reviews / meta-analyses** — Aggregated evidence
2. **Randomized controlled trials** — Gold standard for causation
3. **Cohort / longitudinal studies** — Strong for association
4. **Expert consensus / clinical guidelines** — Authoritative but potentially biased
5. **Cross-sectional / observational** — Descriptive, limited causation
6. **Expert opinion / editorials** — Lowest academic evidence
7. **Grey literature** — Preprints, reports, theses (use with caution)

### Confidence Annotations

Use these in `literature.md` to qualify findings:

- `[HIGH]` — Multiple high-quality sources agree, robust methodology
- `[MEDIUM]` — Limited sources or mixed findings, reasonable methodology
- `[LOW]` — Single source or preliminary evidence
- `[SPECULATIVE]` — Hypothesis, emerging research, unconfirmed

### Red Flags

Flag any source that:
- Makes unsourced quantitative claims
- Is based on a single study with small sample
- Has undisclosed conflicts of interest
- Is significantly outdated for the field
- Cherry-picks statistics
- Overgeneralizes from narrow findings

## Error Handling

| Situation | Action |
|-----------|--------|
| Insufficient results | Broaden keywords, search adjacent concepts, document gap, lower confidence |
| Contradicting sources | Present both, analyze methodology differences, assess quality |
| Source quality concerns | Prefer primary sources, flag issues, note methodology limits |
| API rate limiting | Add delay, use polite pool, reduce page size |
| No abstract available | Use title + metadata for screening, flag for manual review |
