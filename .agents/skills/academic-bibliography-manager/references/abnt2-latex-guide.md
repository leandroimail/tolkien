# ABNT 2 LaTeX and Bibliography Guide

## Overview

When generating or managing bibliographies for Brazilian academic standards (ABNT 2 / ABNT), special LaTeX packages and formatting rules apply. The standard package to use in LaTeX is `abntex2cite` which is part of the `abntex2` suite.

## Bibliography Format in ABNT (BibTeX)

When generating the `.bib` file for an ABNT-formatted article, keep the following in mind:

1.  **Authors' Names in ALL CAPS:** ABNT style generally prints the authors' surnames in uppercase in the reference list (e.g., SILVA, J.). The `abntex2cite` package handles this conversion automatically if configured correctly, but it relies on proper BibTeX formatting: `author = {Surname, First Name}` or `author = {First Name Surname}`.

2.  **Subtitle Separation:** Titles and subtitles should be split by a colon (`:`). The title is usually bold, and the subtitle is not.

3.  **Specific Fields Supported by `abntex2cite`:**
    -   `subtitle`: Can be used to explicitly separate the subtitle.
    -   `url` and `urlaccessdate`: For electronic documents. Format `urlaccessdate = {10 mar. 2024}`.
    -   `pagename`: Used to specify the page abbreviation (e.g., `p.`).

## Setting up `abntex2` in LaTeX

To use the ABNT 2 bibliography style in LaTeX, the preamble must include the `abntex2cite` package:

```latex
% Preamble
\usepackage[alf]{abntex2cite} % 'alf' is for alphabetical style (AUTHOR, Year). 'num' is for numerical.
```

At the end of the document, the bibliography is generated simply via:

```latex
\bibliography{references} % Assuming references.bib
```
*(Note: `\bibliographystyle` is not needed when using `abntex2cite` as it forces its own style).*

## Citation Rules (In-Text)

In ABNT 2, in-text citations are handled mainly by two commands provided by `abntex2cite`:

1.  **Indirect Citation (End of sentence):** (AUTHOR, Year)
    -   Command: `\cite{key}`
    -   Example: `... as seen in recent studies \cite{silva2023}.` -> `... as seen in recent studies (SILVA, 2023).`

2.  **Direct Citation (Part of the text flow):** Author (Year)
    -   Command: `\citeonline{key}`
    -   Example: `Segundo \citeonline{silva2023}, o estudo...` -> `Segundo Silva (2023), o estudo...`

3.  **With Page Numbers:**
    -   Command: `\cite[p.~15]{key}` -> `(AUTHOR, 2023, p. 15)`
    -   Command: `\citeonline[p.~15]{key}` -> `Author (2023, p. 15)`

## Validation Checklist for ABNT

When validating a `.bib` file intended for ABNT format, the `academic-bibliography-manager` must ensure:
- [ ] Electronic sources have `url` and `urlaccessdate` fields.
- [ ] No `abntex2` incompatible fields break generation.
- [ ] Name formats in `author` are clean so the LaTeX compiler can correctly capitalize surnames.

When generating a LaTeX file, ensure the `abntex2cite` package is injected if ABNT style is specified in the PRD.
