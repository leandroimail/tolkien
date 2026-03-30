#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Reconstruct abstract from OpenAlex inverted index format.

Usage:
    echo '{"word": [0, 5], "another": [1]}' | uv run python -B scripts/reconstruct_abstract.py
    uv run python -B scripts/reconstruct_abstract.py --json '{"The": [0], "study": [1], "examines": [2]}'
"""

import argparse
import json
import sys


def reconstruct(inverted_index: dict) -> str:
    """Convert OpenAlex inverted abstract index to plaintext."""
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(word for _, word in word_positions)


def main():
    parser = argparse.ArgumentParser(
        description="Reconstruct abstract from OpenAlex inverted index"
    )
    parser.add_argument("--json", dest="json_str", help="JSON string of inverted index")
    args = parser.parse_args()

    if args.json_str:
        data = json.loads(args.json_str)
    else:
        data = json.load(sys.stdin)

    print(reconstruct(data))


if __name__ == "__main__":
    main()
