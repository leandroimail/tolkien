# Figure Data Sidecar Convention

## The problem

Figures are shipped as images (`.png`, `.eps`, `.pdf`, `.svg`). The numbers drawn
inside a figure are **not machine-readable**, so a script cannot verify that "the
text says 92% but the bar chart shows 89%". OCR of figure images is brittle and out
of scope.

## The convention

Whenever a figure carries quantitative content, store the underlying data next to
the image using the **same stem**:

```
figures/
├── chart_01_latency.png        ← the rendered figure
├── chart_01_latency.csv        ← OR the data behind it
├── chart_01_latency.json       ← OR structured data
└── chart_01_latency.py         ← OR the generating script (academic-media output)
```

Accepted sidecars (in priority order): `<stem>.csv`, `<stem>.json`, `<stem>.py`.

## How the validator uses it

- **Sidecar present** → the agentic pass cross-checks figure-referencing numeric
  claims in the prose against the sidecar values.
- **Sidecar absent** → `data_congruence_gate.py` emits a `figure_manual_verify`
  WARNING listing the figures that cannot be auto-verified. This is **never** a
  silent pass — a human must verify those figures by eye.

## Cross-skill dependency (recommended)

`academic-media` generates figures from `scripts/*.py`. It is recommended that it
also write a `<stem>.csv`/`.json` next to each `savefig(...)` by default, so every
figure becomes verifiable. This is a change in the `academic-media` skill, tracked
separately — this convention documents the contract the data-validator expects.
