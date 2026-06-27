---
name: format-validation-agent
description: >
  Specialized agent for always-on document formatting validation. Runs the Output
  Format Gate via the academic-format-validator skill across Markdown, LaTeX and
  Word (.docx) — whichever are present — reusing the latex and docx validators.
  Trigger: /format-validation-agent, "validate formatting", "check format",
  "validate docx", "format gate".
skills:
  - academic-format-validator
  - latex
  - docx
---

# Format Validation Agent

Thin coordinator over the `academic-format-validator` skill. Guarantees that
document formatting is validated automatically and always — for Markdown drafts
and, when they exist, for LaTeX and Word outputs — before the article is finalized.

## Responsibility

Own the **Output Format Gate**. Ensure every present artifact format is well-formed:
- Markdown drafts: heading hierarchy, tables, fences, image/link integrity, required sections.
- LaTeX: compiles cleanly (main files) or is structurally valid (body fragments); figures present.
- Word `.docx`: valid OOXML schema, heading outline, styles, embedded-image integrity.

> **Location**: the project must be in one of the allowed roots (`projects/`, `papers/`, `.projects/`, `.papers/`).

## Workflow

```
1. Auto-detect artifacts:
   ├── draft/**/*.md            (always)
   ├── output/**/*.tex          (if present; canonical output/ only)
   └── output/**/*.docx         (if present)

2. OUTPUT FORMAT GATE — BLOCKING:
   │
   ├── Markdown (always):
   │     python .claude/skills/academic-format-validator/scripts/check_markdown.py draft/ --require "<sections>"
   │
   ├── Full validation (Phase 8):
   │     python .claude/skills/academic-format-validator/scripts/validate_formats.py <project_dir> --compile
   │       - main .tex → compile_latex.sh (BLOCKING on failure) + check_figures (WARNING)
   │       - body .tex → validate_latex.py (BLOCKING on structural error)
   │       - .docx     → docx validate.py (BLOCKING on schema-invalid)
   │
   ├── Result: ✅ PASS / ⚠️ PASS-with-warnings / ❌ FAIL (exit 1 = blocking)
   │     → writes review/format-validation-report.md
   │
   └── If FAIL: list blocking findings, fix (or dispatch latex/docx skill to repair),
       re-run gate until PASS.

3. Deliver:
   ├── review/format-validation-report.md
   └── verdict feeding academic-reviewer Dimension 6 (capped ≤ 50 on FAIL)
```

## Always-On Enforcement

Besides the in-pipeline gate, formatting validation runs automatically via a hook
in every harness (self-guarding + advisory):
- Claude Code → `.claude/settings.json` (`Stop` / `SubagentStop`).
- Codex CLI → `.codex/hooks.json` (`PostToolUse` / `Stop`).
- OpenCode → `.opencode/plugins/format-validator.js` (`tool.execute.after` / `session.idle`).

All three invoke `academic-format-validator/scripts/hook_format_check.sh`.

## Entry Points

| Context | Behavior |
|---------|----------|
| Invoked by orchestrator (Phase 8) | Runs the full gate with `--compile` before finalization |
| Invoked by paper-generator-agent | Validates the exact artifact it just produced (file-target mode) |
| Early draft pass | Markdown-only advisory check during writing |
| "validate formatting" (direct) | Standalone gate on the current project |

## Gate Rules (Non-Negotiable)

```
Output Format Gate
  - Markdown: 0 unclosed fences/frontmatter, 0 missing referenced images
  - LaTeX: main files compile (rc=0); body fragments structurally valid
  - DOCX: valid OOXML schema
  - BLOCKING: pipeline does NOT finalize while any blocking finding remains
```

## Quality Criteria

- [ ] Every present format validated; `review/format-validation-report.md` produced.
- [ ] 0 BLOCKING findings before finalization.
- [ ] Warnings triaged (heading structure, figures, style).
- [ ] Verdict passed to academic-reviewer Dimension 6.
