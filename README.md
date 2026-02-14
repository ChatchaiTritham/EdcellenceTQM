# EdcellenceTQM Computational TQM Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Computational formalization of Baldrige Excellence Framework assessment logic for Total Quality Management in higher education.**

---

## 📋 Overview

This repository contains the computational engine, database schema, and deployment infrastructure for implementing ADLI (Approach, Deployment, Learning, Integration) and LeTCI (Level, Trend, Comparison, Integration) assessment dimensions as executable algorithms.

**Academic Paper:** Submitted to *Journal of King Saud University - Computer and Information Sciences* (JKSU-CIS)

**Key Features:**
- ✅ 6 assessment algorithms (ADLI, LeTCI, Category, Organizational, IHI, Gap Priority)
- ✅ 138-table star-schema database architecture
- ✅ Multi-framework integration (EdPEx, TQF, AUN-QA)
- ✅ Framework-agnostic parameterization
- ✅ Docker containerization
- ✅ Comprehensive test suite (147 unit tests)

---

## 🏗️ Architecture

### Computational Components

1. **Core Engine** (`src/adli_letci_core.py`)
   - ADLI process scoring (Equation 1)
   - LeTCI results scoring (Equation 2)
   - Category aggregation (Equation 3)
   - Organizational score (Equation 4)
   - Integration Health Index (Equation 5)
   - Gap-based prioritization (Equation 6)

2. **Database Schema** (`database/schema.sql`)
   - 12 fact tables (metrics, assessments, results)
   - 26 dimension tables (hierarchy, taxonomy, time)
   - 8 bridge tables (multi-framework crosswalks)
   - 92 lookup tables (framework parameters)

3. **Framework Mappings** (`config/framework_mappings.yaml`)
   - Baldrige Excellence Framework (BEF)
   - EdPEx (Education Criteria for Performance Excellence - Thailand)
   - TQF (Thailand Qualifications Framework)
   - AUN-QA (ASEAN University Network Quality Assurance)

---

## 📊 Performance Characteristics

| Metric | Value |
|--------|-------|
| Database response time | 47 ms (25 departments) |
| Scalability | O(n log n) for aggregation |
| Concurrent users | 120+ |
| Dashboard initialization | < 2 seconds |
| System availability | 99.2% (12-month avg) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Docker (optional)

### Installation

```bash
# Clone repository
git clone https://github.com/[institution]/EdcellenceTQM.git
cd EdcellenceTQM

# Install dependencies
pip install -r requirements.txt

# Initialize database
psql -U postgres -f database/schema.sql

# Run tests
pytest tests/ -v
```

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# Access dashboard
open http://localhost:8080
```

---

## 📖 Documentation

### Core Algorithms

#### 1. ADLI Process Scoring (Equation 1)
```python
def compute_adli_score(P_A, P_D, P_L, P_I, weights=None):
    """
    Compute ADLI process item score.

    Args:
        P_A: Approach indicator [0,1]
        P_D: Deployment indicator [0,1]
        P_L: Learning indicator [0,1]
        P_I: Integration indicator [0,1]
        weights: Dict with keys {A, D, L, I}, defaults to {0.30, 0.30, 0.20, 0.20}

    Returns:
        float: Score in range [0,100]
    """
    if weights is None:
        weights = {'A': 0.30, 'D': 0.30, 'L': 0.20, 'I': 0.20}

    return 100 * (weights['A'] * P_A +
                  weights['D'] * P_D +
                  weights['L'] * P_L +
                  weights['I'] * P_I)
```

#### 2. LeTCI Results Scoring (Equation 2)
```python
def compute_letci_score(R_Lv, R_Tr, R_Cp, R_I, weights=None):
    """
    Compute LeTCI results item score.

    Args:
        R_Lv: Level indicator [0,1]
        R_Tr: Trend indicator [0,1]
        R_Cp: Comparison indicator [0,1]
        R_I: Integration indicator [0,1]
        weights: Dict with keys {Lv, Tr, Cp, I}, defaults to {0.40, 0.25, 0.25, 0.10}

    Returns:
        float: Score in range [0,100]
    """
    if weights is None:
        weights = {'Lv': 0.40, 'Tr': 0.25, 'Cp': 0.25, 'I': 0.10}

    return 100 * (weights['Lv'] * R_Lv +
                  weights['Tr'] * R_Tr +
                  weights['Cp'] * R_Cp +
                  weights['I'] * R_I)
```

See `docs/API.md` for complete documentation.

---

## 🗄️ Database Schema

### Star-Schema Architecture

```
┌─────────────────────────────────────────────────────┐
│                  FACT TABLES (12)                   │
├─────────────────────────────────────────────────────┤
│ • fact_assessment_scores                            │
│ • fact_results_metrics                              │
│ • fact_category_aggregates                          │
│ • fact_organizational_scores                        │
│ • fact_gap_analysis                                 │
│ • fact_ihi_metrics                                  │
│ • fact_key_reports (EdPEx evidence)                 │
│ • fact_improvement_actions                          │
│ • fact_stakeholder_feedback                         │
│ • fact_learning_outcomes (TQF)                      │
│ • fact_workforce_metrics                            │
│ • fact_operational_kpis                             │
└─────────────────────────────────────────────────────┘
           ↓                     ↓
