---
name: academic-researcher
description: >
  Conducts systematic literature search, screening, and synthesis for academic papers using OpenAlex API.
  Produces literature review, search strategy documentation, and validated BibTeX references.
  Triggers: /academic-researcher, "search literature", "find papers about", "literature review"
allowed-tools: [Read, Write, Edit, Bash, WebSearch, WebFetch]
metadata:
  version: "1.1"
  depends_on: ["academic-prd", "web-browser-search"]
---

Note: Python scripts for this skill must be executed within the project's virtual environment.
Activate the environment with:

```bash
source .venv/bin/activate
```

Alternatively, use `uv run python -B ...` with the `.venv` active.

# Academic Researcher

Systematic literature search, screening, and synthesis for academic papers. This is **Phase 2** of the pipeline. Uses OpenAlex API as primary source (240M+ scholarly works, no API key required).

## When To Use

- User needs to find and review academic literature on a topic
- Pipeline Phase 2: literature research after PRD and plan are approved
- User invokes `/academic-researcher` or asks to "find papers", "search literature"
- User needs a structured literature review with BibTeX output

## When Not To Use

- User needs to validate/enrich existing BibTeX → use `academic-bibliography-manager`
- User needs to verify citations in a draft → use `academic-citation-manager`
- User wants to write the paper → use `academic-writer`
- User only needs a single paper's metadata → use `academic-bibliography-manager` DOI resolution

## Prerequisites

- `{root}/paper-{slug}/prd.md` with research questions, keywords, and search strategy (preferred)
- Or: user-provided topic, keywords, and scope for standalone use
- **`resources/`** (optional) — base/auxiliary files for research (raw data, reference documents, guidelines)

> **Root Path**: The paper must be located in one of: `projects/`, `papers/`, `.projects/`, `.papers/`.

## Modes

| Mode | When | Description |
|------|------|-------------|
| `socratic` | Unclear research question | Dialogue to refine question before searching |
| `full` | Systematic research | Complete search → screen → synthesize pipeline |
| `quick` | Need N relevant papers fast | Search + return top N most relevant papers |

Default: `full` when `prd.md` exists, `socratic` when starting from scratch.

## Method

### Mode: Socratic

1. Ask 2-3 clarifying questions about the research topic
2. Reflect understanding back to the user
3. **CHECKPOINT: Wait for user confirmation before proceeding**
4. Present 3-5 research themes with execution plan
5. **CHECKPOINT: Wait for user approval of research plan**
6. Transition to `full` mode with refined parameters

### Mode: Full (Systematic Research)

#### Step 1: Define Search Strategy

Read `prd.md` and extract: keywords, databases, date range, inclusion/exclusion criteria, minimum sources.

Document the strategy in `research/search-strategy.md`:
- Primary keywords + synonyms + MeSH terms (if medical)
- Boolean combinations planned
- Inclusion/exclusion criteria
- Target number of sources

#### Step 2: Execute Two-Cycle Search

**Cycle 1 — Landscape Analysis:**
1. Search OpenAlex with primary keywords (see [references/openalex-api.md](references/openalex-api.md))
2. Sort by relevance, then by citation count
3. Scan top 50-100 results: titles, abstracts, citation counts
4. Identify: key themes, landmark papers (highly cited), recent advances
5. Note gaps: which research questions lack coverage?

```bash
# Example OpenAlex search
uv run python -B scripts/search_openalex.py \
  --query "machine learning healthcare" \
  --from-year 2020 --to-year 2026 \
  --min-citations 10 --limit 100
```

**Cycle 2 — Deep Investigation:**
1. Refine search based on Cycle 1 findings (new keywords, related terms)
2. Follow citation trails: check `referenced_works` and `cited_by` of landmark papers
3. Search for contradicting evidence and alternative perspectives
4. Fill gaps identified in Cycle 1
5. Verify key claims across multiple sources

#### Step 2.5: Supplementary Web Search (Optional)

When OpenAlex results are insufficient or the topic requires grey literature,
web-accessible reports, or recent preprints not yet indexed:

1. Invoke the `web-browser-search` skill (or `web-browser-search-agent`) with refined keywords
2. DuckDuckGo is used by default; Brave Search if `$BRAVE_SEARCH_API_KEY` is set
3. For results that need full-text access, use browser automation to navigate and extract content

**Use cases:**
- Government reports, white papers, technical documentation
- Recent preprints on arXiv, SSRN, bioRxiv (not yet in OpenAlex)
- Conference proceedings and workshop papers not indexed by OpenAlex
- Industry reports and standards documents

