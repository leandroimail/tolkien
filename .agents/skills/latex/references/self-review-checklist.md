# Self-Review Checklist (Expanded)

Use this expanded checklist during Gate 1 (Code Review) for thorough quality assurance
before compiling. The 3-gate protocol in SKILL.md is mandatory; this file adds depth.

## Syntax Checks

- [ ] All `\begin{ENV}` have matching `\end{ENV}`
- [ ] No stray `%` intended as text (should be `\%`)
- [ ] Braces balanced: `{` count equals `}` count per line
- [ ] No double `$$` used (use `\[...\]` instead)
- [ ] No blank lines inside math environments (causes "missing $ inserted")
- [ ] `\item` only inside `enumerate`, `itemize`, or `description`
- [ ] `\section`, `\subsection` titles not ending with punctuation (except `!` or `?`)

## Package and Command Checks

- [ ] Every used command has its package declared in preamble
- [ ] Package load order correct: `inputenc` → `fontenc` → `babel` → content packages → `hyperref` (last)
- [ ] No conflicting packages (e.g., `subfig` + `subcaption`, `natbib` + `biblatex`)
- [ ] `\usepackage{float}` present if using `[H]` placement
- [ ] `\usepackage{colortbl}` present if using `\rowcolor`
- [ ] `\usepackage{graphicx}` present if using `\includegraphics`

## Text Mode Errors

- [ ] No raw `<` or `>` in text mode — use `$<$`, `$>$`, `\textless`, `\textgreater`
- [ ] Special chars escaped: `%`, `$`, `&`, `#`, `_`, `~`, `^`
- [ ] Ellipsis uses `\ldots` not `...`
- [ ] Date ranges use `--` (en-dash), not `-` (hyphen): `2019--2025`
- [ ] Quotation marks use LaTeX style: `` `single' `` and ` ``double'' `
- [ ] Hyphenation: compound adjectives hyphenated (`state-of-the-art method`)

## Math Environment Checks

- [ ] No `$` inside `align`, `equation`, `gather` environments
- [ ] `\text{}` used for text inside math: `$x \text{ where } x > 0$`
- [ ] `\mathbb{R}` for real numbers, not `\mathbf{R}`
- [ ] Vectors use consistent notation (bold `\mathbf{v}` or arrow `\vec{v}`)
- [ ] Equation numbers present for referenced equations; `\nonumber` or `equation*` for unreferenced

## Float and Reference Checks

- [ ] Every `\label{fig:X}` is referenced somewhere with `\ref{fig:X}` or `\cref{fig:X}`
- [ ] Every `\label{tab:X}` is referenced somewhere with `\ref{tab:X}`
- [ ] Every `\label{eq:X}` is referenced somewhere with `\eqref{eq:X}`
- [ ] Every `\label{alg:X}` is referenced somewhere with `\ref{alg:X}`
- [ ] All `\includegraphics{path}` files exist on disk (check relative paths)
- [ ] Figure captions are self-contained and end with a period
- [ ] Table captions are above the table (convention), figure captions below

## Bibliography Checks

- [ ] Every `\cite{key}` has a matching entry in the `.bib` file
- [ ] No unused `.bib` entries (unless intentional)
- [ ] Bibliography compiled: `bibtex main` or `biber main` depending on backend
- [ ] `\bibliography{refs}` or `\addbibresource{refs.bib}` present
- [ ] `\bibliographystyle{...}` matches venue requirements

## Venue Compliance (Academic Papers)

- [ ] Document class matches target venue (e.g., `neurips_2025`, `acmart`, `IEEEtran`)
- [ ] Anonymous mode configured correctly for blind review (`anonymous` option or equivalent)
- [ ] Author affiliations removed/replaced if anonymous submission
- [ ] ACM CCS concepts present (for ACM venues)
- [ ] Keywords section present
- [ ] TODOs and placeholder text removed (`% TODO`, `[AUTHOR]`, `[CITATION NEEDED]`)
- [ ] Page count within venue limit

## Final Gate Confirmation

After running all checks above, confirm:

```
Gate 1 PASSED: All syntax, package, text, math, float, bib checks resolved
Gate 2 PASSED: latexmk exit code 0, no critical errors in .log
Gate 3 PASSED: PNG previews reviewed, layout and content correct
→ Ready to deliver to user
```
