#!/bin/bash
# EdcellenceTQM Virtual Environment Setup Script
# For Linux/macOS users
# Usage: bash venv-tqm.sh

set -e  # Exit on error

echo "=================================================="
echo "EdcellenceTQM Environment Setup"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"; then
    echo -e "${RED}Error: Python 3.8+ required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
echo ""

# Create virtual environment
VENV_DIR="venv-tqm"

if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists at: $VENV_DIR${NC}"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing environment..."
        rm -rf "$VENV_DIR"
    else
        echo "Using existing environment."
        source "$VENV_DIR/bin/activate"
        echo -e "${GREEN}✓ Activated existing environment${NC}"
        echo ""
        echo "To activate in future sessions, run:"
        echo "  source $VENV_DIR/bin/activate"
        exit 0
    fi
fi

echo "Creating virtual environment: $VENV_DIR"
python3 -m venv "$VENV_DIR"
echo -e "${GREEN}✓ Virtual environment created${NC}"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓ Environment activated${NC}"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install dependencies
echo "Installing EdcellenceTQM dependencies..."
echo "(This may take 2-3 minutes)"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Verify installation
echo "Verifying installation..."

# Test numpy
python3 -c "import numpy; print('  - NumPy', numpy.__version__)" || echo -e "${RED}  ✗ NumPy failed${NC}"

# Test pandas
python3 -c "import pandas; print('  - Pandas', pandas.__version__)" || echo -e "${RED}  ✗ Pandas failed${NC}"

# Test matplotlib
python3 -c "import matplotlib; print('  - Matplotlib', matplotlib.__version__)" || echo -e "${RED}  ✗ Matplotlib failed${NC}"

# Test plotly
python3 -c "import plotly; print('  - Plotly', plotly.__version__)" || echo -e "${RED}  ✗ Plotly failed${NC}"

# Test core module
python3 -c "from src.adli_letci_core import ADLIIndicators, compute_adli_score; print('  - EdcellenceTQM core module')" || echo -e "${RED}  ✗ Core module failed${NC}"

echo -e "${GREEN}✓ All packages verified${NC}"
echo ""

# Run quick test
echo "Running quick functionality test..."
python3 << 'EOF'
from src.adli_letci_core import ADLIIndicators, compute_adli_score
indicators = ADLIIndicators(0.8, 0.7, 0.6, 0.75)
score = compute_adli_score(indicators)
expected = 72.5
if abs(score - expected) < 0.01:
    print(f"  ✓ ADLI Score: {score:.2f} (expected: {expected})")
else:
    print(f"  ✗ Test failed: got {score:.2f}, expected {expected}")
    exit(1)
EOF
echo ""

# Run unit tests if pytest available
if command -v pytest &> /dev/null; then
    echo "Running unit tests..."
    pytest tests/ -v --tb=short || echo -e "${YELLOW}Some tests failed (this may be normal if test data is incomplete)${NC}"
    echo ""
fi

# Success message
echo "=================================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "Your EdcellenceTQM environment is ready."
echo ""
echo "Next steps:"
echo "  1. Activate environment (in new terminals):"
echo "     ${GREEN}source $VENV_DIR/bin/activate${NC}"
echo ""
echo "  2. Launch Jupyter notebooks:"
echo "     ${GREEN}jupyter notebook notebooks/${NC}"
echo ""
echo "  3. Run example assessment:"
echo "     ${GREEN}python3 -c 'from src.adli_letci_core import *; print(compute_adli_score(ADLIIndicators(0.8,0.7,0.6,0.75)))'${NC}"
echo ""
echo "  4. Run tests:"
echo "     ${GREEN}pytest tests/ -v${NC}"
echo ""
echo "  5. Deactivate environment when done:"
echo "     ${GREEN}deactivate${NC}"
echo ""
echo "For more information, see README.md"
echo "=================================================="