```bash
# Example: search for grey literature via DuckDuckGo
source .venv/bin/activate
python3 -c "
from duckduckgo_search import DDGS
results = DDGS().text('machine learning healthcare policy report filetype:pdf', max_results=10)
for r in results:
    print(f\"{r['title']} — {r['href']}\")
"

# Example: browse a result page for content extraction
agent-browser open "https://example.com/report.html"
agent-browser wait --load networkidle
agent-browser get title
agent-browser close
```

**Important**: Web search results require manual quality assessment.
They do not carry the same metadata guarantees as OpenAlex entries.
Always validate and add to `references.bib` via `academic-bibliography-manager`.

> For full web search and browser reference: see `web-browser-search` skill

#### Step 3: Screen Results

Apply inclusion/exclusion criteria from PRD:
- Check publication type, date range, language
- Read abstracts (reconstruct from inverted index if needed)
- Classify: **Include** / **Exclude** / **Maybe**
- For "Maybe": read further or discuss with user

Track screening in `research/literature.md`:
```markdown
## Screening Results
- Total found: {N}
- After deduplication: {N}
- After title/abstract screening: {N}
- After full-text screening: {N}
- Final included: {N}
```

#### Step 4: Synthesize

For each included source, extract:
- Research question addressed
- Methodology (design, sample, variables)
- Key findings
- Limitations
- Relevance to user's research questions

Organize synthesis by theme or research question (not by paper).

#### Step 5: Export BibTeX

Export validated entries to `research/references.bib`:
```bash
uv run python -B scripts/validate_bib_entries.py research/references.bib
```

Each entry must have required fields per type. See [references/openalex-api.md](references/openalex-api.md) for field mapping.

#### Step 6: Self-Review

Evaluate coverage:
- [ ] Every research question from PRD has ≥ 3 supporting sources
- [ ] No duplicate DOIs in references.bib
- [ ] All BibTeX entries have required fields (validate with script)
- [ ] Literature synthesis covers key themes, not just lists papers
- [ ] Contradicting evidence and alternative perspectives included
- [ ] Landmark papers in the field are represented

**Agentic gap report:**
```
### Gap Analysis
- RQ1 "{question}": {N} sources — {assessment}
- RQ2 "{question}": {N} sources — {assessment}
- Missing perspectives: {list}
- Suggested additional searches: {list}
```

### Mode: Quick

1. Search OpenAlex with provided keywords
2. Sort by `cited_by_count:desc` (landmark) or `publication_date:desc` (recent)
3. Return top N results (default: 10) with title, authors, year, abstract, DOI
4. Export BibTeX for selected papers

## Evidence Hierarchy

When assessing sources, apply this hierarchy (highest to lowest):
1. Systematic reviews and meta-analyses
2. Randomized controlled trials (RCTs)
3. Cohort and longitudinal studies
4. Expert consensus and clinical guidelines
5. Cross-sectional and observational studies
6. Expert opinion and editorials
7. Grey literature (preprints, reports)

Annotate confidence: `[HIGH]` (multiple high-quality agree), `[MEDIUM]` (limited/mixed), `[LOW]` (single source), `[SPECULATIVE]` (emerging/hypothesis).

## Quality Checklist

- [ ] Search strategy documented in `research/search-strategy.md`
- [ ] Two complete research cycles executed (full mode)
- [ ] Screening results tracked with counts
- [ ] ≥ minimum sources from PRD included
- [ ] `references.bib` validated (0 errors from `validate_bib_entries.py`)
- [ ] No duplicate DOIs
- [ ] Synthesis organized by theme/question, not by paper
- [ ] Gap analysis completed
- [ ] Evidence hierarchy applied

## Outputs

- `research/literature.md` — sources found, screening results, thematic synthesis
- `research/search-strategy.md` — documented search strategy with keywords, criteria
- `research/references.bib` — BibTeX entries for all included sources

## Integration

- **Input from:** `academic-prd` (keywords, criteria, research questions)
- **Output to:** `academic-writer` (literature for citation), `academic-bibliography-manager` (BibTeX for validation/enrichment)
- **Supplementary search via:** `web-browser-search-agent` (web queries + browsing for grey literature)
- **Called by:** `research-agent`, `academic-orchestrator` (Phase 2)

For detailed OpenAlex API reference: [references/openalex-api.md](references/openalex-api.md)
For research protocol details: [references/research-protocol.md](references/research-protocol.md)
For search strategy patterns: [references/search-strategies.md](references/search-strategies.md)
