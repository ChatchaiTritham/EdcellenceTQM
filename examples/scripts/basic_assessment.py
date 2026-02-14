#!/usr/bin/env python
"""
Basic Assessment Example - EdcellenceTQM

This script demonstrates the basic usage of EdcellenceTQM for
educational quality assessment using ADLI-LeTCI scoring.
"""

from edcellence_tqm.core import (
    ADLIIndicators,
    LeTCIIndicators,
    compute_adli_score,
    compute_letci_score,
    classify_maturity_level,
)


def main():
    """Run basic assessment example."""
    print("=" * 60)
    print("EdcellenceTQM - Basic Assessment Example")
    print("=" * 60)
    print()

    # Example 1: ADLI Process Assessment
    print("1. ADLI Process Assessment")
    print("-" * 40)

    # Create ADLI indicators
    adli = ADLIIndicators(
        approach=0.80,      # Systematic methods (80%)
        deployment=0.70,    # Implementation scope (70%)
        learning=0.65,      # Evaluation cycles (65%)
        integration=0.75    # Organizational alignment (75%)
    )

    # Compute ADLI score
    adli_score = compute_adli_score(adli)

    print(f"ADLI Indicators:")
    print(f"  Approach:    {adli.approach:.2f}")
    print(f"  Deployment:  {adli.deployment:.2f}")
    print(f"  Learning:    {adli.learning:.2f}")
    print(f"  Integration: {adli.integration:.2f}")
    print(f"\nProcess Score: {adli_score:.2f}/100")
    print()

    # Example 2: LeTCI Results Assessment
    print("2. LeTCI Results Assessment")
    print("-" * 40)

    # Create LeTCI indicators
    letci = LeTCIIndicators(
        level=0.85,         # Current performance (85%)
        trend=0.70,         # Improvement rate (70%)
        comparison=0.65,    # vs. Benchmarks (65%)
        integration=0.80    # Cross-category (80%)
    )

    # Compute LeTCI score
    letci_score = compute_letci_score(letci)

    print(f"LeTCI Indicators:")
    print(f"  Level:       {letci.level:.2f}")
    print(f"  Trend:       {letci.trend:.2f}")
    print(f"  Comparison:  {letci.comparison:.2f}")
    print(f"  Integration: {letci.integration:.2f}")
    print(f"\nResults Score: {letci_score:.2f}/100")
    print()

    # Example 3: Maturity Classification
    print("3. Maturity Level Classification")
    print("-" * 40)

    test_scores = [45.0, 62.5, 74.0, 88.5]
    for score in test_scores:
        maturity = classify_maturity_level(score)
        print(f"Score {score:5.1f} → Level {maturity['level']}: {maturity['label']}")

    print()
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
