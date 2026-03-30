# Template Migration Guide

How to migrate an existing paper from one conference template to another.

## Table of Contents
1. [Migration Checklist](#migration-checklist)
2. [Documentclass Swap Patterns](#documentclass-swap-patterns)
3. [Author Block Conversion](#author-block-conversion)
4. [Abstract Position](#abstract-position)
5. [Venue-Specific Sections](#venue-specific-sections)
6. [Bibliography Style Swap](#bibliography-style-swap)
7. [Common Migration Paths](#common-migration-paths)

---

## Migration Checklist

Before migrating, record the source template's settings, then apply target settings.

```
Source analysis:
□ \documentclass[...]{...} — record class and options
□ Author block format — how \author is structured
□ Abstract position (preamble vs. body)
□ Bibliography style (\bibliographystyle)
□ Venue-specific packages loaded
□ Venue-specific environments (CCSXML, keywords, etc.)

Migration steps:
□ Swap \documentclass for target class
□ Replace venue-specific packages
□ Reformat author block for target venue
□ Move abstract if needed
□ Add/remove venue-specific elements (CCS concepts, etc.)
□ Swap bibliography style
□ Configure anonymous mode for submission
□ Run Gate 1–4 self-review
```

---

## Documentclass Swap Patterns

| Source → Target | Change |
|---|---|
| Any → ACM sigconf | `\documentclass[sigconf]{acmart}` |
| Any → NeurIPS | Add `\usepackage{neurips_2025}` to article class |
| Any → ICML | Add `\usepackage{icml2025}` to article class |
| Any → IEEE | `\documentclass[conference]{IEEEtran}` |
| Any → Springer LNCS | `\documentclass{llncs}` |
| Any → AAAI | `\documentclass[letterpaper]{article}` + `\usepackage{aaai25}` |

For full class options per venue, see [venues.md](venues.md).

---

## Author Block Conversion

### Generic article → ACM acmart

```latex
% Before (generic)
\author{John Doe \\ University A \\ john@univ.edu}

% After (acmart)
\author{John Doe}
\affiliation{%
  \institution{University A}
  \city{City}
  \country{Country}
}
\email{john@univ.edu}
```

### Generic article → IEEE IEEEtran

```latex
% Before (generic)
\author{John Doe, Jane Smith}

% After (IEEEtran)
\author{
\IEEEauthorblockN{John Doe}
\IEEEauthorblockA{Department\\University A\\City, Country\\john@univ.edu}
\and
\IEEEauthorblockN{Jane Smith}
\IEEEauthorblockA{Department\\University B\\City, Country\\jane@univ.edu}
}
```

### Generic article → Springer LNCS

```latex
% After (llncs)
\author{John Doe\inst{1} \and Jane Smith\inst{2}}
\institute{
  University A, City, Country \email{john@univ.edu}
  \and
  University B, City, Country \email{jane@univ.edu}
}
```

---

## Abstract Position

| Venue | Abstract Position |
|---|---|
| ACM (acmart) | Before `\begin{document}` (in preamble) |
| NeurIPS, ICML, ICLR | After `\maketitle` inside `\begin{document}` |
| IEEE IEEEtran | After `\maketitle` inside `\begin{document}` |
| Springer LNCS | Before `\maketitle` inside `\begin{document}` |
| AAAI | After `\maketitle` inside `\begin{document}` |
| Generic article | After `\maketitle` inside `\begin{document}` |

**ACM preamble abstract pattern:**
```latex
\begin{abstract}
Abstract text here.
\end{abstract}
\begin{document}
\maketitle
% Abstract auto-renders here
```

---

## Venue-Specific Sections

### ACM — CCS Concepts and Keywords

Required for ACM venues. Add to preamble before `\begin{document}`:

```latex
\begin{CCSXML}
<ccs2012>
  <concept>
    <concept_id>10010405.10010444.10010447</concept_id>
    <concept_desc>Applied computing~Document management and text processing</concept_desc>
    <concept_significance>500</concept_significance>
  </concept>
</ccs2012>
\end{CCSXML}
\ccsdesc[500]{Applied computing~Document management and text processing}
\keywords{machine learning, deep learning, natural language processing}
```

Find CCS concept IDs at: https://dl.acm.org/ccs

### NeurIPS — Paper Checklist

Required appendix since NeurIPS 2022. Add after main content:

```latex
\section*{NeurIPS Paper Checklist}
\begin{enumerate}
  \item \textbf{Claims} ... \answerYes{} / \answerNo{} / \answerNA{}
  ...
\end{enumerate}
```

### Springer LNCS — Running Head

```latex
\titlerunning{Short title for running head}
\authorrunning{Doe et al.}
```

---

## Bibliography Style Swap

| Target Venue | Style Command |
|---|---|
| ACM | `\bibliographystyle{ACM-Reference-Format}` |
| IEEE | `\bibliographystyle{IEEEtran}` |
| NeurIPS | `\bibliographystyle{plainnat}` + `\usepackage{natbib}` |
| ICML | `\bibliographystyle{icml2025}` |
| ICLR | `\bibliographystyle{iclr2025_conference}` |
| AAAI | `\bibliographystyle{aaai25}` |
| Springer LNCS | `\bibliographystyle{splncs04}` |
| CVPR | `\bibliographystyle{ieee_fullname}` |

When switching from `natbib` to `biblatex` or vice versa:
- `\cite{}` → works in both
- `\citet{}`, `\citep{}` → natbib only; use `\textcite{}`, `\parencite{}` in biblatex

---

## Common Migration Paths

### arXiv preprint → NeurIPS submission

1. Replace preamble with `\usepackage{neurips_2025}` (default = anonymous)
2. Reformat to 1-column if using 2-column preprint
3. Check 9-page limit (references don't count)
4. Add NeurIPS paper checklist appendix
5. Remove author info for blind review

### NeurIPS → ICML

1. Replace `\usepackage{neurips_2025}` with `\usepackage{icml2025}`
2. Switch to 2-column layout (ICML uses 2-column)
3. Reformat author block: `\icmlauthor{}{}` + `\icmlaffiliation{}{}`
4. Replace `\bibliographystyle{plainnat}` with `\bibliographystyle{icml2025}`
5. Adjust page limit: 9 pages + references (same as NeurIPS)

### ACM → IEEE

1. Replace `\documentclass[sigconf]{acmart}` with `\documentclass[conference]{IEEEtran}`
2. Remove ACM-specific packages (`\usepackage{acmart}` bundle)
3. Reformat `\author` block to `\IEEEauthorblockN` / `\IEEEauthorblockA`
4. Remove CCS concepts and ACM keywords
5. Replace `\bibliographystyle{ACM-Reference-Format}` with `\bibliographystyle{IEEEtran}`
6. Remove `\settopmatter{}`, `\setcopyright{}`, `\acmConference{}` etc.
7. Add `\IEEEpeerreviewmaketitle` after `\maketitle` for blind review
