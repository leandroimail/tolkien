# Implementation Plan: {Title}

**Source PRD:** `prd.md`
**Created:** {YYYY-MM-DD}
**Paper type:** {type}
**Structure:** {structure}
**Target:** {venue/journal if known}

---

## Phase 0: Academic PRD ✅
- [x] Generate and approve prd.md
### Deliverable: `prd.md`
### Status: Complete

---

## Phase 1: Implementation Plan ✅
- [x] Generate plan.md from prd.md
### Deliverable: `plan.md`
### Status: Complete

---

## Phase 2: Literature Research
### Tasks
- [ ] Define search strategy with keywords: {keywords}
- [ ] Execute OpenAlex search with date range: {range}
- [ ] Apply inclusion criteria: {criteria}
- [ ] Apply exclusion criteria: {criteria}
- [ ] Screen {N} results for relevance
- [ ] Synthesize ≥ {N minimum} primary sources
- [ ] Export BibTeX entries to references.bib
- [ ] Validate BibTeX entries (required fields, no duplicates)
### Deliverables
- `research/literature.md`
- `research/search-strategy.md`
- `research/references.bib`
### Acceptance Criteria
- ≥ {N} sources screened
- references.bib validated (0 errors)
- All research questions covered
### Checkpoint: ⏸ User confirms literature review

---

## Phase 3: Outline & Architecture
### Tasks
- [ ] Create section outline following {structure} structure
- [ ] Allocate word counts per section (total: {N} words)
- [ ] Define argument flow and evidence mapping
- [ ] Map citations to sections
### Deliverables
- `draft/outline.md`
### Acceptance Criteria
- All sections from {structure} represented
- Word allocations sum to target ± 10%
- Each section has at least 1 mapped citation
### Checkpoint: ⏸ **GATE G3** — User approves outline before drafting

---

## Phase 4: Full-text Drafting
### Tasks
- [ ] Write Abstract ({N} words)
- [ ] Write Introduction ({N} words)
- [ ] Write Methods/Methodology ({N} words)
- [ ] Write Results ({N} words)
- [ ] Write Discussion ({N} words)
- [ ] Write Conclusion ({N} words)
- [ ] Request figures/schematics via academic-media (if needed)
### Deliverables
- `draft/abstract.md`
- `draft/introduction.md`
- `draft/methodology.md`
- `draft/results.md`
- `draft/discussion.md`
- `draft/conclusion.md`
### Acceptance Criteria
- Each section passes its checker (see academic-writer section checkers)
- All citations use `\cite{key}` or `[KEY]` format
- Word counts within ± 10% of allocation
### Checkpoint: ⏸ Optional per-section review (interactive mode)

---

## Phase 5: Citation & Bibliography Validation
### Tasks
- [ ] Validate all in-text citations (format per {citation_format})
- [ ] Validate references.bib completeness (required fields per type)
- [ ] Enrich incomplete BibTeX entries via OpenAlex
- [ ] Remove duplicate entries
- [ ] Run Citation↔Bibliography gate
### Deliverables
- `review/citation-report.md`
- `review/bibliography-report.md`
- `research/references.bib` (validated)
### Acceptance Criteria
- **GATE G4**: 0 orphan citations, 0 ghost entries, 0 incomplete entries
- All citations match {citation_format} style
### Checkpoint: ⏸ **GATE G4** — Citation↔Bibliography gate must pass (BLOCKING)

---

## Phase 6: Humanization & Register
### Tasks
- [ ] Scan for AI writing patterns
- [ ] Apply humanization (preserve academic register)
- [ ] Verify consistency of voice across sections
- [ ] Verify no factual changes introduced
### Deliverables
- `draft/*.md` (revised)
### Acceptance Criteria
- AI pattern score improved
- Academic register maintained
- No new factual claims introduced
### Checkpoint: ⏸ Optional review (interactive mode)

---

## Phase 7: Peer Review
### Tasks
- [ ] Execute 5-dimension review (full mode)
- [ ] Address reviewer feedback
- [ ] Execute focused re-review
### Deliverables
- `review/review-report.md`
- `review/revision-log.md`
### Acceptance Criteria
- All CRITICAL issues addressed
- All MAJOR issues addressed or documented as deliberate
- Overall score ≥ threshold for paper type
### Checkpoint: ⏸ **GATE G5** — Review accepted before formatting

---

## Phase 8: Output Formatting
### Tasks
- [ ] Consolidate draft sections into single document
- [ ] Apply template: {template}
- [ ] Convert to LaTeX: `output/paper.tex`
- [ ] Compile LaTeX → PDF: `output/paper.pdf`
- [ ] Validate PDF (pages, sections, references resolved)
- [ ] Generate DOCX if required: `output/paper.docx`
### Deliverables
- `output/paper.tex`
- `output/paper.pdf`
- `output/paper.docx` (if specified in PRD)
- `output/compilation-log.txt`
### Acceptance Criteria
- LaTeX compiles with exit code 0
- PDF generated, non-empty
- 0 undefined citations in compilation log
- 0 undefined references in compilation log
### Checkpoint: ⏸ Gate LaTeX — compilation must succeed (BLOCKING)

---

## Phase 9: Process Documentation
### Tasks
- [ ] Generate process-record.md with session history
- [ ] Document human-AI collaboration decisions
- [ ] Record final statistics (sources, word count, revision cycles)
### Deliverables
- `process-record.md`
### Acceptance Criteria
- All phases documented
- Key decisions recorded

---

## Summary

| Phase | Gate | Status |
|-------|------|--------|
| 0. PRD | G1 | ✅ |
| 1. Plan | G2 | ✅ |
| 2. Research | — | ⏳ |
| 3. Outline | G3 | ⏳ |
| 4. Drafting | — | ⏳ |
| 5. Citation/Bib | G4 | ⏳ |
| 6. Humanization | — | ⏳ |
| 7. Review | G5 | ⏳ |
| 8. Formatting | LaTeX Gate | ⏳ |
| 9. Documentation | — | ⏳ |
