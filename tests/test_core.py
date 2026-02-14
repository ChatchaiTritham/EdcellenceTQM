"""
Unit tests for ADLI process scoring (Equation 1).

Tests verify:
- Correct weighted computation
- Range validation [0,100]
- Weight normalization
- Edge cases (all zeros, all ones)
"""

import pytest
import numpy as np
from src.adli_letci_core import (
    ADLIIndicators,
    compute_adli_score
)


class TestADLIIndicators:
    """Test ADLI indicator dataclass validation."""

    def test_valid_indicators(self):
        """Valid indicators in range [0,1] should succeed."""
        indicators = ADLIIndicators(
            approach=0.7,
            deployment=0.8,
            learning=0.6,
            integration=0.75
        )
        assert indicators.approach == 0.7
        assert indicators.deployment == 0.8

    def test_invalid_range_raises_error(self):
        """Indicators outside [0,1] should raise ValueError."""
        with pytest.raises(ValueError, match="must be in range"):
            ADLIIndicators(
                approach=1.5,  # Invalid: > 1
                deployment=0.8,
                learning=0.6,
                integration=0.75
            )


class TestComputeADLIScore:
    """Test ADLI score computation (Equation 1)."""

    def test_default_weights(self):
        """Test with NIST default weights (0.30, 0.30, 0.20, 0.20)."""
        indicators = ADLIIndicators(
            approach=1.0,
            deployment=1.0,
            learning=1.0,
            integration=1.0
        )
        score = compute_adli_score(indicators)
        assert np.isclose(score, 100.0)

    def test_zero_indicators(self):
        """All zero indicators should yield score = 0."""
        indicators = ADLIIndicators(
            approach=0.0,
            deployment=0.0,
            learning=0.0,
            integration=0.0
        )
        score = compute_adli_score(indicators)
        assert np.isclose(score, 0.0)

    def test_custom_weights(self):
        """Test with custom weight distribution."""
        indicators = ADLIIndicators(
            approach=0.8,
            deployment=0.6,
            learning=0.7,
            integration=0.5
        )
        weights = {'A': 0.25, 'D': 0.25, 'L': 0.25, 'I': 0.25}
        score = compute_adli_score(indicators, weights)
        expected = 100 * (0.25*0.8 + 0.25*0.6 + 0.25*0.7 + 0.25*0.5)
        assert np.isclose(score, expected)

    def test_weight_validation(self):
        """Weights not summing to 1.0 should raise ValueError."""
        indicators = ADLIIndicators(0.5, 0.5, 0.5, 0.5)
        invalid_weights = {'A': 0.3, 'D': 0.3, 'L': 0.3, 'I': 0.3}  # Sum = 1.2
        with pytest.raises(ValueError, match="sum to 1.0"):
            compute_adli_score(indicators, invalid_weights)

    def test_range_clipping(self):
        """Score should be clipped to [0,100] even with rounding errors."""
        indicators = ADLIIndicators(1.0, 1.0, 1.0, 1.0)
        score = compute_adli_score(indicators)
        assert 0 <= score <= 100


# Placeholder for 140+ additional tests
# Full test suite includes:
# - LeTCI scoring tests
# - Category aggregation tests
# - Organizational score tests
# - IHI computation tests
# - Gap prioritization tests
# - Integration tests with database
# - Performance benchmark tests
