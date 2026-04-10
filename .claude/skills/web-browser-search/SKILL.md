---
name: web-browser-search
description: >
  Unified web search and browser automation. Uses DuckDuckGo by default or
  Brave Search when BRAVE_SEARCH_API_KEY is set. Uses agent-browser or
  playwright-cli for page navigation and content extraction. Use when the user
  needs to search the web, browse a URL, validate a DOI online, extract web
  page content, or automate browser interactions. Trigger: /web-browser-search,
  "search the web", "browse URL", "validate DOI online", "check URL",
  "web search", "open website".
allowed-tools: [Bash, Read, Write, Edit]
compatibility: >
  Requires Python 3.9+ with duckduckgo-search package. Optional: agent-browser
  (npm), playwright-cli (npm), Chrome/Chromium. Network access required.
  Run resources/install_skills_deps.sh to install all dependencies.
metadata:
  version: "1.0"
  depends_on: ["web-search", "duckducksearch", "agent-browser", "playwright-cli"]
---

# Virtualenv

Note: When this skill executes Python scripts, run them within the project's virtual environment.
Activate with:

```bash
source .venv/bin/activate
```

# Web Browser Search

Unified interface for web searching and browser automation. Coordinates four
underlying skills to provide seamless web access for the tolkien pipeline and
standalone use.

## Purpose

Provide a single entry point for:
- **Web search**: finding information, papers, reports, DOI metadata
- **Browser automation**: navigating pages, extracting content, validating URLs

## When To Use

- Searching the web for information not available via OpenAlex API
- Browsing a specific URL to extract content or validate it resolves
- Validating DOI resolution (checking `https://doi.org/{DOI}` resolves)
- Extracting metadata from publisher landing pages
- Searching for grey literature (reports, preprints, standards)
- Verifying reference existence via web search
- Checking retraction notices for academic papers
- Any task requiring programmatic web interaction

## When Not To Use

- Systematic academic literature search → use `academic-researcher` (OpenAlex)
- Validating BibTeX field completeness → use `academic-bibliography-manager`
- Verifying in-text citations → use `academic-citation-manager`

## Search Engine Selection

Run the selector script to determine which search engine to use:

```bash
ENGINE=$(bash scripts/select_search_engine.sh)
# Returns: "brave" or "duckduckgo"
```

| Condition | Engine | Skill |
|-----------|--------|-------|
| `$BRAVE_SEARCH_API_KEY` is set and non-empty | Brave Search API | `web-search` |
| Default (no API key) | DuckDuckGo | `duckducksearch` |

### DuckDuckGo Search (Default)

No API key required. Uses the `duckduckgo-search` Python package.

```python
from duckduckgo_search import DDGS

# Text search
results = DDGS().text("machine learning healthcare", max_results=10)
# Each result: {"title": "...", "href": "...", "body": "..."}

# News search
news = DDGS().news("AI regulation 2026", max_results=10)

# Image search
images = DDGS().images("neural network architecture diagram", max_results=5)
```

**CLI usage:**
```bash
source .venv/bin/activate
ddgs text -k "query here" -m 10
ddgs news -k "topic" -m 10 -t d   # last day
```

**Search operators:** `"exact phrase"`, `site:example.com`, `-exclude`, `filetype:pdf`, `intitle:keyword`

**Regions:** `wt-wt` (worldwide), `us-en`, `uk-en`, `br-pt`, `de-de`, `fr-fr`

> For full DuckDuckGo reference: see `duckducksearch` skill

### Brave Search (When API Key Available)

Requires `BRAVE_SEARCH_API_KEY` environment variable.

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=query+here&count=10" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY"
```

**Features:** freshness filters, SafeSearch, Goggles (custom ranking), rich data enrichments.

> For full Brave Search reference: see `web-search` skill

## Browser Tool Selection

| Condition | Tool | Skill |
|-----------|------|-------|
| `agent-browser` is installed | agent-browser (preferred — richer API) | `agent-browser` |
| Fallback | playwright-cli | `playwright-cli` |

Check availability:
```bash
command -v agent-browser &>/dev/null && echo "agent-browser" || echo "playwright-cli"
```

### agent-browser (Preferred)

Chrome DevTools Protocol-based automation.

```bash
# Navigate and extract
agent-browser open "https://example.com"
agent-browser snapshot -i                    # get interactive elements
agent-browser get text @e1                   # extract text from element
agent-browser screenshot page.png            # capture screenshot

# DOI validation
agent-browser open "https://doi.org/10.1234/example"
agent-browser wait --load networkidle
agent-browser get url                        # check final resolved URL
agent-browser get title                      # get page title

# Form interaction
agent-browser fill @e2 "search query"
agent-browser click @e3
agent-browser wait --text "Results"
```

> For full agent-browser reference: see `agent-browser` skill

### playwright-cli (Fallback)

Playwright framework-based automation.

```bash
# Navigate and extract
playwright-cli open "https://example.com"
playwright-cli snapshot                      # get page elements
playwright-cli get text e1                   # extract text
playwright-cli screenshot                    # capture screenshot

# DOI validation
playwright-cli open "https://doi.org/10.1234/example"
playwright-cli eval "document.URL"           # check final URL
playwright-cli eval "document.title"         # get page title
```

> For full playwright-cli reference: see `playwright-cli` skill

## Common Workflows

### 1. Search and Extract

Search for information, then browse top results for full content.

```
1. Run search (DuckDuckGo or Brave) with query
2. Parse results → get URLs of top hits
3. For each relevant URL:
   a. Open in browser (agent-browser or playwright-cli)
   b. Wait for page load
   c. Extract relevant text content
   d. Close page
4. Return consolidated results
```

### 2. DOI Validation

Verify that a DOI resolves to a valid publisher page.

```
1. Open https://doi.org/{DOI} in browser
2. Wait for redirect to complete (networkidle)
3. Get final URL → if not an error page, DOI is valid
4. Optionally extract metadata from the landing page:
   - Title, authors, journal, year
   - Use as fallback enrichment for references.bib
```

### 3. Reference Verification

Confirm a paper exists and retrieve its metadata.

```
1. Search for paper title (exact phrase) via web search engine
2. Check if results include the paper on a known publisher/database
3. If found: extract DOI, authors, year from results
4. Optionally browse the paper's page for complete metadata
```

### 4. Retraction Check via Web

When OpenAlex retraction data is unavailable.

```
1. Search: "{paper title} retracted" or "{DOI} retraction notice"
2. Check if Retraction Watch or publisher notices appear in results
3. Flag if retraction evidence found
```

## Quality Checklist

- [ ] Selector script correctly detects search engine based on env var
- [ ] Search returns structured results (title, URL, snippet)
- [ ] Browser tool gracefully handles page load failures
- [ ] DOI validation correctly distinguishes valid/invalid DOIs
- [ ] All web results are treated as unverified (require validation)

## Outputs

- Search results: list of `{title, url, snippet}` objects
- Browser extraction: page text, screenshots, metadata
- DOI validation: `{doi, valid: bool, resolved_url, title}`

## Deep-Dive References

- **Search engines (DuckDuckGo + Brave):** [references/search-engines.md](references/search-engines.md)
- **Browser tools (agent-browser + playwright-cli):** [references/browser-tools.md](references/browser-tools.md)
- **DuckDuckGo full docs:** see `duckducksearch` skill
- **Brave Search full docs:** see `web-search` skill
- **agent-browser full docs:** see `agent-browser` skill
- **playwright-cli full docs:** see `playwright-cli` skill
