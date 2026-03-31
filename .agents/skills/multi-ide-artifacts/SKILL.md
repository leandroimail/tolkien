---

# Virtualenv

Note: When this skill executes Python scripts, run them within the project's virtual environment.
Ative com:

```bash
source .venv/bin/activate
```

Alternatively, use `uv run python -B ...` with the `.venv` active.

name: multi-ide-artifacts
description: >
  Designs, deduplicates, and converts AI agent artifacts (rules, skills, prompts,
  workflows, agents, tools, MCP servers) across VS Code, Codex, OpenCode,
  Claude Code, Antigravity, Kiro, Qoder, and Qwen Code using a canonical-first
  strategy. Use when creating or migrating AI artifacts across multiple IDEs,
  converting artifact types between tools, wiring MCP server configs, enforcing
  cross-IDE deduplication, or auditing existing AI artifact structures in a repository.
---

# Multi-IDE Agent Artifacts

## Purpose

Build production-grade AI artifact structures for multiple IDEs and agents with minimal duplication and predictable loading behavior.

This skill is optimized for:

- Cross-IDE repositories with overlapping AI tooling.
- Token-efficiency and deterministic precedence.
- Safe migration from ad-hoc files to canonical-first structure.

## When To Use

Use this skill when you need to:

- Create or refactor AI artifact folders/files across VS Code, Codex, OpenCode, Claude Code, Antigravity, Kiro, Qoder, and Qwen Code.
- Convert one artifact type to equivalent formats in multiple IDEs.
- Create custom agents where officially supported and wire tool permissions safely.
- Integrate MCP servers per IDE with repo-safe defaults.
- Enforce deduplication and canonical priority rules.
- Produce auditable documentation of paths, precedence, and support limits.

## When Not To Use

Do not use this skill for:

- Single-IDE quick setup with no reuse goals.
- Non-versioned user-home setup only.
- Tasks that explicitly require duplicating instructions for experimentation.

## Inputs

Collect before writing files:

