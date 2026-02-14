# EdcellenceTQM: Computational Framework for Educational Excellence Assessment

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![Figures: 15](https://img.shields.io/badge/figures-15%20publication--ready-brightgreen.svg)](figures/publication/)
[![DPI: 300](https://img.shields.io/badge/resolution-300%20DPI-blue.svg)](figures/publication/)
[![IEEE](https://img.shields.io/badge/compliant-IEEE%2FSpringer-red.svg)](figures/publication/)

**EdcellenceTQM** is a computational implementation of the Baldrige Excellence Framework for higher education quality assessment, featuring integrated ADLI-LeTCI scoring algorithms with empirical validation from a 12-month longitudinal study.

## Overview

This framework transforms qualitative Total Quality Management (TQM) assessment into executable computational specifications, enabling:

- **Reproducible Scoring**: Six mathematical equations for ADLI (Approach-Deployment-Learning-Integration) process assessment and LeTCI (Level-Trend-Comparison-Integration) results measurement
- **Integration Analytics**: Cross-category Integration Health Index (IHI) for detecting organizational silos
- **Evidence-Based Prioritization**: Gap-based priority scoring combining performance gaps, point values, and deployment urgency
- **Multi-Framework Compatibility**: Mappings between Baldrige, EdPEx, TQF, and AUN-QA frameworks
- **Publication-Quality Visualizations**: IEEE/Springer-compliant figures (300 DPI, Type-2 embedded fonts)

## Publication-Quality Visualizations

This framework includes **8 publication-ready visualization functions** generating IEEE/Springer-compliant figures for academic manuscripts:

### Available Visualizations

| Figure | Type | Description | Formats |
|--------|------|-------------|---------|
| **ADLI Radar** | 2D Polar | Process maturity profile across 4 dimensions | PNG, PDF |
| **LeTCI Radar** | 2D Polar | Results assessment across 4 dimensions | PNG, PDF |
| **Category Scores** | Bar Chart | Performance across 7 Baldrige categories | PNG, PDF |
| **IHI Trajectory** | Time Series | Integration health trends over time | PNG, PDF |
| **Gap Priority** | 3D Scatter | Interactive priority matrix (gap × impact × urgency) | HTML |
| **Scalability** | Dual Panel | Multi-department growth analysis | PNG, PDF |
| **Heatmap** | Matrix | Category correlation and integration patterns | PNG, PDF |
| **Effect Sizes** | Forest Plot | Statistical significance with confidence intervals | PNG, PDF |

### Technical Specifications

✅ **IEEE/Springer Compliance:**
- **Resolution**: 300 DPI (minimum for publication)
- **Column Widths**: 3.5" (single), 7.0" (double)
- **Fonts**: Times New Roman 10pt serif, 8pt legends
- **PDF**: Type-2 TrueType embedded fonts (`pdf.fonttype=42`)
- **Colors**: Wong 2011 colorblind-safe palette
- **Layout**: Constrained layout with 28 anti-overlap features

### Sample Figures

All publication figures are available in [`figures/publication/`](figures/publication/):

```
figures/publication/
├── fig1a_adli_radar.png         (142 KB, 300 DPI)
├── fig1a_adli_radar.pdf         (48 KB, Type-2 fonts)
├── fig1b_letci_radar.png        (148 KB, 300 DPI)
├── fig1b_letci_radar.pdf        (48 KB, Type-2 fonts)
├── fig2_category_scores.png     (109 KB, 300 DPI)
├── fig2_category_scores.pdf     (57 KB, Type-2 fonts)
├── fig3_ihi_trajectory.png      (145 KB, 300 DPI)
├── fig3_ihi_trajectory.pdf      (53 KB, Type-2 fonts)
├── fig4_gap_priority.html       (4.7 MB, interactive Plotly)
├── fig5_scalability.png         (162 KB, 300 DPI)
├── fig5_scalability.pdf         (54 KB, Type-2 fonts)
├── fig6_heatmap.png             (107 KB, 300 DPI)
├── fig6_heatmap.pdf             (55 KB, Type-2 fonts)
├── fig7_effect_sizes.png        (111 KB, 300 DPI)
└── fig7_effect_sizes.pdf        (58 KB, Type-2 fonts)
```

### Generate Figures

Run [`notebooks/08_Publication_Figures.ipynb`](notebooks/08_Publication_Figures.ipynb) to regenerate all figures:

```bash
jupyter notebook notebooks/08_Publication_Figures.ipynb
# All figures will be saved to figures/publication/
```

Or use the visualization API directly:

```python
from src.visualizations import plot_adli_radar, save_figure

# Generate ADLI radar chart
scores = {'Approach': 0.80, 'Deployment': 0.70,
          'Learning': 0.65, 'Integration': 0.75}
fig = plot_adli_radar(scores, title='Department X ADLI Profile')

# Save in publication formats
save_figure(fig, 'output/my_figure', formats=['png', 'pdf'])
# Creates: my_figure.png (300 DPI) + my_figure.pdf (Type-2 fonts)
```

## Architecture

### Core Components

```
EdcellenceTQM/
├── src/
│   ├── adli_letci_core.py         # Core assessment algorithms (6 equations)
│   └── visualizations.py          # 8 publication-quality chart functions (995 lines)
├── database/
│   └── schema_simplified.sql      # 20-table PostgreSQL schema (scalable to 138)
├── notebooks/
│   ├── 01_QuickStart.ipynb        # Basic usage examples
│   ├── 02_ADLI_Analysis.ipynb     # Process assessment with radar charts
│   ├── 03_LeTCI_Results.ipynb     # Results analysis
│   ├── 04_Organizational_Assessment.ipynb
│   ├── 05_Gap_Prioritization.ipynb
│   ├── 06_Integration_Health.ipynb
│   ├── 07_Scalability_Benchmarks.ipynb
│   └── 08_Publication_Figures.ipynb  # Generate all manuscript figures
├── figures/publication/           # 15 IEEE/Springer-compliant figures
│   ├── fig1a_adli_radar.png      # 300 DPI PNG + Type-2 PDF
│   ├── fig1b_letci_radar.png
│   ├── fig2_category_scores.png
│   ├── fig3_ihi_trajectory.png
│   ├── fig4_gap_priority.html    # Interactive 3D (Plotly)
│   ├── fig5_scalability.png
│   ├── fig6_heatmap.png
│   └── fig7_effect_sizes.png
├── data/examples/
│   ├── sample_assessment_data.csv
│   ├── benchmark_results.csv
│   └── department_scores.json
└── tests/
    └── test_adli_scoring.py       # Unit tests for all equations
```

## Assessment Equations

### Equation 1: ADLI Process Scoring
```
S^P_i = 100 × (w_A·P_A + w_D·P_D + w_L·P_L + w_I·P_I)
```
Computes process item scores from four dimensional indicators with NIST-validated weights.

### Equation 2: LeTCI Results Scoring
```
S^R_j = 100 × (w_Lv·R_Lv + w_Tr·R_Tr + w_Cp·R_Cp + w_I·R_I)
```
Evaluates results items across performance level, trend, comparison, and integration.

### Equation 3: Category Score Aggregation
```
C_k = Σ(v_i·S_i) / Σ(v_i)
```
Point-value weighted mean aggregation following Baldrige framework.

### Equation 4: Organizational Score
```
O = Σ(W_k·C_k) for k=1 to 7
```
Weighted sum of seven Baldrige categories (Leadership, Strategy, Customers, Measurement, Workforce, Operations, Results).

### Equation 5: Integration Health Index (IHI)
```
IHI = (1/2)[(1/N_p)ΣP_I + (1/N_r)ΣR_I]
```
Measures cross-category integration strength; values >0.75 indicate strong organizational alignment.

### Equation 6: Gap-Based Prioritization
```
G_i = (T_i - S_i)·v_i·δ_i
```
Prioritizes improvement initiatives by combining performance gap, point value, and deployment urgency.

## Installation

### Requirements
- Python 3.8+
- PostgreSQL 13+ (optional, for full deployment)
- 4GB RAM minimum

### Quick Start

```bash
# Clone repository
git clone https://github.com/ChatchaiTritham/EdcellenceTQM.git
cd EdcellenceTQM

# Install dependencies
pip install -r requirements.txt

# Run example assessment
python -c "
from src.adli_letci_core import *

# Process item example
adli = ADLIIndicators(approach=0.80, deployment=0.70, learning=0.65, integration=0.75)
score = compute_adli_score(adli)
print(f'Process Score: {score:.2f}/100')

# Results item example
letci = LeTCIIndicators(level=0.85, trend=0.70, comparison=0.65, integration=0.80)
results = compute_letci_score(letci)
print(f'Results Score: {results:.2f}/100')
"
```

Expected output:
```
Process Score: 72.50/100
Results Score: 76.75/100
```

## Usage Examples

### Basic Assessment Pipeline

```python
from src.adli_letci_core import AssessmentEngine, ADLIIndicators, LeTCIIndicators

# Initialize assessment engine
engine = AssessmentEngine()

# Define process items with ADLI indicators
process_items = [
    {
        'item_id': '1.1',
        'category': 'Leadership',
        'adli': ADLIIndicators(0.80, 0.75, 0.70, 0.80),
        'point_value': 70,
        'deployment_gap': 0.25
    },
    # ... more items
]

# Define results items with LeTCI indicators
results_items = [
    {
        'item_id': '7.1',
        'category': 'Results',
        'letci': LeTCIIndicators(0.85, 0.80, 0.70, 0.75),
        'point_value': 120,
        'deployment_gap': 0.20
    },
    # ... more items
]

# Compute organizational assessment
results = engine.compute_organizational_assessment(
    process_items=process_items,
    results_items=results_items,
    category_point_allocations={}
)

# Display results
print(f"Organizational Score: {results['organizational_score']:.2f}")
print(f"Integration Health Index: {results['ihi']:.3f}")
print(f"Maturity Level: {results['maturity_level']['label']}")
print("\nTop 5 Improvement Priorities:")
for item_id, priority_score in results['gap_priorities'][:5]:
    print(f"  {item_id}: {priority_score:.0f}")
```

### Radar Chart Visualization

```python
from src.visualizations import create_adli_radar_chart
import matplotlib.pyplot as plt

# Process item radar chart
adli_scores = {
    'Approach': 0.80,
    'Deployment': 0.70,
    'Learning': 0.65,
    'Integration': 0.75
}

fig, ax = create_adli_radar_chart(adli_scores, title="Item 1.1 ADLI Profile")
plt.show()
```

### Integration Health Index Trajectory

```python
from src.visualizations import plot_ihi_trajectory

# Track IHI over 12 months
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ihi_values = [0.45, 0.48, 0.52, 0.55, 0.58, 0.61,
              0.65, 0.68, 0.71, 0.73, 0.76, 0.78]

plot_ihi_trajectory(months, ihi_values, department="Computer Science")
```

## Empirical Validation Results

This framework was validated through a 12-month longitudinal study (March 2023 - February 2024) at Rajamangala University of Technology Krungthep:

| Metric | Value | Significance |
|--------|-------|--------------|
| **Departments Assessed** | 18 | Full academic coverage |
| **Total Assessments** | 216 | Monthly cycles |
| **Mean Organizational Score** | 68.4 ± 12.3 | Maturity Level 4 (Integrated) |
| **Integration Health Index** | 0.72 ± 0.14 | Moderate-to-strong integration |
| **Score Improvement** | +18.7 pts | Baseline→Endline (p<0.001) |
| **IHI Improvement** | +0.31 | Reduced silos (p<0.001) |
| **Inter-Rater Reliability** | ICC(2,k)=0.89 | Strong consistency |
| **Test-Retest Reliability** | r=0.91 | Temporal stability |

### Key Findings

1. **Computational Precision**: Algorithm-based scoring eliminated 94% of manual calculation errors
2. **Silo Detection**: IHI identified 12 departments with integration deficits (IHI < 0.60) requiring intervention
3. **Priority Accuracy**: Gap-based prioritization achieved 87% alignment with expert judgment
4. **Framework Compatibility**: Baldrige-EdPEx mapping demonstrated 92% content coverage

## Jupyter Notebooks

Interactive analysis notebooks are provided in [`notebooks/`](notebooks/):

1. **[01_QuickStart.ipynb](notebooks/01_QuickStart.ipynb)**: Basic assessment workflow and examples
2. **[02_ADLI_Analysis.ipynb](notebooks/02_ADLI_Analysis.ipynb)**: Process assessment with dimensional radar charts
3. **[03_LeTCI_Results.ipynb](notebooks/03_LeTCI_Results.ipynb)**: Results analysis and trend visualization
4. **[04_Organizational_Assessment.ipynb](notebooks/04_Organizational_Assessment.ipynb)**: Complete scoring pipeline
5. **[05_Gap_Prioritization.ipynb](notebooks/05_Gap_Prioritization.ipynb)**: 3D priority matrices (gap × impact × urgency)
6. **[06_Integration_Health.ipynb](notebooks/06_Integration_Health.ipynb)**: IHI trajectory plots and silo detection
7. **[07_Scalability_Benchmarks.ipynb](notebooks/07_Scalability_Benchmarks.ipynb)**: Performance testing (2D/3D charts)
8. **[08_Publication_Figures.ipynb](notebooks/08_Publication_Figures.ipynb)**: ⭐ **Generate all 15 manuscript figures** (300 DPI, IEEE/Springer compliant)

### Quick Start

Launch notebooks:
```bash
jupyter notebook notebooks/
```

Generate all publication figures:
```bash
jupyter notebook notebooks/08_Publication_Figures.ipynb
# Run all cells → figures saved to figures/publication/
```

## API Reference

### Core Classes

#### `ADLIIndicators(approach, deployment, learning, integration)`
Process item dimensional indicators, each in range [0,1].

**Parameters:**
- `approach` (float): Appropriateness and effectiveness of methods
- `deployment` (float): Extent of implementation across organization
- `learning` (float): Refinement through evaluation cycles
- `integration` (float): Alignment with organizational needs

#### `LeTCIIndicators(level, trend, comparison, integration)`
Results item dimensional indicators, each in range [0,1].

**Parameters:**
- `level` (float): Current performance level
- `trend` (float): Rate and direction of improvement
- `comparison` (float): Performance vs. benchmarks
- `integration` (float): Cross-category alignment

#### `AssessmentEngine(adli_weights=None, letci_weights=None, category_weights=None)`
Main assessment orchestration engine.

**Methods:**
- `compute_organizational_assessment(process_items, results_items, category_point_allocations)`: Complete assessment pipeline

### Core Functions

- `compute_adli_score(indicators, weights=None)`: Equation 1 implementation
- `compute_letci_score(indicators, weights=None)`: Equation 2 implementation
- `compute_category_score(item_scores, item_point_values)`: Equation 3 implementation
- `compute_organizational_score(category_scores, category_weights=None)`: Equation 4 implementation
- `compute_integration_health_index(process_integration_scores, results_integration_scores)`: Equation 5 implementation
- `compute_gap_priority_score(current_score, target_score, point_value, deployment_urgency)`: Equation 6 implementation
- `classify_maturity_level(score)`: Maps scores to Baldrige maturity bands

See complete API documentation in `docs/api_reference.md`.

## Database Schema

The framework uses a star schema optimized for educational analytics:

### Fact Tables (5 core)
- `fact_assessment_scores`: ADLI process item assessments
- `fact_results_metrics`: LeTCI results measurements
- `fact_category_aggregates`: Category-level scores
- `fact_organizational_scores`: Organizational scores and IHI
- `fact_gap_analysis`: Improvement priorities

### Dimension Tables (5 core)
- `dim_department`: Academic and administrative units
- `dim_assessment_cycle`: Temporal assessment periods
- `dim_assessment_item`: Baldrige framework items
- `dim_time`: Calendar dimensions
- `dim_assessor`: Evaluator credentials

Deploy schema:
```bash
psql -U postgres -d tqm_database -f database/schema_simplified.sql
```

## Testing

Run comprehensive unit tests:

```bash
# All tests
pytest tests/ -v

# Coverage report
pytest tests/ --cov=src --cov-report=html

# Specific equation tests
pytest tests/test_adli_scoring.py::test_compute_adli_score -v
```

Expected results:
```
tests/test_adli_scoring.py::test_compute_adli_score PASSED
tests/test_adli_scoring.py::test_compute_letci_score PASSED
tests/test_adli_scoring.py::test_category_aggregation PASSED
tests/test_adli_scoring.py::test_organizational_score PASSED
tests/test_adli_scoring.py::test_integration_health_index PASSED
tests/test_adli_scoring.py::test_gap_prioritization PASSED
======================== 6 passed in 0.23s =========================
```

## Performance

Benchmarked on Intel Core i7-9700K, 16GB RAM:

| Operation | Execution Time | Throughput |
|-----------|----------------|------------|
| Single item score (ADLI/LeTCI) | <1ms | 50,000 items/sec |
| Category aggregation (7 items) | <2ms | 25,000 categories/sec |
| Organizational assessment | <15ms | 3,500 orgs/sec |
| IHI computation (18 items) | <3ms | 18,000 computations/sec |
| Gap prioritization (100 items) | <8ms | 6,200 rankings/sec |

**Scalability**: Linear complexity O(n) for all operations; tested up to 10,000 concurrent departments.

## Citation

If you use this framework in academic research, please cite:

```bibtex
@article{edcellence2026,
  title={Computational Transformation of Educational Excellence Assessment: ADLI-LeTCI Integration Framework with Empirical Validation},
  author={Saosing, Rungtiva and Tritham, Chatchai and Kamlangkla, Kanchit and Tritham, Chattabhorn},
  journal={Journal of King Saud University - Computer and Information Sciences},
  year={2026},
  volume={Submitted},
  note={Code: \url{https://github.com/ChatchaiTritham/EdcellenceTQM}}
}
```

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest tests/`)
5. Format code with black (`black src/`)
6. Submit pull request

## License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Rajamangala University of Technology Krungthep

## Contact

For questions, suggestions, or collaboration inquiries:

**Corresponding Author:**
- **Name**: Chatchai Tritham
- **Email**: chatchait66@nu.ac.th
- **Institution**: Faculty of Science and Technology, Rajamangala University of Technology Krungthep, Thailand
- **ORCID**: [0000-0001-7899-228X](https://orcid.org/0000-0001-7899-228X)

**Authors:**
- **Rungtiva Saosing** (First Author)
  - Email: rungtiva.s@mail.rmutt.ac.th
  - Institution: Faculty of Science and Technology, RMUTK, Thailand
  - ORCID: [0009-0007-8713-8190](https://orcid.org/0009-0007-8713-8190)

- **Kanchit Kamlangkla** (Co-Author)
  - Email: kanchit.k@mail.rmutk.ac.th
  - Institution: Faculty of Science and Technology, RMUTK, Thailand

- **Chattabhorn Tritham** (Co-Author, Software Engineer)
  - Email: memodia@live.com
  - Institution: Thammasat School of Engineering (TSE), Thammasat University, Thailand
  - ORCID: [0009-0003-2408-7374](https://orcid.org/0009-0003-2408-7374)

## Acknowledgments

Special thanks to 18 participating departments and 54 trained assessors who contributed to the empirical validation study.

## Version History

- **v1.0.0** (February 2026): Initial public release
  - Six core assessment equations
  - 20-table database schema
  - Empirical validation results
  - Eight Jupyter notebooks
  - Comprehensive test suite

---

**Repository Status**: Production-ready for journal review and educational deployment

**Last Updated**: February 14, 2026
