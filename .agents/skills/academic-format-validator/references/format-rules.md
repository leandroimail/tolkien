# Format Rules

What the Output Format Gate checks per artifact type, and which findings block.

## Markdown (`check_markdown.py`) — always runs

| Check | Severity |
|-------|----------|
| Code fence opened but never closed | BLOCKING |
| YAML frontmatter opened (`---`) but never closed | BLOCKING |
| Local image target does not exist on disk | BLOCKING |
| Heading skips a level (H1→H3) | WARNING |
| More than one H1 | WARNING |
| Pipe table without a header separator row | WARNING |
| Pipe table with ragged column counts | WARNING |
| Local link target not found | WARNING |
| Required section missing (when `--require` given) | WARNING |

Required sections are advisory and configurable per project/outline, e.g.:
`--require "Abstract,Introduction,Methods,Results,Discussion,Conclusion"`.

## LaTeX — reuses the `latex` skill scripts

The validator dispatches by file type:

- **Main file** (`\documentclass` present):
  - `compile_latex.sh` — authoritative compile gate. **BLOCKING** on failure
    (run with `--compile`, i.e. at Phase 8).
  - `check_figures.py` — figure existence / DPI / caption. **WARNING**.
  - `check_format.py` (chktex) — style lint. **WARNING**, opt-in (`--lint`, noisy).
- **Body-only fragment** (no `\documentclass`):
  - `validate_latex.py` — structural batch check (unbalanced envs, stray `&`,
    undefined commands). **BLOCKING** on errors.

Discovery prefers the canonical `output/` directory; if absent, it scans only the
project root's top-level `.tex` (so stale `output_v*` siblings and vendor templates
are not gated). Vendor/template directories are skipped by name.

## DOCX — reuses the `docx` skill validator

- `docx/scripts/office/validate.py` — OOXML XSD schema validation via
  `DOCXSchemaValidator`. **BLOCKING** on schema-invalid `.docx`.
- If the tool is unavailable, a **WARNING** is emitted (not a silent pass).

Checkable .docx formatting (via the docx skill): schema validity (blocking),
heading outline, named-style usage, ToC field presence, embedded-image
relationship integrity.

## Gate semantics

- **BLOCKING** (exit 1): compile failure, schema-invalid docx, unclosed
  fence/frontmatter, missing referenced image, body-fragment structural errors.
- **WARNING** (exit 0): everything advisory above.
- A BLOCKING result caps `academic-reviewer` Dimension 6 at ≤ 50.
