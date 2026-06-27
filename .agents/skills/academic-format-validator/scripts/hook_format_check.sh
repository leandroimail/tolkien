#!/usr/bin/env bash
# Always-on format-validation hook for the tolkien pipeline.
#
# Wired into Claude Code, Codex CLI and OpenCode. SELF-GUARDING: it only acts when
# a paper project (with a draft/ folder) was modified recently; otherwise it exits 0
# silently so it never adds noise to unrelated sessions.
#
# Two modes:
#   (default)   ADVISORY  — prints findings, ALWAYS exits 0. Use on Stop / session.idle
#                           (a "blocking" Stop means "don't stop / loop again", which is
#                           the wrong semantics here).
#   --enforce   BLOCKING  — on a BLOCKING-tier finding it prints the reason to stderr and
#                           exits 2. Use on the tool-after path (Codex PostToolUse,
#                           OpenCode tool.execute.after, Claude PostToolUse) so a broken
#                           edit is actively rejected.
#
# It runs the fast, stage-independent Markdown structural check (unclosed fences /
# frontmatter, missing referenced images). The deeper Data Integrity (G4.5) and full
# Output Format gates remain the pipeline's blocking enforcement (they are heavier:
# LaTeX compile, DOCX schema, table arithmetic).
#
# Reads (and ignores) any hook JSON payload on stdin.

set -uo pipefail

ENFORCE=0
[ "${1:-}" = "--enforce" ] && ENFORCE=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK_MD="$SCRIPT_DIR/check_markdown.py"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." 2>/dev/null && pwd || echo "$PWD")"

# Drain stdin (hook payload) without failing if empty.
[ -t 0 ] || cat >/dev/null 2>&1 || true

# Pick a Python interpreter (prefer the project venv).
PY=""
for cand in "$REPO_ROOT/.venv/bin/python" "$REPO_ROOT/.venv/bin/python3" python3 python; do
  if command -v "$cand" >/dev/null 2>&1 || [ -x "$cand" ]; then PY="$cand"; break; fi
done
[ -n "$PY" ] || exit 0

# Find paper projects with a draft/ folder modified in the last 2 hours.
RECENT_PROJECT=""
for root in papers projects .papers .projects; do
  dir="$REPO_ROOT/$root"
  [ -d "$dir" ] || continue
  while IFS= read -r draftdir; do
    [ -n "$draftdir" ] || continue
    if find "$draftdir" -type f -name '*.md' -mmin -120 2>/dev/null | grep -q .; then
      RECENT_PROJECT="$(dirname "$draftdir")"
      break
    fi
  done < <(find "$dir" -maxdepth 2 -type d -name draft 2>/dev/null)
  [ -n "$RECENT_PROJECT" ] && break
done

# No recently-touched paper project → stay silent.
[ -n "$RECENT_PROJECT" ] || exit 0
[ -f "$CHECK_MD" ] || exit 0

# Run the fast Markdown structural check; capture output + exit code (1 = BLOCKING).
OUT="$("$PY" "$CHECK_MD" "$RECENT_PROJECT/draft" 2>/dev/null)"
RC=$?

if [ "$ENFORCE" = "1" ] && [ "$RC" -ne 0 ]; then
  # Active enforcement: reject on BLOCKING-tier findings.
  echo "── [tolkien] BLOCKING format issues in $RECENT_PROJECT/draft ──" >&2
  echo "$OUT" | grep "BLOCKING" >&2
  echo "Fix the BLOCKING items above (or run academic-format-validator) before continuing." >&2
  exit 2
fi

# Advisory: surface findings without halting.
echo "── [tolkien] Automated format check: $RECENT_PROJECT/draft ──"
echo "$OUT"
echo "── (advisory; run the Output Format Gate before finalizing: academic-format-validator) ──"
exit 0
