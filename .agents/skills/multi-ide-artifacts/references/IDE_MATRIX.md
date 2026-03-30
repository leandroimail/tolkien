# IDE Matrix

This matrix defines canonical-first behavior and the validated repo-level paths for each IDE.
Always consult this before creating or modifying artifacts.

## Table of Contents

- [Artifact support](#artifact-support)
- [Agent, tools, and MCP support map](#agent-tools-and-mcp-support-map)
- [Canonical priority rules](#canonical-priority-rules)
- [Official references](#official-references)

## Artifact support

| IDE | Rules/Instructions | Skills | Prompts/Slash | Workflows/Hooks/Steering | Agents/Subagents/Modes |
|---|---|---|---|---|---|
| VS Code (Copilot) | `AGENTS.md`, `.github/instructions/*.instructions.md` (scoped via `applyTo`), optional `.github/copilot-instructions.md` (always-on, legacy) | `.agents/skills/*/SKILL.md` (also supports `.github/skills`, avoid duplication) | `.github/prompts/*.prompt.md` (frontmatter: `description`, `argument-hint`, `agent`, `model`, `tools`, `mode`) | `handoffs` in custom agent frontmatter (label, agent, prompt, send) | `.github/agents/*.agent.md` (YAML frontmatter: `name`, `description`, `tools`, `mcp-servers`, `agents`, `handoffs`, `model`, `target`, `argument-hint`) |
| OpenAI Codex CLI + IDE | `AGENTS.md` chain (walks up from CWD to repo root, + `AGENTS.override.md` for local overrides) | `.agents/skills/*/SKILL.md` (progressive disclosure: metadata loaded first, full content on demand; supports `agents/openai.yaml` for UI metadata, invocation policy, tool dependencies) | `$skill-name` explicit invocation or `/skills` to browse; repo-level prompt files not preferred | No native repo workflow/hook files | No validated repo custom-agent file format; use skills to achieve agent-like behavior |
| OpenCode | `AGENTS.md`, `.opencode/rules/*.md`, `opencode.json(c)` config instructions | `.agents/skills/*/SKILL.md`, `.opencode/skills/*/SKILL.md`, `.claude/skills/*/SKILL.md`; skill permissions (`allow`/`deny`/`ask`) configurable per pattern in `opencode.json` | `.opencode/commands/*.md` (frontmatter: `description`, `agent`) | No separate steering/hook layer in repo | `.opencode/agents/*.md` (frontmatter: `description`, `mode`, `tools`, `permission`), `.opencode/modes/*.md` (frontmatter: `model`, `prompt`, `tools`) |
| **Claude Code** | `CLAUDE.md` or `.claude/CLAUDE.md` — must contain **only** `@AGENTS.md` to centralize all rules in AGENTS.md as single source of truth; `.claude/rules/*.md` only for path-scoped rules (frontmatter `paths:`) with no AGENTS.md equivalent | `.claude/skills/*/SKILL.md` (project); `~/.claude/skills/*/SKILL.md` (user); also `.claude/commands/<name>.md` (legacy, skills take precedence); frontmatter: `name`, `description`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context`, `agent`, `hooks` | `/<skill-name>` or `/<command-name>`; auto-invoked by Claude when description matches | `.claude/settings.json` or `~/.claude/settings.json` under `hooks` key; also inline in skill/agent YAML frontmatter `hooks:`; events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `Stop`, `SubagentStop`, `SubagentStart`, `TaskCompleted`, `TaskCreated`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `FileChanged`, `Notification`, plus others | `.claude/agents/<name>.md` (project); `~/.claude/agents/<name>.md` (user); frontmatter: `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `isolation` |
| Google Antigravity | `.agent/rules/*.md` | `.agent/skills/*/SKILL.md` | Workflow invocation model | `.agent/workflows/*.md` (trigger + steps) | No validated distinct repo agent file format |
| Kiro | `.kiro/steering/*.md` (frontmatter: `inclusion: always\|fileMatch\|manual\|auto`), `AGENTS.md` compatibility (always included) | `.kiro/skills/*/SKILL.md` | Agent JSON `prompt` field + `/agent` slash command + optional `keyboardShortcut`; steering with `inclusion: auto` (description-matched) | Agent JSON `hooks` object with lifecycle events: `agentSpawn`, `userPromptSubmit`, `preToolUse` (blocking), `postToolUse`, `stop`; plus `.kiro/steering/*.md` | `.kiro/agents/*.json` (fields: `name`, `description`, `prompt`, `mcpServers`, `tools`, `allowedTools`, `toolAliases`, `toolsSettings`, `resources`, `hooks`, `includeMcpJson`, `model`, `keyboardShortcut`, `welcomeMessage`) |
| Qoder | `.qoder/rules/*` (types: Always Apply, Model Decision, Specific Files, Apply Manually), `Agents.md` for Qoder Action | `.qoder/skills/*/SKILL.md` (frontmatter: `name`, `description`) | `.qoder/commands/*.md` (frontmatter: `name`, `description`) | Qoder Action (`.github/workflows/*`) | `.qoder/agents/*.md` (frontmatter: `name`, `description`, `tools`) |
| Qwen Code | N/A (use Subagents) | `.qwen/skills/*/SKILL.md` (frontmatter: `name`, `description`) | `.qwen/commands/*.md` (frontmatter: `description`, body vars `{{args}}`) | None | `.qwen/agents/*.md` (frontmatter: `name`, `description`, `tools`) |

## Agent, tools, and MCP support map

| IDE | Agent file format/path | Tool configuration format | MCP config path/format | Skills usable by agents |
|---|---|---|---|---|
| VS Code (Copilot) | `.github/agents/*.agent.md` (YAML frontmatter + markdown body) | Agent frontmatter `tools`: array of tool names, tool sets, MCP server wildcards (`serverName/*`), extension tools | `.vscode/mcp.json` (workspace) or user profile; format: `{ "servers": {}, "inputs": [] }` | Yes — canonical `.agents/skills` supported |
| OpenAI Codex CLI + IDE | No validated repo custom-agent file | Approval mode in config (`suggest`/`auto-edit`/`full-auto`); tool policy through runtime; skill tool dependencies in `agents/openai.yaml` | `.codex/config.toml` `[mcp_servers.<name>]` (project) or `~/.codex/config.toml` (user) | Yes — canonical `.agents/skills` with progressive disclosure |
| OpenCode | `.opencode/agents/*.md` (YAML frontmatter), `.opencode/modes/*.md` | Per-tool booleans: `read`, `grep`, `glob`, `edit`, `write`, `bash`, `skill`; per-skill permissions: `allow`/`deny`/`ask`; per-agent overrides in frontmatter | `opencode.json` or `opencode.jsonc` under `mcp` key | Yes — canonical `.agents/skills`, `.opencode/skills`, `.claude/skills` |
| **Claude Code** | `.claude/agents/<name>.md` (project); `~/.claude/agents/<name>.md` (user); YAML frontmatter + markdown body (system prompt) | Frontmatter `tools:` (allowlist, comma-separated) or `disallowedTools:` (denylist); `permissionMode`: `default\|acceptEdits\|dontAsk\|bypassPermissions\|plan`; `mcpServers:` (inline or string reference) | `.mcp.json` (project root, team-shared, checked into VCS); `~/.claude.json` (user/local per-project); `claude mcp add [--scope local\|project\|user]`; format: `{ "mcpServers": { "<name>": { "command", "args", "env" } } }` | Yes — `.claude/skills/*/SKILL.md`; `skills:` field in subagent frontmatter for preloading |
| Google Antigravity | No distinct repo custom-agent file path validated | IDE tool control + workflow-scoped behavior | MCP Store / imported `mcp_config.json` integration path | Skills in `.agent/skills/*/SKILL.md` |
| Kiro | `.kiro/agents/*.json` (JSON config, full-featured) | `tools`: array of tool IDs (`*` for all, `@builtin` for built-in, `@server` for MCP); `allowedTools`: whitelist (glob patterns); `toolAliases`: rename tools; `toolsSettings`: per-tool config (paths, commands, denied commands); all in agent JSON | Agent JSON `mcpServers` (per-agent inline) or `~/.kiro/settings/mcp.json` (global) / `<cwd>/.kiro/settings/mcp.json` (workspace); `includeMcpJson: true` to inherit; format: `{ "<name>": { "command", "args", "env", "timeout" } }` | Skills in `.kiro/skills/*/SKILL.md`; resources support `skill://` URI for progressive disclosure |
| Qoder | `.qoder/agents/*.md` (YAML frontmatter + markdown body) | Agent frontmatter `tools:` with comma-separated tool names; local and MCP tools supported (e.g., `Read,Grep,Glob` or `*`) | Qoder MCP settings JSON (`mcpServers`); format: `{ "mcpServers": { "<name>": { "command", "args" } } }` | Yes — canonical `.agents/skills` mapped to `.qoder/skills` |

## Canonical priority rules

1. Rules: prefer `AGENTS.md` where supported; for Claude Code create `CLAUDE.md` containing **only** `@AGENTS.md` (single line) — AGENTS.md is the single source of truth; **never add rules below the import**.
2. Skills: prefer `.agents/skills` where supported; Claude Code requires a copy at `.claude/skills/`.
3. Agents: create IDE-specific agent files only where officially supported at repo level.
4. MCP: keep MCP configuration in native IDE config, not in generic markdown.
5. Remove duplicate always-on text across multiple load paths.
6. When IDE supports canonical path directly (VS Code, Codex, OpenCode for skills), do not create adapter copies.

## Official references

### VS Code (GitHub Copilot)

- Custom Instructions: <https://code.visualstudio.com/docs/copilot/customization/custom-instructions>
- Prompt Files: <https://code.visualstudio.com/docs/copilot/customization/prompt-files>
- Agent Skills: <https://code.visualstudio.com/docs/copilot/customization/agent-skills>
- Custom Agents: <https://code.visualstudio.com/docs/copilot/customization/custom-agents>
- Agent Tools: <https://code.visualstudio.com/docs/copilot/agents/agent-tools>
- MCP Servers: <https://code.visualstudio.com/docs/copilot/customization/mcp-servers>

### OpenAI Codex CLI + IDE

- AGENTS.md: <https://developers.openai.com/codex/guides/agents-md/>
- Skills: <https://developers.openai.com/codex/skills/>
- MCP: <https://developers.openai.com/codex/mcp/>
- Customization: <https://developers.openai.com/codex/concepts/customization>

### OpenCode (opencode.ai)

- Rules: <https://opencode.ai/docs/rules/>
- Skills: <https://opencode.ai/docs/skills/>
- Commands: <https://opencode.ai/docs/commands/>
- Agents: <https://opencode.ai/docs/agents/>
- Modes: <https://opencode.ai/docs/modes/>
- Tools: <https://opencode.ai/docs/tools/>
- MCP Servers: <https://opencode.ai/docs/mcp-servers/>
- Config: <https://opencode.ai/docs/config/>

### Claude Code (Anthropic CLI)

- Features overview: <https://code.claude.com/docs/en/features-overview>
- Memory/CLAUDE.md: <https://code.claude.com/docs/en/memory>
- Skills: <https://code.claude.com/docs/en/skills>
- Subagents: <https://code.claude.com/docs/en/sub-agents>
- Hooks: <https://code.claude.com/docs/en/hooks>
- MCP: <https://code.claude.com/docs/en/mcp>
- Plugins: <https://code.claude.com/docs/en/plugins>
- .claude directory: <https://code.claude.com/docs/en/claude-directory>

### Google Antigravity

- Rules/Workflows: <https://antigravity.google/docs/rules-workflows>
- Skills: <https://antigravity.google/docs/skills>
- MCP: <https://antigravity.google/docs/mcp>

### Kiro

- Custom Agents (CLI): <https://kiro.dev/docs/cli/custom-agents/configuration-reference>
- Agent Examples: <https://kiro.dev/docs/cli/custom-agents/examples>
- Skills: <https://kiro.dev/docs/skills/>
- Steering: <https://kiro.dev/docs/steering/>
- Hooks: <https://kiro.dev/docs/hooks/>
- Slash Commands: <https://kiro.dev/docs/chat/slash-commands/>
- MCP: <https://kiro.dev/docs/mcp/>

### Qoder

- Rules: <https://docs.qoder.com/user-guide/rules>
- Subagents: <https://docs.qoder.com/en/cli/user-guide/subagent>
- Skills: <https://docs.qoder.com/cli/Skills>
- Commands: <https://docs.qoder.com/en/cli/user-guide/command>
- Qoder Action: <https://docs.qoder.com/cli/qoder-action>
- Tools: <https://docs.qoder.com/user-guide/chat/tools>
- MCP: <https://docs.qoder.com/user-guide/chat/model-context-protocol>

### Standards

- Agent Skills Spec: <https://agentskills.io/specification>

### Qwen Code

- Commands: <https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/commands.md\>
- Skills: <https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/skills.md\>
- Subagents: <https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/sub-agents.md\>
- MCP: <https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/mcp.md\>
