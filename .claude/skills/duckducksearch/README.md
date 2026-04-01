# DuckDuckGo Search Skill

A Python-based skill for web searching using DuckDuckGo search engine.

## Features

- **Text Search** - Search web pages with advanced filtering
- **Image Search** - Find images with size, color, and license filters
- **Video Search** - Search videos with resolution and duration options
- **News Search** - Get latest news with time filters

## Installation

```bash
pip install duckduckgo-search
```

Or use the renamed package:

```bash
pip install ddgs
```

## Quick Start

```python
from duckduckgo_search import DDGS

# Text search
results = DDGS().text("python programming", max_results=10)

# Image search
images = DDGS().images("landscape", max_results=20)

# Video search
videos = DDGS().videos("tutorial", max_results=10)

# News search
news = DDGS().news("technology", max_results=10)
```

## Documentation

See [SKILL.md](./SKILL.md) for detailed documentation including:

- All search methods and parameters
- Available regions
- Search operators
- Proxy configuration
- Error handling

## CLI Usage

```bash
# Text search
ddgs text -k "query"

# Image search
ddgs images -k "query" -m 50

# News search
ddgs news -k "query" -m 20 -t d
```

## Requirements

- Python >= 3.9
- `duckduckgo-search` package

## License

MIT License
