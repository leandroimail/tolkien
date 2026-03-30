# Cross-IDE Deployment Guide for Agent Skills

> How to deploy Agent Skills across all supported IDEs.
> Based on the [Agent Skills Specification](https://agentskills.io/specification),
> [multi-ide-artifacts](../../multi-ide-artifacts/SKILL.md) skill, and
> [10 Practical Techniques blog](https://shibuiyusuke.medium.com/10-practical-techniques-for-mastering-agent-skills-in-ai-coding-agents-6070e4038cf1).

## Table of Contents

- [Supported IDEs and Paths](#supported-ides-and-paths)
- [Canonical-First Strategy](#canonical-first-strategy)
- [Workspace vs. User Scope](#workspace-vs-user-scope)
- [Deployment Methods](#deployment-methods)
- [Portability Rules](#portability-rules)
- [IDE-Specific Notes](#ide-specific-notes)
- [Environment Differences](#environment-differences)
- [Copying Rules](#copying-rules)

## Supported IDEs and Paths

### Workspace Skills (Team/Project Scope)

| IDE | Skill Path | Management |
|-----|-----------|------------|
| Claude Code | `.claude/skills/<name>/SKILL.md` | Filesystem, Plugins |
| Gemini CLI | `.gemini/skills/<name>/SKILL.md` | `/skills` command, `gemini skills` CLI |
| OpenAI Codex | `.agents/skills/<name>/SKILL.md` | `config.toml`, `$skill-creator` |
| Cursor | `.cursor/skills/<name>/SKILL.md` | Filesystem |
| Antigravity | `.agents/skills/<name>/SKILL.md` | Filesystem |
| Kiro | `.kiro/skills/<name>/SKILL.md` | Filesystem |
| Qoder | `.qoder/skills/<name>/SKILL.md` | Filesystem |

### User Skills (Personal Scope)

| IDE | Skill Path |
|-----|-----------|
| Claude Code | `~/.claude/skills/<name>/SKILL.md` |
| Gemini CLI | `~/.gemini/skills/<name>/SKILL.md` |
| OpenAI Codex | `~/.agents/skills/<name>/SKILL.md` |

### OpenAI Codex Hierarchical Scopes

| Scope | Path | Purpose |
|-------|------|---------|
| REPO (folder) | `.agents/skills/` (current directory) | Module-specific |
| REPO (root) | `$REPO_ROOT/.agents/skills/` | Repository-wide |
| USER | `$HOME/.agents/skills/` | Personal skills |
| ADMIN | `/etc/codex/skills/` | System-wide defaults |
| SYSTEM | Bundled by OpenAI | Built-in skills |

Higher scopes override lower ones.

## Canonical-First Strategy

Follow the `multi-ide-artifacts` skill's canonical-first approach:

1. **Create the canonical Skill** in `.agents/skills/<name>/` first.
2. **Copy to IDE-specific paths** only when the IDE cannot read `.agents/skills/`.
3. **Do not duplicate content** — keep adapters minimal.
4. **All IDEs that support `.agents/skills/`** share the same canonical copy.

### Which IDEs Need Separate Copies?

| IDE | Reads `.agents/skills/`? | Needs Separate Copy? |
|-----|--------------------------|---------------------|
| OpenAI Codex | ✅ Yes | No |
| Antigravity | ✅ Yes | No |
| Claude Code | ❌ No (uses `.claude/skills/`) | Yes |
| Gemini CLI | ❌ No (uses `.gemini/skills/`) | Yes |
| Cursor | ❌ No (uses `.cursor/skills/`) | Yes |
| Kiro | ❌ No (uses `.kiro/skills/`) | Yes |
| Qoder | ❌ No (uses `.qoder/skills/`) | Yes |

## Workspace vs. User Scope

### Decision Guide

| Criterion | Workspace Skill | User Skill |
|---|---|---|
| Other team members will use it | ✅ Yes | ❌ No |
| Needs Git tracking | ✅ Yes | ⚠️ Maybe |
| Project-specific | ✅ Yes | ❌ No |
| Used across all projects | ❌ No | ✅ Yes |
| Personal preference | ❌ No | ✅ Yes |

### Workspace Skills are best for

- Team coding conventions (PR review, commit message formats).
- Project configurations (database schemas, API specs).
- Shared workflows (deployment, testing procedures).

### User Skills are best for

- Personal coding style preferences.
- Frequently used snippets and boilerplate.
- Personal development environment settings.

## Deployment Methods

### Method 1: Canonical Copy (Recommended)

Keep the Skill source in one location and copy to each IDE's path:

```bash
# Create canonical skill
mkdir -p .agents/skills/my-skill

# Copy to IDE-specific paths (recursive)
cp -r .agents/skills/my-skill .claude/skills/my-skill
cp -r .agents/skills/my-skill .gemini/skills/my-skill
cp -r .agents/skills/my-skill .cursor/skills/my-skill
cp -r .agents/skills/my-skill .kiro/skills/my-skill
cp -r .agents/skills/my-skill .qoder/skills/my-skill
```

### Method 2: Symlinks

Use symlinks to avoid maintaining multiple copies:

```bash
# Keep source in one location
mkdir -p skills/my-skill

# Create symlinks
ln -s ../../skills/my-skill .claude/skills/my-skill
ln -s ../../skills/my-skill .gemini/skills/my-skill
ln -s ../../skills/my-skill .agents/skills/my-skill
```

**Note:** Some IDEs or environments may not support symlinks. Test before relying on this approach.

### Method 3: Gemini CLI Link Command

```bash
gemini skills link ./skills/my-skill --scope workspace
```

### Method 4: OpenAI Codex Skill Creator

```bash
# Inside Codex
$skill-creator
```

## Portability Rules

Follow these rules to write Skills that work across all IDEs:

### 1. Use Forward Slashes in Paths

```markdown
# ✅ Good: works everywhere
scripts/helper.py
references/guide.md

# ❌ Bad: Windows only
scripts\helper.py
references\guide.md
```

### 2. Avoid Tool-Specific Features in Instructions

```markdown
# ✅ Good: generic
Run the following script:
python scripts/validate.py input.json

# ❌ Bad: tool-specific
Use Claude Code's Read tool to read references/guide.md
```

### 3. Use the `compatibility` Field for Requirements

```yaml
---
name: docker-deploy
description: Builds and deploys Docker containers.
compatibility: Requires git, docker, jq. Network access required.
---
```

### 4. Use Relative Paths for All File References

```markdown
# ✅ Good: relative path
See [REFERENCE.md](references/REFERENCE.md)

# ❌ Bad: absolute path
See [REFERENCE.md](/Users/john/.agents/skills/my-skill/references/REFERENCE.md)
```

### 5. Bundle Resources for Offline Environments

Some environments (Claude API) have no network access. Bundle required resources in `assets/` when possible.

## IDE-Specific Notes

### Claude Code

- Supports plugins for Skill installation: `/plugin marketplace add anthropics/skills`
- Skills can be installed from the official Anthropic Skills repository.

### Gemini CLI

- Has built-in Skill management CLI: `gemini skills list`, `gemini skills link`, `gemini skills disable`.
- Supports `/skills` command in interactive mode.

### OpenAI Codex

- Has built-in `$skill-creator` for interactive Skill scaffolding.
- Has `$skill-installer` for external Skill installation.
- Supports hierarchical scoping (REPO → USER → ADMIN → SYSTEM).
- Skills can be disabled via `config.toml`:

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

### Cursor

- Reads Skills from `.cursor/skills/` directory.
- Filesystem-based management only.

### Antigravity

- Shares `.agents/skills/` with OpenAI Codex.
- Has native workflow support that extends beyond standard Skills.

### Kiro

- Uses `.kiro/skills/` directory.
- Supports steering files with inclusion modes (`always`/`fileMatch`/`manual`/`auto`).
- Supports custom agents with lifecycle hooks.

## Environment Differences

| IDE/Platform | Network | Package Installation |
|---|---|---|
| Claude Code | Full access | Possible (local recommended) |
| Claude API | None | Not possible (pre-installed only) |
| Claude.ai | Configurable | Possible from npm/PyPI |
| Gemini CLI | Full access | Possible |
| OpenAI Codex | Configurable | Configurable |
| Cursor | Full access | Possible |
| Antigravity | Full access | Possible |

**Strategy:** For maximum portability, assume no network access. Bundle required resources. Use the `compatibility` field to document requirements.

## Copying Rules

When copying a Skill to IDE-specific directories:

1. **Copy recursively** — include SKILL.md and all subdirectories (`scripts/`, `references/`, `assets/`).
2. **Verify references** — ensure all internal file references remain valid after copying.
3. **Use relative paths** — all file references must be relative, not absolute.
4. **Match directory names** — the directory name must match the `name` field in frontmatter.
5. **No symlink fallback** — if symlinks are not supported, use full copies.

```bash
# Correct: recursive copy
cp -r .agents/skills/my-skill .claude/skills/my-skill

# Verify references
grep -r "references/" .claude/skills/my-skill/SKILL.md
grep -r "scripts/" .claude/skills/my-skill/SKILL.md
```

## Sources

- <https://agentskills.io/specification>
- <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>
- <https://shibuiyusuke.medium.com/10-practical-techniques-for-mastering-agent-skills-in-ai-coding-agents-6070e4038cf1>
