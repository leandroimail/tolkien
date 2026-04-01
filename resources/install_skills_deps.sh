#!/bin/bash
# Install dependencies for AAPMAS skills in a virtual environment
# Generates and sets up the environment to run the agent skills.
# Supports macOS (Homebrew) and Linux (apt-get).

# Exit immediately if a command exits with a non-zero status
set -e

PROJECT_DIR="$(pwd)"
RESOURCES_DIR="$PROJECT_DIR/resources"
VENV_DIR="$PROJECT_DIR/.venv"
OS_TYPE="$(uname -s)"

echo "================================================================="
echo "  Starting Dependency Installation for AAPMAS Agent Skills       "
echo "================================================================="
echo "Project Directory: $PROJECT_DIR"
echo "Virtual Environment: $VENV_DIR"
echo "Detected OS: $OS_TYPE"
echo ""

# 1. System Dependencies
echo "[1/5] Checking System Dependencies..."

if [ "$OS_TYPE" = "Darwin" ]; then
    # --- macOS (Homebrew) ---
    if ! command -v brew &> /dev/null; then
        echo "WARNING: Homebrew not found. Please install Homebrew (https://brew.sh/) to install system dependencies."
        echo "Skipping system package installation."
    else
        echo "Updating Homebrew..."
        brew update > /dev/null 2>&1

        echo "Installing required system packages (Tesseract, Poppler)..."
        brew install tesseract poppler

        echo "Installing TinyTeX (fast, lightweight LaTeX distribution)..."
        if ! command -v pdflatex &> /dev/null && [ ! -d "$HOME/Library/TinyTeX" ] && [ ! -d "$HOME/.TinyTeX" ]; then
            echo "pdflatex not found. Attempting TinyTeX installation..."
            curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh || echo "WARNING: Failed to install TinyTeX via script."
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
            echo "Updating PATH for TinyTeX..."
            export PATH="$TINYTEX_BIN_DIR:$PATH"

            for SHELL_RC in "$HOME/.zshrc" "$HOME/.zprofile" "$HOME/.bash_profile"; do
                if [ -f "$SHELL_RC" ]; then
                    if ! grep -Fq "$TINYTEX_BIN_DIR" "$SHELL_RC" 2>/dev/null; then
                        echo "# TinyTeX bin (added by install_skills_deps.sh)" >> "$SHELL_RC"
                        echo "export PATH=\"$TINYTEX_BIN_DIR:\$PATH\"" >> "$SHELL_RC"
                        echo "Added TinyTeX PATH to $SHELL_RC"
                    fi
                fi
            done

            if command -v tlmgr &> /dev/null; then
                echo "Installing necessary LaTeX tools via tlmgr..."
                tlmgr update --self || echo "WARNING: tlmgr update failed."
                tlmgr install latexmk chktex abntex2 || echo "WARNING: tlmgr install failed."
            fi
        else
            echo "WARNING: Could not locate TinyTeX binaries. LaTeX tools might fail."
        fi

        # Detect MacTeX (full) or BasicTeX and persist their texbin if present
        if [ -d "/Library/TeX/texbin" ]; then
            echo "Detected MacTeX/BasicTeX at /Library/TeX/texbin"
            export PATH="/Library/TeX/texbin:$PATH"
            for SHELL_RC in "$HOME/.zshrc" "$HOME/.zprofile" "$HOME/.bash_profile"; do
                if [ -f "$SHELL_RC" ]; then
                    if ! grep -Fq "/Library/TeX/texbin" "$SHELL_RC" 2>/dev/null; then
                        echo "# MacTeX texbin (added by install_skills_deps.sh)" >> "$SHELL_RC"
                        echo "export PATH=\"/Library/TeX/texbin:\$PATH\"" >> "$SHELL_RC"
                        echo "Added /Library/TeX/texbin to $SHELL_RC"
                    fi
                fi
            done
        fi

        echo "Installing LibreOffice (required by docx skill for soffice command)..."
        brew install --cask libreoffice || echo "WARNING: Failed to install LibreOffice via brew. Check manually."

        echo "System packages installed successfully (macOS)."
    fi

