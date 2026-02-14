"""
Pytest configuration for EdcellenceTQM tests.

This file is automatically loaded by pytest and provides
shared fixtures and configuration for all tests.
"""

import pytest
import sys
from pathlib import Path

# Add package root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_adli_indicators():
    """Sample ADLI indicators for testing."""
    from edcellence_tqm.core import ADLIIndicators

    return ADLIIndicators(
        approach=0.80,
        deployment=0.70,
        learning=0.65,
        integration=0.75
    )


@pytest.fixture
def sample_letci_indicators():
    """Sample LeTCI indicators for testing."""
    from edcellence_tqm.core import LeTCIIndicators

    return LeTCIIndicators(
        level=0.85,
        trend=0.70,
        comparison=0.65,
        integration=0.80
    )


@pytest.fixture
def sample_category_scores():
    """Sample category scores for testing."""
    return {
        'Leadership': 85.2,
        'Strategy': 78.6,
        'Customers': 82.1,
        'Measurement': 75.3,
        'Workforce': 80.5,
        'Operations': 68.4,
        'Results': 82.7,
    }


@pytest.fixture
def sample_item_scores():
    """Sample item scores and point values for testing."""
    return {
        'scores': [75.0, 80.0, 70.0, 85.0],
        'point_values': [70, 80, 60, 90],
    }
