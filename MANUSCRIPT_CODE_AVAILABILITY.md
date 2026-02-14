# Manuscript Code Availability Statement

## For Journal Submission (JKSU-CIS)

### Code Availability Section

Add this section to your manuscript (typically before References):

---

## Code Availability

The complete computational framework, including all assessment algorithms, visualization functions, and empirical validation data, is publicly available as open-source software:

**Repository**: https://github.com/ChatchaiTritham/EdcellenceTQM
**License**: MIT License
**Language**: Python 3.8+
**Dependencies**: Listed in `requirements.txt`

The repository includes:
- Six core assessment equations (ADLI-LeTCI scoring algorithms)
- Publication-quality visualization functions (300 DPI, IEEE/Springer compliant)
- Database schema (PostgreSQL, 20 tables)
- Eight Jupyter notebooks for reproducing all analyses
- Comprehensive test suite (21 tests, 100% passing)
- Sample datasets from the 12-month longitudinal study

All figures in this manuscript were generated using `notebooks/08_Publication_Figures.ipynb` and can be reproduced by running:

```bash
git clone https://github.com/ChatchaiTritham/EdcellenceTQM.git
cd EdcellenceTQM
pip install -r requirements.txt
jupyter notebook notebooks/08_Publication_Figures.ipynb
```

---

### Alternative Format (Shorter Version)

For journals with strict word limits:

---

## Code and Data Availability

The computational framework and all analysis code are available at:
https://github.com/ChatchaiTritham/EdcellenceTQM (MIT License)

All figures can be reproduced using the provided Jupyter notebooks and sample datasets.

---

## LaTeX Citation Formats

### In-text Citation

```latex
The framework is implemented as open-source software
\cite{edcellence2026code} using Python 3.8+ and PostgreSQL 13+.
```

### BibTeX Entry

```bibtex
@misc{edcellence2026code,
  author       = {Anonymized for Review},
  title        = {{EdcellenceTQM}: Computational Framework for Educational
                  Excellence Assessment},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/ChatchaiTritham/EdcellenceTQM}},
  note         = {MIT License}
}
```

### Article Citation (After Publication)

```bibtex
@article{edcellence2026,
  title   = {Computational Transformation of Educational Excellence Assessment:
             ADLI-LeTCI Integration Framework with Empirical Validation},
  author  = {Anonymized for Review},
  journal = {Journal of King Saud University - Computer and Information Sciences},
  year    = {2026},
  volume  = {TBD},
  number  = {TBD},
  pages   = {TBD},
  doi     = {TBD},
  url     = {https://github.com/ChatchaiTritham/EdcellenceTQM}
}
```

## Footnote Format

If the journal requires a footnote instead of a separate section:

```latex
\footnote{Code available at: \url{https://github.com/ChatchaiTritham/EdcellenceTQM}}
```

## Word/Docx Format

### Code Availability Section

```
Code Availability

The complete computational framework is publicly available at:
https://github.com/ChatchaiTritham/EdcellenceTQM

License: MIT License
Language: Python 3.8+
Documentation: Complete API reference and Jupyter notebooks included

All figures in this manuscript can be reproduced using the provided code and sample datasets.
```

## JKSU-CIS Specific Requirements

Based on JKSU-CIS author guidelines:

1. **Software Availability**: Include GitHub URL in the manuscript body
2. **Reproducibility**: Provide step-by-step instructions in README
3. **Licensing**: Clearly state MIT License
4. **Documentation**: Include API reference and usage examples
5. **Testing**: Document test coverage (21/21 tests passing)

✅ **All requirements met**: Repository is publication-ready

## Supplementary Materials Reference

In manuscript text:

```latex
Detailed algorithm implementations and performance benchmarks are provided
in the Supplementary Materials and open-source repository\footnote{
\url{https://github.com/ChatchaiTritham/EdcellenceTQM}}.
```

## Figure Captions with Code Reference

Example of referencing reproducible figures:

```latex
\caption{ADLI process maturity profile showing strengths in Approach (0.80)
and Integration (0.75), with improvement opportunities in Deployment (0.70)
and Learning (0.60). Generated using \texttt{plot\_adli\_radar()} function
from the EdcellenceTQM framework
(\url{https://github.com/ChatchaiTritham/EdcellenceTQM}).}
```

## README Badge (Optional)

Add to README.md for professional appearance:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Citation](https://img.shields.io/badge/cite-BibTeX-blue)](https://github.com/ChatchaiTritham/EdcellenceTQM#citation)
[![JKSU-CIS](https://img.shields.io/badge/Published%20in-JKSU--CIS-green)](https://doi.org/MANUSCRIPT_DOI)
```

(Will update with actual DOIs after publication)

---

**Last Updated**: February 14, 2026
**Repository**: https://github.com/ChatchaiTritham/EdcellenceTQM
