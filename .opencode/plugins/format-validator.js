// tolkien — always-on format/data validation plugin for OpenCode.
//
// Mirrors the Claude Code and Codex hooks. Provides ACTIVE ENFORCEMENT on the
// tool-after path (a broken edit is rejected by throwing) and an advisory pass when
// the session goes idle. The self-guarding script only acts on a recently modified
// paper project, so it is silent in unrelated sessions.
//
//   tool.execute.after  -> runs the hook with --enforce; a non-zero exit (BLOCKING
//                          markdown findings) throws, which blocks/surfaces the error.
//   event/session.idle  -> advisory only (a thrown error on idle cannot roll back
//                          already-completed work, so it just reports).
//
// Deeper BLOCKING enforcement (Data Integrity G4.5, LaTeX compile, DOCX schema)
// remains the pipeline's Output Format Gate / academic-data-validator, which are
// harness-agnostic.
//
// Docs: https://opencode.ai/docs/plugins/
// NOTE: current OpenCode loads plugins from .opencode/plugins/ (PLURAL). If your
// installed version uses the singular .opencode/plugin/, move this file there —
// a wrong directory is a silent no-op. Verify against your opencode version.

const HOOK = ".agents/skills/academic-format-validator/scripts/hook_format_check.sh";

export const FormatValidator = async ({ $, directory }) => {
  return {
    // PostToolUse-equivalent: ACTIVE ENFORCEMENT after each edit/write/bash tool.
    "tool.execute.after": async (input) => {
      if (["edit", "write", "bash"].includes(input.tool)) {
        try {
          await $`bash ${HOOK} --enforce`.cwd(directory);
        } catch (e) {
          // Non-zero exit (exit 2 = BLOCKING findings) throws here -> reject the edit.
          throw new Error(`tolkien format validation blocked this change:\n${e?.stderr ?? e}`);
        }
      }
    },
    // Stop-equivalent: advisory final pass when the session goes idle.
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        try {
          await $`bash ${HOOK}`.cwd(directory);
        } catch (e) {
          console.error(`[tolkien] format check could not run: ${e?.stderr ?? e}`);
        }
      }
    },
  };
};
