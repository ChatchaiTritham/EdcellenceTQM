# EdcellenceTQM Installation Guide

Quick installation guide for EdcellenceTQM computational framework.

## Prerequisites

- **Python**: 3.8 or higher
- **PostgreSQL**: 13+ (optional, for full database deployment)
- **RAM**: 4GB minimum
- **Disk Space**: 500MB for dependencies

## Quick Setup (Recommended)

### Option 1: Automated Setup Scripts

**For Linux/macOS:**
```bash
bash venv-tqm.sh
```

**For Windows:**
```cmd
venv-tqm.bat
```

**Cross-Platform (Python script):**
```bash
python setup_environment.py
python setup_environment.py --jupyter  # Launch Jupyter after setup
python setup_environment.py --test     # Run tests after setup
```

These scripts will:
- ✓ Check Python version
- ✓ Create virtual environment (`venv-tqm/`)
- ✓ Install all dependencies
- ✓ Verify installation
- ✓ Run quick functionality test

---

### Option 2: Manual Installation

```bash
# 1. Clone repository
git clone https://github.com/edcellence-anonymous/EdcellenceTQM.git
cd EdcellenceTQM

# 2. Create virtual environment
python3 -m venv venv-tqm

# 3. Activate environment
# On Linux/macOS:
source venv-tqm/bin/activate
# On Windows:
venv-tqm\Scripts\activate.bat

# 4. Upgrade pip
pip install --upgrade pip setuptools wheel

# 5. Install dependencies
pip install -r requirements.txt

# 6. Verify installation
python -c "from src.adli_letci_core import *; print('✓ Installation successful')"

# 7. Run quick test
python -c "from src.adli_letci_core import ADLIIndicators, compute_adli_score; print(f'ADLI Score: {compute_adli_score(ADLIIndicators(0.8,0.7,0.6,0.75)):.2f}')"
```

Expected output:
```
✓ Installation successful
ADLI Score: 72.50
```

---

## Verify Installation

### Run Unit Tests
```bash
pytest tests/ -v
```

Expected output:
```
tests/test_adli_scoring.py::test_compute_adli_score PASSED
tests/test_adli_scoring.py::test_compute_letci_score PASSED
tests/test_adli_scoring.py::test_category_aggregation PASSED
tests/test_adli_scoring.py::test_organizational_score PASSED
tests/test_adli_scoring.py::test_integration_health_index PASSED
tests/test_adli_scoring.py::test_gap_prioritization PASSED
======================== 6 passed in 0.23s =========================
```

### Run Example Assessment
```bash
python -c "
from src.adli_letci_core import *

# ADLI process assessment
adli = ADLIIndicators(approach=0.80, deployment=0.70, learning=0.65, integration=0.75)
print(f'Process Score: {compute_adli_score(adli):.2f}/100')

# LeTCI results assessment
letci = LeTCIIndicators(level=0.85, trend=0.70, comparison=0.65, integration=0.80)
print(f'Results Score: {compute_letci_score(letci):.2f}/100')
"
```

Expected output:
```
Process Score: 72.50/100
Results Score: 76.75/100
```

---

## Launch Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

This will open your browser with interactive notebooks:
- `01_QuickStart.ipynb` - Basic examples
- `02_ADLI_Analysis.ipynb` - Process assessment
- `03_LeTCI_Results.ipynb` - Results analysis
- ... and 5 more notebooks

---

## Database Setup (Optional)

For full deployment with PostgreSQL:

### 1. Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-13

# macOS (Homebrew)
brew install postgresql@13

# Windows: Download from https://www.postgresql.org/download/windows/
```

### 2. Create Database
```bash
# Create database
createdb -U postgres adli_letci_tqm

# Load schema
psql -U postgres -d adli_letci_tqm -f database/schema_simplified.sql
```

### 3. Verify Database
```bash
psql -U postgres -d adli_letci_tqm -c "\dt"
```

Expected output should show 20 tables including:
- `fact_assessment_scores`
- `fact_results_metrics`
- `dim_department`
- ... etc.

---

## Docker Deployment (Alternative)

For containerized deployment:

```bash
# Build and start all services
docker-compose up -d

# Access dashboard
open http://localhost:8080

# Access database
psql -h localhost -U tqm_admin -d adli_letci_tqm
```

Stop services:
```bash
docker-compose down
```

---

## Troubleshooting

### Python version too old
**Error:** `Python 3.8+ required`

**Solution:**
```bash
# Check current version
python3 --version

# Install Python 3.8+ from:
# - https://www.python.org/downloads/
# - Or use pyenv: pyenv install 3.10.0
```

### Pip install fails
**Error:** `Failed to build wheels for numpy/pandas`

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install build tools (Ubuntu/Debian)
sudo apt-get install python3-dev build-essential

# Install build tools (macOS)
xcode-select --install

# Retry installation
pip install -r requirements.txt
```

### Import errors
**Error:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
```bash
# Ensure you're in the EdcellenceTQM directory
cd /path/to/EdcellenceTQM

# Activate virtual environment
source venv-tqm/bin/activate  # Linux/macOS
venv-tqm\Scripts\activate.bat  # Windows

# Verify current directory
pwd  # Should show .../EdcellenceTQM
```

### Jupyter not found
**Error:** `jupyter: command not found`

**Solution:**
```bash
# Install Jupyter in virtual environment
pip install jupyter ipywidgets

# Launch notebooks
jupyter notebook notebooks/
```

---

## Uninstallation

To remove EdcellenceTQM:

```bash
# 1. Deactivate virtual environment (if active)
deactivate

# 2. Remove virtual environment
rm -rf venv-tqm/  # Linux/macOS
rmdir /s /q venv-tqm  # Windows

# 3. Remove repository (optional)
cd ..
rm -rf EdcellenceTQM/  # Linux/macOS
rmdir /s /q EdcellenceTQM  # Windows
```

---

## Next Steps

After successful installation:

1. **Read the README** - Complete documentation
2. **Try notebooks** - Interactive tutorials in `notebooks/`
3. **Run examples** - Sample assessments in `data/examples/`
4. **Read API docs** - Function reference in `docs/`
5. **Run benchmarks** - Performance testing in `notebooks/07_Scalability_Benchmarks.ipynb`

---

## Support

For installation issues:
- Check troubleshooting section above
- Review README.md
- Open GitHub issue (after manuscript acceptance)

---

**Last Updated:** February 14, 2026
**Tested on:** Python 3.8-3.11, Ubuntu 22.04, macOS 13, Windows 10/11
