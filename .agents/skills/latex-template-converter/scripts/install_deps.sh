#!/usr/bin/env bash
# Thin wrapper around the shared LaTeX helper used by the latex skill.

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "This helper is meant to be sourced, not executed directly." >&2
  exit 1
fi

LATEX_TEMPLATE_CONVERTER_DEPS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${LATEX_TEMPLATE_CONVERTER_DEPS_DIR}/../../latex/scripts/install_deps.sh"
unset LATEX_TEMPLATE_CONVERTER_DEPS_DIR
