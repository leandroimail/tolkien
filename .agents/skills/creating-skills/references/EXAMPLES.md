# Complete Skill Examples

> Full examples of well-structured Agent Skills at different complexity levels.

## Table of Contents

- [Example 1: Simple Skill (Single File)](#example-1-simple-skill-single-file)
- [Example 2: Standard Skill (With References)](#example-2-standard-skill-with-references)
- [Example 3: Complex Skill (Full Structure)](#example-3-complex-skill-full-structure)
- [Example 4: Workflow Skill](#example-4-workflow-skill)
- [Example 5: Data Analysis Skill](#example-5-data-analysis-skill)
- [Common Patterns Cheat Sheet](#common-patterns-cheat-sheet)

## Example 1: Simple Skill (Single File)

### Structure

```
git-commit-helper/
└── SKILL.md
```

### SKILL.md

```markdown
---
name: git-commit-helper
description: >
  Analyzes git diffs and generates descriptive commit messages following
  conventional commit format. Use when the user asks for help creating
  commit messages, reviewing staged changes, or wants conventional commits.
---

# Git Commit Helper

## Commit Message Format

Follow the Conventional Commits specification:

```

<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

## Process

1. Run `git diff --staged` to see what's staged.
2. Analyze the changes: what was added, modified, deleted.
3. Determine the appropriate type and scope.
4. Write a concise subject line (max 50 chars, imperative mood).
5. Add body if changes need explanation.
6. Add footer for breaking changes or issue references.

## Rules

- Subject line: imperative mood ("add" not "added").
- No period at the end of subject line.
- Body: explain **why**, not what (the diff shows what).
- Breaking changes: start footer with `BREAKING CHANGE:`.

```

**Why this works:** Small, focused, under 100 lines. Claude knows git and
commit conventions — the Skill only adds project-specific format preferences.

---

## Example 2: Standard Skill (With References)

### Structure

```

api-documentation/
├── SKILL.md
└── references/
    ├── openapi-patterns.md
    ├── error-codes.md
    └── authentication.md

```

### SKILL.md

```markdown
---
name: api-documentation
description: >
  Generates and maintains API documentation from code annotations and
  OpenAPI specs. Use when the user asks to document an API, generate
  endpoint docs, or update API reference documentation.
---

# API Documentation

## Quick Start

Generate docs from an OpenAPI spec:

```bash
python scripts/generate_docs.py openapi.yaml --output docs/api/
```

## Documentation Standards

- All endpoints must have a description, parameters, and response schemas.
- Error responses must reference the standard error code table.
- Authentication requirements must be specified per endpoint.

## Reference Materials

- **OpenAPI patterns**: See [references/openapi-patterns.md](references/openapi-patterns.md)
- **Error codes**: See [references/error-codes.md](references/error-codes.md)
- **Authentication**: See [references/authentication.md](references/authentication.md)

## Quality Checklist

- [ ] All endpoints documented with description and examples.
- [ ] Request/response schemas include field descriptions.
- [ ] Error responses reference standard error codes.
- [ ] Authentication requirements specified.
- [ ] Examples use realistic data (not "foo", "bar").

```

**Why this works:** Core workflow in SKILL.md. Domain-specific reference
material in separate files loaded only when relevant.

---

## Example 3: Complex Skill (Full Structure)

### Structure

```

pdf-processing/
├── SKILL.md
├── scripts/
│   ├── analyze_form.py
│   ├── fill_form.py
│   └── validate.py
├── references/
│   ├── FORMS.md
│   ├── REFERENCE.md
│   └── EXAMPLES.md
└── assets/
    └── form_template.json

```

### SKILL.md

````markdown
---
name: pdf-processing
description: >
  Extracts text and tables from PDF files, fills forms, and merges
  documents. Use when working with PDF files or when the user mentions
  PDFs, forms, or document extraction.
compatibility: Requires python3 with pdfplumber installed.
metadata:
  author: document-team
  version: "2.0"
---

# PDF Processing

## Quick Start

Extract text with pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Form Analysis

To extract form fields from a PDF, run:

```bash
python scripts/analyze_form.py input.pdf
```

Output: JSON with field names, types, and page numbers.

## Form Filling

To fill a PDF form:

```bash
python scripts/fill_form.py input.pdf data.json output.pdf
```

**For complete form-filling guide**: See [references/FORMS.md](references/FORMS.md)

## Validation

After any PDF operation, validate the result:

```bash
python scripts/validate.py output.pdf
```

If validation fails, review the error message and fix before proceeding.

## Advanced Features

- **API reference**: See [references/REFERENCE.md](references/REFERENCE.md)
- **Code examples**: See [references/EXAMPLES.md](references/EXAMPLES.md)

## Editing Process

1. Perform the PDF operation.
2. **Validate immediately**: `python scripts/validate.py output.pdf`
3. If validation fails:
   - Review the error message.
   - Fix the issue.
   - Re-run validation.
4. **Proceed only when validation passes.**

````

**Why this works:** Progressive disclosure at all three levels. Scripts are
executed (not read into context). References load only when needed. Validation
feedback loop ensures quality.

---

## Example 4: Workflow Skill

### Structure

```
release-workflow/
├── SKILL.md
└── scripts/
    └── version_bump.py
```

### SKILL.md

```markdown
---
name: release-workflow
description: >
  Executes the release process: version bumping, CHANGELOG updates,
  tagging, and deployment. Use when the user requests a release,
  deployment, or version bump.
compatibility: Requires git, python3, and npm.
---

# Release Workflow

Copy this checklist to track progress:

- [ ] Step 1: Run and verify tests
- [ ] Step 2: Bump version
- [ ] Step 3: Update CHANGELOG
- [ ] Step 4: Commit and tag
- [ ] Step 5: Execute deployment
- [ ] Step 6: Verify operation

## Step 1: Run and Verify Tests

```bash
uv run pytest
python -m pytest tests/ -v
```

If any tests fail, **abort the release**. Do not proceed.

## Step 2: Bump Version

```bash
python scripts/version_bump.py --type <major|minor|patch>
```

Follow semantic versioning:
- **major**: Breaking changes.
- **minor**: New features, backwards compatible.
- **patch**: Bug fixes only.

## Step 3: Update CHANGELOG

Add entry under `## [version] - YYYY-MM-DD`:
- Group changes by: Added, Changed, Deprecated, Removed, Fixed, Security.
- Reference issue/PR numbers.

## Step 4: Commit and Tag

```bash
git add -A
git commit -m "chore(release): v<version>"
git tag -a v<version> -m "Release v<version>"
```

## Step 5: Execute Deployment

```bash
git push origin main --tags
npm publish  # if npm package
```

## Step 6: Verify Operation

- [ ] Package published successfully.
- [ ] CI/CD pipeline completed.
- [ ] Smoke tests pass in production.
```

**Why this works:** Checklist pattern ensures reliable step execution.
Abort conditions prevent partial releases. Each step is explicit with
exact commands.

---

## Example 5: Data Analysis Skill

### Structure

```
bigquery-analysis/
├── SKILL.md
└── references/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```

### SKILL.md

````markdown
---
name: bigquery-analysis
description: >
  Builds and executes BigQuery SQL queries for business analytics.
  Use when the user asks about revenue, sales pipeline, product metrics,
  marketing attribution, or needs data from BigQuery tables.
---

# BigQuery Data Analysis

## General Rules

- **Always** filter out test accounts: `WHERE account_type != 'test'`
- **Always** specify date ranges for time-series queries.
- Use `SAFE_DIVIDE` instead of `/` to handle division by zero.
- Partition by date when scanning large tables.

## Available Datasets

Read the relevant reference for your task:

- **Finance**: Revenue, ARR, billing → See [references/finance.md](references/finance.md)
- **Sales**: Opportunities, pipeline → See [references/sales.md](references/sales.md)
- **Product**: API usage, features → See [references/product.md](references/product.md)
- **Marketing**: Campaigns, attribution → See [references/marketing.md](references/marketing.md)

## Quick Search

```bash
grep -i "revenue" references/finance.md
grep -i "pipeline" references/sales.md
grep -i "api usage" references/product.md
```

## Output Format

Present results as:
1. The SQL query used.
2. A summary of findings.
3. A formatted table of key metrics.
4. Recommendations based on the data.
````

**Why this works:** Domain-specific references split by business area.
General rules in SKILL.md apply to all queries. Grep hints for quick
lookups across references.

---

## Common Patterns Cheat Sheet

### Frontmatter Template

```yaml
---
name: my-skill-name
description: >
  [Verb]s [object] for [domain]. Use when the user [trigger 1],
  [trigger 2], or works with [file type/technology].
---
```

### Reference Link Template

```markdown
**For [feature]**: See [descriptive-name.md](references/descriptive-name.md)
```

### Script Documentation Template

```markdown
## [Action Name]

Run the script:

```bash
python scripts/action.py <input> [options]
```

Output: [description of output format].

```

### Validation Loop Template

```markdown
## Process

1. Perform action.
2. **Validate**: `python scripts/validate.py output`
3. If validation fails:
   - Review error message.
   - Fix the issue.
   - Re-run validation.
4. **Proceed only when validation passes.**
```

### Checklist Template

```markdown
Copy this checklist to track progress:

- [ ] Step 1: Description
- [ ] Step 2: Description
- [ ] Step 3: Description
```

## Sources

- <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- <https://github.com/anthropics/skills>
- <https://github.com/anthropics/anthropic-cookbook/tree/main/skills>
