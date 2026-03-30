# Conversion Playbook

This playbook shows how to convert canonical artifacts into IDE-specific equivalents.
For the exhaustive from/to mapping, see [CONVERSION_MATRIX.md](./CONVERSION_MATRIX.md).

## Table of Contents

- [Example A: Canonical Skill → IDE Targets](#example-a-canonical-skill--ide-targets)
- [Example B: Canonical Rule → IDE Rules](#example-b-canonical-rule--ide-rules)
- [Example C: Canonical Prompt/Slash → IDE Formats](#example-c-canonical-promtslash--ide-formats)
- [Example D: Canonical Agent → IDE Agent Files](#example-d-canonical-agent--ide-agent-files)
- [Example E: MCP Conversion](#example-e-mcp-conversion)
- [Example F: Workflow/Hook → IDE Formats](#example-f-workflowhook--ide-formats)
- [Example G: Tool Permissions → IDE Formats](#example-g-tool-permissions--ide-formats)
- [Dedup Exceptions](#dedup-exceptions)

---

## Example A: Canonical Skill → IDE Targets

Source:

- `.agents/skills/review-specialist/SKILL.md`

Targets:

| IDE | Action | Path |
|---|---|---|
| VS Code | Keep canonical as-is (native support) | `.agents/skills/review-specialist/SKILL.md` |
| Codex | Keep canonical as-is (native support, progressive disclosure) | `.agents/skills/review-specialist/SKILL.md` |
| OpenCode | Keep canonical as-is (native support) | `.agents/skills/review-specialist/SKILL.md` |
| **Claude Code** | **Copy to Claude Code path** (does not read `.agents/skills/` natively) | `.claude/skills/review-specialist/SKILL.md` |
| Antigravity | Create workspace copy if needed | `.agent/skills/review-specialist/SKILL.md` |
| Kiro | Create workspace copy if needed | `.kiro/skills/review-specialist/SKILL.md` |
| Qoder | Create workspace copy if needed | `.qoder/skills/review-specialist/SKILL.md` |
| Qwen Code | Create workspace copy if needed | `.qwen/skills/review-specialist/SKILL.md` |

Optional enhancements per IDE:

- **Codex**: Add `agents/openai.yaml` for UI metadata (display_name, icon, brand_color, allow_implicit_invocation).
- **OpenCode**: Configure skill permissions in `opencode.json` if access control is needed:

  ```json
  { "permission": { "skill": { "review-specialist": "allow" } } }
  ```

Rule:

- Do not duplicate skill text into multiple auto-loaded directories unless the IDE cannot consume canonical location.

---

## Example B: Canonical Rule → IDE Rules

Source:

- `AGENTS.md`

Targets:

| IDE | Action | Path |
|---|---|---|
| VS Code | Use directly; add scoped instructions for file-type deltas | `AGENTS.md` + `.github/instructions/*.instructions.md` |
| Codex | Use directly; use override for local domains only | `AGENTS.md` + optional `AGENTS.override.md` |
| OpenCode | Use directly; do not duplicate in config | `AGENTS.md` |
| **Claude Code** | **Create `CLAUDE.md` with only `@AGENTS.md`** — AGENTS.md is the single source of truth; never add rules below the import | `CLAUDE.md` (single line: `@AGENTS.md`); `.claude/rules/*.md` only for path-scoped rules with no AGENTS.md equivalent |
| Antigravity | Convert content to workspace rules | `.agent/rules/<name>.md` |
| Kiro | Convert to steering with `inclusion: always`; or embed in agent JSON `prompt` | `.kiro/steering/<name>.md` or agent JSON |
| Qoder | Convert to project rules; AGENTS.md may coexist | `.qoder/rules/<name>.md` |

Rule:

- Maintain one primary always-on rules source per IDE.
- Do not create both `.github/copilot-instructions.md` and `AGENTS.md` with overlapping content for VS Code.

---

## Example C: Canonical Prompt/Slash → IDE Formats

Source:

- Canonical prompt block defining a user-invokable action.

Targets:

| IDE | Action | Path/Format |
|---|---|---|
| VS Code | Create prompt file with rich frontmatter | `.github/prompts/<name>.prompt.md` with `description`, `agent`, `model`, `tools`, `mode` |
| Codex | Create skill instead (Codex prefers skills over prompts) | `.agents/skills/<name>/SKILL.md` |
| OpenCode | Create command file | `.opencode/commands/<name>.md` with `description`, `agent` |
| **Claude Code** | **Create skill** in Claude Code path | `.claude/skills/<name>/SKILL.md` with `disable-model-invocation: true` + `$ARGUMENTS` for parameters |
| Antigravity | Create workflow | `.agent/workflows/<name>.md` |
| Kiro | Create agent JSON with prompt and keyboard shortcut | `.kiro/agents/<name>.json` with `prompt`, `keyboardShortcut`, `welcomeMessage` |
| Qoder | Create command file | `.qoder/commands/<name>.md` → invoke with `/command-name` |
| Qwen Code | Create command file | `.qwen/commands/<name>.md` → invoke with `/command-name` |

Rule:

- Convert prompts per IDE-specific mechanism; do not force a fake universal prompt directory.

---

## Example D: Canonical Agent → IDE Agent Files

Source:

- Canonical agent behavior defined in generic template.

Targets:

| IDE | Action | Path/Format |
|---|---|---|
| VS Code | Create agent file with YAML frontmatter | `.github/agents/<name>.agent.md` with `name`, `description`, `tools`, `mcp-servers`, `handoffs` |
| Codex | No repo agent file — use skills | `.agents/skills/<name>/SKILL.md` |
| OpenCode | Create agent and/or mode file | `.opencode/agents/<name>.md` with `description`, `mode`, `tools` |
| **Claude Code** | **Create subagent file** | `.claude/agents/<name>.md` with YAML frontmatter + markdown body; use `skills:` to preload; `tools:` allowlist |
| Antigravity | No distinct agent file — use rules + workflows + skills | `.agent/rules/` + `.agent/workflows/` + `.agent/skills/` |
| Kiro | Create JSON agent with full config | `.kiro/agents/<name>.json` (see template) |
| Qoder | Create agent file | `.qoder/agents/<name>.md` with `name`, `description`, `tools` |
| Qwen Code | Create agent file | `.qwen/agents/<name>.md` with `name`, `description`, `tools` |

### Kiro Agent JSON example (complete)

```json
{
  "name": "code-review-agent",
  "description": "Specialized agent for code review and quality analysis",
  "prompt": "You are a code review specialist focused on quality, security, and best practices",
  "mcpServers": {
    "fetch": {
      "command": "fetch-mcp",
      "args": []
    }
  },
  "tools": ["read", "shell"],
  "allowedTools": ["read", "shell"],
  "toolsSettings": {
    "shell": {
      "allowedCommands": ["grep", "find", "git diff", "git log"]
    }
  },
  "resources": [
    "file://CONTRIBUTING.md",
    "file://docs/coding-standards.md"
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
  "model": "claude-sonnet-4",
  "keyboardShortcut": "ctrl+r",
  "welcomeMessage": "Ready to review your code!"
}
```

Rule:

- Create agent files only where official repo-level format/path is documented.
- Agent instructions should reference canonical skills instead of duplicating content.

---

## Example E: MCP Conversion

Source:

- Intent: "agent can use filesystem MCP server".

Targets:

| IDE | Action | Path/Format |
|---|---|---|
| VS Code | Create workspace MCP config | `.vscode/mcp.json` → `{ "servers": { ... } }` |
| Codex | Add to project config | `.codex/config.toml` → `[mcp_servers.<name>]` |
| OpenCode | Add to project config | `opencode.json(c)` → `{ "mcp": { ... } }` |
| **Claude Code** | **Create `.mcp.json`** at project root for team; personal: `claude mcp add --scope user` | `.mcp.json` → `{ "mcpServers": { ... } }` (team-shared, commit to VCS) |
| Antigravity | Configure via IDE MCP Store | Document manual steps |
| Kiro | Add inline to agent JSON or shared config | Agent JSON `mcpServers` (per-agent), `~/.kiro/settings/mcp.json` (global), `<cwd>/.kiro/settings/mcp.json` (workspace) + `includeMcpJson: true` |
| Qoder | Add to settings | Qoder settings `mcpServers` JSON |

### Kiro MCP inline example

```json
{
  "name": "my-agent",
  "description": "Agent with filesystem access",
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "env": {},
      "timeout": 30000
    }
  },
  "tools": ["read", "write", "@filesystem"]
}
```

Rule:

- MCP config stays in IDE-native MCP config system, not in generic markdown agent files.
- Exception: Kiro supports inline MCP in agent JSON, which is the officially documented approach.
- For shared MCP servers across Kiro agents, use `~/.kiro/settings/mcp.json` (global) or `<cwd>/.kiro/settings/mcp.json` (workspace) and set `"includeMcpJson": true` in the agent JSON.

---

## Example F: Workflow/Hook → IDE Formats

Source:

- Canonical workflow: "on agent start, collect git status and recent changes."

Targets:

| IDE | Action | Path/Format |
|---|---|---|
| VS Code | Encode as handoffs in agent file | `.agent.md` `handoffs:` frontmatter |
| Codex | N/A — embed in AGENTS.md or skill | `AGENTS.md` or skill |
| OpenCode | N/A — embed in agent/mode system prompt | `.opencode/agents/<name>.md` or `.opencode/modes/<name>.md` |
| **Claude Code** | **Configure in `.claude/settings.json`** or inline in skill/agent frontmatter | `.claude/settings.json` `hooks:` key; or `hooks:` in skill YAML frontmatter |
| Antigravity | Create workflow file | `.agent/workflows/<name>.md` |
| Kiro | Configure hooks in agent JSON | `hooks: { agentSpawn: [...], stop: [...] }` |
| Qoder | N/A — embed in agent behavior | `.qoder/agents/<name>.md` |
| Qwen Code | N/A — embed in subagent behavior | `.qwen/agents/<name>.md` |

### Claude Code hooks example (settings.json)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "git status --porcelain && git log --oneline -5"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-bash.sh",
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
          { "type": "command", "command": "uv run pytest --tb=short" }
        ]
      }
    ]
  }
}
```

### Kiro hooks example (lifecycle events)

```json
{
  "hooks": {
    "agentSpawn": [
      { "command": "git status --porcelain" },
      { "command": "git log --oneline -5" }
    ],
    "userPromptSubmit": [
      { "command": "ls -la" }
    ],
    "preToolUse": [
      {
        "matcher": "execute_bash",
        "command": "{ echo \"$(date) - Bash:\"; cat; } >> /tmp/audit.log"
      }
    ],
    "postToolUse": [
      { "matcher": "fs_write", "command": "cargo fmt --all" }
    ],
    "stop": [
      { "command": "uv run pytest" }
    ]
  }
}
```

Hook lifecycle events:

- `agentSpawn`: runs when agent starts
- `userPromptSubmit`: runs when user sends a message
- `preToolUse`: runs before a tool executes (can block with `matcher`)
- `postToolUse`: runs after a tool completes (can auto-format with `matcher`)
- `stop`: runs when agent completes

Rule:

- Use hooks for deterministic automation; use agent instructions for flexible behavior.
- `preToolUse` is the only blocking hook — use it for audit or safety gates.

---

## Example G: Tool Permissions → IDE Formats

Source:

- Intent: "reviewer agent has read-only access, no editing or command execution."

Targets:

| IDE | Action | Format |
|---|---|---|
| VS Code | List only read tools in agent frontmatter | `tools: ["codebase", "search", "usages"]` |
| Codex | Configure approval mode | `suggest` mode in `.codex/config.toml` |
| OpenCode | Disable write tools in agent/mode frontmatter | `tools: { read: true, grep: true, glob: true, edit: false, write: false, bash: false }` |
| **Claude Code** | **Set `tools:` allowlist or `disallowedTools:` denylist** in agent frontmatter | `tools: Read, Grep, Glob` (allowlist) or `disallowedTools: Write, Edit` (denylist) |
| Antigravity | IDE-controlled | Workflow scope limits |
| Kiro | Configure tools and allowedTools in agent JSON | `"tools": ["read", "shell"], "allowedTools": ["read"], "toolsSettings": { "shell": { "allowedCommands": ["grep", "find"] } }` |
| Qoder | List tools in frontmatter | `tools: Read, Grep, Glob` |
| Qwen Code | List tools in frontmatter | `tools:\n  - Read\n  - Grep\n  - Glob` |

Rule:

- Apply least-privilege principle: enable only tools required for the task.
- For review agents, always disable `edit`, `write`, and `bash`/`shell` unless explicitly needed.

---

## Dedup Exceptions

Create IDE-specific duplicates only when one of these is true:

- The IDE does not support canonical path.
- The IDE requires additional frontmatter/schema fields not accepted by canonical file.
- The artifact provides genuinely IDE-exclusive behavior (e.g., Kiro lifecycle hooks, VS Code handoffs).

When an exception is used, add a short note in project docs:

- Why duplication exists.
- Which file is canonical source-of-truth.
- How to keep artifacts semantically aligned.
