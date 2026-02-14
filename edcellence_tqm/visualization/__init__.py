"""
Publication-quality visualization functions for EdcellenceTQM.

This module provides IEEE/Springer-compliant visualization functions for
academic manuscripts, featuring 300 DPI resolution, Type-2 embedded fonts,
and colorblind-safe palettes.

Classes:
    PublicationStyle: Style configuration for publication-ready figures

Functions:
    figure_context: Context manager for temporary style application
    save_figure: Save figure in multiple formats with publication settings
    set_publication_style: Apply publication style globally
    plot_adli_radar: ADLI process maturity radar chart
    plot_letci_radar: LeTCI results assessment radar chart
    plot_category_scores: Category performance bar chart
    plot_ihi_trajectory: Integration Health Index time series
    plot_gap_priority_3d: Interactive 3D gap priority matrix
    plot_scalability_analysis: Scalability performance analysis
    plot_framework_comparison_heatmap: Category correlation heatmap
    plot_effect_sizes: Effect sizes forest plot

Examples:
    >>> from edcellence_tqm.visualization import plot_adli_radar, save_figure
    >>> scores = {'Approach': 0.80, 'Deployment': 0.70,
    ...           'Learning': 0.65, 'Integration': 0.75}
    >>> fig = plot_adli_radar(scores, title='Department X')
    >>> save_figure(fig, 'output/adli_radar', formats=['png', 'pdf'])
"""

from edcellence_tqm.visualization.charts import (
    PublicationStyle,
    figure_context,
    save_figure,
    set_publication_style,
    plot_adli_radar,
    plot_letci_radar,
    plot_category_scores,
    plot_ihi_trajectory,
    plot_gap_priority_3d,
    plot_scalability_analysis,
    plot_framework_comparison_heatmap,
    plot_effect_sizes,
)

__all__ = [
    "PublicationStyle",
    "figure_context",
    "save_figure",
    "set_publication_style",
    "plot_adli_radar",
    "plot_letci_radar",
    "plot_category_scores",
    "plot_ihi_trajectory",
    "plot_gap_priority_3d",
    "plot_scalability_analysis",
    "plot_framework_comparison_heatmap",
    "plot_effect_sizes",
]
