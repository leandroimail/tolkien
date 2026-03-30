# Tables Reference (tabularray)

## Why tabularray?

Modern LaTeX3 package replacing `tabular`, `tabularx`, `longtable`, `booktabs`.
Fixed-width columns, clean syntax, better performance. Included in TeX Live 2025.

```bash
# Check installation
kpsewhich tabularray.sty

# Install if missing
sudo tlmgr install tabularray
```

## Quick Reference

```latex
\usepackage{tabularray}

% Minimal table
\begin{tblr}{colspec={ccc}}
  A & B & C \\
\end{tblr}

% With all lines
\begin{tblr}{colspec={ccc}, hlines, vlines}
  Header 1 & Header 2 & Header 3 \\
  Data 1   & Data 2   & Data 3   \\
\end{tblr}

% Fixed widths
\begin{tblr}{colspec={Q[3cm] Q[4cm] Q[2cm]}, hlines}
  Column A & Column B & Column C \\
\end{tblr}

% Bold header row
\begin{tblr}{
  colspec={lll},
  row{1}={font=\bfseries},
  hlines
}
  Method & Metric 1 & Metric 2 \\
  Ours   & 89.4     & 0.97     \\
\end{tblr}

% Flexible width (fills textwidth)
\begin{tblr}{colspec={X[2] X[3] X[1]}, hlines}
  Narrow & Wide column & Short \\
\end{tblr}
```

## Column Specifiers

| Spec | Meaning |
|---|---|
| `c` | Centered, natural width |
| `l` | Left-aligned, natural width |
| `r` | Right-aligned, natural width |
| `Q[2cm]` | Fixed 2cm width, center-aligned |
| `Q[l,3cm]` | Fixed 3cm, left-aligned |
| `X` | Flexible, fills available space |
| `X[2]` | Flexible, twice the weight of X[1] |

## Best Practices

1. Use `Q[width]` for fixed-width columns instead of `p{width}`
2. Use `X` for flexible columns that should expand to fill space
3. Style headers with `row{1}={...}` instead of manual `\textbf{}`
4. Use `colspec=` for column properties, not inline commands
5. `hlines` + `vlines` for full grid; use selectively for booktabs-style

## Migration from Legacy Packages

| Legacy | tabularray Equivalent |
|---|---|
| `\begin{tabular}{lcr}` | `\begin{tblr}{colspec={lcr}}` |
| `p{3cm}` column | `Q[3cm]` column |
| `\hline` | `hlines` in spec or `\hline` in body |
| `\toprule`, `\midrule`, `\bottomrule` | `\toprule`, `\midrule`, `\bottomrule` (also work in tblr) |
| `\multicolumn{2}{c}{text}` | `\SetCell[c=2]{c} text` |
| `\multirow{2}{*}{text}` | `\SetCell[r=2]{} text` |

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| Package not found | tabularray not installed | `sudo tlmgr install tabularray` |
| Table too wide | Fixed widths exceed textwidth | Use smaller `Q[width]` or `X` |
| Text not wrapping | Column spec missing width | Use `Q[width]` instead of `c/l/r` |
| Alignment issues | Mixed column types | Ensure consistent spec |
| hlines not appearing | Missing from spec | Add `hlines` to spec |
| Row style not applied | Wrong row index | `row{1}` = first row (1-indexed) |
| Package version too old | TeX Live outdated | `sudo tlmgr update --self --all` |

For detailed patterns (colored rows, long tables, nested tables):
see `texdoc tabularray` or references/tables.md in the latex-document skill.
