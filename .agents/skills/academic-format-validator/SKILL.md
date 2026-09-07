---
name: academic-format-validator
description: >
  Always-on Output Format Gate: validates document formatting across Markdown
  (drafts), LaTeX (.tex) and Word (.docx) — whichever are present — reusing the
  latex and docx skill validators. Auto-detects artifacts, runs a self-contained
  Markdown linter, and blocks on structural breakage. Trigger:
  /academic-format-validator, "validate formatting", "check format",
  "format gate", "validate docx", "validate markdown".
allowed-tools: [Read, Write, Edit, Bash, Grep]
metadata:
  version: "1.0"
  depends_on: ["latex", "docx", "academic-reviewer"]
---

# Virtualenv

```bash
source .venv/bin/activate
```

Python scripts are stdlib-only; LaTeX/DOCX validation shells out to the `latex`
and `docx` skill scripts (which have their own dependencies — TeX Live, etc.).

# Academic Format Validator

The **always-on Output Format Gate**. Validates the formatting of every document
artifact the project produces — Markdown drafts, LaTeX sources, and Word documents
— and blocks finalization on structural breakage. It is the engine that makes
"automated formatting validation is always performed" true, and feeds **Dimension 6
(Format & Bibliographic Compliance)** of `academic-reviewer`.

## When To Use

- Before finalizing output (Phase 8) — validate `.md` + `.tex` + `.docx`.
- As an early advisory pass on `draft/*.md` during writing.
- Any time formatting consistency must be confirmed (md/tex/docx).

## When Not To Use

- To validate data/results congruence → use `academic-data-validator`.
- To validate citations/bibliography → use `academic-citation-manager` + `academic-bibliography-manager`.
- To compile/convert to a venue template → use `latex` / `latex-template-converter`.

## Prerequisites

1. **Draft** — `draft/*.md` (always present).
2. **Output** — `output/*.tex` and/or `output/*.docx` (validated when present).

## Method

### Phase 1: Auto-detect artifacts

Discover what to validate: `draft/**/*.md` always; LaTeX/DOCX recursively in the
canonical `output/` and `draft/` directories, plus the project root's top-level
`.tex`/`.docx` files. Never descends into stale `output_v*` siblings or vendor
templates (excluded by name). Falls back to the project root only when neither
`output/` nor `draft/` exists.

### Phase 2: Markdown (always, self-contained)

```bash
python scripts/check_markdown.py draft/ --require "Abstract,Introduction,Methods,Results,Discussion,Conclusion"
```
Checks heading hierarchy, closed fences/frontmatter, table well-formedness,
image/link integrity, required-section presence. See `references/format-rules.md`.

### Phase 3: LaTeX (reuse latex skill) + DOCX (reuse docx skill)

```bash
# Full gate (Phase 8): compiles main .tex (BLOCKING on failure), validates .docx schema.
python scripts/validate_formats.py <project_dir> --compile
```
- Main `.tex` → `compile_latex.sh` (BLOCKING with `--compile`), `check_figures.py` (WARNING).
- Body-only `.tex` → `validate_latex.py` (BLOCKING on structural errors).
- `.docx` → `docx/scripts/office/validate.py` (BLOCKING on schema-invalid).

### Phase 4: Aggregate + gate

`validate_formats.py` writes `review/format-validation-report.md` and returns the
gate exit code (0 = PASS/PASS-with-warnings, 1 = FAIL).

```bash
# Validate a single explicit artifact (used by paper-generator-agent):
python scripts/validate_formats.py output/paper.tex --compile
python scripts/validate_formats.py output/paper.docx
```

## Always-On Enforcement

Enforced two ways (see the orchestrator and each harness config):

1. **Blocking gate (primary)** — the **Output Format Gate** runs in Phase 8 and is
   non-skippable; a BLOCKING result stops finalization.
2. **Automated hook (reinforcement)** — `scripts/hook_format_check.sh` is wired into
   every harness so the markdown check runs automatically:
   - Claude Code: `Stop` / `SubagentStop` hook in `.claude/settings.json`.
   - Codex CLI: `PostToolUse` / `Stop` hook in `.codex/hooks.json`.
   - OpenCode: `tool.execute.after` / `session.idle` plugin in `.opencode/plugins/`.
   The hook is **self-guarding** (acts only on a recently modified paper project)
   and **advisory** (exit 0); hard blocking is the gate's job.

## Two-tier Gate Semantics

| Tier | Examples | Effect |
|------|----------|--------|
| **BLOCKING** (exit 1) | unclosed fence/frontmatter, missing image, `.tex` compile failure, schema-invalid `.docx` | Pipeline blocked; Dimension 6 capped ≤ 50 |
| **WARNING** (exit 0) | heading skips, table raggedness, figure DPI, chktex lint | Surfaced; not blocking |

## Self-Review

### Deterministic
- [ ] Markdown linter run on all `draft/*.md`; 0 BLOCKING.
- [ ] Every present `.tex`/`.docx` validated; 0 BLOCKING.
- [ ] `review/format-validation-report.md` written with exit code.

### Agentic
- [ ] Warnings triaged (heading structure, figures, style).
- [ ] Required sections confirmed against the outline/PRD.

## Output

```markdown
# Format Validation Report (Output Format Gate)
- **Gate result**: ✅ PASS | ⚠️ PASS (with warnings) | ❌ FAIL
- table of formats: present / artifacts / findings
- Blocking findings (list) · Warnings (list)
```

## References

- `references/format-rules.md` — per-format checks and severities.

## Related

- `latex`, `docx` — provide the underlying compile/schema validators reused here.
- `academic-reviewer` — Dimension 6 scores this gate's output qualitatively.
