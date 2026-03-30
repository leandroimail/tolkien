# Search Strategies

## Keyword Development

### From PRD to Search Terms

1. Extract primary keywords from `prd.md` research questions
2. Generate synonyms and related terms for each keyword
3. Add field-specific terminology (MeSH terms for medical, IEEE keywords for engineering)
4. Create Boolean combinations

**Example:**
```
PRD keyword: "machine learning in healthcare"

Primary: machine learning, healthcare
Synonyms: deep learning, artificial intelligence, neural networks, medical, clinical
MeSH: "Machine Learning"[MeSH], "Delivery of Health Care"[MeSH]
Combinations:
  - "machine learning" AND healthcare
  - "deep learning" AND "clinical decision"
  - "artificial intelligence" AND "medical diagnosis"
```

### Search Term Expansion

| Strategy | Example |
|----------|---------|
| Synonyms | ML → machine learning, deep learning, AI |
| Broader | healthcare → medicine, clinical, biomedical |
| Narrower | healthcare → radiology, pathology, ICU |
| Related | healthcare → electronic health records, clinical trials |
| Acronyms | NLP → natural language processing |

## Database-Specific Strategies

### OpenAlex (Primary — Always Use)

```
# Broad keyword search
/works?search=machine learning healthcare&filter=publication_year:2020-2026

# Title-specific search
/works?search=machine learning healthcare&search_field=title

# Combined filters for precision
/works?search=deep learning diagnosis&filter=publication_year:2022-2026,type:journal-article,cited_by_count:>5,is_retracted:false
```

### Google Scholar (Supplementary — via web_search)

```
site:scholar.google.com "machine learning" "healthcare" after:2020
```

Useful for: finding grey literature, theses, non-indexed papers.

### PubMed (Medical/Health — via web_search)

```
site:pubmed.ncbi.nlm.nih.gov "machine learning"[Title] AND "healthcare"[Title]
```

Useful for: medical research, MeSH-indexed literature, clinical trials.

## Inclusion/Exclusion Criteria Templates

### Standard Research Article

**Include:**
- Peer-reviewed journal articles or conference papers
- Published within date range (from PRD)
- In specified language(s)
- Directly addresses at least one research question
- Original research or systematic review

**Exclude:**
- Editorials, letters, commentaries (unless highly cited)
- Preprints without peer review (unless field-standard, e.g., arXiv in CS)
- Duplicate publications
- Retracted papers
- Papers in languages not specified in PRD

### Systematic Review (PRISMA-aligned)

**Include:**
- Studies matching PICO/SPIDER criteria from PRD
- Published within date range
- Study design matches (RCTs only, or RCTs + observational)
- Full text available

**Exclude:**
- Animal studies (unless specified)
- In vitro only studies
- Protocols without results
- Conference abstracts without full paper
- Studies with high risk of bias (per quality assessment)

## Screening Workflow

### Stage 1: Title Screening
- Read title only
- Classify: Relevant / Not relevant / Unclear
- Keep all "Unclear" for Stage 2
- Expected yield: 30-50% of search results

### Stage 2: Abstract Screening
- Read abstract (reconstruct from inverted index if needed)
- Apply inclusion/exclusion criteria
- Classify: Include / Exclude / Full-text needed
- Expected yield: 40-60% of Stage 1

### Stage 3: Full-text Review (when available)
- Read available full text
- Final inclusion/exclusion decision
- Extract key data for synthesis
- Expected yield: 70-90% of Stage 2

## PRISMA Flow Template

```
Records identified through OpenAlex: {N}
Records from other sources: {N}
                    ↓
Total records: {N}
Duplicates removed: {N}
                    ↓
Records screened (title/abstract): {N}
Records excluded: {N}
                    ↓
Full-text assessed for eligibility: {N}
Full-text excluded with reasons: {N}
                    ↓
Studies included in synthesis: {N}
```
