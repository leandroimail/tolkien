---
name: creating-skills
description: >
  Creates, validates, and deploys Agent Skills following the open standard
  specification, Anthropic best practices, and cross-IDE compatibility rules.
  Use when the user asks to create a new Skill, improve an existing Skill,
  validate Skill structure, or migrate Skills across IDEs like Claude Code,
  Gemini CLI, OpenAI Codex, Cursor, Antigravity, Kiro, or Qoder.
---

# Creating Agent Skills

## Purpose

Guide the creation of production-grade Agent Skills that follow the official
[Agent Skills Specification](https://agentskills.io/specification), Anthropic
best practices, and cross-IDE portability standards.

This skill is optimized for:

- Building new Skills from scratch following the open standard.
- Validating and improving existing Skills against best practices.
- Ensuring cross-IDE portability (Claude Code, Gemini CLI, OpenAI Codex, Cursor, Antigravity, Kiro, Qoder).
- Token-efficient progressive disclosure design.

## When To Use

Use this skill when you need to:

- Create a new Agent Skill from scratch.
- Validate an existing Skill against the official specification and best practices.
- Redesign a Skill for better trigger accuracy, token efficiency, or portability.
- Migrate Skills between IDEs or make them cross-IDE compatible.
- Review a Skill for security concerns before deployment.
- Set up evaluation workflows for Skills.

## When Not To Use

Do not use this skill for:

- Using (not creating) an existing Skill.
- MCP server configuration (use the `multi-ide-artifacts` skill).
- General prompting or instruction writing unrelated to Agent Skills.

## Prerequisites

Before creating a Skill, collect:

- **Purpose**: What specific gap in agent capability does this Skill fill?
- **Target audience**: Workspace (team) or User (personal) scope?
- **Target IDEs**: Which IDEs must support this Skill?
- **Complexity estimate**: Will it need `references/`, `scripts/`, or `assets/`?
- **Environment constraints**: Does it require network, specific packages, or tools?

## Core Principles

Follow these principles strictly. They come from the official Anthropic best
practices and the Agent Skills specification.

### 1. Conciseness is Key

The context window is a shared resource. Only add information Claude does not
already know. Challenge every line:

- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Claude is already very smart.** Do not explain general concepts. Focus on
what is unique to your domain, workflow, or toolchain.

> See [BEST_PRACTICES.md](references/BEST_PRACTICES.md) for detailed
> conciseness guidelines and examples.

### 2. Progressive Disclosure (Three-Stage Loading)

Design Skills to load information progressively:

| Level | When Loaded | Token Cost | Content |
|-------|-------------|------------|---------|
| **L1: Metadata** | Always (at startup) | ~100 tokens/Skill | YAML `name` and `description` |
| **L2: Instructions** | When Skill triggers | < 5,000 tokens recommended | SKILL.md body |
| **L3: Resources** | On demand | Virtually unlimited | Files in `scripts/`, `references/`, `assets/` |

**Key rules:**

- Keep SKILL.md body **under 500 lines**.
- Move detailed content to `references/` files.
- Keep file references **one level deep** from SKILL.md (no nested chains).
- Add a Table of Contents to reference files over 100 lines.

> See [PROGRESSIVE_DISCLOSURE.md](references/PROGRESSIVE_DISCLOSURE.md) for
> patterns and anti-patterns.

### 3. Set Appropriate Degrees of Freedom

Match specificity to the task's fragility:

- **High freedom** (text guidance): Multiple valid approaches exist.
- **Medium freedom** (pseudocode/templates): A preferred pattern exists.
- **Low freedom** (exact scripts): Operations are fragile, consistency critical.

### 4. Cross-IDE Portability

Write Skills that work across all compatible tools:

- Use **forward slashes** in all paths (`scripts/helper.py`, not `scripts\helper.py`).
- **Avoid tool-specific features** in instructions (don't reference "Claude Code's Read tool").
- Use the `compatibility` field for environment requirements.
- Use **relative paths** for all internal file references.

> See [CROSS_IDE_GUIDE.md](references/CROSS_IDE_GUIDE.md) for IDE-specific
> paths and deployment strategies.

### 5. Security by Design

- Never include secrets, API keys, or credentials in Skill files.
- Scripts should not make unexpected network calls.
- External URLs carry tampering risk — bundle data in `assets/` when possible.
- Audit all external Skills before use.

> See [SECURITY_CHECKLIST.md](references/SECURITY_CHECKLIST.md) for the
> complete audit checklist.

## Method

Follow this step-by-step workflow to create a Skill.

### Step 1: Identify the Gap

1. Run the target task **without** a Skill.
2. Record where the agent struggles, requires extra context, or makes errors.
3. Document the specific knowledge, procedures, or tools the agent lacks.

### Step 2: Design the Skill Structure

Choose the appropriate structure based on complexity:

**Simple Skill** (single-file):

```
my-skill/
└── SKILL.md
```

**Standard Skill** (with references):

```
my-skill/
├── SKILL.md
└── references/
    ├── guide.md
    └── api-reference.md
```

**Complex Skill** (full structure):

```
my-skill/
├── SKILL.md
├── scripts/
│   ├── validate.py
│   └── process.sh
├── references/
│   ├── domain-a.md
│   ├── domain-b.md
│   └── api-reference.md
└── assets/
    ├── template.json
    └── schema.yaml
```

### Step 3: Write the Frontmatter

Apply these rules strictly:

```yaml
---
name: my-skill-name        # REQUIRED: 1-64 chars, lowercase + hyphens only
description: >             # REQUIRED: 1-1024 chars, MUST be third-person
  Performs X and Y for Z workflows. Use when the user mentions
  A, B, or C, or when working with D files.
license: MIT               # OPTIONAL: license name or file reference
compatibility: >           # OPTIONAL: 1-500 chars, environment requirements
  Requires git and python3. Network access needed for API calls.
metadata:                  # OPTIONAL: arbitrary key-value pairs
  author: team-name
  version: "1.0"
---
```

**`name` field rules:**

- Lowercase letters, numbers, and hyphens only.
- Must not start or end with a hyphen.
- No consecutive hyphens (`--`).
- **Must match the parent directory name.**
- Prefer gerund form: `processing-pdfs`, `analyzing-data`, `creating-skills`.

**`description` field rules:**

- **Always write in third person** ("Processes files..." not "I help you...").
- Describe **what it does** AND **when to use it**.
- Include specific **trigger keywords** users are likely to say.
- Use explicit verbs: "analyze", "generate", "extract", "validate".
- **Make it slightly "pushy"**: LLMs often undertrigger skills. Encourage proactive use (e.g., "Use this whenever the user mentions X, even if they don't explicitly ask for this skill").

> See [SPECIFICATION.md](references/SPECIFICATION.md) for the complete
> field specification.

### Step 4: Write the SKILL.md Body

Structure the body with these sections:

```markdown
# Skill Title

## Purpose
Brief description of what this skill does and why.

## When To Use
Bullet list of scenarios.

## When Not To Use
Bullet list of exclusions.

## Inputs
What the agent needs to collect before proceeding.

## Method
Step-by-step instructions. Use numbered lists for strict sequences,
bullet lists for flexible order.

## Quality Checklist
- [ ] Checklist items to verify output quality.

## Outputs
What the skill produces.
```

**Body writing rules:**

- Keep under 500 lines.
- Use code blocks for exact commands or scripts.
- Link to `references/` for detailed content.
- Use checklists for multi-step workflows.
- Include feedback loops ("validate → fix → re-validate").
- Make content grep-searchable when referencing large files.
- **Explain the "WHY" (Theory of Mind)**: Avoid rigid, heavy-handed "MUSTs". Explain the reasoning behind the rules so the agent can generalize correctly to unexpected edge cases.

### Step 5: Create Reference Files (if needed)

For each reference file:

- Use **descriptive filenames** (`form_validation_rules.md`, not `doc1.md`).
- Add a **Table of Contents** for files over 100 lines.
- Keep each file **domain-focused** (one topic per file).
- Reference from SKILL.md with explicit links:

```markdown
**For advanced features**: See [advanced.md](references/advanced.md)
**API reference**: See [api-reference.md](references/api-reference.md)
```

### Step 6: Create Scripts (if needed)

Use scripts for operations that are:

- **Deterministic** (validation, conversion, formatting).
- **Complex** (multi-step library interactions).
- **Repetitive** (identical processing each time).

Script requirements:

- Self-contained or clearly document dependencies.
- Include **specific error messages** (not "an error occurred").
- Use proper exit codes.
- Document usage in SKILL.md:

```markdown
## Validation

Run the validation script:

\```bash
python scripts/validate.py input_file.json
\```

Output: JSON with validation results and error details.
```

### Step 7: Validate & Benchmark

Run the validation script or manually check structural compliance:

```bash
bash scripts/validate_skill.sh path/to/my-skill
```

**Quantitative & Qualitative testing:**
- **Parallel Test Runs**: Run realistic user prompts both *with* the skill and *without* the skill (baseline) to measure the true delta in quality.
- **Assertions**: For objective skills, define verifiable assertions (e.g., in an `evals.json`) and aggregate metrics (pass rate, tokens, duration).
- **Blind Comparison**: If the output is subjective (e.g., writing style or design), use a neutral evaluator or subagent to blindly compare the baseline vs. the skill-generated output.

> See [EVALUATION_GUIDE.md](references/EVALUATION_GUIDE.md) for the full
> evaluation and testing workflow.

### Step 8: Optimize Trigger Accuracy (Trigger Evals)

The description is what tells the LLM when to invoke the skill. To maximize accuracy before deployment:
1. Create a set of realistic, messy user queries (~10 "should-trigger" and ~10 "should-not-trigger").
2. **"Should-trigger" queries** must test edge cases, casual phrasing, typos, and implicit needs (e.g., "my boss sent me this xlsx...").
3. **"Should-not-trigger" queries** must be tricky near-misses (adjacent domains or overlapping keywords that actually require a different tool).
4. Run an automated loop testing the description against these queries, adjusting the frontmatter description iteratively to minimize false positives and negatives.

### Step 9: Deploy Cross-IDE

Follow the `multi-ide-artifacts` skill for cross-IDE deployment:

1. Create the canonical Skill in `.agents/skills/<name>/`.
2. Copy recursively to IDE-specific paths as needed.
3. Verify all internal references remain correct.
4. Use relative paths in all file references.

> See [CROSS_IDE_GUIDE.md](references/CROSS_IDE_GUIDE.md) for IDE-specific
> deployment paths.

## Quality Checklist

A Skill is acceptable only if all checks pass:

- [ ] `name` follows spec: lowercase, hyphens, 1-64 chars, matches directory.
- [ ] `description` is third-person, includes triggers, under 1024 chars.
- [ ] SKILL.md body is under 500 lines.
- [ ] All file references use relative paths.
- [ ] References are one level deep (no nested chains).
- [ ] Reference files over 100 lines have a Table of Contents.
- [ ] Scripts include specific error messages and usage docs.
- [ ] No secrets, API keys, or credentials in any file.
- [ ] No tool-specific language in instructions (portable).
- [ ] Forward slashes used in all paths.
- [ ] Tested with target models (Haiku, Sonnet, Opus if applicable).
- [ ] Directory name matches `name` in frontmatter.
- [ ] Copied artifacts include all subdirectories recursively.

## Iterative Development Workflow

Use the two-instance approach recommended by Anthropic:

1. **Agent A (Skill Creator)**: Designs and refines the Skill.
2. **Agent B (Skill User)**: Uses the Skill to execute real tasks.
3. **Observe**: Note where Agent B struggles.
4. **Feedback**: Bring observations back to Agent A.
5. **Improve**: Refine SKILL.md based on real behavior, not assumptions.
6. **Repeat**: Continue until evaluation scenarios pass consistently.

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| Vague description | Skill won't trigger correctly | Include trigger keywords and specific verbs |
| Over-explaining basics | Wastes tokens Claude doesn't need | Assume Claude's general knowledge |
| Monolithic SKILL.md | Context window spike | Split into references |
| Nested reference chains | Agent loses context | Keep one level deep |
| Tool-specific language | Breaks portability | Use generic instructions |
| Hardcoded credentials | Security vulnerability | Use env vars |
| Generic filenames | Agent can't navigate | Use descriptive names |
| No error messages in scripts | Agent can't diagnose failures | Add specific error messages |

## Reference Documentation

- **Official Specification**: [SPECIFICATION.md](references/SPECIFICATION.md)
- **Best Practices (Detailed)**: [BEST_PRACTICES.md](references/BEST_PRACTICES.md)
- **Progressive Disclosure Patterns**: [PROGRESSIVE_DISCLOSURE.md](references/PROGRESSIVE_DISCLOSURE.md)
- **Cross-IDE Deployment Guide**: [CROSS_IDE_GUIDE.md](references/CROSS_IDE_GUIDE.md)
- **Security Audit Checklist**: [SECURITY_CHECKLIST.md](references/SECURITY_CHECKLIST.md)
- **Evaluation & Testing Guide**: [EVALUATION_GUIDE.md](references/EVALUATION_GUIDE.md)
- **Complete Examples**: [EXAMPLES.md](references/EXAMPLES.md)

## External Links

- [Agent Skills Official Site](https://agentskills.io/)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Anthropic Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic Engineering Blog: Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Anthropic Skills Enterprise Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Anthropic Skills Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [10 Practical Techniques for Mastering Agent Skills](https://shibuiyusuke.medium.com/10-practical-techniques-for-mastering-agent-skills-in-ai-coding-agents-6070e4038cf1)
