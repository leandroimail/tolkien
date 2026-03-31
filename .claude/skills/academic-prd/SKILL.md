---
name: academic-prd
description: >
  Conducts a structured configuration interview to generate the Academic PRD (prd.md) for a scientific article.
  Use when starting a new academic paper, configuring an article project, or initiating the academic pipeline.
  Triggers: /academic-prd, "create academic PRD", "configure article", "start pipeline", "new paper"
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
metadata:
  version: "1.0"
  depends_on: ""
---

Note: Python scripts for this skill must be executed within the project's virtual environment.
Activate the environment with:

```bash
source .venv/bin/activate
```

Alternatively, use `uv run python -B ...` with the `.venv` active.

# Academic PRD

Generate the foundational requirements document (`prd.md`) for an academic article through a structured interview with the user. This is **Phase 0** of the academic pipeline — nothing proceeds without an approved PRD.

## When To Use

- User wants to start writing a new academic paper
- User invokes `/academic-prd` or says "start pipeline", "new paper", "configure article"
- No `prd.md` exists yet in the project directory
- User wants to reconfigure an existing paper's requirements

## When Not To Use

- A `prd.md` already exists and user wants to proceed to planning → use `academic-plan`
- User wants to write content directly → use `academic-writer`
- User is asking about an existing paper's status → use `academic-orchestrator`

## Prerequisites

- A root directory for the paper project (must be one of: `projects/`, `papers/`, `.projects/`, `.papers/`)
- A working directory for the paper project (will be created as `root/paper-{slug}/`)
- User availability for the interview (10 mandatory fields require input)

## Method

### 1. Initialize Project Directory

```bash
# Create project folder structure in one of the allowed roots
# roots: projects/, papers/, .projects/, .papers/
mkdir -p {root}/paper-{slug}/{research,draft,review,output}
```

Ask the user for:
1. The **root directory** where the project should be created (`projects/`, `papers/`, `.projects/`, or `.papers/`).
2. A short **slug** (e.g., "ml-healthcare-review") or derive one from the topic.

### 2. Conduct Configuration Interview

Collect the **10 mandatory fields** through conversational interview. Ask questions naturally — group related fields, adapt to context. Do NOT present a rigid form.

**10 Mandatory Fields:**

| # | Field | Key Question | Examples |
|---|-------|-------------|----------|
| 1 | `paper_type` | What type of paper? | research article, review, systematic review, meta-analysis, case study |
| 2 | `discipline` | What field/discipline? | medicine, engineering, psychology, computer science |
| 3 | `research_questions` | What are the research questions/objectives? | List of 1-5 specific questions |
| 4 | `citation_format` | Which citation style? | APA, MLA, Chicago, IEEE, Vancouver, ABNT |
| 5 | `output_format` | What output format(s)? | LaTeX, DOCX, PDF, Markdown |
| 6 | `template` | Any conference/journal template? | IEEE template, ACM acmart, NeurIPS, custom .cls |
| 7 | `support_documents` | Any guidelines, templates, reference papers? | Upload paths or URLs |
| 8 | `search_strategy` | Keywords, databases, inclusion/exclusion criteria? | Keywords list, date range, databases |
| 9 | `paper_structure` | What structure? | IMRaD, thematic, systematic review, case study |
| 10 | `languages` | Language(s) for the article + abstract? | English, Portuguese, bilingual abstract |

**Interview flow:**
1. Start with fields 1-2 (type + discipline) — these shape all subsequent questions
2. Ask field 3 (research questions) — the core of the paper
3. Fields 4-6 (format decisions) — may have dependencies (e.g., IEEE → LaTeX)
4. Fields 7-8 (supporting material + search strategy)
5. Fields 9-10 (structure + language)

Adapt the interview based on answers:
- If user provides a conference name → infer template, citation format, page limits
- If systematic review → ask about PRISMA compliance, registration
- If user uploads a template file → extract formatting constraints automatically

### 3. Validate Coherence

After collecting all fields, run coherence checks. See [interview-guide.md](references/interview-guide.md) for the full coherence matrix.

Key rules:
- IEEE citation format typically requires LaTeX output
- ABNT is compatible with both LaTeX and DOCX
- Systematic reviews require PRISMA-compatible structure
- If template file specified, output_format must match template type
- If bilingual abstract requested, both languages must be specified

Run validation script:
```bash
uv run python -B scripts/validate_prd.py paper-{slug}/prd.md
```

### 4. Generate prd.md

Write the `prd.md` file using the template in [assets/prd-template.md](assets/prd-template.md).

The document must include:
- YAML frontmatter with all 10 fields as structured data
- Prose summary of the paper's goals and constraints
- Decision log (why each choice was made)
- Derived constraints (page limits, word counts, section requirements from template)

### 5. Present Summary for Confirmation

Print a concise decision summary to the terminal:

```
━━━ Academic PRD Summary ━━━
Paper type:     Research Article
Discipline:     Computer Science
Questions:      3 research questions defined
Citation:       IEEE
Output:         LaTeX → PDF
Template:       IEEE Conference (ieeeconf.cls)
Structure:      IMRaD
Language:       English (abstract: EN + PT-BR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**CHECKPOINT: Ask the user to confirm or request changes before proceeding.**

### 6. Self-Review

Before delivering, verify:
- [ ] All 10 mandatory fields are filled (no empty or placeholder values)
- [ ] Coherence checks pass (script returns 0 errors)
- [ ] `prd.md` is parseable (YAML frontmatter is valid)
- [ ] Decision log captures rationale for key choices
- [ ] Derived constraints are realistic (e.g., page limits match template)

## Quality Checklist

- [ ] 10/10 mandatory fields populated with user-confirmed values
- [ ] Coherence validation passes (`validate_prd.py` returns 0 errors)
- [ ] `prd.md` written to `paper-{slug}/prd.md`
- [ ] Summary printed and user confirmed
- [ ] Project directory structure created

## Outputs

- `{root}/paper-{slug}/prd.md` — the Academic PRD document
- Terminal summary of all decisions for user confirmation

## Integration

This skill is **Phase 0** of the pipeline. After confirmation:
- Next step: `academic-plan` reads `prd.md` to generate `plan.md`
- The orchestrator (`academic-orchestrator`) invokes this skill first in both auto and interactive modes
