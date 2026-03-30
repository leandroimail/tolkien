#!/usr/bin/env bash
# validate_skill.sh — Validates an Agent Skill directory against the official specification.
# Usage: bash scripts/validate_skill.sh <path-to-skill-directory>
#
# Checks:
#   1. SKILL.md exists
#   2. YAML frontmatter is present and valid
#   3. name field follows spec rules
#   4. description field is non-empty
#   5. Directory name matches name field
#   6. SKILL.md body is under 500 lines
#   7. File references use relative paths
#   8. No hardcoded credentials detected
#   9. No deeply nested references
#  10. Forward slashes in paths

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0
WARN=0

pass() {
  echo -e "  ${GREEN}✅ PASS${NC}: $1"
  PASS=$((PASS + 1))
}

fail() {
  echo -e "  ${RED}❌ FAIL${NC}: $1"
  FAIL=$((FAIL + 1))
}

warn() {
  echo -e "  ${YELLOW}⚠️  WARN${NC}: $1"
  WARN=$((WARN + 1))
}

# --- Argument validation ---
if [ $# -lt 1 ]; then
  echo "Usage: bash validate_skill.sh <path-to-skill-directory>"
  echo "Example: bash validate_skill.sh .agents/skills/my-skill"
  exit 1
fi

SKILL_DIR="$1"
SKILL_FILE="$SKILL_DIR/SKILL.md"
DIR_NAME=$(basename "$SKILL_DIR")

echo ""
echo "═══════════════════════════════════════════════════"
echo "  Agent Skill Validation Report"
echo "  Directory: $SKILL_DIR"
echo "═══════════════════════════════════════════════════"
echo ""

# --- Check 1: SKILL.md exists ---
echo "📄 File Structure"
if [ -f "$SKILL_FILE" ]; then
  pass "SKILL.md exists"
else
  fail "SKILL.md not found at $SKILL_FILE"
  echo ""
  echo "Result: Cannot continue without SKILL.md"
  exit 1
fi

# --- Check 2: YAML frontmatter ---
echo ""
echo "📋 Frontmatter"
FRONTMATTER=$(sed -n '/^---$/,/^---$/p' "$SKILL_FILE")
if [ -n "$FRONTMATTER" ]; then
  pass "YAML frontmatter block detected"
else
  fail "No YAML frontmatter found (must start and end with ---)"
fi

# --- Check 3: name field ---
NAME_LINE=$(echo "$FRONTMATTER" | grep -E "^name:" | head -1 || true)
if [ -n "$NAME_LINE" ]; then
  NAME_VALUE=$(echo "$NAME_LINE" | sed 's/^name:[[:space:]]*//')
  
  # Check lowercase + hyphens only
  if echo "$NAME_VALUE" | grep -qE '^[a-z0-9]([a-z0-9-]*[a-z0-9])?$'; then
    pass "name field is valid: '$NAME_VALUE'"
  else
    fail "name field contains invalid characters: '$NAME_VALUE' (must be lowercase letters, numbers, hyphens only; cannot start/end with hyphen)"
  fi
  
  # Check length
  NAME_LEN=${#NAME_VALUE}
  if [ "$NAME_LEN" -le 64 ]; then
    pass "name length is $NAME_LEN chars (max 64)"
  else
    fail "name length is $NAME_LEN chars (exceeds max 64)"
  fi
  
  # Check consecutive hyphens
  if echo "$NAME_VALUE" | grep -q '\-\-'; then
    fail "name contains consecutive hyphens: '$NAME_VALUE'"
  else
    pass "No consecutive hyphens in name"
  fi
  
  # Check directory match
  if [ "$NAME_VALUE" = "$DIR_NAME" ]; then
    pass "name matches directory name: '$DIR_NAME'"
  else
    fail "name '$NAME_VALUE' does not match directory name '$DIR_NAME'"
  fi
else
  fail "name field not found in frontmatter"
fi

# --- Check 4: description field ---
DESC_CONTENT=$(sed -n '/^---$/,/^---$/p' "$SKILL_FILE" | sed '1d;$d')
if echo "$DESC_CONTENT" | grep -q "description:"; then
  DESC_VALUE=$(echo "$DESC_CONTENT" | sed -n '/^description:/,/^[a-z]/p' | head -5 | sed 's/^description:[[:space:]]*//' | tr -d '\n' | sed 's/^[[:space:]]*//')
  if [ -n "$DESC_VALUE" ] && [ "$DESC_VALUE" != ">" ]; then
    DESC_LEN=${#DESC_VALUE}
    pass "description field is present ($DESC_LEN chars)"
    if [ "$DESC_LEN" -gt 1024 ]; then
      fail "description exceeds 1024 characters ($DESC_LEN)"
    fi
  else
    # Multi-line description with >
    pass "description field is present (multi-line)"
  fi

  # Check third person
  if echo "$DESC_VALUE" | grep -qiE "^(I can|I will|You can|You should)"; then
    fail "description should be third person (avoid 'I can', 'You can')"
  else
    pass "description uses appropriate voice"
  fi
else
  fail "description field not found in frontmatter"
fi

# --- Check 5: Body line count ---
echo ""
echo "📏 Body Size"
BODY_START=$(grep -n '^---$' "$SKILL_FILE" | sed -n '2p' | cut -d: -f1)
if [ -n "$BODY_START" ]; then
  TOTAL_LINES=$(wc -l < "$SKILL_FILE" | tr -d ' ')
  BODY_LINES=$((TOTAL_LINES - BODY_START))
  if [ "$BODY_LINES" -le 500 ]; then
    pass "SKILL.md body has $BODY_LINES lines (max 500)"
  else
    fail "SKILL.md body has $BODY_LINES lines (exceeds max 500)"
  fi
fi

# --- Check 6: Relative paths ---
echo ""
echo "🔗 File References"
if grep -qnE '\(/[A-Z]|(/Users/|/home/|/var/|/etc/)' "$SKILL_FILE"; then
  fail "Absolute paths detected in SKILL.md"
  grep -nE '\(/[A-Z]|(/Users/|/home/|/var/|/etc/)' "$SKILL_FILE" | head -5 | while read -r line; do
    echo "     $line"
  done
else
  pass "No absolute paths detected"
fi

# Forward slashes check (no backslashes in paths)
if grep -qnE '\\[a-zA-Z]' "$SKILL_FILE"; then
  warn "Backslash path separators detected (not portable)"
else
  pass "All paths use forward slashes"
fi

# --- Check 7: Nested references ---
echo ""
echo "🔍 Reference Depth"
if [ -d "$SKILL_DIR/references" ]; then
  NESTED=0
  for ref_file in "$SKILL_DIR/references"/*.md; do
    if [ -f "$ref_file" ]; then
      if grep -qlE '\[.*\]\(references/' "$ref_file" 2>/dev/null; then
        warn "Nested reference detected in $(basename "$ref_file")"
        NESTED=1
      fi
    fi
  done
  if [ $NESTED -eq 0 ]; then
    pass "No deeply nested references found"
  fi
else
  pass "No references directory (simple skill)"
fi

# --- Check 8: Credential check ---
echo ""
echo "🔒 Security"
CRED_PATTERNS="(api[_-]?key|secret[_-]?key|password|token|credentials)[[:space:]]*[:=][[:space:]]*['\"][^'\"]+"
if grep -qiE "$CRED_PATTERNS" "$SKILL_FILE"; then
  fail "Potential hardcoded credentials in SKILL.md"
else
  pass "No hardcoded credentials in SKILL.md"
fi

if [ -d "$SKILL_DIR/scripts" ]; then
  SCRIPT_CREDS=0
  for script_file in "$SKILL_DIR/scripts"/*; do
    if [ -f "$script_file" ]; then
      if grep -qiE "$CRED_PATTERNS" "$script_file" 2>/dev/null; then
        fail "Potential hardcoded credentials in $(basename "$script_file")"
        SCRIPT_CREDS=1
      fi
    fi
  done
  if [ $SCRIPT_CREDS -eq 0 ]; then
    pass "No hardcoded credentials in scripts"
  fi
fi

# --- Check 9: Tool-specific language ---
echo ""
echo "🔄 Portability"
if grep -qiE "(Claude Code's|Gemini CLI's|Codex's|Cursor's) (Read|Write|Bash|tool)" "$SKILL_FILE"; then
  warn "Tool-specific language detected (reduces portability)"
else
  pass "No tool-specific language detected"
fi

# --- Check 10: Optional directories ---
echo ""
echo "📁 Directory Structure"
for dir in scripts references assets; do
  if [ -d "$SKILL_DIR/$dir" ]; then
    COUNT=$(find "$SKILL_DIR/$dir" -type f | wc -l | tr -d ' ')
    pass "$dir/ directory found ($COUNT files)"
  fi
done

# --- Check 11: Reference files with TOC ---
if [ -d "$SKILL_DIR/references" ]; then
  for ref_file in "$SKILL_DIR/references"/*.md; do
    if [ -f "$ref_file" ]; then
      REF_LINES=$(wc -l < "$ref_file" | tr -d ' ')
      if [ "$REF_LINES" -gt 100 ]; then
        if grep -qiE "^## (Table of Contents|Contents|TOC)" "$ref_file"; then
          pass "$(basename "$ref_file") ($REF_LINES lines) has Table of Contents"
        else
          warn "$(basename "$ref_file") ($REF_LINES lines) — consider adding Table of Contents"
        fi
      fi
    fi
  done
fi

# --- Summary ---
echo ""
echo "═══════════════════════════════════════════════════"
echo "  Summary"
echo "═══════════════════════════════════════════════════"
echo -e "  ${GREEN}Passed${NC}: $PASS"
echo -e "  ${RED}Failed${NC}: $FAIL"
echo -e "  ${YELLOW}Warnings${NC}: $WARN"
echo ""

if [ $FAIL -eq 0 ]; then
  echo -e "  ${GREEN}✅ Skill validation PASSED${NC}"
  exit 0
else
  echo -e "  ${RED}❌ Skill validation FAILED — fix $FAIL issue(s) above${NC}"
  exit 1
fi
