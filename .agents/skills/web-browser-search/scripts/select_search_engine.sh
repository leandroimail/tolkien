#!/bin/bash
# select_search_engine.sh
# Determines which search engine to use based on available API keys.
# Output: "brave" or "duckduckgo" (one word, to stdout)
#
# Usage:
#   ENGINE=$(bash scripts/select_search_engine.sh)
#   echo "Using: $ENGINE"

if [ -n "$BRAVE_SEARCH_API_KEY" ]; then
    echo "brave"
else
    echo "duckduckgo"
fi
