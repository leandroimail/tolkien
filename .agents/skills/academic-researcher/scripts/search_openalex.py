#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""Search OpenAlex for scholarly works with filters and export as BibTeX.

Usage:
    uv run python -B scripts/search_openalex.py --query "machine learning" --from-year 2020 --limit 50
    uv run python -B scripts/search_openalex.py --query "healthcare AI" --min-citations 10 --output results.bib
    uv run python -B scripts/search_openalex.py --doi "10.1038/nature12345"

Exit codes:
    0 = success
    1 = no results found
    2 = API error
"""

import argparse
import json
import re
import sys
import time

import requests

BASE_URL = "https://api.openalex.org"
DEFAULT_EMAIL = "agent@academic-pipeline.org"
RATE_LIMIT_DELAY = 0.12  # 100ms + margin for polite pool


def search_works(
    query: str,
    mailto: str = DEFAULT_EMAIL,
    from_year: int | None = None,
    to_year: int | None = None,
    min_citations: int | None = None,
    work_type: str | None = None,
    open_access: bool = False,
    sort: str = "relevance_score:desc",
    limit: int = 50,
) -> list[dict]:
    """Search OpenAlex works with filters."""
    params = {
        "search": query,
        "mailto": mailto,
        "sort": sort,
        "per_page": min(limit, 200),
        "select": "id,doi,title,publication_year,cited_by_count,authorships,"
        "abstract_inverted_index,primary_location,biblio,type,is_retracted",
    }

    filters = ["is_retracted:false"]
    if from_year and to_year:
        filters.append(f"publication_year:{from_year}-{to_year}")
    elif from_year:
        filters.append(f"publication_year:>{from_year - 1}")
    if min_citations:
        filters.append(f"cited_by_count:>{min_citations - 1}")
    if work_type:
        filters.append(f"type:{work_type}")
    if open_access:
        filters.append("open_access.is_oa:true")

    if filters:
        params["filter"] = ",".join(filters)

    results = []
    page = 1

    while len(results) < limit:
        params["page"] = page
        time.sleep(RATE_LIMIT_DELAY)

        try:
            resp = requests.get(f"{BASE_URL}/works", params=params, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"ERROR: API request failed: {e}", file=sys.stderr)
            break

        data = resp.json()
        works = data.get("results", [])
        if not works:
            break

        results.extend(works)
        page += 1

        if page > (limit // min(limit, 200)) + 1:
            break

    return results[:limit]


def resolve_doi(doi: str, mailto: str = DEFAULT_EMAIL) -> dict | None:
    """Resolve a single DOI to OpenAlex work."""
    if not doi.startswith("https://doi.org/"):
        doi = f"https://doi.org/{doi}"

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(
            f"{BASE_URL}/works/{doi}",
            params={"mailto": mailto},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def reconstruct_abstract(inverted_index: dict | None) -> str:
    """Convert OpenAlex inverted abstract index to plaintext."""
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(word for _, word in word_positions)


def make_bib_key(work: dict) -> str:
    """Generate BibTeX key from first author surname + year."""
    authorships = work.get("authorships", [])
    if authorships:
        name = authorships[0].get("author", {}).get("display_name", "Unknown")
        surname = name.split()[-1] if name else "Unknown"
        surname = re.sub(r"[^a-zA-Z]", "", surname)
    else:
        surname = "Unknown"
    year = work.get("publication_year", "XXXX")
    # Add short hash to avoid collisions
    work_id = work.get("id", "")
    short_hash = work_id[-4:] if work_id else "0000"
    return f"{surname}{year}_{short_hash}"


def work_to_bibtex(work: dict) -> str:
    """Convert OpenAlex work to BibTeX entry."""
    key = make_bib_key(work)
    wtype = work.get("type", "article")

    # Map OpenAlex type to BibTeX type
    bib_type = "article"
    if wtype in ("book", "monograph"):
        bib_type = "book"
    elif wtype in ("proceedings-article", "conference-paper"):
        bib_type = "inproceedings"

    # Extract fields
    authors = " and ".join(
        a.get("author", {}).get("display_name", "Unknown")
        for a in work.get("authorships", [])
    )
    title = work.get("title", "Untitled")
    year = str(work.get("publication_year", ""))
    doi = (work.get("doi") or "").replace("https://doi.org/", "")

    loc = work.get("primary_location", {}) or {}
    source = (loc.get("source") or {}).get("display_name", "")

    biblio = work.get("biblio", {}) or {}
    volume = biblio.get("volume", "")
    number = biblio.get("issue", "")
    first_page = biblio.get("first_page", "")
    last_page = biblio.get("last_page", "")
    pages = f"{first_page}--{last_page}" if first_page and last_page else first_page

    # Build entry
    fields = [f"  author = {{{authors}}}"]
    fields.append(f"  title = {{{title}}}")
    fields.append(f"  year = {{{year}}}")

    if bib_type == "article":
        if source:
            fields.append(f"  journal = {{{source}}}")
        if volume:
            fields.append(f"  volume = {{{volume}}}")
        if number:
            fields.append(f"  number = {{{number}}}")
    elif bib_type == "inproceedings":
        if source:
            fields.append(f"  booktitle = {{{source}}}")

    if pages:
        fields.append(f"  pages = {{{pages}}}")
    if doi:
        fields.append(f"  doi = {{{doi}}}")

    return f"@{bib_type}{{{key},\n" + ",\n".join(fields) + "\n}"


def main():
    parser = argparse.ArgumentParser(description="Search OpenAlex for scholarly works")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--doi", help="Resolve a single DOI")
    parser.add_argument("--mailto", default=DEFAULT_EMAIL, help="Email for polite pool")
    parser.add_argument("--from-year", type=int, help="Start year filter")
    parser.add_argument("--to-year", type=int, help="End year filter")
    parser.add_argument("--min-citations", type=int, help="Minimum citation count")
    parser.add_argument("--type", dest="work_type", help="Work type filter")
    parser.add_argument("--open-access", action="store_true", help="Only open access")
    parser.add_argument("--sort", default="relevance_score:desc", help="Sort order")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--output", "-o", help="Output BibTeX file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of BibTeX")

    args = parser.parse_args()

    if args.doi:
        work = resolve_doi(args.doi, args.mailto)
        if not work:
            print(f"ERROR: Could not resolve DOI: {args.doi}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(work, indent=2))
        else:
            print(work_to_bibtex(work))
        sys.exit(0)

    if not args.query:
        parser.error("Either --query or --doi is required")

    works = search_works(
        query=args.query,
        mailto=args.mailto,
        from_year=args.from_year,
        to_year=args.to_year,
        min_citations=args.min_citations,
        work_type=args.work_type,
        open_access=args.open_access,
        sort=args.sort,
        limit=args.limit,
    )

    if not works:
        print("No results found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(works)} results.", file=sys.stderr)

    if args.json:
        output = json.dumps(
            [
                {
                    "title": w.get("title"),
                    "year": w.get("publication_year"),
                    "doi": w.get("doi"),
                    "cited_by_count": w.get("cited_by_count"),
                    "type": w.get("type"),
                    "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
                    "authors": [
                        a.get("author", {}).get("display_name")
                        for a in w.get("authorships", [])
                    ],
                }
                for w in works
            ],
            indent=2,
        )
    else:
        output = "\n\n".join(work_to_bibtex(w) for w in works)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(output)

    sys.exit(0)


if __name__ == "__main__":
    main()
