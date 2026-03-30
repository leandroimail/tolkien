# AI IDE Multi-Target Setup

This repository follows a **canonical-first** strategy for AI artifacts.

## Table of Contents

- [Canonical defaults](#canonical-defaults)
- [Current repository structure](#current-repository-structure)
  - [Canonical shared](#canonical-shared)
  - [VS Code / GitHub Copilot](#vs-code--github-copilot)
  - [OpenAI Codex (CLI + IDE)](#openai-codex-cli--ide)
  - [OpenCode](#opencode)
  - [Google Antigravity](#google-antigravity)
  - [Kiro](#kiro)
  - [Qoder](#qoder)
  - [Qwen Code](#qwen-code)
  - [Claude Code](#claude-code)
- [What each IDE loads in this project](#what-each-ide-loads-in-this-project)
- [Canonical-first deduplication policy](#canonical-first-deduplication-policy)
- [Dedup status in this repository](#dedup-status-in-this-repository)
- [Official references](#official-references)

## Canonical defaults

- Canonical rules: `AGENTS.md` (preserved exactly as requested)
- Canonical skills: `.agents/skills/<skill>/SKILL.md`

Use IDE-specific folders only for capabilities that cannot be expressed by canonical files.

## Current repository structure

### Canonical shared

- `AGENTS.md`
- `.agents/skills/multi-ide-artifacts/` (master skill)

### VS Code / GitHub Copilot

- `.github/instructions/python.instructions.md`

### OpenAI Codex (CLI + IDE)

- Reuses `AGENTS.md`
- Reuses `.agents/skills/*/SKILL.md`
- No repo-specific custom-agent file format is used

### OpenCode

- `opencode.jsonc`

### Google Antigravity

- `.agent/rules/workspace-rules.md`
- `.agent/workflows/pair-review-workflow.md`
- `.agent/skills/multi-ide-artifacts/` (skill copy — IDE does not read `.agents/skills/`)

### Kiro

- `.kiro/steering/product.md`
- `.kiro/steering/testing.md`
- `.kiro/hooks/README.md`
- `.kiro/skills/multi-ide-artifacts/` (skill copy — IDE does not read `.agents/skills/`)
- `.kiro/agents/*.json` (custom agents with full config)

### Qoder

- `.qoder/rules/project-rules.md`
- `.qoder/agents/multi-ide-artifacts.md`
- `.qoder/skills/multi-ide-artifacts/`

### Qwen Code

- `.qwen/agents/multi-ide-artifacts.md`
- `.qwen/skills/multi-ide-artifacts/`

### Claude Code

- `.claude/CLAUDE.md` → contains only `@AGENTS.md`
- `.claude/skills/multi-ide-artifacts/` (skill copy — IDE does not read `.agents/skills/`)
- `.claude/agents/` (custom subagents)
- `.claude/settings.json` (hooks config)
- `.mcp.json` (project-shared MCP, if applicable)

## What each IDE loads in this project

## 1) VS Code (GitHub Copilot)

- Rules/instructions:
  - `AGENTS.md` (always-on shared policy)
  - `.github/instructions/*.instructions.md` for scoped deltas (for example Python-only)
- Skills:
  - `.agents/skills/*/SKILL.md` (canonical)
- Prompts/slash:
  - `.github/prompts/*.prompt.md`
- Agents/subagents/modes:
  - `.github/agents/*.agent.md`
- Tools:
  - Agent tool list in `.agent.md` frontmatter
- MCP:
  - Workspace: `.vscode/mcp.json` (optional, not committed currently)

## 2) OpenAI Codex (CLI + IDE UI/Extension)

- Rules/instructions:
  - `AGENTS.md` (directory chain behavior)
- Skills:
  - `.agents/skills/*/SKILL.md`
- Prompts/slash:
  - Repo-level custom prompt files are not the preferred pattern
- Agents/subagents/modes:
  - No validated repo-level custom-agent file format currently adopted
- Tools:
  - Tool policy and approvals through Codex config/runtime
- MCP:
  - `.codex/config.toml` (project when trusted) or `~/.codex/config.toml`

## 3) OpenCode (opencode.ai)

- Rules/instructions:
  - `AGENTS.md`
  - `opencode.jsonc` for config (without duplicate instruction injection)
- Skills:
  - `.agents/skills/*/SKILL.md` (canonical)
- Prompts/slash:
  - `.opencode/commands/*.md`
- Agents/subagents/modes:
  - `.opencode/agents/*.md`
  - `.opencode/modes/*.md`
- Tools:
  - tool toggles in mode/agent frontmatter and config
- MCP:
  - `opencode.json` or `opencode.jsonc` under `mcp`

## 4) Google Antigravity

- Rules/instructions:
  - `.agent/rules/*.md`
- Skills:
  - `.agent/skills/*/SKILL.md`
- Prompts/slash:
  - workflow invocation model
- Workflows/hooks/steering:
  - `.agent/workflows/*.md`
- Agents/subagents/modes:
  - No separate repo-level agent file format currently validated
- Tools:
  - controlled by IDE workflow/runtime
- MCP:
  - via Antigravity MCP integration/store flow (workspace-level config path depends on product flow)

## 5) Kiro

- Rules/instructions:
  - `.kiro/steering/*.md` (with `inclusion: always|fileMatch|manual|auto` frontmatter)
  - `AGENTS.md` compatibility (always included, no inclusion modes)
  - Agent JSON `prompt` field (per-agent behavioral instructions, supports inline text or `file://` URI)
- Skills:
  - `.kiro/skills/*/SKILL.md`
- Prompts/slash:
  - Agent JSON `prompt` + `keyboardShortcut` for quick invocation
  - `/agent <name>` slash command in CLI
  - Steering with `inclusion: manual` for on-demand content
  - Steering with `inclusion: auto` for description-matched content
- Workflows/hooks/steering:
  - `.kiro/steering/*.md` (markdown steering files with inclusion modes)
  - Agent JSON `hooks` with lifecycle events: `agentSpawn`, `userPromptSubmit`, `preToolUse` (blocking), `postToolUse`, `stop`
  - Hook config: `command` (required), `matcher` (optional for preToolUse/postToolUse)
- Agents/subagents/modes:
  - `.kiro/agents/*.json` (full-featured JSON custom agents)
  - Fields: `name`, `description`, `prompt`, `mcpServers`, `tools`, `allowedTools`, `toolAliases`, `toolsSettings`, `resources`, `hooks`, `includeMcpJson`, `model`, `keyboardShortcut`, `welcomeMessage`
- Tools:
  - `tools`: array of available tool IDs (built-in + MCP with `@server` prefix, `*` for all, `@builtin` for all built-in)
  - `allowedTools`: whitelist of permitted tools (supports glob patterns)
  - `toolAliases`: rename tools for convenience
  - `toolsSettings`: per-tool config (allowed paths, allowed shell commands, denied commands)
- Resources:
  - `file://` — loaded into context at startup
  - `skill://` — progressive disclosure (metadata at startup, full content on demand)
  - `knowledgeBase` — indexed searchable documentation with `source`, `name`, `description`, `indexType`, `autoUpdate`
- MCP:
  - Agent JSON `mcpServers` (per-agent inline, with `command`, `args`, `env`, `timeout`)
  - `~/.kiro/settings/mcp.json` (global shared across agents)
  - `<cwd>/.kiro/settings/mcp.json` (workspace shared)
  - `includeMcpJson: true` in agent JSON to inherit shared servers
  - Kiro MCP IDE settings flow

## 6) Qoder

- Rules/instructions:
  - `.qoder/rules/*`
  - `AGENTS.md` for Qoder Action
  - Rule types: Always Apply, Model Decision, Specific Files (glob patterns), Apply Manually (`@rule`)
- Skills:
  - `.qoder/skills/*/SKILL.md`
- Prompts/slash:
  - `.qoder/commands/*.md`
- Agents/subagents/modes:
  - `.qoder/agents/*.md`
- Tools:
  - comma-separated tool names in agent frontmatter (e.g., `Read,Grep`)
- MCP:
  - Qoder MCP settings JSON (`mcpServers`)

## 7) Qwen Code

- Rules/instructions:
  - Subagents are used instead of global rules files
- Skills:
  - `.qwen/skills/*/SKILL.md` (or `~/.qwen/skills/`)
- Prompts/slash:
  - `.qwen/commands/*.md` (or `~/.qwen/commands/`)
- Agents/subagents/modes:
  - `.qwen/agents/*.md` (or `~/.qwen/agents/`)
- Tools:
  - YAML array under `tools:` in subagent frontmatter
- MCP:
  - `mcpServers` object in `.qwen/settings.json` or `~/.qwen/settings.json`

## 8) Claude Code (Anthropic CLI)

- Rules/instructions:
  - `CLAUDE.md` (contains only `@AGENTS.md` — all rules come from AGENTS.md)
  - `.claude/rules/*.md` for path-scoped rules only (`paths:` frontmatter)
- Skills:
  - `.claude/skills/*/SKILL.md` (adapted copy — IDE does NOT read `.agents/skills/` natively)
- Prompts/slash:
  - Skill invocation: `/skill <name>` or `@agent <name>` via agent frontmatter `skills:` preload
- Agents/subagents/modes:
  - `.claude/agents/*.md` (frontmatter: `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `isolation`)
- Hooks:
  - `.claude/settings.json` `hooks:` key (types: `command`, `http`, `prompt`, `agent`)
  - Events: `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SubagentStart`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PermissionRequest`, `FileChanged`, `Notification`, etc.
- Tools:
  - `tools:` allowlist and `disallowedTools:` denylist in agent frontmatter
  - `permissionMode`: `default` | `acceptEdits` | `dontAsk` | `bypassPermissions` | `plan`
- MCP:
  - `.mcp.json` (project root, team-shared, committed to VCS)
  - `~/.claude.json` (user/local scope)
  - CLI: `claude mcp add [--scope local|project|user] <name> -- <cmd>`

## Canonical-first deduplication policy

1. Keep one always-on shared rule source per IDE.
2. Prefer `.agents/skills` whenever the IDE supports it.
3. Do not duplicate canonical policy in IDE-specific always-on files.
4. Create IDE-specific agent files only where repo-level format is officially supported.
5. Keep MCP configuration in the IDE-native MCP config location.

## Dedup status in this repository

- `AGENTS.md` is the canonical shared rule baseline.
- `.agents/skills` is used as canonical skills for VS Code, Codex, and OpenCode.
- `.github/skills` was intentionally not created.
- `.github/copilot-instructions.md` was intentionally not created to avoid duplicating `AGENTS.md`.
- OpenCode does not duplicate canonical instructions in config-level instruction arrays.
- IDE-specific agent files reference the canonical review skill to reduce duplicated checklist text.
- Claude Code uses `CLAUDE.md` containing only `@AGENTS.md` — no Claude-specific rules below the import.
- Claude Code requires a skill copy at `.claude/skills/` since it does not read `.agents/skills/` natively.

## Official references

- VS Code custom instructions: <https://code.visualstudio.com/docs/copilot/customization/custom-instructions>
- VS Code prompt files: <https://code.visualstudio.com/docs/copilot/customization/prompt-files>
- VS Code agent skills: <https://code.visualstudio.com/docs/copilot/customization/agent-skills>
- VS Code custom agents: <https://code.visualstudio.com/docs/copilot/customization/custom-agents>
- VS Code agent tools: <https://code.visualstudio.com/docs/copilot/agents/agent-tools>
- VS Code MCP servers: <https://code.visualstudio.com/docs/copilot/customization/mcp-servers>
- Codex AGENTS: <https://developers.openai.com/codex/guides/agents-md/>
- Codex slash commands: <https://developers.openai.com/codex/cli/slash-commands/>
- Codex skills: <https://developers.openai.com/codex/skills/>
- Codex MCP: <https://developers.openai.com/codex/mcp/>
- OpenCode rules: <https://opencode.ai/docs/rules/>
- OpenCode config: <https://opencode.ai/docs/config/>
- OpenCode commands: <https://opencode.ai/docs/commands/>
- OpenCode agents: <https://opencode.ai/docs/agents/>
- OpenCode modes: <https://opencode.ai/docs/modes/>
- OpenCode tools: <https://opencode.ai/docs/tools/>
- OpenCode MCP servers: <https://opencode.ai/docs/mcp-servers/>
- Antigravity rules/workflows: <https://antigravity.google/docs/rules-workflows>
- Antigravity skills: <https://antigravity.google/docs/skills>
- Antigravity MCP: <https://antigravity.google/docs/mcp>
- Kiro custom agents config: <https://kiro.dev/docs/cli/custom-agents/configuration-reference>
- Kiro agent examples: <https://kiro.dev/docs/cli/custom-agents/examples>
- Kiro steering: <https://kiro.dev/docs/steering/>
- Kiro skills: <https://kiro.dev/docs/skills/>
- Kiro slash commands: <https://kiro.dev/docs/chat/slash-commands/>
- Kiro hooks: <https://kiro.dev/docs/hooks/>
- Kiro MCP: <https://kiro.dev/docs/mcp/>
- Qoder rules: <https://docs.qoder.com/user-guide/rules>
- Qoder subagent: <https://docs.qoder.com/en/cli/user-guide/subagent>
- Qoder skills: <https://docs.qoder.com/cli/Skills>
- Qoder commands: <https://docs.qoder.com/en/cli/user-guide/command>
- Qoder action: <https://docs.qoder.com/cli/qoder-action>
- Qoder tools: <https://docs.qoder.com/user-guide/chat/tools>
- Qoder MCP: <https://docs.qoder.com/user-guide/chat/model-context-protocol>
- Claude Code memory/CLAUDE.md: <https://code.claude.com/docs/en/memory>
- Claude Code skills: <https://code.claude.com/docs/en/skills>
- Claude Code agents/subagents: <https://code.claude.com/docs/en/sub-agents>
- Claude Code hooks: <https://code.claude.com/docs/en/hooks>
- Claude Code MCP: <https://code.claude.com/docs/en/mcp>
- Claude Code .claude directory: <https://code.claude.com/docs/en/claude-directory>