┌────────────────────┐  ┌────────────────────────────┐
│  DIMENSION (26)    │  │  BRIDGE TABLES (8)         │
│  • dim_department  │  │  • bridge_framework_items  │
│  • dim_assessment  │  │  • bridge_evidence_links   │
│  • dim_time        │  │  • bridge_multi_mapping    │
│  • ...             │  │  • ...                     │
└────────────────────┘  └────────────────────────────┘
                              ↓
                    ┌──────────────────────┐
                    │  LOOKUP TABLES (92)  │
                    │  • EdPEx parameters  │
                    │  • TQF specifications│
                    │  • AUN-QA criteria   │
                    │  • ADLI/LeTCI scales │
                    └──────────────────────┘
```

See `database/README.md` for detailed schema documentation.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v --cov=src

# Run specific test modules
pytest tests/test_adli_scoring.py
pytest tests/test_letci_scoring.py
pytest tests/test_integration_health.py

# Test coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

**Test Coverage:** 147 unit tests, >85% code coverage

---

## 🌍 Multi-Framework Integration

### Framework Crosswalk Example

```yaml
# config/framework_mappings.yaml
Leadership:
  baldrige_category: 1
  baldrige_weight: 0.12
  edpex_items:
    - governance_ethics
    - community_contributions
  tqf_alignment:
    - TQF1_institutional_policy
  aunqa_criteria:
    - C1.1_qa_system
    - C1.2_qa_policy
```

### Bridge Table Architecture

```sql
-- Example: Multi-framework evidence routing
CREATE TABLE bridge_framework_items (
    bridge_id SERIAL PRIMARY KEY,
    evidence_id INT REFERENCES fact_key_reports(report_id),
    baldrige_item VARCHAR(10),
    edpex_item VARCHAR(10),
    tqf_form VARCHAR(10),
    aunqa_criterion VARCHAR(10),
    mapping_confidence DECIMAL(3,2) -- 0.00-1.00
);
```

---

## 📈 Empirical Validation

**Study Details:**
- **Institution:** Mid-scale Thai public university
- **Sample:** 25 academic departments
- **Duration:** 12-month evaluation (Apr 2024 - Mar 2025)
- **Design:** Single-group interrupted time-series quasi-experimental

**Key Results:**
| Metric | Baseline | Post-Implementation | Improvement | p-value |
|--------|----------|---------------------|-------------|---------|
| Preparation time | 6.5±1.2 weeks | 2.0±0.4 weeks | -69% | <0.001 |
| Documentation duplication | 450±85 items | 80±15 items | -82% | <0.001 |
| Inter-rater reliability | α=0.62 | α=0.88 | +0.26 | <0.01 |
| Review duration | 4.5±0.8 hours | 2.5±0.3 hours | -44% | <0.001 |

See paper for complete statistical analysis.

---

## 🔧 Configuration

### Framework Parameters

```python
# config/weights.py
BALDRIGE_CATEGORY_WEIGHTS = {
    'Leadership': 0.12,
    'Strategy': 0.085,
    'Customers': 0.085,
    'Measurement': 0.10,
    'Workforce': 0.10,
    'Operations': 0.15,
    'Results': 0.36
}

ADLI_DEFAULT_WEIGHTS = {
    'Approach': 0.30,
    'Deployment': 0.30,
    'Learning': 0.20,
    'Integration': 0.20
}

LETCI_DEFAULT_WEIGHTS = {
    'Level': 0.40,
    'Trend': 0.25,
    'Comparison': 0.25,
    'Integration': 0.10
}
```

### Maturity Levels

```python
# config/maturity.py
MATURITY_BANDS = {
    1: {'range': (0, 20), 'label': 'Reactive'},
    2: {'range': (21, 40), 'label': 'Early Systematic'},
    3: {'range': (41, 60), 'label': 'Aligned'},
    4: {'range': (61, 85), 'label': 'Integrated'},
    5: {'range': (86, 100), 'label': 'Role Model'}
}
```

---

## 🌐 International Adaptation

The framework is designed for international transfer via parameterization:

1. **Framework-agnostic core:** ADLI/LeTCI logic applies across excellence frameworks (Baldrige, EFQM, ISO 9001)
2. **Configurable mappings:** Replace EdPEx/TQF/AUN-QA with local frameworks via YAML configuration
3. **Scalable database:** Adjust lookup tables for institutional size (simplified 45-table version for <5,000 students)

See `docs/INTERNATIONAL_DEPLOYMENT.md` for adaptation guide.

---

## 📄 License

MIT License - see `LICENSE` file for details.

**Citation:**
```bibtex
@article{author2026adli,
  title={Computational TQM System Implementation in Higher Education:
         Formalizing Baldrige Excellence Assessment as Operational Infrastructure},
  author={[Authors]},
  journal={Journal of King Saud University - Computer and Information Sciences},
  year={2026},
  note={Under review}
}
```

---

## 👥 Contributing

Contributions welcome! Please see `CONTRIBUTING.md` for guidelines.

**Areas for contribution:**
- Additional framework mappings (EFQM, ISO 9001, etc.)
- Performance optimizations
- Dashboard UI improvements
- Internationalization (i18n)
- Unit test coverage expansion

---

## 📞 Contact

**Corresponding Author:** [To be revealed upon acceptance]

**Issues:** Please use GitHub Issues for bug reports and feature requests.

**Institutional Contact:** Rajamangala University of Technology Krungthep, Thailand

---

## 🙏 Acknowledgments

- Faculty of Science and Technology, RMUTK (Fiscal Budget Year 2024)
- Quality coordinators and administrative staff across 25 departments
- NIST Baldrige Performance Excellence Program for framework specifications

---

**Last Updated:** February 2026
**Repository Status:** Active Development
**Documentation:** See `/docs` directory for detailed guides
