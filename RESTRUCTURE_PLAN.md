# EdcellenceTQM - Restructuring to Standard Python Package

**Date**: 2026-02-15
**Goal**: Transform into installable Python package following PEP standards

---

## 🎯 Target Structure

```
EdcellenceTQM/
├── pyproject.toml                 # Modern packaging configuration (PEP 518/621)
├── setup.py                       # Backward compatibility setup
├── MANIFEST.in                    # Include non-Python files
├── requirements.txt               # Runtime dependencies
├── requirements-dev.txt           # Development dependencies
├── README.md                      # Main documentation
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore patterns
│
├── edcellence_tqm/                # Main package directory (snake_case)
│   ├── __init__.py                # Package initialization
│   ├── __version__.py             # Version info
│   │
│   ├── core/                      # Core assessment algorithms
│   │   ├── __init__.py
│   │   ├── adli_letci.py         # Moved from src/adli_letci_core.py
│   │   ├── equations.py          # Core equations (extracted)
│   │   └── engine.py             # Assessment engine
│   │
│   ├── visualization/             # Visualization module
│   │   ├── __init__.py
│   │   ├── charts.py             # Moved from src/visualizations.py
│   │   ├── styles.py             # PublicationStyle class
│   │   └── utils.py              # Helper functions
│   │
│   ├── database/                  # Database utilities
│   │   ├── __init__.py
│   │   ├── schema.py             # Schema definitions
│   │   └── models.py             # ORM models (optional)
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       └── helpers.py
│
├── tests/                         # Test suite (pytest)
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_core.py              # Moved from tests/test_adli_scoring.py
│   ├── test_visualization.py     # Visualization tests
│   └── test_integration.py       # Integration tests
│
├── examples/                      # Usage examples
│   ├── notebooks/                # Jupyter notebooks
│   │   ├── 01_QuickStart.ipynb
│   │   ├── 02_ADLI_Analysis.ipynb
│   │   ├── 03_LeTCI_Results.ipynb
│   │   ├── 04_Organizational_Assessment.ipynb
│   │   ├── 05_Gap_Prioritization.ipynb
│   │   ├── 06_Integration_Health.ipynb
│   │   ├── 07_Scalability_Benchmarks.ipynb
│   │   └── 08_Publication_Figures.ipynb
│   │
│   └── scripts/                  # Example Python scripts
│       ├── basic_assessment.py
│       └── generate_figures.py
│
├── docs/                         # Documentation
│   ├── index.md                  # Documentation home
│   ├── installation.md           # Installation guide
│   ├── quickstart.md             # Quick start guide
│   ├── api/                      # API reference
│   │   ├── core.md
│   │   └── visualization.md
│   └── tutorials/                # Tutorials
│       └── first_assessment.md
│
├── data/                         # Sample data
│   └── examples/
│       ├── sample_assessment_data.csv
│       ├── benchmark_results.csv
│       └── department_scores.json
│
├── scripts/                      # Utility scripts
│   ├── schema_simplified.sql     # Moved from database/
│   └── setup_database.py         # Database setup script
│
└── figures/                      # Generated figures
    └── publication/              # Publication-ready figures
        └── ... (15 files)
```

---

## 📦 Benefits of New Structure

### 1. **Installable Package**
```bash
pip install -e .                  # Development install
pip install edcellence-tqm        # PyPI install (future)
```

### 2. **Importable Modules**
```python
from edcellence_tqm.core import ADLIIndicators, compute_adli_score
from edcellence_tqm.visualization import plot_adli_radar
```

### 3. **Standard Testing**
```bash
pytest tests/                     # Run all tests
pytest tests/test_core.py         # Run specific tests
pytest --cov=edcellence_tqm      # Coverage report
```

### 4. **Documentation**
```bash
mkdocs serve                      # Local documentation server
mkdocs build                      # Build docs for deployment
```

---

## 🔄 Migration Steps

### Phase 1: Create Package Structure
- [ ] Create `edcellence_tqm/` directory
- [ ] Create `__init__.py` files
- [ ] Create `pyproject.toml`
- [ ] Create `setup.py`

### Phase 2: Move Core Files
- [ ] Move `src/adli_letci_core.py` → `edcellence_tqm/core/adli_letci.py`
- [ ] Move `src/visualizations.py` → `edcellence_tqm/visualization/charts.py`
- [ ] Update all imports

### Phase 3: Reorganize Tests
- [ ] Move `tests/test_adli_scoring.py` → `tests/test_core.py`
- [ ] Create `tests/conftest.py`
- [ ] Update test imports

### Phase 4: Reorganize Examples
- [ ] Move `notebooks/` → `examples/notebooks/`
- [ ] Update notebook imports
- [ ] Create example scripts

### Phase 5: Update Documentation
- [ ] Create `docs/` directory
- [ ] Extract documentation from README
- [ ] Create API reference

### Phase 6: Configuration Files
- [ ] Update `requirements.txt`
- [ ] Create `requirements-dev.txt`
- [ ] Create `MANIFEST.in`
- [ ] Update `.gitignore`

---

## 📝 New Configuration Files

### `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "edcellence-tqm"
version = "1.0.0"
description = "Computational Framework for Educational Excellence Assessment"
authors = [
    {name = "Rungtiva Saosing", email = "rungtiva.s@mail.rmutt.ac.th"},
    {name = "Chatchai Tritham", email = "chatchait66@nu.ac.th"},
]
license = {text = "MIT"}
requires-python = ">=3.8"
dependencies = [
    "numpy>=1.20.0",
    "pandas>=1.3.0",
    "matplotlib>=3.4.0",
    "plotly>=5.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=3.0",
    "black>=22.0",
    "flake8>=4.0",
]
```

### `setup.py` (Backward compatibility)
```python
from setuptools import setup, find_packages

setup(
    name="edcellence-tqm",
    packages=find_packages(),
    install_requires=[...],
)
```

---

## ✅ Benefits

1. **PyPI Publishing**: Ready to publish to PyPI
2. **Easy Installation**: `pip install edcellence-tqm`
3. **Import Anywhere**: Use in any Python project
4. **Standard Testing**: pytest, coverage, CI/CD ready
5. **Documentation**: Auto-generated API docs
6. **Version Control**: Semantic versioning
7. **Development Mode**: `pip install -e .` for development

---

## 🔗 Resources

- PEP 518: https://peps.python.org/pep-0518/
- PEP 621: https://peps.python.org/pep-0621/
- Python Packaging Guide: https://packaging.python.org/

---

**Ready to proceed with restructuring?**
