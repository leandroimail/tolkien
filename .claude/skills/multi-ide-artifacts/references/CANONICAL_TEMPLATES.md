# Canonical Templates

Use these templates when creating new artifacts. Always start with the canonical template, then adapt for IDE-specific targets.

## Table of Contents

- [Canonical Rule Template — AGENTS.md](#canonical-rule-template-agentsmd)
- [Canonical Skill Template — .agents/skills/](#canonical-skill-template-agentsskills)
- [Canonical Prompt/Slash Template](#canonical-promtslash-template)
- [Canonical Workflow/Hook/Steering Template](#canonical-workflowhooksteering-template)
- [Canonical Agent/Mode Template](#canonical-agentmode-template)
- [IDE-Specific Templates](#ide-specific-templates)
  - [VS Code Agent](#vs-code-agent-githubagentsagentmd)
  - [VS Code Scoped Instructions](#vs-code-scoped-instructions-githubinstructionsinstructionsmd)
  - [VS Code Prompt File](#vs-code-prompt-file-githubpromptspromptmd)
  - [OpenCode Agent](#opencode-agent-opencodeagentsmd)
  - [OpenCode Mode](#opencode-mode-opencodemodessmd)
  - [OpenCode Command](#opencode-command-opencodecommandsmd)
  - [Codex Skill Metadata](#codex-skill-metadata-agentsopenai-yaml)
  - [Kiro Agent (JSON)](#kiro-agent-kiroagentsjson)
  - [Kiro Steering](#kiro-steering-kirosteeringmd)
  - [Kiro MCP inline](#kiro-mcp-inline-in-agent-json)
  - [Antigravity Rules](#antigravity-rules-agentrulesmsd)
  - [Antigravity Workflow](#antigravity-workflow-agentworkflowsmd)
  - [Qoder Agent](#qoder-agent-qoderagentsmd)
  - [Qoder Rules](#qoder-rules-qoderulesmd)
- [MCP Config Templates](#mcp-config-templates)

---

## Canonical Rule Template (`AGENTS.md`)

```md
# Project AI Operating Rules

## Scope
- Apply to all AI-assisted tasks in this repository.

## Behavior
- Prioritize bug prevention, security, and test adequacy.
- Return severity-ranked findings with file references.
- Prefer minimal, safe fixes over large rewrites.

## Constraints
- Do not add secrets.
- Do not use destructive git commands unless explicitly requested.
```

## Canonical Skill Template (`.agents/skills/<name>/SKILL.md`)

```md
---
name: <skill-name>
description: <1-1024 chars. Explain exactly when this skill should and should not trigger.>
---

# Skill Title

## Purpose
What this skill does and when to use it.

## Process
1. Step one.
2. Step two.
3. Step three.
4. Step four.

## Output
- Expected format and structure.
- Severity or priority scheme if applicable.
```

**Name validation** (enforced by Codex and OpenCode):

- 1–64 characters, lowercase alphanumeric, single hyphen separators
- No leading/trailing hyphens, no consecutive `--`
- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Directory name must match `name` field exactly

## Canonical Prompt/Slash Template

```md
---
description: <what this prompt does>
argument-hint: <optional hint for user input>
---

<Prompt body with clear instructions.>

Output:
- Expected format.
- Constraints.
```

## Canonical Workflow/Hook/Steering Template

```md
# Workflow Title

## Trigger
- Manual slash invocation or configured hook event.

## Steps
1. Collect changed files.
2. Run review checklist.
3. Produce structured findings and next actions.
```

## Canonical Agent/Mode Template

```md
---
name: <agent-name>
description: <what this agent does>
tools: [<minimum required tools>]
---

You are a <role>. <Core behavioral instruction>.
Return severity-ranked findings with concrete remediation suggestions.
```

---

## IDE-Specific Templates

### VS Code Agent (`.github/agents/*.agent.md`)

```md
---
name: code-review
description: Repository code review specialist
tools: ['codebase', 'changes', 'search', 'usages']
# Optional fields:
# mcp-servers:
#   - type: stdio
#     command: npx
#     args: ['-y', '@modelcontextprotocol/server-filesystem', '.']
# handoffs:
#   - label: "Run tests"
#     agent: test-runner
#     prompt: "Run the test suite for changed files"
#     send: false
# model: gpt-4o
# target: vscode
# argument-hint: "file or scope to review"
---

Run a defect-first review:
1. correctness regressions
2. security exposure
3. test gaps

Return concise findings with file references.
```

### VS Code Scoped Instructions (`.github/instructions/*.instructions.md`)

```md
---
applyTo: "**/*.py"
---

# Python Instructions

- Check behavior regressions and edge cases first.
- Flag unsafe patterns (injection, unsafe eval/exec, secret exposure).
- Verify exception handling and input validation.
- Confirm tests cover changed execution paths.
```

### VS Code Prompt File (`.github/prompts/*.prompt.md`)

```md
---
name: pair-review
description: Run AI pair code review and return prioritized findings.
agent: agent
# Optional:
# model: gpt-4o
# tools: ['codebase', 'changes']
# mode: agent
---

Review current repository changes in pair mode.

Requirements:
- Focus on defects, security issues, and missing tests.
- Provide findings ordered by severity (high, medium, low).
- Include file path and minimal remediation for each finding.
```

### OpenCode Agent (`.opencode/agents/*.md`)

```md
---
description: Focused reviewer for defects, security issues, and test gaps.
mode: subagent
tools:
  read: true
  grep: true
  glob: true
  bash: false
  edit: false
  write: false
# Optional:
# permission:
#   skill:
#     "review-*": "allow"
#     "internal-*": "deny"
---

You are a repository reviewer. Return severity-ranked findings.
```

### OpenCode Mode (`.opencode/modes/*.md`)

```md
---
model: openai/gpt-5
prompt: ./prompts/<name>-system.md
tools:
  read: true
  grep: true
  glob: true
  bash: false
  edit: false
  write: false
---

# Mode Title

Description of mode behavior and constraints.
```

### OpenCode Command (`.opencode/commands/*.md`)

```md
---
description: Run AI pair code review on current diff with prioritized findings.
agent: general
---

Review the current git diff in pair mode.

Output:
- Findings sorted by severity.
- File path per finding.
- Minimal safe fix for each finding.
```

### Codex Skill Metadata (`agents/openai.yaml`)

Place inside the skill directory alongside `SKILL.md`:

```yaml
interface:
  display_name: "Review Specialist"
  short_description: "AI pair code review focused on defects and security"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Review changed files for defects and security issues"

policy:
  allow_implicit_invocation: true

dependencies:
  tools:
    - type: "mcp"
      value: "filesystem"
      description: "Filesystem MCP server for file access"
      transport: "stdio"
```

Fields:

- `allow_implicit_invocation` (default: `true`): When `false`, requires explicit `$skill-name` invocation.
- `dependencies.tools`: Declares MCP or other tool requirements for seamless setup.

### Kiro Agent (`.kiro/agents/*.json`)

```json
{
  "name": "code-review-agent",
  "description": "Specialized agent for code review and quality analysis",
  "prompt": "file://./prompts/code-review.md",
  "tools": [
    "read",
    "shell"
  ],
  "allowedTools": [
    "read",
    "shell"
  ],
  "toolsSettings": {
    "shell": {
      "allowedCommands": [
        "grep", "find", "wc", "head", "tail",
        "git diff", "git log", "git status"
      ],
      "deniedCommands": [
        "rm", "mv", "chmod"
      ]
    }
  },
  "resources": [
    "file://CONTRIBUTING.md",
    "file://docs/coding-standards.md",
    "skill://code-review-checklist"
  ],
  "hooks": {
    "agentSpawn": [
      {
        "command": "git diff --name-only HEAD~1"
      }
    ],
    "stop": [
      {
        "command": "uv run pytest"
      }
    ]
  },
  "includeMcpJson": true,
  "model": "claude-sonnet-4",
  "keyboardShortcut": "ctrl+r",
  "welcomeMessage": "Ready to review your code!"
}
```

Fields reference:

- `name`: Agent identifier
- `description`: Shown in agent picker
- `prompt`: System prompt / behavioral instructions (inline string or `file://` URI for external prompt file)
- `mcpServers`: Inline MCP server config (per-agent)
- `tools`: Available tools (built-in + MCP with `@server` prefix; use `*` for all, `@builtin` for all built-in)
- `allowedTools`: Whitelist of allowed tools (subset of `tools`, supports glob patterns)
- `toolAliases`: Rename tools for convenience (`{ "@git/git_status": "status" }`)
- `toolsSettings`: Per-tool config (`allowedPaths`, `allowedCommands`, `deniedCommands`)
- `resources`: Auto-loaded context:
  - `file://path/to/file` — loaded into context at startup
  - `skill://skill-name` — progressive disclosure (metadata at startup, full content on demand)
  - `knowledgeBase` object — indexed searchable docs with `source`, `name`, `description`, `indexType`, `autoUpdate`
- `hooks`: Lifecycle event handlers (see Hooks section)
- `includeMcpJson`: Boolean — when `true`, inherits MCP servers from `~/.kiro/settings/mcp.json` (global) and `<cwd>/.kiro/settings/mcp.json` (workspace)
- `model`: AI model to use
- `keyboardShortcut`: Keyboard shortcut for quick access
- `welcomeMessage`: Greeting when agent starts

### Kiro Steering (`.kiro/steering/*.md`)

Always-on steering (default behavior):

```md
---
inclusion: always
---

# Steering Title

- Default behavioral rule.
- Priority and constraint.
- Output preference.
```

File-match steering (triggered by file type):

```md
---
inclusion: fileMatch
fileMatchPattern: "**/*.ts"
---

# TypeScript Guidelines

- Use strict TypeScript.
- Prefer interfaces over types for public APIs.
```

Manual steering (on-demand via `#steering-name` or `/`):

```md
---
inclusion: manual
---

# Security Review Checklist

- Check for SQL injection.
- Validate all inputs.
```

Auto steering (loaded when request matches description):

```md
---
inclusion: auto
name: performance-tips
description: Performance optimization tips for database queries
---

# Performance Guidelines

- Use indexed queries.
- Avoid N+1 patterns.
```

Inclusion modes:

- `always`: loaded for every request (always-on rules, default)
- `fileMatch`: loaded when active files match `fileMatchPattern` glob
- `manual`: user must explicitly include via `#steering-name` or `/` slash command
- `auto`: agent loads when request matches the `description` (requires `name` + `description` frontmatter)

### Kiro MCP (inline in agent JSON)

Per-agent inline config:

```json
{
  "name": "agent-with-mcp",
  "description": "Agent with external tool access",
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "env": {},
      "timeout": 30000
    }
  },
  "includeMcpJson": true,
  "tools": ["read", "@filesystem"],
  "allowedTools": ["read", "@filesystem/list_files"]
}
```

Shared MCP config (`~/.kiro/settings/mcp.json` or `<cwd>/.kiro/settings/mcp.json`):

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "npx",
      "args": ["-y", "@example/shared-mcp-server"],
      "env": {
        "API_KEY": "$SHARED_API_KEY"
      }
    }
  }
}
```

> To inherit shared MCP servers in an agent, set `"includeMcpJson": true` in the agent JSON.

### Antigravity Rules (`.agent/rules/*.md`)

```md
# Rule Category

- Behavioral rule 1.
- Behavioral rule 2.
- Constraint.
```

### Antigravity Workflow (`.agent/workflows/*.md`)

```md
# Workflow Title

Description: What this workflow automates.

Steps:
1. Collect context.
2. Execute core logic.
3. Validate results.
4. Produce output.
```

### Qoder Agent (`.qoder/agents/*.md`)

```md
---
name: code-review
description: AI pair code review expert
tools: Read, Grep, Glob
---

You are a strict reviewer.
- Find defects, security issues, and missing tests.
- Propose the smallest safe fix.
```

### Qoder Skill (`.qoder/skills/*/SKILL.md` or `~/.qoder/skills/*/SKILL.md`)

```md
---
name: <skill-name>
description: <Brief description of functionality and when to use>
---

# Skill Name

## Instructions
Provide clear step-by-step guidance.

## Examples
Show specific usage examples.
```

### Qoder Command (`.qoder/commands/*.md` or `~/.qoder/commands/*.md`)

```md
---
name: <command-name>
description: <Brief description shown in command list>
---

This is the system prompt content.
When a user executes `/command-name`, this prompt guides it to complete the task.
```

### Qoder Rules (`.qoder/rules/*.md`)

Always Apply (default):

```md
# Project Rules

- Follow existing code conventions.
- Prioritize correctness and security.
- Minimal, safe changes over large rewrites.
```

Rule types reference:

- **Always Apply**: Loaded for every interaction (default behavior)
- **Model Decision**: AI decides when the rule is relevant based on context
- **Specific Files**: Rule applies only when working with files matching glob patterns
- **Apply Manually**: User explicitly references via `@rule` in chat

---

### Claude Code Memory / Rules (`CLAUDE.md`)

Project-level instructions — import AGENTS.md como única fonte de verdade:

```md
@AGENTS.md
```

Claude Code-specific notes:

- `CLAUDE.md` deve conter **apenas** `@AGENTS.md` (uma única linha), centralizando todas as regras no AGENTS.md.
- O import `@AGENTS.md` injeta o conteúdo completo no contexto da sessão do Claude Code.
- **Não adicione regras extras abaixo** — qualquer regra deve ir para o próprio AGENTS.md para que todos os IDEs se beneficiem.
- Também funciona em `.claude/CLAUDE.md` para manter a raiz do projeto limpa.

### Claude Code Scoped Rules (`.claude/rules/*.md`)

Path-scoped rules (only loaded when matching files are active):

```md
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All endpoints must validate input.
- Use the standard `{ data, error }` response shape.
- Include OpenAPI comments on each handler.
```

Always-on rule (no `paths` frontmatter):

```md
# Security Guidelines

- Never hardcode credentials.
- Validate all external input at system boundaries.
```

### Claude Code Skill (`.claude/skills/<name>/SKILL.md`)

Basic skill (auto-invocable by Claude):

```md
---
name: review-specialist
description: Reviews code for defects, security issues, and test gaps. Use when reviewing files, PRs, or changes.
---

Run a defect-first review:
1. Check for correctness regressions.
2. Flag security exposures (injection, auth gaps, secrets).
3. Identify missing test coverage.

Return findings sorted by severity with file references.
```

User-triggered-only skill with arguments (`disable-model-invocation: true`):

```md
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
allowed-tools: Bash(./scripts/*)
---

Deploy $ARGUMENTS to production:

1. Run `npm test`
2. Run `npm run build`
3. Execute `./scripts/deploy.sh $ARGUMENTS`
4. Verify deploy succeeded
```

Skill forked into subagent context (`context: fork`):

```md
---
name: deep-research
description: Research a topic thoroughly in isolated context
context: fork
agent: Explore
---

Research $ARGUMENTS:

1. Find relevant files with Glob and Grep
2. Analyze code and documentation
3. Return a structured summary with file references
```

Skill with shell injection and lifecycle hooks:

```md
---
name: pr-review
description: Review a pull request before merging
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-bash.sh"
---

## PR context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`

## Task
Review for defects, security gaps, and missing tests.
```

### Claude Code Agent/Subagent (`.claude/agents/<name>.md`)

Read-only reviewer subagent:

```md
---
name: code-reviewer
description: Reviews code for correctness, security, and maintainability. Use proactively after code changes.
tools: Read, Grep, Glob
model: sonnet
---

You are a senior code reviewer.
- Focus on defects, security vulnerabilities, and missing tests.
- Return severity-ranked findings with file references.
- Provide the minimal safe fix for each finding.
```

Full-featured subagent with MCP and preloaded skills:

```md
---
name: db-analyst
description: Analyzes database queries and schema. Invoke for performance or correctness issues.
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
permissionMode: dontAsk
mcpServers:
  - postgres:
      type: stdio
      command: npx
      args: ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
skills:
  - db-patterns
memory: user
hooks:
  Stop:
    - hooks:
        - type: command
          command: "echo 'Analysis complete' | notify-send"
---

You are a database expert.
- Analyze query performance and schema correctness.
- Reference the db-patterns skill for this project's conventions.
- Return findings with severity rating and remediation steps.
```

### Claude Code Hooks (`.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/pre-bash-check.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint -- --fix",
            "async": true
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run pytest --tb=short"
          }
        ]
      }
    ]
  }
}
```

Hook type reference:

- `type: command` — shell command; exit code and stdout control behavior
- `type: http` — POST to URL; response JSON controls behavior
- `type: prompt` — LLM prompt evaluation; returns allow/block decision
- `type: agent` — spawns a subagent verifier with tool access

Supported events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `Stop`, `SubagentStop`, `SubagentStart`, `TaskCompleted`, `TaskCreated`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `FileChanged`, `Notification`, `InstructionsLoaded`, `ConfigChange`, `PostCompact`, `PreCompact`, `StopFailure`, `TeammateIdle`, `WorktreeCreate`, `WorktreeRemove`, `Elicitation`, `ElicitationResult`.

---

## MCP Config Templates

### VS Code (`.vscode/mcp.json`)

```json
{
  "servers": {
    "example": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

With inputs for secrets:

```json
{
  "inputs": [
    {
      "id": "api-key",
      "description": "API Key",
      "type": "promptString",
      "password": true
    }
  ],
  "servers": {
    "example": {
      "command": "npx",
      "args": ["-y", "@example/server"],
      "env": {
        "API_KEY": "${input:api-key}"
      }
    }
  }
}
```

### OpenCode (`opencode.jsonc`)

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "example": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

### Codex (`.codex/config.toml`)

```toml
[mcp_servers.example]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "."]
```

### Claude Code (`.mcp.json` — project-shared)

Team-shared project-scoped config (commit to VCS):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Add via CLI (project scope, stored in `.mcp.json`):

```bash
claude mcp add --scope project --transport stdio github -- \
  npx -y @modelcontextprotocol/server-github
```

User-scoped (personal, stored in `~/.claude.json`):

```bash
claude mcp add --scope user --transport stdio my-server -- python3 ./server.py
```

### Qoder (`mcpServers` JSON settings)

```json
{
  "mcpServers": {
    "example": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

### Kiro (inline in agent JSON)

```json
{
  "mcpServers": {
    "example": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "env": {},
      "timeout": 30000
    }
  }
}
```

### OpenCode Skill Permissions (`opencode.json`)

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

## 7. Qwen Code CLI Templates

### Qwen Code Subagent (`.qwen/agents/*.md` or `~/.qwen/agents/*.md`)

```md
---
name: code-review
description: AI pair code review expert
tools:
  - Read
  - Grep
  - Glob
---

You are a strict reviewer.
- Find defects, security issues, and missing tests.
- Propose the smallest safe fix.
```

### Qwen Code Skill (`.qwen/skills/*/SKILL.md` or `~/.qwen/skills/*/SKILL.md`)

```md
---
name: <skill-name>
description: <Brief description of functionality and when to use>
---

# Skill Name

## Instructions
Provide clear step-by-step guidance.

## Examples
Show specific usage examples.
```

### Qwen Code Command (`.qwen/commands/*.md` or `~/.qwen/commands/*.md`)

```md
---
description: <Optional description shown in /help>
---

This is the system prompt content.
Use {{args}} for parameter injection, like parameter: {{args}}
```
