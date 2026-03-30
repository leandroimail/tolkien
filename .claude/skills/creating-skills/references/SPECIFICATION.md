# Agent Skills Specification Reference

> Local reference extracted from the official [Agent Skills Specification](https://agentskills.io/specification).
> Last updated: 2026-02-28.

## Table of Contents

- [Directory Structure](#directory-structure)
- [SKILL.md Format](#skillmd-format)
- [Frontmatter Fields](#frontmatter-fields)
- [Body Content](#body-content)
- [Optional Directories](#optional-directories)
- [Progressive Disclosure](#progressive-disclosure)
- [File References](#file-references)
- [Validation](#validation)

## Directory Structure

A skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md          # Required
```

Full structure with optional directories:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable scripts
├── references/       # Optional: reference documents
└── assets/           # Optional: templates, images, data files
```

## SKILL.md Format

The `SKILL.md` file must contain YAML frontmatter followed by Markdown content.

### Basic frontmatter

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### Full frontmatter with optional fields

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
compatibility: Requires pdfplumber, python3. No network access needed.
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

## Frontmatter Fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | **Yes** | Max 64 chars. Lowercase letters, numbers, hyphens only. Must not start/end with hyphen. No consecutive hyphens. **Must match parent directory name.** |
| `description` | **Yes** | Max 1024 chars. Non-empty. Must describe what the skill does AND when to use it. |
| `license` | No | License name or reference to bundled LICENSE file. |
| `compatibility` | No | Max 500 chars. Environment requirements (product, packages, network). |
| `metadata` | No | Arbitrary key-value map (string → string). |
| `allowed-tools` | No | Space-delimited list of pre-approved tools. **Experimental.** |

### `name` field rules

- Must be 1-64 characters.
- May only contain lowercase alphanumeric characters and hyphens (`a-z`, `0-9`, `-`).
- Must not start or end with `-`.
- Must not contain consecutive hyphens (`--`).
- **Must match the parent directory name.**

**Valid examples:**

```yaml
name: pdf-processing
name: analyzing-data
name: git-commit-helper
name: my-custom-skill
```

**Invalid examples:**

```yaml
name: PDF-Processing      # uppercase not allowed
name: -pdf                 # cannot start with hyphen
name: pdf--processing      # consecutive hyphens not allowed
name: my_skill             # underscores not allowed
```

### `description` field rules

- Must be 1-1024 characters.
- Should describe both **what the skill does** and **when to use it**.
- Should include specific keywords that help agents identify relevant tasks.
- **Must be written in third person.**

**Good example:**

```yaml
description: >
  Extracts text and tables from PDF files, fills PDF forms, and merges
  multiple PDFs. Use when working with PDF documents or when the user
  mentions PDFs, forms, or document extraction.
```

**Poor example:**

```yaml
description: Helps with PDFs.
```

### `compatibility` field examples

```yaml
# Product-specific
compatibility: Designed for Claude Code (or similar products)

# System requirements
compatibility: Requires git, docker, jq, and access to the internet

# Restricted environment
compatibility: No network access needed. Requires python3 with pdfplumber.
```

### `metadata` field examples

```yaml
metadata:
  author: example-org
  version: "1.0"
  category: document-processing
```

## Body Content

The Markdown body after the frontmatter contains the skill instructions.

**Recommended sections:**

- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases
- Quality checklists

**Important:** The agent loads this entire file once it decides to activate the skill. Keep it **under 500 lines** and split longer content into referenced files.

## Optional Directories

### `scripts/`

Contains executable code. Scripts should:

- Be self-contained or clearly document dependencies.
- Include helpful, specific error messages.
- Handle edge cases gracefully.
- Use proper exit codes.

Common languages: Python, Bash, JavaScript.

### `references/`

Contains additional documentation loaded on demand:

- Domain-specific guides.
- API references.
- Templates and structured data formats.

Keep individual files focused (one topic per file).

### `assets/`

Contains static resources:

- Templates (document, configuration).
- Images (diagrams, examples).
- Data files (lookup tables, schemas).

## Progressive Disclosure

Skills load in three stages:

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup for all skills.
2. **Instructions** (< 5,000 tokens recommended): Full SKILL.md body loaded when activated.
3. **Resources** (as needed): Files in `scripts/`, `references/`, `assets/` loaded on demand.

## File References

Use relative paths from the skill root:

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
```bash
python scripts/extract.py input.pdf
```

```

**Critical rule:** Keep file references **one level deep** from SKILL.md.
Do not create nested reference chains (SKILL.md → A.md → B.md).

## Validation

Use the `skills-ref` reference library:

```bash
skills-ref validate ./my-skill
```

Or validate manually against this checklist:

- [ ] `name` field follows all naming rules.
- [ ] `name` matches parent directory name.
- [ ] `description` is non-empty and under 1024 chars.
- [ ] SKILL.md contains valid YAML frontmatter.
- [ ] Body is under 500 lines.
- [ ] All file references use relative paths.
- [ ] No deeply nested reference chains.

## Source

- Official specification: <https://agentskills.io/specification>
- Anthropic documentation: <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>
