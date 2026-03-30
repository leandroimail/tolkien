# Academic Review Modules

## Table of Contents
1. [Bibliography Module](#bibliography-module)
2. [Grammar Module](#grammar-module)
3. [Logic Module](#logic-module)
4. [Expression Module](#expression-module)
5. [Figures Module](#figures-module)
6. [Pseudocode Module](#pseudocode-module)
7. [Experiment Module](#experiment-module)
8. [DeAI Module](#deai-module)

---

## Bibliography Module

**When:** Missing citations, unused entries, BibTeX errors, inconsistent citation keys.

**Script:**
```bash
python verify_bib.py references.bib --tex main.tex
```

**Manual checks:**
- Every `\cite{key}` has a matching entry in the `.bib` file
- No entries in `.bib` that are never cited (unless intentional)
- BibTeX keys are consistent (e.g., `Smith2023` not `smith_2023` mixed)
- `@article` entries have: author, title, journal, year, volume, pages
- `@inproceedings` entries have: author, title, booktitle, year, pages
- URLs in `.bib` entries include access date when citing web sources
- No duplicate entries for the same paper
- `doi` field present when available

**Output format:** `% BIB (Key) [ERROR]: Missing field 'pages' in @article{Smith2023}`

---

## Grammar Module

**When:** Surface-level grammar errors, awkward phrasing, non-native English issues.

**Script:**
```bash
python analyze_grammar.py main.tex --section introduction
```

**Key issues to check:**
- Subject-verb agreement
- Article usage (a/an/the) — common for non-native authors
- Passive voice overuse (acceptable in methods, problematic elsewhere)
- Dangling modifiers
- Run-on sentences (> 40 words)
- Missing Oxford comma in academic lists

**Output format:** `% GRAMMAR (Line N) [WARNING]: Dangling modifier — "Using our method, the results show..."`

**Preserve:** LaTeX commands, math environments, `\cite{}`, `\ref{}`

---

## Logic Module

**When:** Weak argument flow, unclear transitions, introduction funnel problems, abstract/conclusion misalignment.

**Script:**
```bash
python analyze_logic.py main.tex --section methods
```

**Key checks:**
- Introduction funnel: broad context → specific gap → proposed approach → contributions
- Abstract matches introduction and conclusion (no new claims)
- Each paragraph has one main claim supported by evidence
- Transitions between sections are explicit
- Claims in contributions list are all demonstrated in experiments
- Related work positions the paper without over-selling

**Output format:** `% LOGIC (Section: Introduction, Para 3) [WARNING]: Transition missing between gap statement and proposed approach`

---

## Expression Module

**When:** Academic tone polish, improving clarity without changing scientific claims.

**Script:**
```bash
python improve_expression.py main.tex --section related
```

**Guidelines:**
- Prefer precise verbs: "demonstrates" over "shows", "proposes" over "presents"
- Avoid hedging chains: "may potentially suggest" → "suggests"
- Avoid filler phrases: "it is worth noting that", "as can be seen"
- Vary sentence structure to avoid monotony
- Avoid starting consecutive sentences with the same word

**Preserve:** All scientific claims, citations, math, experimental results

---

## Figures Module

**When:** Missing figures, wrong file extensions, low DPI, caption issues.

**Script:**
```bash
python check_figures.py main.tex
```

**Checks:**
- All `\includegraphics{path}` files exist on disk
- Preferred formats: PDF or EPS for vector graphics; PNG/JPG for raster (min 300 DPI)
- Every figure has a `\caption{}` and `\label{fig:...}`
- Every `\label{fig:X}` is referenced in text with `\ref{fig:X}` or `\cref{fig:X}`
- Captions are self-contained (reader should understand without body text)
- Subfigures labeled (a), (b), etc. when used
- Figure placement: `[htbp]` preferred; `[H]` only when necessary

**Output format:** `% FIGURES (Line N) [ERROR]: File 'figures/result.png' not found`

---

## Pseudocode Module

**When:** IEEE-safe pseudocode review, algorithm2e cleanup, caption/label/reference checks.

**Script:**
```bash
python check_pseudocode.py main.tex --venue ieee
```

**IEEE-safe pseudocode checklist:**
- Use `algorithmicx` + `algpseudocode` (preferred) or `algorithm2e`
- Algorithm block wrapped in `algorithm` float (not bare `algorithmic`)
- Every algorithm has `\caption{}` and `\label{alg:...}`
- Caption position: above the algorithm (IEEE convention)
- Referenced in text: "Algorithm \ref{alg:main}"
- Comment length: ≤ 40 characters per line
- `\Require` / `\Ensure` for preconditions / postconditions
- No font-size commands inside algorithm blocks
- Consistent use of `\gets` for assignment (not `:=` or `=`)

**Migration from algorithm2e to algorithmicx:**
```latex
% algorithm2e (old)
\begin{algorithm2e}
\KwIn{...}
\end{algorithm2e}

% algorithmicx (preferred)
\usepackage{algorithm}
\usepackage{algpseudocode}
\begin{algorithm}
\caption{My Algorithm}
\label{alg:myalg}
\begin{algorithmic}[1]
  \Require{input}
  \Ensure{output}
  \State $x \gets 0$
\end{algorithmic}
\end{algorithm}
```

---

## Experiment Module

**When:** Experiment design quality, discussion depth, conclusion completeness.

**Script:**
```bash
python analyze_experiment.py main.tex --section experiments
```

**Checks:**
- Baseline comparisons are fair (same data splits, same hyperparameter budget)
- Ablation study covers key design choices
- Statistical significance reported (p-values or confidence intervals)
- Error bars present in graphs
- Hyperparameters reported (enables reproducibility)
- No overclaiming: "our method achieves state-of-the-art" requires SOTA baseline comparison
- Discussion section explains WHY results happen, not just WHAT they are
- Limitations section present (required by most top venues)
- Conclusion matches abstract claims

**Output format:** `% EXPERIMENT (Section: Results, Para 2) [WARNING]: No error bars reported for Table 2 results`

---

## DeAI Module

**When:** Reducing AI-writing traces while preserving LaTeX syntax.

**Script:**
```bash
python deai_check.py main.tex --section introduction
```

**AI-writing patterns to flag:**
- Overuse of "delve", "intricate", "multifaceted", "crucial", "pivotal", "leverage"
- Verbose academic filler: "it is important to note that", "in the realm of"
- Excessive hedging and qualifiers stacked together
- Perfect parallelism in every sentence (unnaturally consistent)
- Transition phrases: "Furthermore,", "Moreover,", "In addition," at every paragraph

**Preserve:** LaTeX environments, math, citations, technical terminology
**Do not:** Paraphrase scientific claims or change experimental descriptions
