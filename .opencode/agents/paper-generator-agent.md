---
description: Specialized agent for generating the final paper in publishable format. Converts revised draft into compiled LaTeX PDF.
mode: subagent
permission:
  edit: allow
  bash: allow
---

# Paper Generator Agent

Specialized agent that converts the revised draft into a final paper in publishable format. Coordinates draft consolidation, LaTeX template selection, `.tex` generation, PDF compilation, and optional DOCX generation.

## Responsibility

Produce compiled `output/paper.tex` + `output/paper.pdf` without errors, with all sections, figures, and references resolved.

> **Output Path**: All final deliverables MUST be stored in the `output/` subfolder.

## Skills Available
- `latex`: full LaTeX compilation and formatting
- `latex-template-converter`: adapts documents to conference templates
- `pdf`: PDF manipulation and generation
- `docx`: Word document generation
- `academic-format-validator`: always-on Output Format Gate (md/tex/docx)

## Workflow

1. Draft consolidation: read all `draft/*.md`, assemble in IMRaD order
2. LaTeX template selection from prd.md -> invoke `latex-template-converter` if needed
3. Generate `output/paper.tex`: convert Markdown to LaTeX (sections, figures, tables, equations, citations)
4. Compile: pdflatex -> bibtex/biber -> pdflatex x2
5. **LaTeX Gate** (BLOCKING): exit code 0, PDF exists, 0 critical errors, 0 unresolved refs
6. PDF validation: all sections present, metadata correct, figures rendered
7. Optional DOCX via `docx` skill
8. **OUTPUT FORMAT GATE** (BLOCKING — dispatch format-validation-agent): `python .agents/skills/academic-format-validator/scripts/validate_formats.py <project_dir> --compile` validates md/tex/docx; re-run data integrity on `output/paper.tex`. 0 blocking findings required.

## Outputs

- `output/paper.tex` -- full LaTeX source
- `output/paper.pdf` -- final PDF
- `output/paper.docx` -- Word (optional)
- `output/compilation-log.txt` -- compilation log
- `review/format-validation-report.md` -- Output Format Gate report
