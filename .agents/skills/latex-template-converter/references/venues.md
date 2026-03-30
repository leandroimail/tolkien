# Venue Template Specifications

## Table of Contents
1. [ACM Conferences (acmart)](#acm-conferences-acmart)
2. [IEEE (IEEEtran)](#ieee-ieeetran)
3. [NeurIPS](#neurips)
4. [ICML](#icml)
5. [ICLR](#iclr)
6. [AAAI](#aaai)
7. [CVPR / ICCV / ECCV](#cvpr--iccv--eccv)
8. [Springer LNCS](#springer-lncs)
9. [Common Anonymous Submission Patterns](#common-anonymous-submission-patterns)

---

## ACM Conferences (acmart)

Covers: KDD, SIGMOD, VLDB, CHI, WWW, SIGCOMM, CCS, SOSP, and others using `acmart`.

```latex
% Submission (anonymous)
\documentclass[sigconf,anonymous,review,nonacm]{acmart}
\settopmatter{printacmref=false}
\setcopyright{none}
\acmConference[]{}{}{}
\acmYear{}
\acmISBN{}
\acmDOI{}

% Camera-ready
\documentclass[sigconf]{acmart}
\settopmatter{printacmref=true}
\setcopyright{acmcopyright}
\acmConference[CONF '26]{Full Conference Name}{Month DD--DD, Year}{City, Country}
\acmYear{2026}
\acmISBN{978-1-4503-XXXX-X/26/08}
\acmDOI{10.1145/nnnnnnn.nnnnnnn}
```

**Required venue-specific elements:**
```latex
\begin{CCSXML}
<ccs2012>
  <concept>
    <concept_id>10010405.10010444.10010447</concept_id>
    <concept_desc>Applied computing~...</concept_desc>
    <concept_significance>500</concept_significance>
  </concept>
</ccs2012>
\end{CCSXML}
\ccsdesc[500]{Applied computing~...}
\keywords{keyword1, keyword2, keyword3}
```

**Format:** 2-column, 9pt, typically 10–12 pages + references
**Bibliography:** `\bibliographystyle{ACM-Reference-Format}`
**Abstract:** Before `\maketitle`, inside `\begin{abstract}...\end{abstract}`

**KDD-specific note:** `nonacm` option is required for anonymous submission to suppress
ACM footnotes with doi/isbn. Restore all `\acmConference`, `\acmISBN`, `\acmDOI` for camera-ready.

---

## IEEE (IEEEtran)

```latex
\documentclass[conference]{IEEEtran}
% For journal:
\documentclass[journal]{IEEEtran}
```

**Author block format:**
```latex
\author{
\IEEEauthorblockN{First Author}
\IEEEauthorblockA{Department\\University\\City, Country\\email@example.com}
\and
\IEEEauthorblockN{Second Author}
\IEEEauthorblockA{...}
}
```

**Format:** 2-column, 10pt, varies by conference/journal
**Bibliography:** `\bibliographystyle{IEEEtran}`
**Keywords:** `\begin{IEEEkeywords}...\end{IEEEkeywords}`
**Peer review:** Add `\IEEEpeerreviewmaketitle` after `\maketitle` for double-blind

---

## NeurIPS

```latex
% Final submission
\usepackage[final]{neurips_2025}

% Preprint (e.g., arXiv) — shows author info
\usepackage[preprint]{neurips_2025}

% Anonymous review
\usepackage{neurips_2025}  % default is anonymous
```

**Format:** 1-column, 10pt, 9 pages + references (unlimited)
**Bibliography:** `\bibliographystyle{plainnat}` + `\usepackage{natbib}`
**Abstract:** Standard position after `\maketitle`
**Checklist:** NeurIPS requires a paper checklist appendix (since 2022)

---

## ICML

```latex
% Anonymous submission
\usepackage{icml2025}

% Camera-ready (accepted)
\usepackage[accepted]{icml2025}
```

**Format:** 2-column, 10pt, 9 pages + references
**Bibliography:** `\bibliographystyle{icml2025}`
**Author line:** Use `\icmlauthor{}{}` and `\icmlaffiliation{}{}`

---

## ICLR

```latex
\documentclass{article}
\usepackage{iclr2025_conference,times}

% Camera-ready: no extra option needed (author info auto-enabled when accepted)
```

**Format:** 1-column, 10pt, 10 pages + references
**Bibliography:** `\bibliographystyle{iclr2025_conference}`
**Anonymous:** Default behavior (submission is always anonymous until accepted)

---

## AAAI

```latex
\documentclass[letterpaper]{article}
\usepackage{aaai25}
\usepackage{times}
\usepackage{helvet}
\usepackage{courier}
\usepackage[hyphens]{url}
\usepackage{graphicx}
\setcounter{secnumdepth}{0}  % No section numbering in AAAI
```

**Format:** 2-column, 10pt, strict 8 pages + references
**Bibliography:** `\bibliographystyle{aaai25}`
**No section numbers** (per AAAI style)

---

## CVPR / ICCV / ECCV

```latex
% CVPR 2025
\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage{cvpr}
\usepackage{times}
\usepackage{epsfig}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}

% For anonymous review:
\cvprfinalcopy  % Comment this out for submission; uncomment for camera-ready
```

**Format:** 2-column, 10pt, 8 pages + references
**Bibliography:** `\bibliographystyle{ieee_fullname}` or `\bibliographystyle{cvpr}`

---

## Springer LNCS

```latex
\documentclass{llncs}
\usepackage{graphicx}
```

**Author format:**
```latex
\author{First Author\inst{1} \and Second Author\inst{2}}
\institute{University A, City, Country \and University B, City, Country}
```

**Format:** 1-column, 10pt, varies (12–20 pages typical)
**Bibliography:** `\bibliographystyle{splncs04}`
**Abstract:** Before `\maketitle`, inside `\begin{abstract}...\end{abstract}`

---

## Common Anonymous Submission Patterns

| Venue | Anonymous Option | Footnote Removal |
|---|---|---|
| ACM (acmart) | `anonymous,review,nonacm` | `\settopmatter{printacmref=false}` + clear metadata |
| IEEE | Remove author block; add `\IEEEpeerreviewmaketitle` | Automatic |
| NeurIPS | Default (no `final` or `preprint` option) | Automatic |
| ICML | Default (no `accepted` option) | Automatic |
| ICLR | Default (always anonymous until accepted) | Automatic |
| AAAI | Remove `\author{}` content | Automatic |
| CVPR | Comment out `\cvprfinalcopy` | Automatic |

**Universal checklist for anonymous submissions:**
- Remove or comment out author names, affiliations, email addresses
- Remove or replace self-identifying acknowledgments ("This work supported by [Grant X]")
- Anonymize self-citations if required ("In our previous work [ANON]")
- Remove "Supplementary Material" links that reveal identity
