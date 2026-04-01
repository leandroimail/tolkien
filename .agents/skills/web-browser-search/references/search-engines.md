# Search Engines Reference

Detailed usage guide for both search backends supported by the `web-browser-search` skill.

## Table of Contents

- [DuckDuckGo (Default)](#duckduckgo-default)
- [Brave Search (API Key Required)](#brave-search-api-key-required)
- [Choosing Between Engines](#choosing-between-engines)

---

## DuckDuckGo (Default)

No API key required. Uses the `duckduckgo-search` Python package (`pip install duckduckgo-search`).

### Text Search

```python
from duckduckgo_search import DDGS

results = DDGS().text(
    keywords="machine learning healthcare",
    region="wt-wt",          # worldwide (default)
    safesearch="moderate",   # off | moderate | strict
    timelimit="y",           # d=day, w=week, m=month, y=year, None=all
    max_results=20
)

for r in results:
    print(f"Title: {r['title']}")
    print(f"URL:   {r['href']}")
    print(f"Body:  {r['body']}")
```

### Image Search

```python
results = DDGS().images(
    keywords="neural network architecture",
    region="wt-wt",
    safesearch="moderate",
    size=None,            # Small | Medium | Large | Wallpaper
    color=None,           # Monochrome | Red | Orange | Yellow | Green | Blue | Purple | Pink | Brown | Black | Gray | Teal | White
    type_image=None,      # photo | clipart | gif | transparent | line
    layout=None,          # Square | Tall | Wide
    license_image=None,   # any | Public | Share | ShareCommercially | Modify | ModifyCommercially
    max_results=10
)

for r in results:
    print(f"Title: {r['title']}, Image URL: {r['image']}, Size: {r['width']}x{r['height']}")
```

### Video Search

```python
results = DDGS().videos(
    keywords="deep learning tutorial",
    region="wt-wt",
    safesearch="moderate",
    timelimit="m",         # d | w | m
    resolution="high",     # high | standard
    duration="medium",     # short | medium | long
    max_results=10
)

for r in results:
    print(f"Title: {r['title']}, Duration: {r['duration']}, Provider: {r['provider']}")
```

### News Search

```python
results = DDGS().news(
    keywords="artificial intelligence regulation",
    region="wt-wt",
    safesearch="moderate",
    timelimit="w",         # d | w | m
    max_results=20
)

for r in results:
    print(f"Date: {r['date']}, Title: {r['title']}, Source: {r['source']}")
```

### CLI Usage

```bash
source .venv/bin/activate

# Text search
ddgs text -k "machine learning healthcare" -m 10

# With region and time filter
ddgs text -k "AI ethics" -r us-en -t m -m 20

# Export to CSV
ddgs text -k "research filetype:pdf" -m 50 -o results.csv

# News
ddgs news -k "technology" -m 50 -t d -o json

# Images
ddgs images -k "data visualization" -m 20
```

### Search Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `"..."` | `"exact phrase"` | Exact match |
| `-` | `cats -dogs` | Exclude term |
| `+` | `cats +dogs` | Require term |
| `site:` | `site:arxiv.org` | Specific domain |
| `-site:` | `-site:pinterest.com` | Exclude domain |
| `filetype:` | `filetype:pdf` | File type |
| `intitle:` | `intitle:review` | Title must contain |
| `inurl:` | `inurl:2024` | URL must contain |

### Available Regions

| Code | Region | Code | Region |
|------|--------|------|--------|
| `wt-wt` | Worldwide | `us-en` | United States |
| `uk-en` | United Kingdom | `br-pt` | Brazil |
| `de-de` | Germany | `fr-fr` | France |
| `jp-jp` | Japan | `cn-zh` | China |
| `kr-kr` | Korea | `in-en` | India |
| `au-en` | Australia | `ca-en` | Canada |

### Error Handling

```python
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException, RatelimitException

try:
    results = DDGS().text("query", max_results=10)
except RatelimitException:
    # Back off and retry after delay
    import time
    time.sleep(5)
    results = DDGS().text("query", max_results=10)
except DuckDuckGoSearchException as e:
    print(f"Search error: {e}")
```

### Proxy Support

```python
# Tor Browser proxy
ddgs = DDGS(proxy="tb", timeout=20)

# Custom SOCKS5 proxy
ddgs = DDGS(proxy="socks5://user:password@host:port")
```

---

## Brave Search (API Key Required)

Requires `BRAVE_SEARCH_API_KEY` from https://api.search.brave.com.

### Basic Web Search

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=machine+learning+healthcare&count=10" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY"
```

### Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `q` | Search query (required) | URL-encoded string |
| `country` | Market code | `us`, `gb`, `br`, `de`, etc. |
| `search_lang` | Document language | `en`, `pt`, `de`, etc. |
| `count` | Results per page | 1-20 (default 10) |
| `offset` | Pagination offset | 0-9 |
| `safesearch` | Content filter | `off`, `moderate`, `strict` |
| `freshness` | Time filter | `pd` (day), `pw` (week), `pm` (month), `py` (year) |
| `result_filter` | Result types | `web`, `news`, `videos`, etc. |

### Freshness Filter

```bash
# Results from last 24 hours
curl -s "https://api.search.brave.com/res/v1/web/search?q=AI&freshness=pd&count=10" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY"

# Results from last week
# freshness=pw

# Custom date range
# freshness=2024-01-01to2024-12-31
```

### Response Structure

```json
{
  "web": {
    "results": [
      {
        "title": "...",
        "url": "...",
        "description": "...",
        "age": "2 days ago",
        "language": "en"
      }
    ]
  },
  "news": { "results": [...] },
  "videos": { "results": [...] }
}
```

### Search Operators (Brave)

Same as standard: `site:`, `filetype:`, `intitle:`, `inurl:`, `"exact phrase"`, `-exclude`

---

## Choosing Between Engines

| Criteria | DuckDuckGo | Brave |
|----------|-----------|-------|
| API key required | No | Yes (`BRAVE_SEARCH_API_KEY`) |
| Rate limits | Moderate (may throttle) | Higher (paid tiers available) |
| Result quality | Good | Very good |
| Rich data | Basic | Weather, stocks, sports, etc. |
| Custom ranking | No | Goggles support |
| Freshness filters | Basic (d/w/m/y) | Advanced (custom ranges) |
| Best for | Default/fallback, no setup | High-volume, production use |
