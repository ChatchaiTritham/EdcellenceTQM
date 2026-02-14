"""
EdcellenceTQM: Computational Framework for Educational Excellence Assessment

A computational implementation of the Baldrige Excellence Framework for higher
education quality assessment, featuring integrated ADLI-LeTCI scoring algorithms.

Examples:
    >>> from edcellence_tqm.core import ADLIIndicators, compute_adli_score
    >>> indicators = ADLIIndicators(0.80, 0.70, 0.65, 0.75)
    >>> score = compute_adli_score(indicators)
    >>> print(f"Process Score: {score:.2f}/100")
"""

from edcellence_tqm.__version__ import (
    __version__,
    __author__,
    __email__,
    __license__,
    __copyright__,
)

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]
