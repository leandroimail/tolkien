---
name: academic-media
description: >
  Criação de figuras, esquemas, diagramas e análises exploratórias de dados
  para artigos acadêmicos. Gera elementos visuais publication-quality.
  Trigger: /academic-media, "criar figura", "gerar esquema", "gerar diagrama",
  "análise exploratória", "EDA", "create figure", "generate schematic".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "1.0"
  depends_on: ""
---

# Academic Media

Criação de elementos visuais publication-quality para artigos acadêmicos: figuras de resultados, diagramas conceituais, flowcharts metodológicos e análises exploratórias de dados. Consolida scientific-eda, scientific-paper-figure-generator e scientific-schematics.

## When To Use

- Gerar figuras de resultados (bar charts, line plots, scatterplots, heatmaps)
- Criar diagramas conceituais e workflows (Transformer, CONSORT, PRISMA)
- Produzir esquemas de circuitos, pathways biológicos, arquiteturas de sistema
- Realizar análise exploratória de dados (EDA) com visualizações
- Quando o academic-writer emite chamada: `→ academic-media: {descrição}`

## When Not To Use

- Para redigir texto → use `academic-writer`
- Para formatar LaTeX → use skill `latex`
- Para compilar PDF → use skill `pdf`

## Prerequisites

1. Descrição clara do elemento visual necessário
2. Dados brutos (para figuras de resultados e EDA)
3. `prd.md` — para estilo visual e template do paper (opcional)

## Modes

| Mode | Trigger | Output |
|------|---------|--------|
| `figure` | "criar gráfico de resultados" | Figuras de dados (matplotlib/ggplot2) |
| `schematic` | "gerar diagrama" | Diagramas conceituais (graphviz/tikz) |
| `eda` | "análise exploratória" | Visualizações de EDA + journal |

## Method

### Mode: Figure (Publication-Quality Data Figures)

1. **Identify chart type** baseado nos dados:
   - Bar graphs: comparar categorias discretas
   - Line graphs: tendências ao longo do tempo
   - Scatterplots: correlações
   - Box plots: distribuições e outliers
   - Heatmaps: visualizar matrizes

2. **Generate with publication standards**:
   - Resolução ≥ 300 DPI
   - Formato vetor preferido (PDF, SVG, EPS)
   - Colorblind-safe palettes (Okabe-Ito)
   - Fontes sans-serif (Arial, Helvetica)
   - Mínimo 7-8pt text at final print size

3. **APA 7.0 figure formatting** (quando aplicável):
   - Title acima da figura
   - Note abaixo com estatísticas
   - Labels em todos os eixos com unidades

```python
# Template base para figuras
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

Segue processo **defensive, human-guided**:

1. **Context first** — capturar pergunta/domínio ANTES de tocar nos dados
2. **One step at a time** — propor um plot/sumário, executar, sugerir próximo passo
3. **Ask why** — quando usuário pede plot específico, perguntar qual decisão apoia
4. **Session journal** — append-only `analysis/journal.md`

Scripts com PEP723 + `uv run`:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "matplotlib"]
# ///
import pandas as pd
# ... EDA code ...
```

Plots em WebP para tamanho reduzido:
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

Figuras geradas devem ser referenciáveis:
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.9\textwidth]{figures/figure_name.pdf}
  \caption{Description of the figure.}
  \label{fig:figure_name}
\end{figure}
```

## Self-Review

### Determinístico
- [ ] Figuras têm caption, label e referência no texto (`\ref{fig:X}`)
- [ ] Resolução ≥ 300 DPI (para raster) ou formato vetor (PDF/SVG/EPS)
- [ ] Paleta colorblind-safe utilizada
- [ ] Text legível (≥ 7pt no tamanho final de impressão)

### Agêntico
- Aderência ao estilo visual do template especificado no PRD
- Clareza: a figura é auto-explicativa com caption?
- Completude: dados-chave do paper estão representados visualmente?

## Output

Arquivos em `output/figures/`:
- `*.pdf` — para LaTeX
- `*.svg` — para slides/web
- `*.eps` — para journals legacy
- `scripts/*.py` — código de geração (reprodutibilidade)

## References

- `references/publication-standards.md` — standards por journal
- `references/chart-decision-tree.md` — qual tipo de gráfico usar
- `references/colorblind-palettes.md` — paletas acessíveis