elif [ "$OS_TYPE" = "Linux" ]; then
    # --- Linux (apt-get) ---
    if command -v apt-get &> /dev/null; then
        echo "Detected apt-get package manager."
        echo "Installing system packages..."
        sudo apt-get update -y
        sudo apt-get install -y \
            tesseract-ocr \
            poppler-utils \
            libreoffice \
            chromium-browser || sudo apt-get install -y chromium || echo "WARNING: chromium install failed, try installing manually."

        echo "Installing TinyTeX..."
        if ! command -v pdflatex &> /dev/null; then
            curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh || echo "WARNING: Failed to install TinyTeX."
        fi

        # Determine TinyTeX bin dir (Linux)
        TINYTEX_BIN_DIR=""
        if [ -d "$HOME/.TinyTeX/bin/x86_64-linux" ]; then
            TINYTEX_BIN_DIR="$HOME/.TinyTeX/bin/x86_64-linux"
        elif [ -d "$HOME/.TinyTeX/bin/aarch64-linux" ]; then
            TINYTEX_BIN_DIR="$HOME/.TinyTeX/bin/aarch64-linux"
        fi

        if [ -n "$TINYTEX_BIN_DIR" ]; then
            export PATH="$TINYTEX_BIN_DIR:$PATH"
            for SHELL_RC in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
                if [ -f "$SHELL_RC" ]; then
                    if ! grep -Fq "$TINYTEX_BIN_DIR" "$SHELL_RC" 2>/dev/null; then
                        echo "# TinyTeX bin (added by install_skills_deps.sh)" >> "$SHELL_RC"
                        echo "export PATH=\"$TINYTEX_BIN_DIR:\$PATH\"" >> "$SHELL_RC"
                    fi
                fi
            done

            if command -v tlmgr &> /dev/null; then
                echo "Installing LaTeX tools via tlmgr..."
                tlmgr update --self || echo "WARNING: tlmgr update failed."
                tlmgr install latexmk chktex abntex2 || echo "WARNING: tlmgr install failed."
            fi
        fi

        echo "System packages installed successfully (Linux)."
    else
        echo "WARNING: apt-get not found. Please install system dependencies manually:"
        echo "  tesseract-ocr, poppler-utils, libreoffice, chromium"
    fi
else
    echo "WARNING: Unsupported OS ($OS_TYPE). Please install system dependencies manually."
fi
echo ""

# 2. Node.js & NPM
echo "[2/5] Checking Node.js and NPM..."
if ! command -v npm &> /dev/null; then
    echo "WARNING: NPM not found. Please install Node.js."
    if [ "$OS_TYPE" = "Darwin" ] && command -v brew &> /dev/null; then
        echo "Installing Node.js via Homebrew..."
        brew install node
    elif [ "$OS_TYPE" = "Linux" ] && command -v apt-get &> /dev/null; then
        echo "Installing Node.js via apt-get..."
        sudo apt-get install -y nodejs npm
    fi
fi

if command -v npm &> /dev/null; then
    echo "Installing global NPM packages (docx)..."
    npm install -g docx
    echo "NPM packages installed successfully."
else
    echo "WARNING: NPM still not available. Skipping NPM packages."
fi
echo ""

# 3. Browser Automation Tools
echo "[3/5] Installing Browser Automation Tools..."

