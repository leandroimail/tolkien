# Security Checklist for Agent Skills

> Security review procedures for creating and auditing Agent Skills.
> Based on [Anthropic Enterprise Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
> and [Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

## Table of Contents

- [Risk Tier Assessment](#risk-tier-assessment)
- [Pre-Deployment Review Checklist](#pre-deployment-review-checklist)
- [External Skill Audit Checklist](#external-skill-audit-checklist)
- [Script Security Rules](#script-security-rules)
- [Credential Management](#credential-management)
- [Network Security](#network-security)
- [Trust Hierarchy](#trust-hierarchy)

## Risk Tier Assessment

Evaluate each Skill against these risk indicators before deployment:

| Risk Indicator | What to Look For | Concern Level |
|---|---|---|
| **Code execution** | Scripts in `*.py`, `*.sh`, `*.js` | 🔴 High: scripts run with full environment access |
| **Instruction manipulation** | Directives to ignore safety rules, hide actions, alter behavior conditionally | 🔴 High: can bypass security controls |
| **MCP server references** | Instructions referencing MCP tools (`ServerName:tool_name`) | 🔴 High: extends access beyond the Skill |
| **Network access** | URLs, API endpoints, `fetch`, `curl`, `requests` calls | 🔴 High: potential data exfiltration |
| **Hardcoded credentials** | API keys, tokens, passwords in Skill files or scripts | 🔴 High: secrets exposed in Git and context |
| **File system scope** | Paths outside Skill directory, broad globs, path traversal (`../`) | 🟡 Medium: may access unintended data |
| **Tool invocations** | Instructions directing Claude to use bash, file operations | 🟡 Medium: review what operations are performed |

## Pre-Deployment Review Checklist

Complete ALL checks before deploying any Skill:

### Content Review

- [ ] Read all files in the Skill directory: SKILL.md, references, scripts.
- [ ] Verify instructions match the Skill's stated purpose.
- [ ] Check for directives that tell Claude to:
  - [ ] Ignore safety rules.
  - [ ] Hide actions from users.
  - [ ] Exfiltrate data through responses.
  - [ ] Alter behavior based on specific inputs.

### Scripts Review

- [ ] Scripts only perform operations described in SKILL.md.
- [ ] No unexpected network calls (`http`, `requests.get`, `urllib`, `curl`, `fetch`).
- [ ] No access to environment variables or credentials beyond what's needed.
- [ ] Error handling does not leak sensitive information.
- [ ] Dependencies are documented and trustworthy.

### Credential Review

- [ ] No hardcoded API keys, tokens, or passwords.
- [ ] Credentials use environment variables or secure credential stores.
- [ ] No `echo $API_KEY` or similar credential exposure in scripts.

### Network Review

- [ ] All external URLs point to expected domains.
- [ ] No data exfiltration patterns (read sensitive data → send externally).
- [ ] Network access is documented in `compatibility` field if required.

### File Access Review

- [ ] File paths stay within the Skill directory and project scope.
- [ ] No path traversal attacks (`../../sensitive-file`).
- [ ] File access patterns match the Skill's stated purpose.

## External Skill Audit Checklist

Before installing Skills from external sources:

- [ ] **Source reputation**: Is the author/organization trusted?
- [ ] **Read the entire SKILL.md**: Understand all instructions before installing.
- [ ] **Inspect all scripts**: Read every script file for suspicious commands.
- [ ] **Check for network calls**: Search for URLs, API calls, fetch/curl commands.
- [ ] **Verify no credential access**: Search for API key, token, or env var access.
- [ ] **Test in sandbox**: Run scripts in an isolated environment first.
- [ ] **Review dependencies**: Check that all referenced packages are legitimate.
- [ ] **Check external URLs**: Verify all URLs point to expected domains.

### Trust Hierarchy

| Source | Trust Level | Action Required |
|---|---|---|
| Skills you created yourself | ✅ Safe | Standard review |
| Anthropic official Skills | ✅ Safe | Standard review |
| Trusted organizations | ⚠️ Review | Content audit before use |
| Unknown sources | 🔴 Audit | Full security audit required |

## Script Security Rules

When writing scripts for Skills:

### ✅ Do

- Use specific, well-scoped file paths.
- Provide clear error messages (without leaking paths or credentials).
- Document all dependencies.
- Use proper exit codes.
- Handle edge cases gracefully.

### ❌ Don't

- Access files outside the project directory.
- Make network calls not documented in SKILL.md.
- Read environment variables beyond documented requirements.
- Write to system directories.
- Install packages without user consent.
- Execute commands received from external sources.

### Script Error Message Security

```python
# ✅ Good: specific without leaking sensitive info
print(f"Error: Field 'signature_date' not found. "
      f"Available fields: {', '.join(available_fields)}",
      file=sys.stderr)

# ❌ Bad: leaks file paths
print(f"Error: Cannot read /Users/john/.ssh/id_rsa",
      file=sys.stderr)
```

## Credential Management

### Rules

1. **Never commit credentials** to version-controlled files.
2. **Use environment variables** for API keys and tokens.
3. **Reference secure stores** for complex credential management.
4. **Document required credentials** in SKILL.md or `compatibility` field.

### Example

```markdown
## Prerequisites

Set the following environment variables:

```bash
export DATABASE_URL="your-database-url"
export API_KEY="your-api-key"
```

Do not hardcode these values in any file.

```

## Network Security

### External URL Risks

Skills that reference external URLs carry elevated risk. If the content at
the target URL changes, the Skill's behavior can be compromised.

**Mitigation strategies:**

1. **Bundle static resources** in `assets/` instead of fetching from URLs.
2. **Pin versions** when referencing external packages or APIs.
3. **Document all external calls** in SKILL.md and `compatibility` field.
4. **Validate responses** from external services before using them.

### Disabling Suspicious Skills

```bash
# Gemini CLI
gemini skills disable suspicious-skill

# OpenAI Codex (via config.toml)
[[skills.config]]
path = "/path/to/suspicious-skill/SKILL.md"
enabled = false
```

## Sources

- <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise>
- <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
- <https://shibuiyusuke.medium.com/10-practical-techniques-for-mastering-agent-skills-in-ai-coding-agents-6070e4038cf1>