- Target IDEs and artifact types (see [IDE_MATRIX.md](./references/IDE_MATRIX.md) for what each IDE supports).
- Canonical policy preference: `AGENTS.md` for rules, `.agents/skills/<name>/SKILL.md` for skills.
- Existing repo inventory (run `bash scripts/inventory.sh` or the commands in [Execution Commands](#execution-commands-suggested)).
- Constraints: no symlinks, no global/home writes, preserve existing files.

## Outputs

Produce:

- Minimal, valid file set per IDE.
- Conversion map from canonical artifacts to IDE-specific artifacts.
- Deduplication report (what was not created and why).
- Compatibility matrix: type -> IDE -> path -> scope -> precedence -> notes.
- Agent/tool/MCP mapping table per IDE.
- Migration plan from existing docs/processes.

## Method

Follow this sequence exactly.

1. Discover

- Inventory repository paths first:
  - `AGENTS.md`
  - `CLAUDE.md` / `.claude/`
  - `.agents/skills/`
  - `.github/`
  - `.opencode/`
  - `.agent/`
  - `.kiro/`
  - `.qoder/`
- Detect overlapping artifacts with equivalent intent.

1. Validate from official docs

- Confirm path, format, and precedence before creating each file.
- If docs conflict or are ambiguous, choose the safest non-duplicating fallback and record the assumption.
- Prefer primary docs only.

1. Define canonical model

- Canonical rules baseline: `AGENTS.md` when IDE supports it.
- Canonical skills baseline: `.agents/skills/<name>/SKILL.md` when IDE supports it.
- IDE-specific files only for exclusive capabilities (for example, VS Code prompt files and custom agents, VS Code handoffs, OpenCode agents/modes with tool toggles, Antigravity workflows, Kiro custom agents JSON with lifecycle hooks and tool control, Kiro steering with inclusion modes (`always`/`fileMatch`/`manual`/`auto`), Qoder custom subagents, Commands, and rules, Qwen Code CLI subagents and commands, Claude Code subagents in `.claude/agents/`, hooks in `.claude/settings.json`, and path-scoped rules in `.claude/rules/*.md`).

1. Plan & Approvals

- Before generating or overwriting any artifact file across IDE directories, draft a summary migration plan.
- **Wait for the user's explicit approval** before proceeding to file creation.

1. Generate canonical artifacts first

- Create canonical rule and skill content before any adapter.
- Keep semantics stable across adapters.

1. Create IDE adapters

- Materialize only what each IDE uniquely requires.
- Avoid mirrored clones of identical instructions in multiple always-on paths.
- For agent files, keep instructions compact and reference canonical policy instead of duplicating it.
- For tool permissions, allow minimum required tools only.
- For MCP, prefer project/workspace config when supported; do not write user-home paths inside repo.

1. Run deduplication checks

- Verify no two always-on files inject the same policy text for the same IDE.
- Remove redundant files when one canonical path is sufficient.

1. Document load behavior

- For each IDE, document exactly what is loaded, from where, and with which precedence.
- For each IDE, document how agents consume tools, skills, and MCP.

## Objective Deduplication Criteria

Apply these criteria strictly.

1. Single always-on source per IDE for shared policy

- If IDE reads `AGENTS.md` as always-on and no additional behavior is needed, do not duplicate in another always-on instruction file.

1. Canonical skill source first

- If IDE supports `.agents/skills`, do not create duplicate skill trees in IDE-specific directories unless feature metadata requires it.

1. Native-only artifacts are exceptions

- Keep IDE-native prompt/command/workflow/hook/mode/agent files only when no canonical equivalent exists.

1. No dual injection

- Do not inject the same instruction text via both `AGENTS.md` and config-level instruction arrays in the same IDE unless explicitly required.

1. Scope minimization

- Prefer repo-level portable files over user-home files for shared behavior.

1. Agent declaration minimization

- Create agent files only in IDEs with validated repo-level support.
- If no validated repo-level agent format exists, document fallback and avoid speculative files.

## Path and Copying Rules

Apply these rules strictly when copying, referencing, or linking artifacts:

1. **Recursive Copying**
   - When copying a skill or other artifact, you must recursively copy the main file along with all its subdirectories and associated files.
   - Always verify that all internal references within the copied files remain correct in the new location.

2. **Relative File References**
   - All file references within Skills and other canonical artifacts must use **relative paths**, never absolute paths.

## Quality Checklist

A change is acceptable only if all checks pass.

- [ ] Every created path is officially supported.
- [ ] `name` and folder names match for every `SKILL.md`.
- [ ] Copied artifacts include all subdirectories and files recursively with verified references.
- [ ] File references in Skills and canonical artifacts use relative paths (not absolute paths).
- [ ] Canonical artifacts exist before adapters.
- [ ] No duplicated always-on instructions per IDE.
- [ ] IDE-specific files contain only IDE-specific delta.
- [ ] All artifacts are version-control friendly (no secret material).
- [ ] No symlinks.
- [ ] Documentation includes precedence and scope.
- [ ] MCP configuration paths are validated per IDE.
- [ ] Agent tool lists are least-privilege and task-focused.

## Agent, Tools, and MCP Rules

Apply this policy when adding agent capabilities.

1. Agents

- Prefer canonical behavior in `AGENTS.md` + `.agents/skills` first.
- Create IDE-native agent files only when needed to expose IDE-specific agent UX (for example slash-invokable custom agents).

1. Tools

- Enable read/search tools by default for review agents.
- Keep write/execute tools disabled unless the workflow truly requires editing or command execution.
- Record tool policy in the IDE-specific agent file only (do not duplicate in multiple config layers).

1. Skills by Agents

- Canonical skills live in `.agents/skills/<name>/SKILL.md`.
- Agent files should reference or invoke canonical skills conceptually; avoid copying full skill bodies into every agent file.
- Create IDE-local skill folders only when canonical skills are not loaded by that IDE.

1. MCP

- Configure MCP in IDE-native config files only. See [IDE_MATRIX.md](./references/IDE_MATRIX.md) → "Agent, tools, and MCP support map" for exact paths and formats per IDE.
- Never create fake MCP file names or schemas in repo.
- If workspace MCP path is unsupported/unclear for an IDE, document manual setup only.

## Artifact Templates

Use canonical templates in [CANONICAL_TEMPLATES.md](./references/CANONICAL_TEMPLATES.md).

## Conversion Rules

Use explicit conversion playbooks in [CONVERSION_PLAYBOOK.md](./references/CONVERSION_PLAYBOOK.md).

## Conversion Matrix

Use the exhaustive from/to mapping in [CONVERSION_MATRIX.md](./references/CONVERSION_MATRIX.md) for converting any artifact type across all 6 IDEs.

## Creation Guide

Follow the step-by-step workflow in [CREATION_GUIDE.md](./references/CREATION_GUIDE.md) when creating artifacts from scratch.

## IDE Capability Matrix

Use [IDE_MATRIX.md](./references/IDE_MATRIX.md) as execution truth.

## Project Baseline Reference

Use [PROJECT_CONTEXT.md](./references/PROJECT_CONTEXT.md) to align decisions with the repository baseline in `references/AI_IDE_SETUP.md`.

## Safe Fallback Policy

If any IDE capability is uncertain:

- Mark the artifact as `not validated`.
- Do not create speculative files.
- Keep canonical artifacts only.
- Document required manual follow-up.

## Execution Commands (Suggested)

Run the bundled inventory script for a full artifact scan and duplicate check:

```bash
bash scripts/inventory.sh
```

Or use these inline commands:

```bash
# List all artifact files
find . -maxdepth 4 -type f | sort

# Check for duplicate policy text across IDE dirs
rg -n "code review|security|test coverage|AGENTS.md|SKILL.md" .

# Validate SKILL.md frontmatter
rg -n "^---$|name:|description:" .agents .agent .kiro .opencode .github .qoder
```

## Security Policy

Apply when creating MCP configs, agent files, or importing external artifacts.

- [ ] No secrets or API keys committed to version-controlled files; use env vars or IDE secret inputs.
- [ ] MCP `command` values reference local executables only, not remote URLs.
- [ ] Agent `tools` lists follow least-privilege: read-only by default, write/execute only when the task requires it.
- [ ] Agent files do not echo credentials to stdout (no `echo $API_KEY` in hooks or scripts).
- [ ] External skills or agents from unknown sources are audited before use:
  - Check instructions for suspicious commands or external fetches.
  - Verify scripts in `scripts/` do not exfiltrate data.

## Final Report Template

Include these sections in your handoff:

- Research findings (official links only).
- Skill design decisions.
- Files created/updated.
- Canonical-to-IDE mapping table.
- Migration plan.
- Open risks and assumptions.
