"""
Core assessment algorithms for EdcellenceTQM.

This module provides the core ADLI-LeTCI scoring algorithms and assessment engine
for educational excellence evaluation based on the Baldrige Excellence Framework.

Classes:
    ADLIIndicators: Process item dimensional indicators
    LeTCIIndicators: Results item dimensional indicators
    AssessmentEngine: Complete assessment orchestration

Functions:
    compute_adli_score: Calculate ADLI process score (Equation 1)
    compute_letci_score: Calculate LeTCI results score (Equation 2)
    compute_category_score: Aggregate item scores to category level (Equation 3)
    compute_organizational_score: Calculate overall organizational score (Equation 4)
    compute_integration_health_index: Calculate IHI (Equation 5)
    compute_gap_priority_score: Calculate gap-based priority (Equation 6)
    rank_improvement_priorities: Rank items by priority score
    classify_maturity_level: Map score to Baldrige maturity level

Examples:
    >>> from edcellence_tqm.core import ADLIIndicators, compute_adli_score
    >>> indicators = ADLIIndicators(0.80, 0.70, 0.65, 0.75)
    >>> score = compute_adli_score(indicators)
    >>> print(f"Process Score: {score:.2f}/100")
"""

from edcellence_tqm.core.adli_letci import (
    ADLIIndicators,
    LeTCIIndicators,
    AssessmentEngine,
    compute_adli_score,
    compute_letci_score,
    compute_category_score,
    compute_organizational_score,
    compute_integration_health_index,
    compute_gap_priority_score,
    rank_improvement_priorities,
    classify_maturity_level,
)

__all__ = [
    "ADLIIndicators",
    "LeTCIIndicators",
    "AssessmentEngine",
    "compute_adli_score",
    "compute_letci_score",
    "compute_category_score",
    "compute_organizational_score",
    "compute_integration_health_index",
    "compute_gap_priority_score",
    "rank_improvement_priorities",
    "classify_maturity_level",
]
