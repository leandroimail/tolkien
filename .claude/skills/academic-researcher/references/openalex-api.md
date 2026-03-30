# OpenAlex API Reference

OpenAlex indexes 240M+ scholarly works. Free, no API key required. Polite pool (10 req/sec) requires `mailto` parameter.

## Base Configuration

```
BASE_URL = https://api.openalex.org
MAILTO = user@institution.edu   # from prd.md or user config

# Always include mailto for polite pool (10x rate limit)
curl -s "${BASE_URL}/works?search=query&mailto=${MAILTO}"
```

## Core Entities

| Entity | Endpoint | Count | Description |
|--------|----------|-------|-------------|
| Works | `/works` | 240M+ | Papers, articles, books, datasets |
| Authors | `/authors` | 90M+ | Researcher profiles |
| Sources | `/sources` | 250K+ | Journals, repositories, conferences |
| Institutions | `/institutions` | 100K+ | Universities, research organizations |
| Topics | `/topics` | 4K+ | Research topic classification |

## Work Object — Key Fields

```json
{
  "id": "https://openalex.org/W2741809807",
  "doi": "https://doi.org/10.1038/s41586-019-1099-1",
  "title": "Paper title",
  "publication_year": 2019,
  "publication_date": "2019-04-01",
  "type": "journal-article",
  "cited_by_count": 150,
  "fwci": 12.5,
  "is_retracted": false,
  "open_access": {
    "is_oa": true,
    "oa_status": "gold",
    "oa_url": "https://..."
  },
  "authorships": [
    {
      "author": {"id": "...", "display_name": "Author Name"},
      "institutions": [{"display_name": "University"}],
      "author_position": "first"
    }
  ],
  "abstract_inverted_index": {"word": [0, 5], "another": [1]},
  "referenced_works": ["https://openalex.org/W..."],
  "related_works": ["https://openalex.org/W..."],
  "primary_location": {
    "source": {"display_name": "Nature", "issn_l": "0028-0836"}
  },
  "biblio": {
    "volume": "568", "issue": "7753", "first_page": "496", "last_page": "502"
  }
}
```

## Abstract Reconstruction

OpenAlex stores abstracts as inverted indexes. Reconstruct with:

```python
def reconstruct_abstract(inverted_index: dict) -> str:
    """Convert OpenAlex inverted abstract index to plaintext."""
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(word for _, word in word_positions)
```

## Search Patterns

### Text Search
```
/works?search=machine learning healthcare
/works?search=machine learning healthcare&search_field=title
/works?search=machine learning healthcare&search_field=abstract
```

### Filters

Filters use `filter=` parameter. Multiple filters are AND-joined with commas.

```
# By year range
filter=publication_year:2020-2026

# By minimum citations
filter=cited_by_count:>50

# By type
filter=type:journal-article

# By open access
filter=open_access.is_oa:true
filter=open_access.oa_status:gold|green

# By language
filter=language:en

# Not retracted
filter=is_retracted:false

# By author (use OpenAlex ID, not name)
filter=authorships.author.id:A5023888391

# By institution
filter=authorships.institutions.id:I27837315

# By DOI
filter=doi:https://doi.org/10.1038/nature12345

# By source/journal
filter=primary_location.source.id:S137773608

# Indexed in specific database
filter=indexed_in:arxiv
filter=indexed_in:pubmed

# Combine multiple filters (AND)
filter=publication_year:2020-2026,cited_by_count:>10,type:journal-article,is_retracted:false

# Multiple values (OR) — use pipe
filter=type:journal-article|review-article
```

### Sorting

```
sort=cited_by_count:desc     # Most cited first
sort=publication_date:desc   # Most recent first
sort=relevance_score:desc    # Most relevant (with search)
```

### Pagination

**Basic (up to 10,000 results):**
```
per_page=50&page=1
per_page=50&page=2
```

**Cursor (unlimited, for large result sets):**
```
per_page=200&cursor=*              # First page
per_page=200&cursor={next_cursor}  # Subsequent pages
```

The `next_cursor` value is returned in `meta.next_cursor`. When it's `null`, no more results.

### Field Selection

Reduce response size by selecting only needed fields:
```
select=id,doi,title,publication_year,cited_by_count,authorships
```

## Citation Graph Traversal

```
# Papers cited BY a specific work
filter=cited_by:W2741809807

# Papers that a specific work CITES
filter=cites:W2741809807

# Related works
filter=related_to:W2741809807
```

## External ID Lookups

```
# By DOI
/works/https://doi.org/10.1038/nature12345

# By PubMed ID
/works/pmid:29694395

# By arXiv ID
/works/arxiv:2106.15928

# Batch lookup (up to 50)
filter=doi:https://doi.org/10.1038/a|https://doi.org/10.1038/b|https://doi.org/10.1038/c
```

## Author Lookup (Two-Step Pattern)

IMPORTANT: Never filter by author name directly. Always use two-step:

```
# Step 1: Find author ID
/authors?search=John Smith&select=id,display_name,works_count

# Step 2: Get their works
/works?filter=authorships.author.id:A5023888391&sort=cited_by_count:desc
```

## OpenAlex → BibTeX Mapping

| OpenAlex Field | BibTeX Field |
|---------------|-------------|
| `authorships[].author.display_name` | `author` |
| `title` | `title` |
| `publication_year` | `year` |
| `primary_location.source.display_name` | `journal` / `booktitle` |
| `biblio.volume` | `volume` |
| `biblio.issue` | `number` |
| `biblio.first_page`-`biblio.last_page` | `pages` |
| `doi` | `doi` |
| `id` | (generate key from first author + year) |

## Rate Limits

| Pool | Rate | How |
|------|------|-----|
| Common | 1 req/sec | No email |
| Polite | 10 req/sec | Add `mailto=email` |
| Premium | Higher | Paid plan |

Always use polite pool. Add 100ms delay between requests for safety.

## Practical Workflows

### Literature Survey
1. Search with broad keywords: `search=topic&filter=publication_year:2020-2026`
2. Sort by citations: `sort=cited_by_count:desc&per_page=50`
3. Identify landmark papers (top 10 by citations)
4. Follow citation chains: `filter=cited_by:W{landmark_id}`
5. Search for recent additions: `sort=publication_date:desc&per_page=20`

### Finding Review Articles
```
search=machine learning healthcare&filter=type:review-article&sort=cited_by_count:desc
```

### Finding Open Access Papers
```
search=topic&filter=open_access.is_oa:true&select=id,doi,title,open_access
```
