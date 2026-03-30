---
name: academic-media
description: >
  Creation of figures, schematics, diagrams, and exploratory data analysis
  for academic papers. Generates publication-quality visual elements.
  Trigger: /academic-media, "create figure", "generate schematic", "generate diagram",
  "exploratory analysis", "EDA", "create figure", "generate schematic".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "1.0"
  depends_on: ""
---

# Academic Media

Creation of publication-quality visual elements for academic papers: results figures, conceptual diagrams, methodological flowcharts, and exploratory data analysis. Consolidates scientific-eda, scientific-paper-figure-generator, and scientific-schematics.

## When To Use

- Generating results figures (bar charts, line plots, scatterplots, heatmaps)
- Creating conceptual diagrams and workflows (Transformer, CONSORT, PRISMA)
- Producing circuit diagrams, biological pathways, system architectures
- Performing exploratory data analysis (EDA) with visualizations
- When `academic-writer` issues a call: `→ academic-media: {description}`

## When Not To Use

- To draft text → use `academic-writer`
- To format LaTeX → use the `latex` skill
- To compile PDF → use the `pdf` skill

## Prerequisites

1. Clear description of the necessary visual element
2. Raw data (for results figures and EDA)
3. `prd.md` — for visual style and paper template (optional)

## Modes

| Mode | Trigger | Output |
|------|---------|--------|
| `figure` | "create results chart" | Data figures (matplotlib/ggplot2) |
| `schematic` | "generate diagram" | Conceptual diagrams (graphviz/tikz) |
| `eda` | "exploratory analysis" | EDA visualizations + journal |

## Method

### Mode: Figure (Publication-Quality Data Figures)

1. **Identify chart type** based on the data:
   - Bar graphs: compare discrete categories
   - Line graphs: trends over time
   - Scatterplots: correlations
   - Box plots: distributions and outliers
   - Heatmaps: visualize matrices

2. **Generate with publication standards**:
   - Resolution ≥ 300 DPI
   - Preferred vector format (PDF, SVG, EPS)
   - Colorblind-safe palettes (Okabe-Ito)
   - Sans-serif fonts (Arial, Helvetica)
   - Minimum 7-8pt text at final print size

3. **APA 7.0 figure formatting** (when applicable):
   - Title above the figure
   - Note below with statistics
   - Labels on all axes with units

```python
# Base template for figures
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
# ... plot code ...
plt.savefig('output/figures/figure_name.pdf', dpi=300, bbox_inches='tight')
plt.savefig('output/figures/figure_name.svg', bbox_inches='tight')
```

### Mode: Schematic (Diagrams and Workflows)

**Library selection by diagram type:**

| Diagram Type | Best Library | Alternative |
|-------------|-------------|-------------|
| Neural networks | graphviz (pygraphviz) | matplotlib custom |
| Flowcharts (CONSORT/PRISMA) | graphviz (dot) | TikZ |
| Circuit diagrams | schemdraw | — |
| Biological pathways | networkx + matplotlib | graphviz |
| System architecture | graphviz | diagrams |

**Output always in vector format:**
```python
import graphviz

dot = graphviz.Digraph('diagram_name', format='pdf')
# ... diagram code ...
dot.render('output/figures/diagram_name', cleanup=True)
```

### Mode: EDA (Exploratory Data Analysis)

Follows a **defensive, human-guided** process:

1. **Context first** — capture the question/domain BEFORE touching the data
2. **One step at a time** — propose one plot/summary, execute, suggest next step
3. **Ask why** — when the user asks for a specific plot, ask which decision it supports
4. **Session journal** — append-only `analysis/journal.md`

Scripts with PEP723 + `uv run`:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "matplotlib"]
# ///
import pandas as pd
# ... EDA code ...
```

WebP plots for reduced size:
```python
fig.savefig("plots/overview.webp", format="webp")
```

## Colorblind-Safe Palettes

```python
OKABE_ITO = {
    'orange': '#E69F00', 'sky_blue': '#56B4E9',
    'green': '#009E73',  'yellow': '#F0E442',
    'blue': '#0072B2',   'vermillion': '#D55E00',
    'purple': '#CC79A7', 'black': '#000000'
}
```

## LaTeX Integration

Generated figures must be referencable:
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.9\textwidth]{figures/figure_name.pdf}
  \caption{Description of the figure.}
  \label{fig:figure_name}
\end{figure}
```

## Self-Review

### Deterministic
- [ ] Figures have caption, label, and text reference (`\ref{fig:X}`)
- [ ] Resolution ≥ 300 DPI (for raster) or vector format (PDF/SVG/EPS)
- [ ] Colorblind-safe palette used
- [ ] Legible text (≥ 7pt at final print size)

### Agentic
- Adherence to visual style of the template specified in the PRD
- Clarity: is the figure self-explanatory with a caption?
- Completeness: are key paper data represented visually?

## Output

Files in `output/figures/`:
- `*.pdf` — for LaTeX
- `*.svg` — for slides/web
- `*.eps` — for legacy journals
- `scripts/*.py` — generation code (reproducibility)

## References

- `references/publication-standards.md` — standards by journal
- `references/chart-decision-tree.md` — which chart type to use
- `references/colorblind-palettes.md` — accessible palettes
