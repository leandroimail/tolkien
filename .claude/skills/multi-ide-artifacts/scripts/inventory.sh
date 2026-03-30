#!/usr/bin/env bash
# inventory.sh — Lists all AI artifact files in a repository (up to depth 4).
# Usage: bash scripts/inventory.sh [root_dir]
# Outputs sorted file paths for AGENTS.md, SKILL.md and all IDE-specific config files.

ROOT="${1:-.}"

echo "=== AI Artifact Inventory: $ROOT ==="
echo

find "$ROOT" -maxdepth 4 -type f \( \
  -name "AGENTS.md" \
  -o -name "AGENTS.override.md" \
  -o -name "SKILL.md" \
  -o -name "*.prompt.md" \
  -o -name "*.agent.md" \
  -o -name "*.instructions.md" \
  -o -name "opencode.json" \
  -o -name "opencode.jsonc" \
  -o -name "mcp.json" \
  -o -name "config.toml" \
\) \
  | grep -vE '(node_modules|\.git|\.cache)' \
  | sort

echo
echo "=== Duplicate Policy Text Check ==="
grep -Erl "code review|security|test coverage|AGENTS.md|SKILL.md" \
  "$ROOT/.agent" "$ROOT/.agents" "$ROOT/.github" \
  "$ROOT/.opencode" "$ROOT/.kiro" "$ROOT/.qoder" \
  "$ROOT/.vscode" "$ROOT/.codex" 2>/dev/null | sort

echo
echo "=== SKILL.md Frontmatter Validation ==="
grep -Ern "^---$|^name:|^description:" \
  "$ROOT/.agents" "$ROOT/.agent" "$ROOT/.kiro" \
  "$ROOT/.opencode" "$ROOT/.github" "$ROOT/.qoder" 2>/dev/null
