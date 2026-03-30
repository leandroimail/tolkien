# Best Practices for Creating Agent Skills

> Consolidated from [Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
> [Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills),
> [Skills Enterprise Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise),
> and [10 Practical Techniques for Mastering Agent Skills](https://shibuiyusuke.medium.com/10-practical-techniques-for-mastering-agent-skills-in-ai-coding-agents-6070e4038cf1).
> Last updated: 2026-02-28.

## Table of Contents

- [Conciseness Guidelines](#conciseness-guidelines)
- [Description Writing Guide](#description-writing-guide)
- [Naming Conventions](#naming-conventions)
- [Degrees of Freedom](#degrees-of-freedom)
- [Iterative Development](#iterative-development)
- [Observing Agent Behavior](#observing-agent-behavior)
- [Token Budget Management](#token-budget-management)
- [Team Collaboration](#team-collaboration)
- [Scope Selection](#scope-selection)
- [Workflow Skills](#workflow-skills)
- [Enterprise Considerations](#enterprise-considerations)

## Conciseness Guidelines

The context window is a shared resource. Your Skill competes with:

- The system prompt.
- Conversation history.
- Other Skills' metadata.
- The user's actual request.

### The Default Assumption: Claude Is Already Smart

Only add context Claude does not already have. For every piece of information, ask:

1. "Does Claude really need this explanation?"
2. "Can I assume Claude knows this?"
3. "Does this paragraph justify its token cost?"

### Good vs. Bad Examples

**Good — Concise (~50 tokens):**

````markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Bad — Too verbose (~150 tokens):**

```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but
pdfplumber is recommended because it's easy to use and handles most cases well.
First, you'll need to install it using pip...
```

The concise version assumes Claude knows what PDFs are and how libraries work.

## Description Writing Guide

The `description` field is the most critical part of your Skill. It determines
whether the Skill triggers correctly from potentially 100+ installed Skills.

### Rules

1. **Always write in third person.** The description is injected into the system prompt. Inconsistent point-of-view causes discovery problems.
   - **Good:** "Processes Excel files and generates reports"
   - **Bad:** "I can help you process Excel files"
   - **Bad:** "You can use this to process Excel files"

2. **Include both what it does AND when to use it.**

3. **Include trigger keywords.** Incorporate the specific words users are likely to type.

4. **Stay within 1,024 characters.** Keep it concise but specific.

5. **Use explicit verbs.** "Analyze", "generate", "extract", "validate", "deploy".

### Template

```yaml
description: >
  [Verb]s [object] and [verb]s [object] for [domain/context].
  Use when the user [trigger scenario 1], [trigger scenario 2],
  or when working with [file type/technology].
```

### Examples

```yaml
# PDF Processing
description: >
  Extracts text and tables from PDF files, fills forms, and merges
  documents. Use when working with PDF files or when the user mentions
  PDFs, forms, or document extraction.

# Excel Analysis
description: >
  Analyzes Excel spreadsheets, creates pivot tables, generates charts.
  Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.

# Git Commit Helper
description: >
  Generates descriptive commit messages by analyzing git diffs. Use when
  the user asks for help writing commit messages or reviewing staged changes.

# Code Review
description: >
  Performs systematic code review checking for defects, security risks,
  and test coverage gaps. Use when the user asks to review code, check
  a PR, or audit code quality before merge.
```

## Naming Conventions

Use consistent naming patterns. The official recommendation is **gerund form**
(verb + -ing):

### Preferred (Gerund Form)

```
processing-pdfs
analyzing-spreadsheets
managing-databases
testing-code
writing-documentation
creating-skills
```

### Acceptable Alternatives

```
# Noun phrases
pdf-processing
spreadsheet-analysis

# Action-oriented
process-pdfs
analyze-spreadsheets
```

### Avoid

```
helper          # too vague
utils           # too generic
tools           # too broad
documents       # no verb, unclear action
anthropic-x     # reserved word
claude-tools    # reserved word
my_skill        # underscores not allowed
```

## Degrees of Freedom

Match the level of specificity to the task's fragility and variability.

### High Freedom (Text Guidance)

Use when multiple approaches are valid and decisions depend on context.

```markdown
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
```

### Medium Freedom (Pseudocode/Templates)

Use when a preferred pattern exists but some variation is acceptable.

````markdown
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
````

### Low Freedom (Exact Scripts)

Use when operations are fragile, error-prone, or consistency is critical.

````markdown
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
````

### The Bridge Analogy

Think of Claude as a robot exploring a path:

- **Narrow bridge with cliffs**: Only one safe way forward → Low freedom, exact instructions.
- **Open field**: Many paths lead to success → High freedom, general direction.

## Iterative Development

The most effective Skill development uses Claude itself.

### Two-Instance Workflow

1. **Complete a task without a Skill**: Work through a problem with Claude A (the expert) using normal prompting. Notice what information you repeatedly provide.

2. **Identify the reusable pattern**: What context would be useful for similar future tasks? Table names, field definitions, filtering rules, common query patterns?

3. **Ask Claude A to create the Skill**: "Create a Skill that captures this pattern we just used."

4. **Review for conciseness**: Check that Claude hasn't added unnecessary explanations. Ask: "Remove the explanation about what X means — Claude already knows that."

5. **Improve information architecture**: Ask: "Organize this so the table schema is in a separate reference file."

6. **Test with Claude B** (a fresh instance with the Skill loaded) on related use cases. Observe whether it finds the right information and applies rules correctly.

7. **Iterate based on observation**: "When Claude used this Skill, it forgot to filter by date. Should we add a section about date filtering patterns?"

### Continuous Improvement Loop

```
Create/Update Skill → Test with real tasks → Observe behavior → Identify gaps → Refine → Repeat
```

## Observing Agent Behavior

Watch for these signals during testing:

| Observation | Remedy |
|---|---|
| Agent doesn't trigger the Skill | Revisit keywords in `description` |
| Agent doesn't read reference files | Make links in SKILL.md more explicit |
| Agent reads the same file repeatedly | Move that content into the SKILL.md body |
| Agent reads unnecessary files | Reorganize directory structure |
| Script execution fails | Improve error messages |
| Agent ignores a bundled file | File might be unnecessary or poorly signaled |
| Agent explores files in unexpected order | Structure may not be intuitive |

## Token Budget Management

- **SKILL.md body**: Under 500 lines (< 5,000 tokens recommended).
- **Metadata** (name + description): ~100 tokens per Skill.
- **References**: Loaded on demand, no hard limit.
- **Scripts**: Executed (not loaded into context), token-free.

### When to Split

Split content into reference files when:

- SKILL.md exceeds 300 lines.
- Content is domain-specific and not always relevant.
- Information applies to only some workflows.
- You have large code examples or data schemas.

## Team Collaboration

### Gathering Feedback

1. Share Skills with teammates and observe their usage.
2. Ask: Does the Skill activate when expected? Are instructions clear? What's missing?
3. Incorporate feedback to address blind spots.

### Separation of Duties

For enterprise deployments, Skill authors should not be their own reviewers.
Require peer review for all production Skills.

## Scope Selection

| Criterion | Workspace Skill | User Skill |
|---|---|---|
| Other team members will use it | Yes | No |
| Needs Git tracking | Yes | Maybe |
| Project-specific | Yes | No |
| Used across all projects | No | Yes |
| Depends on personal preference | No | Yes |

### Workspace Skill paths

```
.claude/skills/       # Claude Code
.gemini/skills/       # Gemini CLI
.agents/skills/       # OpenAI Codex / Antigravity
.cursor/skills/       # Cursor
```

### User Skill paths

```
~/.claude/skills/     # Claude Code
~/.gemini/skills/     # Gemini CLI
~/.agents/skills/     # OpenAI Codex (USER scope)
```

## Workflow Skills

### Checklist Pattern

Define complex procedures as checklists for reliable execution:

```markdown
# Release Workflow

Copy this checklist to track progress:

- [ ] Step 1: Run and verify tests
- [ ] Step 2: Bump version
- [ ] Step 3: Update CHANGELOG
- [ ] Step 4: Commit and tag
- [ ] Step 5: Execute deployment
- [ ] Step 6: Verify operation
```

### Feedback Loop Pattern

Include validation steps to catch errors early:

```markdown
## Editing Process

1. Apply edits
2. **Validate immediately**: `python scripts/validate.py`
3. If validation fails:
   - Review the error message
   - Fix the issue
   - Re-run validation
4. **Proceed only when validation passes**
```

### Conditional Workflow Pattern

Branch based on task type:

```markdown
## Document Change Workflow

1. Determine the change type:
   **If creating new** → Proceed to "Creation Workflow"
   **If editing existing** → Proceed to "Editing Workflow"
```

## Enterprise Considerations

### Recall Limits

Limit the number of Skills loaded simultaneously. With too many active,
Claude may fail to select the right one. Use evaluations to measure
accuracy as you add Skills.

**API limit:** Maximum 8 Skills per request.

### Start Specific, Consolidate Later

1. Start with narrow, workflow-specific Skills.
2. As patterns emerge, consolidate into broader Skills.
3. Merge only when evaluations confirm equivalent performance.

**Example progression:**

- Start: `formatting-sales-reports`, `querying-pipeline-data`, `updating-crm-records`
- Consolidate: `sales-operations` (when evals confirm equivalent performance)

### Internal Registry

Maintain for each Skill:

- **Purpose**: What workflow it supports.
- **Owner**: Team or individual responsible.
- **Version**: Current deployed version.
- **Dependencies**: MCP servers, packages, external services.
- **Evaluation status**: Last evaluation date and results.

## Sources

- <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise>
- <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
- <https://shibuiyusuke.medium.com/10-practical-techniques-for-mastering-agent-skills-in-ai-coding-agents-6070e4038cf1>
- <https://github.com/anthropics/anthropic-cookbook/tree/main/skills>
