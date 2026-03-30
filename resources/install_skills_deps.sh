#!/bin/bash
# Install dependencies for AAPMAS skills in a virtual environment
# Generates and sets up the environment to run the agent skills.

# Exit immediately if a command exits with a non-zero status
set -e

PROJECT_DIR="$(pwd)"
RESOURCES_DIR="$PROJECT_DIR/resources"
VENV_DIR="$PROJECT_DIR/.venv"

echo "================================================================="
echo "  Starting Dependency Installation for AAPMAS Agent Skills       "
echo "================================================================="
echo "Project Directory: $PROJECT_DIR"
echo "Virtual Environment: $VENV_DIR"
echo ""

# 1. Check for Homebrew (macOS package manager)
echo "[1/4] Checking System Dependencies (macOS)..."
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew not found. Please install Homebrew (https://brew.sh/) to install system dependencies."
    echo "Skipping system package installation."
else
    echo "Updating Homebrew..."
    brew update > /dev/null 2>&1
    
    echo "Installing required system packages (Tesseract, Poppler)..."
    brew install tesseract poppler
    
    echo "Installing TinyTeX (fast, lightweight LaTeX distribution)..."
    if ! command -v pdflatex &> /dev/null && [ ! -d "$HOME/Library/TinyTeX" ] && [ ! -d "$HOME/.TinyTeX" ]; then
        curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh
    fi

    # Determine TinyTeX bin dir (macOS default is ~/Library/TinyTeX/bin/universal-darwin)
    TINYTEX_BIN_DIR=""
    if [ -d "$HOME/Library/TinyTeX/bin/universal-darwin" ]; then
        TINYTEX_BIN_DIR="$HOME/Library/TinyTeX/bin/universal-darwin"
    elif [ -d "$HOME/.TinyTeX/bin/universal-darwin" ]; then
        TINYTEX_BIN_DIR="$HOME/.TinyTeX/bin/universal-darwin"
    elif [ -d "$HOME/.TinyTeX/bin/x86_64-darwin" ]; then
        TINYTEX_BIN_DIR="$HOME/.TinyTeX/bin/x86_64-darwin"
    elif [ -d "$HOME/.TinyTeX/bin/aarch64-darwin" ]; then
        TINYTEX_BIN_DIR="$HOME/.TinyTeX/bin/aarch64-darwin"
    fi

    if [ -n "$TINYTEX_BIN_DIR" ]; then
        echo "Updating PATH and symlinking TinyTeX to virtual environment..."
        export PATH="$TINYTEX_BIN_DIR:$PATH"
        
        # We will symlink binaries later, after .venv is created in step 3.
        # But we can install the needed LaTeX tools now using tlmgr from TinyTeX
        if command -v tlmgr &> /dev/null; then
            echo "Installing necessary LaTeX tools via tlmgr..."
            tlmgr update --self || echo "⚠️  tlmgr update failed."
            tlmgr install latexmk chktex abntex2 || echo "⚠️  tlmgr install failed."
        fi
    else
        echo "⚠️  Could not locate TinyTeX binaries. LaTeX tools might fail."
    fi

    echo "Installing LibreOffice (required by docx skill for soffice command)..."
    brew install --cask libreoffice

    echo "System packages installed successfully."
fi
echo ""

# 2. Check for Node.js / NPM (required for docx skill)
echo "[2/4] Checking Node.js and NPM..."
if ! command -v npm &> /dev/null; then
    echo "⚠️  NPM not found. Please install Node.js to use the 'docx' skill."
    if command -v brew &> /dev/null; then
        echo "Installing Node.js via Homebrew..."
        brew install node
        echo "Installing global NPM packages..."
        npm install -g docx
    fi
else
    echo "Installing global NPM packages (docx)..."
    npm install -g docx
    echo "NPM packages installed successfully."
fi
echo ""

# 3. Setting up Python Virtual Environment
echo "[3/4] Setting up Python Virtual Environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists at $VENV_DIR."
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Ensure pip is up to date
pip install --upgrade pip > /dev/null 2>&1
echo ""

if [ -n "$TINYTEX_BIN_DIR" ]; then
    echo "Symlinking TinyTeX binaries to virtual environment ($VENV_DIR/bin)..."
    for file in "$TINYTEX_BIN_DIR"/*; do
        if [ -x "$file" ] && [ ! -d "$file" ]; then
            ln -sf "$file" "$VENV_DIR/bin/$(basename "$file")"
        fi
    done
    echo "TinyTeX successfully linked."
    echo ""
fi
echo ""

# 4. Installing Python Packages
echo "[4/4] Installing Python Packages..."
echo "The following dependencies were identified across the skills:"
echo "- pyyaml (academic-prd)"
echo "- pandas, matplotlib (academic-media)"
echo "- pypdf, pdfplumber, reportlab, pillow, pytesseract, pdf2image (pdf)"
echo "- requests (academic-researcher)"
echo "- defusedxml (docx office scripts)"

# Create a temporary requirements file to install
cat << EOF > "$RESOURCES_DIR/requirements_skills.txt"
pyyaml
requests
pandas
matplotlib
pypdf
pdfplumber
reportlab
pillow
pytesseract
pdf2image
defusedxml
EOF

echo "Installing requirements via pip..."
pip install -r "$RESOURCES_DIR/requirements_skills.txt"
echo "Python dependencies installed successfully."
echo ""

echo "================================================================="
echo "  Installation Complete!                                         "
echo "================================================================="
echo "System, Node.js, and Python dependencies have been set up."
echo "Dependencies list saved to: $RESOURCES_DIR/requirements_skills.txt"
echo ""
echo "To activate the virtual environment later, run:"
echo "source .venv/bin/activate"
echo "================================================================="
