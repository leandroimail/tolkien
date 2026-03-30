# Artifact Creation Guide

Step-by-step workflow for creating AI agent artifacts from scratch.
Follow this guide whenever you need to create a new artifact for one or more IDEs.

## Table of Contents

- [Phase 1: Define Intent](#phase-1-define-intent)
- [Phase 2: Create Canonical Artifact](#phase-2-create-canonical-artifact)
  - [2a. Rules → AGENTS.md](#2a-rules--agentsmd)
  - [2b. Skill → .agents/skills/](#2b-skill--agentsskills)
  - [2c. Prompt/Slash](#2c-promptslash--generic-template)
  - [2d. Workflow/Hook](#2d-workflowhook--generic-template)
  - [2e. Agent/Mode](#2e-agentmode--generic-template)
  - [2f. MCP Server](#2f-mcp-server--generic-intent)
- [Phase 3: Convert to Target IDEs](#phase-3-convert-to-target-ides)
- [Phase 4: Validate](#phase-4-validate)
- [Phase 5: Document](#phase-5-document)
- [Decision Tree (Quick Reference)](#decision-tree-quick-reference)

---

## Phase 1: Define Intent

Before creating any file, answer these questions:

1. **What type of artifact?**
   - [ ] Rules/Instructions (persistent behavior)
   - [ ] Skill (reusable task-specific capability)
   - [ ] Prompt/Slash Command (user-invokable action)
   - [ ] Workflow/Hook/Steering (lifecycle automation)
   - [ ] Agent/Subagent/Mode (specialized persona)
   - [ ] Tool Configuration (permission boundaries)
   - [ ] MCP Server (external tool integration)

2. **What is the scope?**
   - [ ] Always-on (loaded for every request)
   - [ ] Scoped (loaded for specific files/tasks)
   - [ ] Manual (user must explicitly invoke)

3. **Which IDEs must support this?**
   - [ ] VS Code (GitHub Copilot)
   - [ ] OpenAI Codex CLI + IDE
   - [ ] OpenCode (opencode.ai)
   - [ ] Claude Code (Anthropic CLI)
   - [ ] Google Antigravity
   - [ ] Kiro
   - [ ] Qoder

4. **Does a canonical equivalent already exist?**
   - Search `.agents/skills/` and `AGENTS.md` first.
   - If yes, extend or reference it — do not create from scratch.

---

## Phase 2: Create Canonical Artifact

Always create the canonical version first. This is the source of truth.

### 2a. Rules → `AGENTS.md`

If the artifact defines persistent behavior rules, add to or create `AGENTS.md` at repo root.

```markdown
# Section Title

- Rule 1: describe the behavior.
- Rule 2: describe the constraint.
- Rule 3: describe the preference.
```

**When to create a new file instead**: Only if the rules are file-scoped or domain-specific (e.g., Python-only rules). In that case, the canonical file depends on the target IDE.

### 2b. Skill → `.agents/skills/<name>/SKILL.md`

```markdown
---
name: <skill-name>
description: <1-1024 chars explaining when to use/not use this skill>
---

# Skill Title

## Purpose
What this skill does and when to use it.

## Process
1. Step one.
2. Step two.
3. Step three.

## Output
- Expected output format.
- Severity or priority scheme if applicable.
```

**Name validation rules** (enforced by Codex and OpenCode):

- 1–64 characters
- Lowercase alphanumeric with single hyphen separators
- No leading/trailing hyphens, no consecutive `--`
- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Directory name must match `name` field exactly

### 2c. Prompt/Slash → Generic Template

```markdown
---
description: <what this prompt does>
argument-hint: <optional hint for user input>
---

<Prompt body with clear instructions.>

Output:
- Expected format.
- Constraints.
```

### 2d. Workflow/Hook → Generic Template

```markdown
# Workflow Title

## Trigger
- When this runs (manual invocation, hook event, agent lifecycle).

## Steps
1. Collect context.
2. Execute core logic.
3. Produce output.

## Output
- Shape of results.
```

### 2e. Agent/Mode → Generic Template

```markdown
---
name: <agent-name>
description: <what this agent does>
tools: [<minimum required tools>]
---

You are a <role>. <Core behavioral instruction>.

Rules:
- <Constraint 1>.
- <Constraint 2>.

Output:
- <Expected output format>.
```

### 2f. MCP Server → Generic Intent

Define the intent only — actual config is always IDE-specific:

```
Server name: <name>
Purpose: <what the server provides>
Command: <executable>
Args: <arguments>
Env: <required environment variables>
```

---

## Phase 3: Convert to Target IDEs

For each target IDE, consult [CONVERSION_MATRIX.md](./CONVERSION_MATRIX.md) and follow these steps:

### 3a. Check if IDE reads canonical directly

Look at the "Quick Reference" table in CONVERSION_MATRIX.md:

- If marked ✅ → the IDE reads the canonical file. **Do not create an adapter.**
- If marked 🔄 → the IDE needs an adapted copy. Proceed to step 3b.

### 3b. Create IDE-specific adapter

Use the templates in [CANONICAL_TEMPLATES.md](./CANONICAL_TEMPLATES.md) for the target IDE:

#### VS Code (GitHub Copilot)

| Artifact | Action |
|---|---|
| Rules | Use `AGENTS.md` directly. Add `.github/instructions/*.instructions.md` only for file-scoped rules with `applyTo` glob |
| Skills | Use `.agents/skills/` directly. Do not create `.github/skills/` |
| Prompts | Create `.github/prompts/<name>.prompt.md` with VS Code frontmatter (`description`, `agent`, `model`, `tools`, `mode`) |
| Agents | Create `.github/agents/<name>.agent.md` with YAML frontmatter (`name`, `description`, `tools`, `mcp-servers`, `handoffs`) + body referencing canonical skill |
| MCP | Create `.vscode/mcp.json` with `servers` object |

#### OpenAI Codex CLI + IDE

| Artifact | Action |
|---|---|
| Rules | Use `AGENTS.md` directly. Add `AGENTS.override.md` for local overrides only |
| Skills | Use `.agents/skills/` directly. Optionally add `agents/openai.yaml` for UI metadata |
| Prompts | Create skill instead — Codex prefers skills over prompt files |
| Agents | No repo agent files — use skills to achieve agent-like behavior |
| MCP | Add `[mcp_servers.<name>]` to `.codex/config.toml` |

#### OpenCode (opencode.ai)

| Artifact | Action |
|---|---|
| Rules | Use `AGENTS.md` directly. Do not duplicate in `opencode.json(c)` |
| Skills | Use `.agents/skills/` directly. Configure permissions in `opencode.json` if needed |
| Prompts | Create `.opencode/commands/<name>.md` with `description` and optional `agent` frontmatter |
| Agents | Create `.opencode/agents/<name>.md` with tool toggles (`read`, `grep`, `glob`, `edit`, `write`, `bash`) |
| Modes | Create `.opencode/modes/<name>.md` with `model`, `prompt` (path to system prompt), and tool config |
| MCP | Add to `opencode.json(c)` under `mcp` key |

#### Google Antigravity

| Artifact | Action |
|---|---|
| Rules | Convert to `.agent/rules/<name>.md` |
| Skills | Copy to `.agent/skills/<name>/SKILL.md` |
| Prompts | Create `.agent/workflows/<name>.md` (workflow-style invocation) |
| Agents | No distinct agent file — use rules + skills + workflows |
| MCP | Configure via IDE MCP Store; document manual steps only |

#### Kiro

| Artifact | Action |
|---|---|
| Rules | Convert to `.kiro/steering/<name>.md` with `inclusion: always` frontmatter (or `fileMatch`, `manual`, `auto` as needed) |
| Skills | Copy to `.kiro/skills/<name>/SKILL.md` |
| Prompts | Create agent JSON with `prompt` field (inline or `file://` URI) + optional `keyboardShortcut`; or steering with `inclusion: auto` |
| Agents | Create `.kiro/agents/<name>.json` with full config (see template) |
| Hooks | Configure `hooks` object in agent JSON with lifecycle events (`command` required, `matcher` optional) |
| MCP | Add `mcpServers` to agent JSON (per-agent) or `~/.kiro/settings/mcp.json` (global) / `<cwd>/.kiro/settings/mcp.json` (workspace) + `includeMcpJson: true` |

#### Qoder

| Artifact | Action |
|---|---|
| Rules | Convert to `.qoder/rules/<name>.md`; `Agents.md` is supported for Qoder Action |
| Skills | Copy to `.qoder/skills/<name>/SKILL.md` |
| Prompts | Create `.qoder/commands/<name>.md` and invoke via `/command-name` |
| Agents | Create `.qoder/agents/<name>.md` with `name`, `description`, `tools` frontmatter |
| MCP | Configure in Qoder `mcpServers` settings JSON |

#### Qwen Code

| Artifact | Action |
|---|---|
| Rules | N/A — Embed directly into a subagent if necessary |
| Skills | Copy to `.qwen/skills/<name>/SKILL.md` |
| Prompts | Create `.qwen/commands/<name>.md` and invoke via `/command-name` |
| Agents | Create `.qwen/agents/<name>.md` with `name`, `description`, `tools` frontmatter |
| MCP | Configure in Qwen Code `mcpServers` in `settings.json` |

#### Claude Code

| Artifact | Action |
|---|---|
| Rules | Create `CLAUDE.md` containing **only** `@AGENTS.md` (single line) — all rules live in AGENTS.md as the single source of truth; use `.claude/rules/*.md` with `paths:` exclusively for path-scoped rules that cannot go in AGENTS.md |
| Skills | Copy to `.claude/skills/<name>/SKILL.md` (Claude Code does not read `.agents/skills/` natively); include all subdirectories recursively |
| Prompts/Commands | Create `.claude/skills/<name>/SKILL.md` with `disable-model-invocation: true` para user-triggered-only; use `$ARGUMENTS` / `$N` para parâmetros |
| Agents/Subagents | Create `.claude/agents/<name>.md` com YAML frontmatter + markdown body como system prompt; use `skills:` para preload; `tools:` allowlist ou `disallowedTools:` denylist |
| Hooks | Configure `hooks:` key em `.claude/settings.json` (project) ou `~/.claude/settings.json` (user); ou embutir `hooks:` inline no YAML frontmatter de skills/agents |
| MCP | Para team-shared: criar `.mcp.json` na raiz do projeto; para pessoal: `claude mcp add --scope user`; para agent-only: inline `mcpServers:` no agent frontmatter |

---

## Phase 4: Validate

Run this checklist after creating all files:

### Deduplication checks

- [ ] No two always-on files inject the same policy for the same IDE
- [ ] Canonical artifacts exist before any adapter
- [ ] IDE-specific files contain only IDE-specific deltas
- [ ] Agent files reference canonical skills instead of copying content
- [ ] MCP is configured only in native IDE config locations

### Path validation

- [ ] Every path is officially documented for the target IDE
- [ ] `name` fields match directory names for all `SKILL.md` files
- [ ] Name follows validation regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- [ ] No symlinks (unless Codex, which explicitly supports them)
- [ ] No secret material in version-controlled files

### Quick verification commands

```bash
# Inventory all artifact files
find . -maxdepth 4 -type f \( -name "*.md" -o -name "*.json" -o -name "*.toml" -o -name "*.jsonc" \) \
  | grep -E '\.(agent|agents|github|opencode|kiro|qoder|vscode|codex)' | sort

# Check for duplicate instruction text
rg -l "code review|security|test coverage" .agent .agents .github .opencode .kiro .qoder

# Validate SKILL.md frontmatter
rg -n "^---$|name:|description:" .agents .agent .kiro .opencode .github .qoder
```

---

## Phase 5: Document

Record what was created in the project documentation:

1. **Update `AI_IDE_SETUP.md`** — add new paths to the repository structure section
2. **Update dedup status** — note any new deduplication exceptions and why
3. **Record assumptions** — if any IDE capability was uncertain, mark as `not validated`

---

## Decision Tree (Quick Reference)

```
Is this a persistent behavior rule?
  YES → Add to AGENTS.md → Convert per Matrix 1
  NO ↓

Is this a reusable task capability?
  YES → Create .agents/skills/<name>/SKILL.md → Convert per Matrix 2
  NO ↓

Is this a user-invokable action?
  YES → Create canonical prompt → Convert per Matrix 3
  NO ↓

Is this a lifecycle automation?
  YES → Create canonical workflow → Convert per Matrix 4
  NO ↓

Is this a specialized persona?
  YES → Create canonical agent template → Convert per Matrix 5
  NO ↓

Is this a tool permission boundary?
  YES → Define policy → Convert per Matrix 6
  NO ↓

Is this an external tool integration?
  YES → Define MCP intent → Convert per Matrix 7
```
