#!/usr/bin/env python
"""
Generate Publication Figures Example - EdcellenceTQM

This script demonstrates how to generate publication-quality figures
using EdcellenceTQM visualization functions.
"""

from pathlib import Path
from edcellence_tqm.visualization import (
    plot_adli_radar,
    plot_letci_radar,
    plot_category_scores,
    save_figure,
)


def main():
    """Generate example publication figures."""
    print("=" * 60)
    print("EdcellenceTQM - Generate Publication Figures")
    print("=" * 60)
    print()

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Example 1: ADLI Radar Chart
    print("1. Generating ADLI Radar Chart...")
    adli_scores = {
        'Approach': 0.80,
        'Deployment': 0.70,
        'Learning': 0.65,
        'Integration': 0.75,
    }

    fig_adli = plot_adli_radar(
        adli_scores,
        title='Department X - ADLI Process Maturity',
        ci_radius=0.65
    )

    save_figure(fig_adli, output_dir / 'adli_radar', formats=['png', 'pdf'])
    print("   ✓ Saved: adli_radar.png, adli_radar.pdf")

    # Example 2: LeTCI Radar Chart
    print("2. Generating LeTCI Radar Chart...")
    letci_scores = {
        'Level': 0.85,
        'Trend': 0.70,
        'Comparison': 0.65,
        'Integration': 0.80,
    }

    fig_letci = plot_letci_radar(
        letci_scores,
        title='Department X - LeTCI Results Assessment',
        ci_radius=0.70
    )

    save_figure(fig_letci, output_dir / 'letci_radar', formats=['png', 'pdf'])
    print("   ✓ Saved: letci_radar.png, letci_radar.pdf")

    # Example 3: Category Scores Bar Chart
    print("3. Generating Category Scores Chart...")
    category_scores = {
        'Leadership': 85.2,
        'Strategy': 78.6,
        'Customers': 82.1,
        'Measurement': 75.3,
        'Workforce': 80.5,
        'Operations': 68.4,
        'Results': 82.7,
    }

    fig_categories = plot_category_scores(
        category_scores,
        title='Organizational Performance by Category',
        target_score=80.0
    )

    save_figure(fig_categories, output_dir / 'category_scores', formats=['png', 'pdf'])
    print("   ✓ Saved: category_scores.png, category_scores.pdf")

    print()
    print("=" * 60)
    print(f"All figures saved to: {output_dir.absolute()}")
    print("=" * 60)
    print()
    print("Figure Specifications:")
    print("  - Resolution: 300 DPI")
    print("  - PDF: Type-2 embedded fonts")
    print("  - IEEE/Springer compliant")
    print("  - Colorblind-safe palette")


if __name__ == "__main__":
    main()
