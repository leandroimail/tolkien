# Evaluation and Testing Guide for Agent Skills

> How to evaluate, test, and iterate on Agent Skills.
> Based on [Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
> and [Anthropic Enterprise Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise).

## Table of Contents

- [Evaluation-Driven Development](#evaluation-driven-development)
- [What to Evaluate](#what-to-evaluate)
- [Building Evaluation Scenarios](#building-evaluation-scenarios)
- [Two-Instance Testing Workflow](#two-instance-testing-workflow)
- [Testing Across Models](#testing-across-models)
- [Observation Patterns](#observation-patterns)
- [Enterprise Evaluation Gates](#enterprise-evaluation-gates)
- [Lifecycle Decisions from Evaluations](#lifecycle-decisions-from-evaluations)

## Evaluation-Driven Development

Build Skills based on observed gaps, not assumptions.

### The Process

1. **Identify gaps**: Run the target task without a Skill. Record where the agent struggles or requires additional context.
2. **Create evaluations**: Prepare 3-5 representative scenarios that test those gaps.
3. **Measure baseline**: Record the agent's behavior without the Skill.
4. **Write minimal instructions**: Create the smallest SKILL.md that bridges the gaps.
5. **Test**: Run evaluations and compare against baseline.
6. **Iterate**: Refine based on failures.

### Evaluation Scenario Format

```json
{
  "skills": ["my-skill-name"],
  "query": "User's natural language request",
  "files": ["test-files/sample-input.pdf"],
  "expected_behavior": [
    "Agent selects and triggers the correct Skill",
    "Agent reads the appropriate reference files",
    "Agent applies the documented rules correctly",
    "Agent produces the expected output format"
  ],
  "should_not_trigger_for": [
    "Unrelated query that mentions similar keywords",
    "Query that another Skill should handle"
  ]
}
```

## What to Evaluate

### Five Evaluation Dimensions

| Dimension | What It Measures | Example Failure |
|---|---|---|
| **Triggering accuracy** | Does the Skill activate for the right queries and stay inactive for unrelated ones? | Skill triggers on every spreadsheet mention, even when user just wants to discuss data |
| **Isolation behavior** | Does the Skill work correctly on its own? | Skill references files that don't exist |
| **Coexistence** | Does adding this Skill degrade other Skills? | New Skill's description is too broad, stealing triggers from existing Skills |
| **Instruction following** | Does Claude follow the Skill's instructions accurately? | Claude skips validation steps or uses wrong libraries |
| **Output quality** | Does the Skill produce correct, useful results? | Reports have formatting errors or missing data |

### Minimum Test Coverage

For each Skill, prepare evaluation queries for:

1. **Should trigger** (3+ scenarios): Queries where this Skill is the correct choice.
2. **Should NOT trigger** (2+ scenarios): Queries that are similar but belong to another Skill or need no Skill.
3. **Edge cases** (1+ scenarios): Ambiguous queries or unusual inputs.

## Building Evaluation Scenarios

### Example: PDF Processing Skill

```json
[
  {
    "name": "basic-extraction",
    "query": "Extract all text from this PDF file and save it to output.txt",
    "expected": ["Skill triggers", "Uses pdfplumber", "Extracts all pages", "Saves to output.txt"]
  },
  {
    "name": "form-filling",
    "query": "Fill out the signature field in this PDF form",
    "expected": ["Skill triggers", "Reads FORMS.md reference", "Uses form-filling script", "Fills correct field"]
  },
  {
    "name": "should-not-trigger",
    "query": "What's the difference between PDF and DOCX formats?",
    "expected": ["Skill does NOT trigger", "Claude answers from general knowledge"]
  },
  {
    "name": "edge-case-scanned",
    "query": "Extract text from this scanned PDF",
    "expected": ["Skill triggers", "Recognizes OCR need", "Uses appropriate OCR approach"]
  }
]
```

### Example: Code Review Skill

```json
[
  {
    "name": "pr-review",
    "query": "Review this pull request for security issues",
    "expected": ["Skill triggers", "Checks for security patterns", "Produces structured report"]
  },
  {
    "name": "should-not-trigger",
    "query": "Write a new function that sorts a list",
    "expected": ["Skill does NOT trigger", "Claude writes code normally"]
  }
]
```

## Two-Instance Testing Workflow

Recommended by Anthropic for iterative development:

### Roles

- **Claude A (Skill Creator)**: The expert instance that designs and refines the Skill.
- **Claude B (Skill User)**: A fresh instance that uses the Skill for real tasks.

### Workflow

1. **Create**: Work with Claude A to design the initial Skill.
2. **Test**: Give Claude B (with Skill loaded) actual tasks.
3. **Observe**: Note where Claude B struggles, succeeds, or makes unexpected choices.
4. **Report back**: Share observations with Claude A: "When I asked Claude B for X, it forgot Y."
5. **Refine**: Claude A improves the Skill based on real behavior.
6. **Repeat**: Test again with Claude B. Continue until all evaluation scenarios pass.

### What to Report to Claude A

Be specific about failures:

```
"When I asked Claude B for a regional sales report:
- It wrote the query correctly (✅)
- But forgot to filter test accounts (❌)
- The Skill mentions filtering, but maybe it's not prominent enough?"
```

## Testing Across Models

Skill effectiveness varies by model. Test with all models you plan to use.

| Model Tier | What to Check |
|---|---|
| **Haiku / lightweight** | Does the Skill provide enough guidance? Are instructions clear enough for a smaller model? |
| **Sonnet / mid-tier** | Are instructions clear and efficient? No unnecessary explanation? |
| **Opus / high-performance** | Does the Skill avoid over-explaining? Is there too much unnecessary detail? |

### Key Insight

A Skill that works perfectly with Opus may need more detailed instructions for Haiku. Aim for instructions that work well across all target models.

## Observation Patterns

Watch for these signals during testing:

| Observation | What It Means | Remedy |
|---|---|---|
| Agent doesn't trigger the Skill | Description keywords don't match user's query | Add more trigger keywords to `description` |
| Agent triggers for wrong queries | Description is too broad | Narrow description, add exclusions |
| Agent doesn't read reference files | Links not explicit enough | Make reference links more prominent in SKILL.md |
| Agent reads same file repeatedly | Content should be in main SKILL.md | Move frequently-needed content to body |
| Agent reads unnecessary files | Directory structure is confusing | Reorganize files, improve naming |
| Agent ignores bundled files | Files are poorly signaled | Make links more explicit or file may be unnecessary |
| Agent explores unexpected order | Structure isn't intuitive | Reorganize for natural navigation |
| Scripts fail | Error messages are inadequate | Add specific, actionable error messages |
| Agent overwrites user's intent | Instructions are too prescriptive | Increase degrees of freedom |
| Agent produces inconsistent output | Instructions are too vague | Decrease degrees of freedom, add templates |

## Enterprise Evaluation Gates

For production deployment, require these approval gates:

| Dimension | Approval Criteria |
|---|---|
| Triggering accuracy | Skill activates for all "should trigger" scenarios and stays inactive for all "should not trigger" scenarios |
| Isolation behavior | Skill works correctly without any other Skills loaded |
| Coexistence | Adding this Skill does not degrade existing Skills' trigger accuracy or output quality |
| Instruction following | Claude follows all Skill instructions accurately in 90%+ of test runs |
| Output quality | Output meets defined quality standards in all test scenarios |

### Evaluation Requirements

- 3-5 representative queries per Skill.
- Cover should-trigger, should-not-trigger, and edge cases.
- Test across all models the organization uses.
- Test both in isolation and alongside existing Skills.

## Lifecycle Decisions from Evaluations

Use evaluation results to decide next actions:

| Signal | Action |
|---|---|
| Declining trigger accuracy | Update description or instructions |
| Coexistence conflicts | Consolidate overlapping Skills or narrow descriptions |
| Consistently low output quality | Rewrite instructions or add validation steps |
| Persistent failures across updates | Deprecate the Skill |
| New use cases emerge | Extend the Skill or create a complementary one |
| Skill outgrows its scope | Split into multiple focused Skills |

## Sources

- <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise>
- <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- <https://shibuiyusuke.medium.com/10-practical-techniques-for-mastering-agent-skills-in-ai-coding-agents-6070e4038cf1>
