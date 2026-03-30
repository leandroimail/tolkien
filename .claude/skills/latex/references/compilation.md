# Compilation Reference

## Table of Contents
1. [Quick Commands](#quick-commands)
2. [compile_latex.sh Flags](#compile_latexsh-flags)
3. [Engine Auto-Detection](#engine-auto-detection)
4. [latexmk Reference](#latexmk-reference)
5. [Troubleshooting](#troubleshooting)

---

## Quick Commands

```bash
# One-time build (latexmk — recommended)
latexmk -pdf main.tex

# Live preview (auto-rebuild on save)
latexmk -pvc -pdf main.tex

# Force rebuild
latexmk -gg -pdf main.tex

# Clean auxiliary files (keep PDF)
latexmk -c

# Clean everything including PDF
latexmk -C

# Non-interactive (CI/scripts)
latexmk -pdf -interaction=nonstopmode main.tex

# With SyncTeX (for editor source sync)
latexmk -pdf -synctex=1 main.tex

# XeLaTeX (for CJK, fontspec, custom fonts)
latexmk -xelatex main.tex

# LuaLaTeX (for luacode, advanced scripting)
latexmk -lualatex main.tex
```

## compile_latex.sh Flags

If the project uses the `latex-document` compile script:

```bash
bash compile_latex.sh main.tex                    # Auto-detect engine
bash compile_latex.sh main.tex --preview          # Compile + PNG page previews
bash compile_latex.sh main.tex --verbose          # Full log output
bash compile_latex.sh main.tex --quiet            # Errors only
bash compile_latex.sh main.tex --engine xelatex   # Force engine
bash compile_latex.sh main.tex --use-latexmk      # latexmk backend
bash compile_latex.sh main.tex --pdfa             # PDF/A output (thesis/archival)
bash compile_latex.sh main.tex --clean            # Remove aux files, no compile
bash compile_latex.sh main.tex --preview --preview-dir ./outputs
```

**Log filtering**: When `texfot` is available (included with TeX Live), noisy package messages
are filtered automatically in default verbosity. Use `--verbose` for unfiltered output.

## Engine Auto-Detection

| Trigger in .tex | Engine Used |
|---|---|
| `fontspec`, `xeCJK`, `polyglossia` | xelatex |
| `luacode`, `luatextra` | lualatex |
| (default) | pdflatex |

Override with `--engine` when auto-detection is wrong.

## latexmk Reference

**Why latexmk?** Runs the correct number of compilation passes automatically (handles
cross-references, bibliography, index, glossaries). Recommended for all documents with
`\bibliography{}`, `\addbibresource{}`, `\makeindex`, or `\makeglossaries`.

**Multi-pass sequence (manual fallback):**
```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main          # or: biber main (for biblatex)
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

**.latexmkrc for project settings:**
```perl
# Force xelatex
$pdf_mode = 5;
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode %O %S';
```

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `latexmk not found` | Not in PATH | Add `/Library/TeX/texbin` to PATH |
| `Undefined control sequence` | Missing package | Check `\usepackage` for required package |
| References show `??` | Need multiple passes | latexmk handles this automatically |
| Build hangs | Interactive prompt triggered | Use `-interaction=nonstopmode` |
| PDF not updating | Build error | Check `.log` for the specific error |
| `SyncTeX not working` | Missing flag | Add `-synctex=1` |
| `Too many aux files` | Normal build artifacts | Run `latexmk -c` |
| `dpkg lock` error | Parallel install conflict | Install TeX Live once, then compile |
| `Package not found` | TeX Live package missing | `sudo tlmgr install <package>` |
| `.bbl file not found` | BibTeX not run | Run bibtex/biber manually or use latexmk |
| `I can't find file` | Missing .tex include | Verify `\input{}` or `\include{}` path |

**Reading the .log file:**
- Search for `! ` (exclamation mark) for fatal errors
- Search for `Warning:` for non-fatal issues
- Error lines show the line number: `l.123 \badcommand`
- `Overfull \hbox` with > 10pt badness needs attention
