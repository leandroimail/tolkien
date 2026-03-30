#!/usr/bin/env bash
# Shared dependency helpers for LaTeX skill scripts.
# This file is meant to be sourced by the wrappers in this directory.

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "This helper is meant to be sourced, not executed directly." >&2
  exit 1
fi

if [[ -n "${LATEX_SKILL_DEPS_LOADED:-}" ]]; then
  return 0
fi
LATEX_SKILL_DEPS_LOADED=1

_latex_is_darwin() {
  [[ "$(uname -s 2>/dev/null)" == "Darwin" ]]
}

_latex_prepend_path() {
  local dir="$1"

  [[ -d "$dir" ]] || return 0

  case ":${PATH:-}:" in
    *":${dir}:"*) return 0 ;;
  esac

  PATH="$dir:${PATH:-}"
}

_brew_post_texlive() {
  if ! _latex_is_darwin; then
    return 0
  fi

  if [[ -x /usr/libexec/path_helper ]]; then
    eval "$(/usr/libexec/path_helper -s 2>/dev/null)" || true
  fi

  local candidate
  for candidate in \
    /Library/TeX/texbin \
    /usr/local/texlive/*/bin/universal-darwin \
    /opt/homebrew/texlive/*/bin/universal-darwin
  do
    _latex_prepend_path "$candidate"
  done

  export PATH
}

detect_pkg_manager() {
  if command -v brew &>/dev/null; then
    echo "brew"
  elif command -v apt-get &>/dev/null; then
    echo "apt"
  elif command -v dnf &>/dev/null; then
    echo "dnf"
  elif command -v apk &>/dev/null; then
    echo "apk"
  elif command -v pacman &>/dev/null; then
    echo "pacman"
  else
    echo "unknown"
  fi
}

print_install_help() {
  local package="${1:-}"

  case "$package" in
    texlive)
      cat >&2 <<'EOF'
  macOS:          brew install --cask basictex
  Debian/Ubuntu:  sudo apt-get install texlive-latex-extra texlive-fonts-recommended texlive-binaries texlive-extra-utils
  Fedora/RHEL:    sudo dnf install texlive-scheme-medium
  Alpine:         sudo apk add texlive
  Arch:           sudo pacman -S texlive-most
EOF
      ;;
    poppler)
      cat >&2 <<'EOF'
  macOS:          brew install poppler
  Debian/Ubuntu:  sudo apt-get install poppler-utils
  Fedora/RHEL:    sudo dnf install poppler-utils
  Alpine:         sudo apk add poppler-utils
  Arch:           sudo pacman -S poppler
EOF
      ;;
    chktex)
      cat >&2 <<'EOF'
  macOS:          brew install chktex
  Debian/Ubuntu:  sudo apt-get install chktex
  Fedora/RHEL:    sudo dnf install chktex
  Alpine:         sudo apk add chktex
  Arch:           sudo pacman -S chktex
EOF
      ;;
    detex)
      cat >&2 <<'EOF'
  macOS:          brew install --cask basictex
  Debian/Ubuntu:  sudo apt-get install texlive-extra-utils
  Fedora/RHEL:    sudo dnf install texlive-scheme-medium
  Alpine:         sudo apk add texlive
  Arch:           sudo pacman -S texlive-most
EOF
      ;;
    poppler-utils)
      print_install_help poppler
      ;;
    *)
      cat >&2 <<'EOF'
  Install the missing LaTeX package using your system package manager.
EOF
      ;;
  esac
}

_install_with_brew() {
  local package="$1"

  case "$package" in
    texlive|basictex|detex)
      if command -v pdflatex &>/dev/null; then
        return 0
      fi

      if brew list --cask basictex &>/dev/null; then
        brew reinstall --cask basictex
      else
        brew install --cask basictex
      fi

      _brew_post_texlive

      if command -v pdflatex &>/dev/null; then
        return 0
      fi

      echo "Error: BasicTeX was installed but pdflatex is still unavailable." >&2
      return 1
      ;;
    poppler|chktex)
      brew install "$package"
      ;;
    *)
      brew install "$package"
      ;;
  esac
}

_install_with_apt() {
  local package="$1"
  local -a packages=()

  case "$package" in
    texlive)
      packages=(
        texlive-latex-base
        texlive-latex-recommended
        texlive-latex-extra
        texlive-fonts-recommended
        texlive-binaries
        texlive-extra-utils
      )
      ;;
    poppler)
      packages=(poppler-utils)
      ;;
    chktex)
      packages=(chktex)
      ;;
    detex)
      packages=(texlive-extra-utils)
      ;;
    *)
      packages=("$package")
      ;;
  esac

  if ! sudo -n true &>/dev/null; then
    echo "Error: sudo is required to install $package on apt-based systems." >&2
    return 1
  fi

  sudo -n apt-get update
  sudo -n apt-get install -y "${packages[@]}"
}

_install_with_dnf() {
  local package="$1"
  local -a packages=()

  case "$package" in
    texlive)
      packages=(texlive-scheme-medium texlive-collection-latexextra)
      ;;
    poppler)
      packages=(poppler-utils)
      ;;
    chktex)
      packages=(chktex)
      ;;
    detex)
      packages=(texlive-scheme-medium)
      ;;
    *)
      packages=("$package")
      ;;
  esac

  if ! sudo -n true &>/dev/null; then
    echo "Error: sudo is required to install $package on dnf-based systems." >&2
    return 1
  fi

  sudo -n dnf install -y "${packages[@]}"
}

_install_with_apk() {
  local package="$1"
  local -a packages=()

  case "$package" in
    texlive)
      packages=(texlive)
      ;;
    poppler)
      packages=(poppler-utils)
      ;;
    chktex)
      packages=(chktex)
      ;;
    detex)
      packages=(texlive)
      ;;
    *)
      packages=("$package")
      ;;
  esac

  if ! sudo -n true &>/dev/null; then
    echo "Error: sudo is required to install $package on apk-based systems." >&2
    return 1
  fi

  sudo -n apk add --no-cache "${packages[@]}"
}

_install_with_pacman() {
  local package="$1"
  local -a packages=()

  case "$package" in
    texlive)
      packages=(texlive-basic texlive-latexextra texlive-fontsextra texlive-bibtexextra)
      ;;
    poppler)
      packages=(poppler)
      ;;
    chktex)
      packages=(chktex)
      ;;
    detex)
      packages=(texlive-basic)
      ;;
    *)
      packages=("$package")
      ;;
  esac

  if ! sudo -n true &>/dev/null; then
    echo "Error: sudo is required to install $package on pacman-based systems." >&2
    return 1
  fi

  sudo -n pacman -S --noconfirm "${packages[@]}"
}

run_pkg_install() {
  local package="$1"

  case "$(detect_pkg_manager)" in
    brew)
      _install_with_brew "$package"
      ;;
    apt)
      _install_with_apt "$package"
      ;;
    dnf)
      _install_with_dnf "$package"
      ;;
    apk)
      _install_with_apk "$package"
      ;;
    pacman)
      _install_with_pacman "$package"
      ;;
    *)
      echo "Error: No supported package manager found for installing $package." >&2
      return 1
      ;;
  esac
}

install_packages() {
  local package status=0

  for package in "$@"; do
    if ! run_pkg_install "$package"; then
      status=1
    fi
  done

  return "$status"
}

# Apply local PATH fixes immediately so wrappers can find TeX tools.
_brew_post_texlive
