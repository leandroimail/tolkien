# Conversion Matrix

This document provides an exhaustive from/to mapping for every artifact type across all supported IDEs.
Use this matrix as the single source of truth for converting any canonical artifact to IDE-specific equivalents.

## Table of Contents

- [How to read this matrix](#how-to-read-this-matrix)
- [Matrix 1: Rules / Instructions](#matrix-1-rules--instructions)
- [Matrix 2: Skills (SKILL.md)](#matrix-2-skills-skillmd)
- [Matrix 3: Prompts / Slash Commands](#matrix-3-prompts--slash-commands)
- [Matrix 4: Workflows / Hooks / Steering](#matrix-4-workflows--hooks--steering)
- [Matrix 5: Agents / Subagents / Modes](#matrix-5-agents--subagents--modes)
- [Matrix 6: Tools / Tool Permissions](#matrix-6-tools--tool-permissions)
- [Matrix 7: MCP Server Configuration](#matrix-7-mcp-server-configuration)
- [Quick Reference: Canonical → IDE Path Lookup](#quick-reference-canonical--ide-path-lookup)

## How to read this matrix

- **Canonical** = the source artifact, always created first.
- Each IDE column shows the **target path/format** and whether it is **direct** (IDE reads canonical), **adapted** (new file needed), or **N/A** (IDE has no equivalent).
- When the IDE reads the canonical path directly, do **not** create an adapter unless IDE-exclusive metadata is required.

---

## Matrix 1: Rules / Instructions

| Dimension | Canonical | VS Code (Copilot) | Codex CLI + IDE | OpenCode | **Claude Code** | Antigravity | Kiro | Qoder | Qwen Code |
|---|---|---|---|---|---|---|---|--- |---|
| **Primary path** | `AGENTS.md` | `AGENTS.md` (always-on) | `AGENTS.md` (directory chain) | `AGENTS.md` | `CLAUDE.md` or `.claude/CLAUDE.md` (auto-loaded every session; directory chain) | `.agent/rules/*.md` | `.kiro/steering/*.md` (`inclusion: always`) | `.qoder/rules/*.md` | N/A |
| **Load behavior** | — | Auto-loaded for every request | Walks up from CWD to repo root | Auto-loaded | Auto-loaded; walks up from CWD; `@path` import syntax supported | Auto-loaded from workspace | Loaded per `inclusion` field | Auto-loaded | N/A |
| **Scoped rules** | N/A | `.github/instructions/*.instructions.md` (`applyTo` glob) | `AGENTS.override.md` (local override) | `.opencode/rules/*.md` or config `instructions` | `.claude/rules/*.md` with `paths:` frontmatter for file/directory scoping (glob patterns); user-level: `~/.claude/rules/` | Additional `.agent/rules/*.md` files | Additional steering files with `inclusion: manual`, `fileMatch` (glob-triggered), or `auto` (description-matched) | Additional `.qoder/rules/*.md` files (types: Always Apply, Model Decision, Specific Files, Apply Manually) | N/A |
| **Global fallback** | N/A | `.github/copilot-instructions.md` (always-on, legacy) | `~/.codex/config.toml` instructions | `~/.config/opencode/rules/` | `~/.claude/rules/` (user-level); managed org: `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | N/A | Agent JSON `prompt` field | N/A | N/A |
| **Conversion rule** | Create first | Use directly; add `.instructions.md` only for file-scoped deltas | Use directly; use override for local domains | Use directly; do not duplicate in config `instructions` | Create `CLAUDE.md` containing **only** `@AGENTS.md` (single line); all rules live in `AGENTS.md` as the single source of truth; use `.claude/rules/*.md` only for path-scoped rules with no AGENTS.md equivalent | Convert content to `.agent/rules/*.md` | Convert to steering with `inclusion: always`; or embed in agent JSON `prompt` | Convert to `.qoder/rules/*.md`; create `Agents.md` if Qoder Action PR review applies | N/A |
| **Dedup check** | — | Do not also create `.github/copilot-instructions.md` with same content | Do not duplicate in override unless truly local | Do not duplicate in `opencode.json(c)` instructions | `CLAUDE.md` must not repeat any content from `AGENTS.md`; it only imports it — **never add rules below `@AGENTS.md`** | — | Do not duplicate between steering and agent JSON prompt | Do not duplicate between AGENTS.md and `.qoder/rules/` | Do not duplicate in `.qwen/` and `~/.qwen/` |

---

## Matrix 2: Skills (SKILL.md)

| Dimension | Canonical | VS Code (Copilot) | Codex CLI + IDE | OpenCode | **Claude Code** | Antigravity | Kiro | Qoder | Qwen Code |
|---|---|---|---|---|---|---|---|--- |---|
| **Primary path** | `.agents/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` (direct) | `.agents/skills/<name>/SKILL.md` (direct) | `.agents/skills/<name>/SKILL.md` (direct) | `.claude/skills/<name>/SKILL.md` (project) | `.agent/skills/<name>/SKILL.md` | `.kiro/skills/<name>/SKILL.md` | `.qoder/skills/<name>/SKILL.md` | `.qwen/skills/<name>/SKILL.md` (direct) |
| **Alt paths** | — | `.github/skills/<name>/SKILL.md` (avoid) | User: `~/.agents/skills/`, Admin: `/etc/codex/skills/` | `.opencode/skills/`, `.claude/skills/`, global `~/.config/opencode/skills/` | User: `~/.claude/skills/<name>/SKILL.md`; legacy: `.claude/commands/<name>.md` (single-file, skills take precedence) | — | — | `~/.qoder/skills/` | `~/.qwen/skills/` |
| **Required frontmatter** | `name`, `description` | `name`, `description` | `name`, `description` | `name`, `description` | `name`, `description` | `name`, `description` | `name`, `description` | `name`, `description` | `name`, `description` |
| **Name validation** | dir name = `name` field | Same | Same + 1-64 chars, lowercase, `^[a-z0-9]+(-[a-z0-9]+)*$` | Same + 1-64 chars, `^[a-z0-9]+(-[a-z0-9]+)*$`, dir must match | Same regex; dir must match `name` | Same | Same | N/A | N/A |
| **Extra metadata** | — | — | `agents/openai.yaml` (display_name, icon, brand_color, default_prompt, allow_implicit_invocation, tool dependencies) | Permissions: `allow`/`deny`/`ask` per skill pattern in `opencode.json` | `disable-model-invocation: true` (user-only); `user-invocable: false` (Claude-only); `allowed-tools:` (allowlist); `context: fork` (run in subagent); `agent:` (agent type); `hooks:` (lifecycle hooks in frontmatter); `` !`cmd` `` (shell inject at load time) | — | — | — | — |
| **Invocation** | — | Automatic by Copilot | Explicit: `$skill-name` or `/skills`; Implicit: matched by description | Agent calls `skill({ name: "..." })` tool | `/<name>` explicit or auto by Claude based on description; `$ARGUMENTS` / `$N` for positional args; enable extended thinking with `ultrathink` keyword | Auto by workspace | Auto by workspace | `/skill-name` explicitly | `/skill-name` explicitly |
| **Conversion rule** | Create first | Use directly (do not create `.github/skills/` duplicate) | Use directly; add `openai.yaml` only for UI/policy metadata | Use directly; configure permissions in `opencode.json` only if needed | **Copy to `.claude/skills/<name>/SKILL.md`** (Claude Code does not read `.agents/skills/` natively); include all subdirectories and supporting files | Copy to `.agent/skills/<name>/SKILL.md` | Copy to `.kiro/skills/<name>/SKILL.md` | Copy to `.qoder/skills/<name>/SKILL.md` | Use canonical directory `.qwen/skills/` natively |
| **Dedup check** | — | Do not also create `.github/skills/` | — | Do not create `.opencode/skills/` if canonical works | Do not duplicate between `.claude/skills/` and `.claude/commands/`; skills take precedence over commands with same name | — | — | Do not duplicate in `.qoder/` and `~/.qoder/` | Do not duplicate in `.qwen/` and `~/.qwen/` |

---

## Matrix 3: Prompts / Slash Commands

| Dimension | Canonical | VS Code (Copilot) | Codex CLI + IDE | OpenCode | **Claude Code** | Antigravity | Kiro | Qoder | Qwen Code |
|---|---|---|---|---|---|---|---|--- |---|
| **Path** | (template) | `.github/prompts/<name>.prompt.md` | N/A (use skill `$name` invocation) | `.opencode/commands/<name>.md` | `.claude/skills/<name>/SKILL.md` or `.claude/commands/<name>.md` (legacy) | `.agent/workflows/<name>.md` | Agent JSON `prompt` field + `/agent` slash | `.qoder/commands/<name>.md` | `.qwen/commands/<name>.md` |
| **Format** | Markdown + frontmatter | Frontmatter: `description`, `argument-hint`, `agent`, `model`, `tools`, `mode` + body | — | Frontmatter: `description`, `agent` + body | Frontmatter: `name`, `description`, `disable-model-invocation`, `allowed-tools` + body with `$ARGUMENTS` | Plain markdown with trigger/steps | JSON config with `prompt`, `welcomeMessage` | Frontmatter: `name`, `description` + Markdown body | Frontmatter: `description` + Markdown body |
| **Invocation** | — | Dropdown or `#<name>` in chat | `$skill-name` or `/skills` to browse | `/command-name` in chat | `/<name>` in chat; or auto by Claude | Workflow invocation in IDE | `/agent <name>` in CLI; keyboard shortcut in IDE | `/command-name` in chat | `/command-name` in chat |
| **Conversion rule** | Define intent | Create `.prompt.md` with agent/tool hints | Create skill instead (Codex prefers skills over prompt files) | Create `.opencode/commands/<name>.md` | Create `.claude/skills/<name>/SKILL.md` with `disable-model-invocation: true` for user-triggered-only; `$ARGUMENTS` for parameters | Create `.agent/workflows/<name>.md` | Embed in agent JSON `prompt` + configure `keyboardShortcut` | Create `.qoder/commands/<name>.md` with frontmatter | Create `.qwen/commands/<name>.md` with frontmatter |
| **Dedup check** | — | — | Skill already covers behavior | — | Prefer skill over `.claude/commands/`; skill takes precedence when same name | — | Do not also create steering file with same content | — | Do not duplicate in `.qwen/` and `~/.qwen/` |

---

## Matrix 4: Workflows / Hooks / Steering

| Dimension | Canonical | VS Code (Copilot) | Codex CLI + IDE | OpenCode | **Claude Code** | Antigravity | Kiro | Qoder | Qwen Code |
|---|---|---|---|---|---|---|---|--- |---|
| **Path** | (template) | Agent `.agent.md` `handoffs` field | N/A | N/A | `.claude/settings.json` `hooks` key (project) or `~/.claude/settings.json` (user); also inline in skill/agent YAML frontmatter `hooks:` | `.agent/workflows/<name>.md` | Agent JSON `hooks` object | N/A | N/A |
| **Hook types** | — | `handoffs` (label, agent, prompt, send) for agent transitions | — | — | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `Stop`, `SubagentStop`, `SubagentStart`, `TaskCompleted`, `TaskCreated`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `FileChanged`, `Notification`, and others | Manual trigger / workflow steps | `agentSpawn`, `userPromptSubmit`, `preToolUse`, `postToolUse`, `stop` | — | — |
| **Hook config** | — | Frontmatter in `.agent.md` | — | — | JSON: `{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "..." }] }`; types: `command`, `http`, `prompt`, `agent`; `if` field for conditional filtering | Steps in markdown body | JSON: `command` (required), `matcher` (optional, for preToolUse/postToolUse only) | — | — |
| **Blocking hooks** | — | N/A | — | — | `PreToolUse` can block; `PermissionRequest` can allow/deny; return JSON `{ "decision": "block" }` | N/A | `preToolUse` can block execution | — | — |
| **Conversion rule** | Define steps | Encode agent transitions as `handoffs` in `.agent.md` frontmatter | N/A — use skills or AGENTS.md | N/A — encode in agent/mode system prompt | Configure `hooks` in `.claude/settings.json`; or add `hooks:` to skill/agent frontmatter for lifecycle-scoped hooks | Create `.agent/workflows/<name>.md` with steps | Create `hooks` block in agent JSON with lifecycle events | N/A — encode in agent behavior | N/A |
| **Dedup check** | — | Do not duplicate hook logic in multiple agents | — | — | Do not configure same hook in both settings.json and skill frontmatter | — | Do not duplicate between steering and agent JSON hooks | — | — |

---

## Matrix 5: Agents / Subagents / Modes

| Dimension | Canonical | VS Code (Copilot) | Codex CLI + IDE | OpenCode | **Claude Code** | Antigravity | Kiro | Qoder | Qwen Code |
|---|---|---|---|---|---|---|---|--- |---|
| **Path** | (template) | `.github/agents/<name>.agent.md` | N/A (use skills) | `.opencode/agents/<name>.md` + `.opencode/modes/<name>.md` | `.claude/agents/<name>.md` (project); `~/.claude/agents/<name>.md` (user) | N/A (use rules + workflows) | `.kiro/agents/<name>.json` | `.qoder/agents/<name>.md` | `.qwen/agents/<name>.md` |
| **Format** | — | YAML frontmatter + markdown body | — | YAML frontmatter + markdown body | YAML frontmatter + markdown body (system prompt) | — | JSON | YAML frontmatter + markdown body | YAML frontmatter + markdown body |
| **Key fields** | `name`, `description` | `name`, `description`, `tools`, `mcp-servers`, `agents`, `handoffs`, `model`, `target`, `argument-hint` | — | `description`, `mode` (`subagent`/`primary`/`all`), `tools` (per-tool booleans incl. `skill`), `model`, `prompt` | `name`, `description`, `tools` (allowlist), `disallowedTools` (denylist), `model`, `permissionMode` (`default`/`acceptEdits`/`dontAsk`/`bypassPermissions`/`plan`), `mcpServers`, `hooks`, `maxTurns`, `skills` (preloaded), `initialPrompt`, `memory`, `isolation` (`worktree`/`none`) | — | `name`, `description`, `prompt` (inline or `file://` URI), `mcpServers`, `tools`, `allowedTools`, `toolAliases`, `toolsSettings`, `resources` (`file://`, `skill://`, `knowledgeBase`), `hooks`, `includeMcpJson`, `model`, `keyboardShortcut`, `welcomeMessage` | `name`, `description`, `tools` | `name`, `description`, `tools` |
| **Mode/subagent** | — | `agents` field for nesting | — | `mode: subagent` or `mode: primary` | Subagents inherit parent tools; `Agent(type)` syntax restricts spawnable types | — | Standalone agents invoked via `/agent` | Invoked via `/agents` UI or `@agent-name` | Invoked via `/agents` UI |
| **Conversion rule** | Define behavior | Create `.agent.md` with frontmatter + instructions body | Create skill instead; Codex has no repo agent files | Create agent `.md` and optionally mode `.md` with tool config | Create `.claude/agents/<name>.md` with YAML frontmatter + markdown body as system prompt; use `skills:` to preload canonical skills; define `hooks:` inline | Use rules + workflows to achieve agent behavior | Create `.json` agent with all config fields | Create `.md` agent with frontmatter | Create `.md` agent with frontmatter |
| **Dedup check** | — | Instructions should reference canonical skill, not copy it | — | Agent should reference canonical skill | System prompt body should reference canonical skill path, not copy content; `skills:` preloads skills cleanly | — | Use `resources` to auto-load context; reference skills | Agent should reference canonical skill | Agent should reference canonical skill |

---

## Matrix 6: Tools / Tool Permissions

| Dimension | Canonical | VS Code (Copilot) | Codex CLI + IDE | OpenCode | **Claude Code** | Antigravity | Kiro | Qoder | Qwen Code |
|---|---|---|---|---|---|---|---|--- |---|
| **Config location** | — | Agent `.agent.md` `tools` frontmatter | `.codex/config.toml` or `~/.codex/config.toml` | Agent/mode frontmatter `tools` block | Subagent/skill frontmatter `tools:` or `disallowedTools:` | IDE runtime + workflow scope | Agent JSON `tools`, `allowedTools`, `toolsSettings` | Agent `tools` frontmatter | Agent `tools` frontmatter |
| **Format** | — | Array of tool names/sets: `["codebase", "search", "serverName/*"]` | Approval mode (`suggest`/`auto-edit`/`full-auto`) + per-tool config | Per-tool booleans: `read: true`, `edit: false`, `skill: false`, etc. | `tools:` comma-separated allowlist (e.g. `Read, Grep, Glob`); `disallowedTools:` denylist; `allowed-tools:` in skill frontmatter; `permissionMode` in agent frontmatter | IDE-controlled | `tools`: array of tool IDs (`*`, `@builtin`, `@server`); `allowedTools`: whitelist (glob); `toolsSettings`: per-tool config (paths, commands, denied commands) | Comma-separated names (e.g. `Read,Grep`), default `*` | Array of tool names |
| **Granularity** | — | Tool sets, individual tools, MCP server wildcards | Global approval level | Per-tool enable/disable (incl. `skill`); per-skill permissions (`allow`/`deny`/`ask`) | Per-tool allowlist/denylist; `Agent(type)` restricts spawnable subagent types; `permissionMode` overrides session-level behavior | Workflow-level | Tool aliases, allowed commands, allowed paths, denied commands, per-tool settings | Tool name list | Tool name list |
| **Conversion rule** | Define policy | List tools in agent frontmatter; use `serverName/*` for MCP tools | Configure approval mode in config; tool access through runtime | Set tool booleans in agent/mode frontmatter | Set `tools:` allowlist or `disallowedTools:` denylist in agent frontmatter; use `allowed-tools:` in skill frontmatter for skill-scoped limits | IDE-controlled, no repo file | Configure `tools` + `allowedTools` + `toolsSettings` in agent JSON | List tools in agent frontmatter | List tools in agent frontmatter |
| **Least privilege** | — | Include only needed tools | Use `suggest` mode by default | Disable `edit`, `write`, `bash` for read-only agents | Use `tools: Read, Grep, Glob` for read-only subagents; omit `Agent` from tools to prevent subagent spawning | — | Use `allowedTools` to whitelist only needed tools | List only read tools for review agents | List only read tools for review agents |

---

## Matrix 7: MCP Server Configuration

| Dimension | Canonical | VS Code (Copilot) | Codex CLI + IDE | OpenCode | **Claude Code** | Antigravity | Kiro | Qoder | Qwen Code |
|---|---|---|---|---|---|---|---|--- |---|
| **Path** | — | `.vscode/mcp.json` (workspace) | `.codex/config.toml` (project) or `~/.codex/config.toml` (user) | `opencode.json` or `opencode.jsonc` under `mcp` key | `.mcp.json` (project root, team-shared, version-controlled ✅); `~/.claude.json` (user/local per-project); inline in agent frontmatter `mcpServers:` (agent-scoped) | MCP Store / imported config | Agent JSON `mcpServers` object (inline) or `~/.kiro/settings/mcp.json` (global) / `<cwd>/.kiro/settings/mcp.json` (workspace); `includeMcpJson: true` to inherit | `mcpServers` in settings JSON | `mcpServers` JSON settings in `.qwen/settings.json` |
| **Format** | — | JSON: `{ "servers": { "<name>": { "command", "args" } } }` | TOML: `[mcp_servers.<name>]` with `command`, `args` | JSON(C): `{ "mcp": { "<name>": { "type", "command" } } }` | JSON: `{ "mcpServers": { "<name>": { "command", "args", "env" } } }`; CLI: `claude mcp add [--scope local\|project\|user] [--transport stdio\|http\|sse] <name> -- <cmd>` | IDE UI flow | JSON: `{ "mcpServers": { "<name>": { "command", "args", "env", "timeout" } } }` | JSON: `{ "mcpServers": { "<name>": { "command", "args" } } }` | JSON: `{ "mcpServers": { "<name>": { "command", "args" } } }` |
| **Scope** | — | Workspace (`.vscode/`) or user profile | Project (`.codex/`) or user (`~/.codex/`) | Project root config file | `local` (default, private, `~/.claude.json` per-project); `project` (`.mcp.json`, team-shared); `user` (`~/.claude.json` global mcpServers); precedence: local > project > user | Workspace via IDE | Per-agent (inline) or shared | Settings-level | Settings-level |
| **Inputs/secrets** | — | `"inputs": []` for API keys with variable substitution | Env vars or config values | Env vars | `"env": { "KEY": "${VAR}" }` with env var expansion in `.mcp.json`; IDE prompts approval before using project-scoped servers | IDE-managed | `"env": { "KEY": "$VAR" }` per server | Settings-managed | Settings-managed |
| **Conversion rule** | Define server intent | Create `.vscode/mcp.json` with `servers` object | Add `[mcp_servers.<name>]` to `.codex/config.toml` | Add to `opencode.json(c)` `mcp` key | For team-shared: create `.mcp.json` at project root; for personal: `claude mcp add --scope user`; for agent-only: add inline `mcpServers:` to agent frontmatter | Configure via IDE MCP Store flow; document manual setup | Add `mcpServers` to agent JSON (per-agent) or `~/.kiro/settings/mcp.json` / `<cwd>/.kiro/settings/mcp.json` (shared); use `includeMcpJson: true` in agent JSON to inherit | Add to `mcpServers` settings JSON | Add to `mcpServers` settings JSON |
| **Dedup check** | — | Keep in `.vscode/mcp.json` only | Keep in project config only | Keep in one config file | Do not define same server in both `.mcp.json` (project) and `~/.claude.json` (local) — local takes precedence; prefer inline `mcpServers:` in agent when server is agent-specific | — | Prefer per-agent inline when agent-specific | — | — |

---

## Quick Reference: Canonical → IDE Path Lookup

Use this table for fast lookups when you know the artifact type and target IDE.

| Artifact Type | VS Code | Codex CLI | OpenCode | **Claude Code** | Antigravity | Kiro | Qoder | Qwen Code |
|---|---|---|---|---|---|--- |---|---|
| Rules (always-on) | `AGENTS.md` ✅ | `AGENTS.md` ✅ | `AGENTS.md` ✅ | `CLAUDE.md` (only `@AGENTS.md`) 🔄 | `.agent/rules/*.md` 🔄 | `.kiro/steering/*.md` 🔄 | `.qoder/rules/*.md` 🔄 | N/A 🔄 |
| Rules (scoped) | `.github/instructions/*.instructions.md` | `AGENTS.override.md` | `.opencode/rules/*.md` | `.claude/rules/*.md` (`paths:` frontmatter) | Additional rules files | Steering `inclusion: manual\|fileMatch\|auto` | Additional rules files (4 types) | N/A |
| Skills | `.agents/skills/` ✅ | `.agents/skills/` ✅ | `.agents/skills/` ✅ | `.claude/skills/` 🔄 | `.agent/skills/` 🔄 | `.kiro/skills/` 🔄 | `.qoder/skills/` 🔄 | `.qwen/skills/` ✅ |
| Prompts/Slash | `.github/prompts/*.prompt.md` | `$skill` invocation | `.opencode/commands/*.md` | `.claude/skills/<name>/` + `/<name>` | `.agent/workflows/*.md` | Agent JSON + `/agent` | `.qoder/commands/*.md` 🔄 | `.qwen/commands/*.md` 🔄 |
| Agents | `.github/agents/*.agent.md` | N/A (use skills) | `.opencode/agents/*.md` | `.claude/agents/*.md` | N/A (use rules+wf) | `.kiro/agents/*.json` | `.qoder/agents/*.md` | `.qwen/agents/*.md` |
| Modes | N/A | N/A | `.opencode/modes/*.md` | N/A | N/A | N/A | N/A | N/A |
| Workflows/Hooks | `handoffs` in `.agent.md` | N/A | N/A | `.claude/settings.json` `hooks:` | `.agent/workflows/*.md` | `hooks` in agent JSON | N/A | N/A |
| Tool config | `.agent.md` `tools:` | `.codex/config.toml` | Agent/mode `tools:` | Agent `tools:` / `disallowedTools:` | IDE-controlled | Agent JSON `tools`+`allowedTools` | Agent `tools:` | Agent `tools:` |
| MCP config | `.vscode/mcp.json` | `.codex/config.toml` | `opencode.json(c)` `mcp:` | `.mcp.json` (project) / `~/.claude.json` (user/local) | IDE MCP Store | Agent JSON `mcpServers` | `mcpServers` JSON | `mcpServers` JSON |

**Legend**: ✅ = reads canonical directly | 🔄 = requires adapted copy
