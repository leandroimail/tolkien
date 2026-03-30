# Progressive Disclosure Patterns

> How to structure Skills for efficient context window usage.
> Based on [Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
> and [Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

## Table of Contents

- [The Three Levels](#the-three-levels)
- [How It Works at Runtime](#how-it-works-at-runtime)
- [Pattern 1: High-Level Guide with References](#pattern-1-high-level-guide-with-references)
- [Pattern 2: Domain-Specific Organization](#pattern-2-domain-specific-organization)
- [Pattern 3: Conditional Details](#pattern-3-conditional-details)
- [Anti-Patterns](#anti-patterns)
- [Decision Matrix: What Goes Where](#decision-matrix-what-goes-where)
- [Reference File Guidelines](#reference-file-guidelines)

## The Three Levels

Progressive disclosure is the core design principle of Agent Skills:

```
Level 1: Metadata      →  ~100 tokens/Skill  →  Always loaded at startup
Level 2: Instructions  →  < 5,000 tokens      →  Loaded when Skill triggers
Level 3: Resources     →  Virtually unlimited  →  Loaded only as needed
```

### Level 1: Metadata (Always loaded)

Only the `name` and `description` fields from YAML frontmatter. This is why
the description must be carefully crafted — it's the only content always in
the context window.

### Level 2: Instructions (When triggered)

The full SKILL.md body. Loaded entirely when Claude decides the Skill is
relevant. **Must stay under 500 lines** to avoid context window spikes.

### Level 3: Resources (On demand)

Files in `scripts/`, `references/`, `assets/`. Claude reads these only when
it determines they're needed for the current task. Scripts are **executed**
(not loaded into context), making them token-free.

## How It Works at Runtime

1. **Startup**: Context window has the system prompt + metadata for all installed Skills + user message.
2. **Trigger**: Claude reads the full SKILL.md for the relevant Skill.
3. **Navigate**: Claude reads specific reference files as needed.
4. **Execute**: Claude may run scripts without loading them into context.
5. **Complete**: Claude performs the task with the loaded context.

Key insight: **Agents with filesystem access don't need to read everything.** The amount of bundled content is effectively unbounded.

## Pattern 1: High-Level Guide with References

Best for: Skills with multiple distinct features.

### Structure

```
pdf-processing/
├── SKILL.md              # Overview + quick start
├── FORMS.md              # Form-filling guide
├── REFERENCE.md          # API reference
└── EXAMPLES.md           # Usage examples
```

### SKILL.md

````markdown
---
name: pdf-processing
description: >
  Extracts text and tables from PDF files, fills forms, and merges
  documents. Use when working with PDF files or when the user mentions
  PDFs, forms, or document extraction.
---

# PDF Processing

## Quick Start

Extract text with pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced Features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
````

Claude loads `FORMS.md`, `REFERENCE.md`, or `EXAMPLES.md` only when needed.

## Pattern 2: Domain-Specific Organization

Best for: Skills with multiple non-overlapping domains.

### Structure

```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md      # Revenue, billing metrics
    ├── sales.md        # Opportunities, pipeline
    ├── product.md      # API usage, features
    └── marketing.md    # Campaigns, attribution
```

### SKILL.md

````markdown
# BigQuery Data Analysis

## Available Datasets

Read the relevant reference for your task to build queries.

- **Finance**: Revenue, ARR, billing → See [references/finance.md](references/finance.md)
- **Sales**: Opportunities, pipeline → See [references/sales.md](references/sales.md)
- **Product**: API usage, features → See [references/product.md](references/product.md)
- **Marketing**: Campaigns, attribution → See [references/marketing.md](references/marketing.md)

## Quick Search

Find specific metrics using grep:

```bash
grep -i "revenue" references/finance.md
grep -i "pipeline" references/sales.md
```
````

When the user asks about sales, Claude reads only `references/sales.md`.

## Pattern 3: Conditional Details

Best for: Skills where most tasks are simple but some require advanced knowledge.

### Structure

```
docx-processing/
├── SKILL.md              # Basic operations
├── REDLINING.md          # Track changes (advanced)
└── OOXML.md              # XML structure (advanced)
```

### SKILL.md

```markdown
# DOCX Processing

## Creating Documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing Documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads `REDLINING.md` or `OOXML.md` only when the user needs those features.

## Anti-Patterns

### ❌ Monolithic SKILL.md

```
my-skill/
└── SKILL.md    # 800+ lines with everything
```

**Problem:** Context window spike when triggered. Irrelevant content loaded for every task.
**Fix:** Split into references.

### ❌ Deeply Nested References

```markdown
# SKILL.md → see advanced.md
# advanced.md → see details.md
# details.md → actual information here...
```

**Problem:** Claude may partially read files, using `head -100` instead of reading complete nested files. Information gets lost.
**Fix:** Keep all references one level deep from SKILL.md.

### ❌ Loading Everything at L2

```yaml
---
name: my-skill
description: >
  Very long description that tries to include all instructions,
  examples, edge cases, and reference material directly in the
  description field to avoid needing additional files...
---
```

**Problem:** Wastes the ~100 token budget per Skill that applies to ALL installed Skills.
**Fix:** Keep description focused on triggers and summary. Details go in the body.

### ❌ Referencing Scripts as Documentation

```markdown
## Understanding the Process

Read `scripts/process.py` to understand how processing works.
```

**Problem:** Loading script source into context is expensive and usually unnecessary.
**Fix:** Describe the process in SKILL.md. Tell Claude to **execute** scripts, not read them.

## Decision Matrix: What Goes Where

| Content Type | Where | Why |
|---|---|---|
| Trigger keywords and summary | `description` field | Always loaded, enables discovery |
| Core workflow and quick start | SKILL.md body | Loaded when triggered |
| Domain-specific schemas | `references/*.md` | Loaded only for relevant domain |
| Detailed API reference | `references/API.md` | Loaded only when needed |
| Deterministic operations | `scripts/*.py` | Executed, not loaded (token-free) |
| Templates and schemas | `assets/` | Loaded only when needed |
| Rarely-used advanced features | Separate `.md` file | Loaded only for specific tasks |

## Reference File Guidelines

### Use Descriptive Filenames

```
# Good
references/form_validation_rules.md
references/api_authentication.md
references/bigquery_schemas.md

# Bad
references/doc1.md
references/file2.md
references/notes.md
```

### Add Table of Contents for Files Over 100 Lines

```markdown
# API Reference

## Table of Contents
- Authentication and Setup
- Core Methods (Create, Read, Update, Delete)
- Advanced Features (Batch Operations, Webhooks)
- Error Handling Patterns
- Code Examples

## Authentication and Setup
...
```

### Make Content Grep-Searchable

Include grep hints in SKILL.md for large reference sets:

```markdown
## Quick Search

Use grep to find specific metrics:

```bash
grep -i "revenue" references/finance.md
grep -i "pipeline" references/sales.md
grep -i "api usage" references/product.md
```

```

## Sources

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://agentskills.io/specification