if command -v npm &> /dev/null; then
    # agent-browser
    if ! command -v agent-browser &> /dev/null; then
        echo "Installing agent-browser..."
        npm install -g agent-browser || echo "WARNING: Failed to install agent-browser."
        if command -v agent-browser &> /dev/null; then
            echo "Downloading Chrome for agent-browser..."
            agent-browser install || echo "WARNING: agent-browser install (Chrome download) failed."
        fi
    else
        echo "agent-browser already installed."
    fi

    # playwright-cli
    if ! command -v playwright-cli &> /dev/null; then
        echo "Installing @playwright/cli..."
        npm install -g @playwright/cli@latest || echo "WARNING: Failed to install @playwright/cli."
    else
        echo "playwright-cli already installed."
    fi

    # Install Playwright browsers (Chromium)
    echo "Installing Playwright browsers (Chromium)..."
    npx playwright install chromium 2>/dev/null || echo "WARNING: Playwright browser install failed."
else
    echo "WARNING: NPM not available. Skipping browser automation tools."
fi
echo ""

# 4. Python Virtual Environment
echo "[4/5] Setting up Python Virtual Environment..."
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

# If pdflatex still missing, offer to install BasicTeX (macOS only)
if ! command -v pdflatex &> /dev/null; then
    if [ "$OS_TYPE" = "Darwin" ] && command -v brew &> /dev/null; then
        echo "pdflatex still not found. Installing BasicTeX via Homebrew Cask..."
        brew install --cask basictex || echo "WARNING: Failed to install basictex via brew."
        if [ -d "/Library/TeX/texbin" ]; then
            export PATH="/Library/TeX/texbin:$PATH"
            for SHELL_RC in "$HOME/.zshrc" "$HOME/.zprofile" "$HOME/.bash_profile"; do
                if [ -f "$SHELL_RC" ]; then
                    if ! grep -Fq "/Library/TeX/texbin" "$SHELL_RC" 2>/dev/null; then
                        echo "# MacTeX texbin (added by install_skills_deps.sh)" >> "$SHELL_RC"
                        echo "export PATH=\"/Library/TeX/texbin:\$PATH\"" >> "$SHELL_RC"
                    fi
                fi
            done
        fi
    fi
fi
echo ""

# 5. Python Packages
echo "[5/5] Installing Python Packages..."
echo "The following dependencies were identified across the skills:"
echo "- pyyaml (academic-prd)"
echo "- pandas, matplotlib (academic-media)"
echo "- pypdf, pdfplumber, reportlab, pillow, pytesseract, pdf2image (pdf)"
echo "- requests (academic-researcher)"
echo "- defusedxml (docx office scripts)"
echo "- duckduckgo-search (web-browser-search / duckducksearch)"

# Use existing requirements_skills.txt if present, otherwise create a default
if [ -f "$RESOURCES_DIR/requirements_skills.txt" ]; then
    echo "Using existing $RESOURCES_DIR/requirements_skills.txt."
    # Ensure duckduckgo-search is in the file
    if ! grep -q "duckduckgo-search" "$RESOURCES_DIR/requirements_skills.txt"; then
        echo "Adding duckduckgo-search to requirements_skills.txt..."
        echo "duckduckgo-search" >> "$RESOURCES_DIR/requirements_skills.txt"
    fi
else
    echo "Creating default $RESOURCES_DIR/requirements_skills.txt."
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
duckduckgo-search
EOF
fi

echo "Installing requirements via pip..."
pip install -r "$RESOURCES_DIR/requirements_skills.txt"
echo "Python dependencies installed successfully."
echo ""

echo "================================================================="
echo "  Installation Complete!                                         "
echo "================================================================="
echo "System, Node.js, Browser Tools, and Python dependencies set up."
echo "Dependencies list saved to: $RESOURCES_DIR/requirements_skills.txt"
echo ""
echo "Installed components:"
echo "  - System: tesseract, poppler, TinyTeX, LibreOffice"
echo "  - NPM: docx, agent-browser, @playwright/cli"
echo "  - Python: $(cat $RESOURCES_DIR/requirements_skills.txt | tr '\n' ', ')"
echo ""
echo "To activate the virtual environment later, run:"
echo "source .venv/bin/activate"
echo "================================================================="
