"""
EdcellenceTQM Visualization Module
====================================

Publication-quality 2D/3D visualizations for JKSU-CIS manuscript.
IEEE/Springer double-column standard: 7.0 in wide, 300 DPI, Times New Roman 10 pt.

This module generates all figures referenced in the paper:
- Figure 1: ADLI-LeTCI Radar Charts (process maturity)
- Figure 2: Category Score Distributions
- Figure 3: Integration Health Index (IHI) Trajectory
- Figure 4: Gap Priority Matrix (3D visualization)
- Figure 5: Scalability Analysis (performance curves)
- Figure 6: Comparative Framework Analysis

Features:
- Publication-ready figures (300 DPI PNG + embedded-font PDF)
- IEEE/Springer double-column widths (single=3.5", double=7.0")
- No overlapping elements (constrained_layout, dynamic offsets)
- Interactive 3D visualizations via Plotly
- Colorblind-friendly Wong 2011 palette
- Unified PublicationStyle class for consistent appearance

Author: EdcellenceTQM Development Team
License: MIT
Version: 2.0.0
"""

import contextlib
import textwrap
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from scipy import stats

warnings.filterwarnings('ignore')


# ============================================================================
# Publication Style — IEEE / Springer Double-Column Standard
# ============================================================================

class PublicationStyle:
    """
    Centralised IEEE/Springer publication style settings.

    Column widths follow IEEE transactions double-column format:
      single = 3.5 in  (one column)
      double = 7.0 in  (full page width, two columns side-by-side)
      full   = 9.0 in  (landscape or supplementary)

    Usage:
        PublicationStyle.apply()          # apply globally
        with figure_context('double'):    # apply temporarily
            fig = plot_adli_radar(...)
    """

    COLUMN_WIDTHS: Dict[str, float] = {
        'single': 3.5,
        'double': 7.0,
        'full':   9.0,
    }

    COLORS: Dict[str, str] = {
        'blue':   '#0173B2',
        'orange': '#DE8F05',
        'green':  '#029E73',
        'red':    '#CC78BC',
        'purple': '#CA9161',
        'gray':   '#949494',
        'black':  '#000000',
    }

    CATEGORY_COLORS: Dict[str, str] = {
        'Leadership':  '#0173B2',
        'Strategy':    '#DE8F05',
        'Customers':   '#029E73',
        'Measurement': '#CC78BC',
        'Workforce':   '#CA9161',
        'Operations':  '#949494',
        'Results':     '#000000',
    }

    RCPARAMS: Dict = {
        # Font
        'font.family':           'serif',
        'font.serif':            ['Times New Roman', 'DejaVu Serif'],
        'font.size':             10,           # IEEE body: 10 pt
        'mathtext.fontset':      'stix',       # matches Times New Roman math
        # Axes labels & titles
        'axes.labelsize':        10,
        'axes.titlesize':        10,
        'axes.titleweight':      'bold',
        'axes.labelweight':      'bold',
        # Ticks
        'xtick.labelsize':       8,
        'ytick.labelsize':       8,
        'xtick.major.pad':       4,
        'ytick.major.pad':       4,
        # Legend
        'legend.fontsize':       8,
        'legend.framealpha':     0.9,
        'legend.fancybox':       False,
        'legend.edgecolor':      '0.6',
        # Lines / markers
        'lines.linewidth':       1.5,
        'lines.markersize':      5.0,
        # Grid & spines
        'axes.linewidth':        0.6,
        'grid.linewidth':        0.4,
        'grid.alpha':            0.35,
        'axes.spines.top':       False,
        'axes.spines.right':     False,
        # Save
        'savefig.dpi':           300,
        'savefig.pad_inches':    0.05,
        'figure.constrained_layout.use': True,
    }

    @classmethod
    def apply(cls) -> None:
        """Apply publication-quality rcParams globally."""
        plt.style.use('default')
        plt.rcParams.update(cls.RCPARAMS)
        sns.set_palette(list(cls.COLORS.values()))


# Back-compat alias exposed in __all__
COLORS = PublicationStyle.COLORS
CATEGORY_COLORS = PublicationStyle.CATEGORY_COLORS


# ============================================================================
# Context Manager & Save Helper
# ============================================================================

@contextlib.contextmanager
def figure_context(layout: str = 'double', extra_rcparams: Optional[Dict] = None):
    """
    Context manager: apply PublicationStyle temporarily and restore on exit.

    Args:
        layout:          'single' (3.5"), 'double' (7.0"), or 'full' (9.0")
        extra_rcparams:  Optional additional rcParams to merge

    Yields:
        PublicationStyle class (for access to COLORS, COLUMN_WIDTHS, etc.)

    Example:
        with figure_context('double') as PS:
            fig, ax = plt.subplots(figsize=(PS.COLUMN_WIDTHS['double'], 3.5))
    """
    previous = dict(plt.rcParams)
    try:
        PublicationStyle.apply()
        if extra_rcparams:
            plt.rcParams.update(extra_rcparams)
        yield PublicationStyle
    finally:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            plt.rcParams.update(previous)


def save_figure(
    fig: plt.Figure,
    path: Union[str, Path],
    formats: Optional[List[str]] = None,
    dpi: int = 300,
    pad_inches: float = 0.05,
) -> List[Path]:
    """
    Save a matplotlib figure to PNG and/or PDF with IEEE-compliant settings.

    PDF uses pdf.fonttype=42 (TrueType / Type 2) so fonts are fully embedded,
    satisfying IEEE and Springer submission requirements.

    Args:
        fig:        matplotlib Figure object
        path:       Base path without extension (e.g. Path('figures/fig1_adli'))
        formats:    List of formats, default ['png', 'pdf']
        dpi:        Resolution for raster formats (default 300)
        pad_inches: Padding around figure (default 0.05)

    Returns:
        List of Path objects for each file written

    Example:
        paths = save_figure(fig, 'figures/fig1_adli', formats=['png', 'pdf'])
    """
    if formats is None:
        formats = ['png', 'pdf']

    base = Path(path)
    base.parent.mkdir(parents=True, exist_ok=True)

    saved: List[Path] = []
    for fmt in formats:
        out = base.with_suffix(f'.{fmt}')
        if fmt == 'pdf':
            with plt.rc_context({'pdf.fonttype': 42, 'ps.fonttype': 42}):
                fig.savefig(out, format='pdf', bbox_inches='tight',
                            pad_inches=pad_inches)
        else:
            fig.savefig(out, dpi=dpi, bbox_inches='tight',
                        format=fmt, pad_inches=pad_inches)
        saved.append(out)
    return saved


# Legacy helper — preserved for backward compatibility
def set_publication_style() -> None:
    """Apply publication-quality matplotlib style (legacy entry point)."""
    PublicationStyle.apply()


# ============================================================================
# Figure 1a: ADLI Radar Chart
# ============================================================================

def plot_adli_radar(
    adli_scores: Dict[str, float],
    title: str = "ADLI Process Maturity",
    save_path: Optional[str] = None,
    ci_radius: Optional[float] = None,
) -> plt.Figure:
    """
    Generate IEEE-compliant ADLI radar chart (single-column, 3.5×3.5 in).

    Args:
        adli_scores:  Dict with keys 'Approach','Deployment','Learning','Integration'
                      Values in [0, 1]
        title:        Chart title
        save_path:    Optional path to save figure (PNG)
        ci_radius:    Optional confidence-interval ring radius in [0,1]

    Returns:
        matplotlib Figure

    Example:
        >>> scores = {'Approach': 0.80, 'Deployment': 0.70,
        ...           'Learning': 0.60, 'Integration': 0.75}
        >>> fig = plot_adli_radar(scores, save_path='figures/fig1a_adli.pdf')
    """
    with figure_context('single') as PS:
        W = PS.COLUMN_WIDTHS['single']
        categories = ['Approach', 'Deployment', 'Learning', 'Integration']
        values = [adli_scores.get(cat, 0.0) for cat in categories]
        values += values[:1]

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(
            figsize=(W, W),
            subplot_kw=dict(projection='polar'),
            constrained_layout=True,
        )

        # Confidence interval ring
        if ci_radius is not None:
            ci_vals = [ci_radius] * (len(categories) + 1)
            ax.fill(angles, ci_vals, alpha=0.10, color=PS.COLORS['blue'])
            ax.plot(angles, ci_vals, ':', linewidth=0.8, color=PS.COLORS['blue'], alpha=0.5)

        # Data polygon
        ax.plot(angles, values, 'o-', linewidth=1.5,
                color=PS.COLORS['blue'], label='Current', markersize=5)
        ax.fill(angles, values, alpha=0.20, color=PS.COLORS['blue'])

        # Excellence threshold
        target = [0.85] * (len(categories) + 1)
        ax.plot(angles, target, '--', linewidth=1.2, color=PS.COLORS['red'],
                label='Excellence (85%)')

        # Formatting
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=8)
        ax.tick_params(pad=6)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], size=7)
        ax.grid(True, linewidth=0.4, alpha=0.4)
        ax.set_title(title, size=10, pad=14, weight='bold')

        # Legend below chart — avoids overlap with spider web
        fig.legend(
            loc='lower center',
            bbox_to_anchor=(0.5, -0.06),
            ncol=2,
            framealpha=0.9,
            fontsize=7,
            fancybox=False,
        )

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig


# ============================================================================
# Figure 1b: LeTCI Radar Chart
# ============================================================================

def plot_letci_radar(
    letci_scores: Dict[str, float],
    title: str = "LeTCI Results Maturity",
    save_path: Optional[str] = None,
    ci_radius: Optional[float] = None,
) -> plt.Figure:
    """
    Generate IEEE-compliant LeTCI radar chart (single-column, 3.5×3.5 in).

    Args:
        letci_scores: Dict with keys 'Level','Trend','Comparison','Integration'
                      Values in [0, 1]
        title:        Chart title
        save_path:    Optional path to save figure (PNG)
        ci_radius:    Optional confidence-interval ring radius in [0,1]

    Returns:
        matplotlib Figure

    Example:
        >>> scores = {'Level': 0.85, 'Trend': 0.80,
        ...           'Comparison': 0.75, 'Integration': 0.85}
        >>> fig = plot_letci_radar(scores, save_path='figures/fig1b_letci.pdf')
    """
    with figure_context('single') as PS:
        W = PS.COLUMN_WIDTHS['single']
        categories = ['Level', 'Trend', 'Comparison', 'Integration']
        values = [letci_scores.get(cat, 0.0) for cat in categories]
        values += values[:1]

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(
            figsize=(W, W),
            subplot_kw=dict(projection='polar'),
            constrained_layout=True,
        )

        if ci_radius is not None:
            ci_vals = [ci_radius] * (len(categories) + 1)
            ax.fill(angles, ci_vals, alpha=0.10, color=PS.COLORS['orange'])
            ax.plot(angles, ci_vals, ':', linewidth=0.8, color=PS.COLORS['orange'], alpha=0.5)

        ax.plot(angles, values, 'o-', linewidth=1.5,
                color=PS.COLORS['orange'], label='Current', markersize=5)
        ax.fill(angles, values, alpha=0.20, color=PS.COLORS['orange'])

        target = [0.85] * (len(categories) + 1)
        ax.plot(angles, target, '--', linewidth=1.2, color=PS.COLORS['red'],
                label='Excellence (85%)')

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=8)
        ax.tick_params(pad=6)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], size=7)
        ax.grid(True, linewidth=0.4, alpha=0.4)
        ax.set_title(title, size=10, pad=14, weight='bold')

        fig.legend(
            loc='lower center',
            bbox_to_anchor=(0.5, -0.06),
            ncol=2,
            framealpha=0.9,
            fontsize=7,
            fancybox=False,
        )

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig


# ============================================================================
# Figure 2: Category Score Comparison
# ============================================================================

def plot_category_scores(
    baseline_scores: Dict[str, float],
    current_scores: Dict[str, float],
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plot category score comparison (baseline vs post-implementation).

    IEEE double-column: 7.0×4.5 in.  X-labels are wrapped to avoid rotation
    overlap; value offsets are proportional (not hardcoded).

    Args:
        baseline_scores: Category names → baseline scores [0, 100]
        current_scores:  Category names → post scores [0, 100]
        save_path:       Optional save path

    Returns:
        matplotlib Figure

    Example:
        >>> baseline = {'Leadership': 45, 'Strategy': 38, 'Customers': 42,
        ...             'Measurement': 35, 'Workforce': 40, 'Operations': 37, 'Results': 30}
        >>> current  = {'Leadership': 75, 'Strategy': 68, 'Customers': 72,
        ...             'Measurement': 65, 'Workforce': 70, 'Operations': 67, 'Results': 60}
        >>> fig = plot_category_scores(baseline, current, 'figures/fig2_categories.pdf')
    """
    with figure_context('double') as PS:
        W = PS.COLUMN_WIDTHS['double']
        categories = [
            'Leadership', 'Strategy', 'Customers', 'Measurement',
            'Workforce', 'Operations', 'Results',
        ]

        base_vals = [baseline_scores.get(c, 0) for c in categories]
        curr_vals = [current_scores.get(c, 0)  for c in categories]

        x = np.arange(len(categories))
        width = 0.34

        fig, ax = plt.subplots(figsize=(W, 4.5), constrained_layout=True)

        bars1 = ax.bar(x - width / 2, base_vals, width,
                       label='Baseline (Sept 2022)',
                       color=PS.COLORS['gray'], alpha=0.75,
                       edgecolor='black', linewidth=0.5)
        bars2 = ax.bar(x + width / 2, curr_vals, width,
                       label='Post-Implementation (Mar 2025)',
                       color=PS.COLORS['blue'], alpha=0.90,
                       edgecolor='black', linewidth=0.5)

        # Value labels — offset proportional to y-range to avoid overlap
        y_range = 108
        offset = y_range * 0.012

        for bar in bars1:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, h + offset,
                    f'{h:.0f}', ha='center', va='bottom', size=7)

        for bar in bars2:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, h + offset,
                    f'{h:.0f}', ha='center', va='bottom', size=7, weight='bold')

        # Excellence threshold
        ax.axhline(y=61, color=PS.COLORS['red'], linestyle='--', linewidth=1.2,
                   label='Integrated Threshold (61)', alpha=0.80)

        ax.set_xlabel('Baldrige Categories', weight='bold')
        ax.set_ylabel('Score (0–100)', weight='bold')
        ax.set_title('Category Score Improvement (n = 25 departments)', weight='bold')
        ax.set_xticks(x)

        # Wrapped x-tick labels — no rotation, no overlap
        wrapped = [textwrap.fill(c, width=10) for c in categories]
        ax.set_xticklabels(wrapped, rotation=0, ha='center')

        ax.legend(loc='upper left', framealpha=0.9)
        ax.set_ylim(0, 108)
        ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))
        ax.grid(axis='y', which='major', alpha=0.30, linewidth=0.4)
        ax.grid(axis='y', which='minor', alpha=0.15, linewidth=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig


# ============================================================================
# Figure 3: Integration Health Index Trajectory
# ============================================================================

def plot_ihi_trajectory(
    quarters: List[int],
    ihi_values: List[float],
    confidence_intervals: Optional[List[Tuple[float, float]]] = None,
    significance_markers: Optional[List[str]] = None,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plot IHI progression over time with axhspan integration zones.

    IEEE double-column: 7.0×3.5 in.  Annotations appear on first and last
    data points only to avoid label clutter on inner points.

    Args:
        quarters:             List of quarter numbers [1, 2, …, N]
        ihi_values:           IHI values in [0, 1]
        confidence_intervals: Optional list of (lower, upper) CI tuples
        significance_markers: Optional per-quarter significance strings
                              (e.g. ['', '', '**', '***'])
        save_path:            Optional save path

    Returns:
        matplotlib Figure

    Example:
        >>> quarters = [1, 2, 3, 4]
        >>> ihi = [0.61, 0.68, 0.74, 0.78]
        >>> ci  = [(0.57,0.65),(0.64,0.72),(0.70,0.78),(0.74,0.82)]
        >>> fig = plot_ihi_trajectory(quarters, ihi, ci, save_path='fig3.pdf')
    """
    with figure_context('double') as PS:
        W = PS.COLUMN_WIDTHS['double']
        fig, ax = plt.subplots(figsize=(W, 3.5), constrained_layout=True)

        # Zone shading (axhspan) — cleaner than threshold lines
        ax.axhspan(0.75, 1.00, alpha=0.08, color=PS.COLORS['green'],
                   label='Strong (>0.75)', zorder=0)
        ax.axhspan(0.60, 0.75, alpha=0.08, color=PS.COLORS['orange'],
                   label='Moderate (0.60–0.75)', zorder=0)
        ax.axhspan(0.00, 0.60, alpha=0.08, color=PS.COLORS['red'],
                   label='Weak (<0.60)', zorder=0)

        # Confidence band
        if confidence_intervals:
            lower = [ci[0] for ci in confidence_intervals]
            upper = [ci[1] for ci in confidence_intervals]
            ax.fill_between(quarters, lower, upper,
                            alpha=0.18, color=PS.COLORS['blue'],
                            label='95% CI')

        # Main trajectory
        ax.plot(quarters, ihi_values, 'o-', linewidth=1.8, markersize=6,
                color=PS.COLORS['blue'], label='IHI', zorder=3)

        # Annotate first and last point only
        for idx in [0, len(quarters) - 1]:
            q, v = quarters[idx], ihi_values[idx]
            stars = ''
            if significance_markers and idx < len(significance_markers):
                stars = significance_markers[idx]
            ax.annotate(
                f'{v:.2f}{stars}',
                xy=(q, v),
                xytext=(0, 9),
                textcoords='offset points',
                ha='center', size=7, weight='bold',
                zorder=4,
            )

        ax.set_xlabel('Assessment Quarter', weight='bold')
        ax.set_ylabel('Integration Health Index (IHI)', weight='bold')
        ax.set_title('Cross-Category Integration Progression (n = 25 departments)',
                     weight='bold')
        ax.set_xticks(quarters)
        ax.set_xticklabels([f'Q{q}' for q in quarters])
        ax.set_ylim(0.50, 0.90)
        ax.legend(loc='lower right', ncol=2, framealpha=0.9)
        ax.grid(True, which='major', alpha=0.30, linewidth=0.4)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig


# ============================================================================
# Figure 4: 3D Gap Priority Matrix
# ============================================================================

def plot_gap_priority_3d(
    items: List[str],
    gap_scores: List[float],
    point_values: List[int],
    deployment_urgency: List[float],
    save_path: Optional[str] = None,
) -> go.Figure:
    """
    Create interactive Plotly 3D scatter plot of gap priorities.

    For journal-quality static output, use save_path (requires kaleido).
    The Plotly figure is returned for interactive HTML embedding in notebooks.

    Args:
        items:              Item IDs (e.g. ['1.1', '2.1', …])
        gap_scores:         Gap scores (0–100)
        point_values:       Baldrige point allocations
        deployment_urgency: Deployment gaps [0, 1]
        save_path:          Optional path (.html → Plotly HTML, .png → static)

    Returns:
        plotly Figure

    Example:
        >>> items   = ['1.1', '2.1', '3.2', '4.1', '5.1']
        >>> gaps    = [55, 32, 48, 28, 40]
        >>> points  = [70, 45, 50, 40, 45]
        >>> urgency = [0.8, 0.5, 0.7, 0.4, 0.6]
        >>> fig = plot_gap_priority_3d(items, gaps, points, urgency, 'fig4.html')
    """
    priority_scores = [g * p * u for g, p, u in
                       zip(gap_scores, point_values, deployment_urgency)]

    fig = go.Figure(data=[go.Scatter3d(
        x=gap_scores,
        y=point_values,
        z=deployment_urgency,
        mode='markers+text',
        marker=dict(
            size=[max(4, p / 100) for p in priority_scores],
            color=priority_scores,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title=dict(text='Priority Score', font=dict(size=11)),
                thickness=14,
                len=0.70,
            ),
            line=dict(width=1, color='black'),
        ),
        text=items,
        textposition='top center',
        textfont=dict(size=9, color='black'),
        hovertemplate=(
            '<b>%{text}</b><br>'
            'Gap Score: %{x:.0f}<br>'
            'Point Value: %{y}<br>'
            'Deployment Urgency: %{z:.2f}<br>'
            '<extra></extra>'
        ),
    )])

    fig.update_layout(
        title=dict(
            text='3D Gap Priority Matrix (n = 25 departments)',
            font=dict(size=14, family='Times New Roman'),
        ),
        scene=dict(
            xaxis=dict(
                title=dict(text='Gap Score (0–100)',
                           font=dict(size=11, family='Times New Roman')),
            ),
            yaxis=dict(
                title=dict(text='Baldrige Point Value',
                           font=dict(size=11, family='Times New Roman')),
            ),
            zaxis=dict(
                title=dict(text='Deployment Urgency (0–1)',
                           font=dict(size=11, family='Times New Roman')),
            ),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3)),
        ),
        width=860,
        height=660,
        font=dict(family='Times New Roman', size=10),
        margin=dict(l=0, r=0, b=0, t=50),
    )

    if save_path:
        p = Path(save_path)
        if p.suffix.lower() == '.html':
            fig.write_html(str(p))
        else:
            try:
                fig.write_image(str(p), scale=2)
            except Exception:
                # kaleido not installed — skip static export
                pass

    return fig


# ============================================================================
# Figure 5: Scalability Analysis
# ============================================================================

def plot_scalability_analysis(
    department_counts: List[int],
    response_times: List[float],
    theoretical_curves: Optional[Dict[str, List[float]]] = None,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plot scalability performance with theoretical complexity curves.

    IEEE double-column: 7.0×3.8 in, two panels (ratio 1.6:1).
    Label offsets are proportional so they never collide with bar tops.

    Args:
        department_counts:  Department sizes [10, 25, 50, 100, 200]
        response_times:     Measured response times (any unit)
        theoretical_curves: Optional dict {'Linear O(n)': [...], ...}
        save_path:          Optional save path

    Returns:
        matplotlib Figure

    Example:
        >>> depts  = [10, 25, 50, 100, 200]
        >>> times  = [0.82, 1.23, 1.87, 2.54, 3.89]
        >>> curves = {'Linear O(n)': [0.82, 2.05, 4.10, 8.20, 16.4]}
        >>> fig = plot_scalability_analysis(depts, times, curves, 'fig5.pdf')
    """
    with figure_context('double') as PS:
        W = PS.COLUMN_WIDTHS['double']
        fig, (ax1, ax2) = plt.subplots(
            1, 2,
            figsize=(W, 3.8),
            gridspec_kw={'width_ratios': [1.6, 1]},
            constrained_layout=True,
        )

        # ── Left: response time vs department count ──────────────────────
        ax1.plot(
            department_counts, response_times,
            'o-', linewidth=1.8, markersize=6,
            color=PS.COLORS['blue'], label='Measured (Star-Schema)',
        )

        if theoretical_curves:
            linestyles = ['--', '-.', ':']
            curve_colors = [PS.COLORS['red'], PS.COLORS['green'], PS.COLORS['purple']]
            for i, (name, vals) in enumerate(theoretical_curves.items()):
                ax1.plot(
                    department_counts, vals,
                    linestyles[i % 3], linewidth=1.5,
                    color=curve_colors[i % 3],
                    label=f'Theoretical {name}', alpha=0.75,
                )

        ax1.set_xlabel('Number of Departments', weight='bold')
        ax1.set_ylabel('Response Time (s)', weight='bold')
        ax1.set_title('Scalability: Query Performance', weight='bold')
        ax1.legend(loc='upper left', fontsize=7)
        ax1.set_ylim(0, max(response_times) * 1.15)
        ax1.grid(True, which='major', alpha=0.30, linewidth=0.4)

        # ── Right: percentage increase ────────────────────────────────────
        baseline = response_times[0]
        pct_increase = [(rt / baseline - 1) * 100 for rt in response_times]
        max_pct = max(pct_increase) if max(pct_increase) > 0 else 1

        ax2.bar(range(len(department_counts)), pct_increase,
                width=0.60, color=PS.COLORS['orange'],
                alpha=0.85, edgecolor='black', linewidth=0.5)

        # Proportional offsets (3% of y-range above bar, 8% below for label)
        y_range = max_pct * 1.30
        top_offset    = y_range * 0.03
        bottom_offset = y_range * 0.08

        for i, (dept, pct) in enumerate(zip(department_counts, pct_increase)):
            ax2.text(i, pct + top_offset,
                     f'+{pct:.0f}%', ha='center', va='bottom', size=7, weight='bold')
            ax2.text(i, -bottom_offset,
                     f'n={dept}', ha='center', va='top', size=7)

        ax2.set_xlabel('Department Scale', weight='bold')
        ax2.set_ylabel('Response Time Increase (%)', weight='bold')
        ax2.set_title('Relative Performance', weight='bold')
        ax2.set_xticks(range(len(department_counts)))

        scale_factors = [dc / department_counts[0] for dc in department_counts]
        ax2.set_xticklabels(
            ['Baseline' if i == 0 else f'{scale_factors[i]:.0f}×'
             for i in range(len(department_counts))],
            fontsize=7,
        )
        ax2.axhline(y=0, color='black', linewidth=0.6)
        ax2.set_ylim(-y_range * 0.18, y_range)
        ax2.grid(axis='y', which='major', alpha=0.30, linewidth=0.4)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig


# ============================================================================
# Figure 6: Comparative Framework Heatmap
# ============================================================================

def plot_framework_comparison_heatmap(
    systems: List[str],
    features: List[str],
    scores: np.ndarray,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Create heatmap comparing TQM systems across features.

    IEEE double-column: 7.0×dynamic in.  Cell symbol size scales with number
    of features to prevent overflow.  All four spines are shown at 0.6 pt
    to frame the heatmap cells.

    Args:
        systems:  List of system names (rows)
        features: List of feature names (columns)
        scores:   2D ndarray (systems × features), values in {0, 0.5, 1}
        save_path: Optional save path

    Returns:
        matplotlib Figure

    Example:
        >>> systems  = ['MasterControl', 'Qualaris', 'EdcellenceTQM']
        >>> features = ['ADLI/LeTCI', 'Multi-Framework', 'Real-time', 'Auto-route']
        >>> scores   = np.array([[0, 0, 1, 0],[0, 0.5, 1, 0.5],[1, 1, 1, 1]])
        >>> fig = plot_framework_comparison_heatmap(systems, features, scores)
    """
    with figure_context('double') as PS:
        W = PS.COLUMN_WIDTHS['double']
        n_feat = len(features)
        n_sys  = len(systems)

        # Dynamic height: ~0.55 in per row + header space
        height = max(2.8, n_sys * 0.55 + 1.2)
        # Dynamic symbol size: shrink when many features
        sym_size = min(14, max(8, int(56 / n_feat)))

        fig, ax = plt.subplots(figsize=(W, height), constrained_layout=True)

        im = ax.imshow(scores, cmap='RdYlGn', aspect='equal', vmin=0, vmax=1)

        ax.set_xticks(np.arange(n_feat))
        ax.set_yticks(np.arange(n_sys))
        ax.set_xticklabels(features, rotation=45, ha='right', fontsize=8)
        ax.set_yticklabels(systems, fontsize=8)

        # Symbol annotations
        for i in range(n_sys):
            for j in range(n_feat):
                v = scores[i, j]
                if v == 0:
                    sym, col = '○', 'darkred'
                elif v == 0.5:
                    sym, col = '△', 'darkorange'
                else:
                    sym, col = '●', 'darkgreen'
                ax.text(j, i, sym, ha='center', va='center',
                        color=col, size=sym_size, weight='bold')

        # Separator lines between rows and columns (0.4 pt)
        for i in range(n_sys - 1):
            ax.axhline(i + 0.5, color='white', linewidth=0.8)
        for j in range(n_feat - 1):
            ax.axvline(j + 0.5, color='white', linewidth=0.8)

        # Restore all four spines to frame the grid
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.6)

        cbar = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
        cbar.set_ticks([0, 0.5, 1])
        cbar.set_ticklabels(['Absent (○)', 'Partial (△)', 'Full (●)'])
        cbar.ax.tick_params(labelsize=7)

        ax.set_title('Comparative System Feature Analysis', weight='bold')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig


# ============================================================================
# Statistical Utilities: Effect Sizes
# ============================================================================

def plot_effect_sizes(
    metrics: List[str],
    cohens_d: List[float],
    p_values: List[float],
    ci_lower: Optional[List[float]] = None,
    ci_upper: Optional[List[float]] = None,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plot Cohen's d effect sizes with significance markers and optional CI bars.

    IEEE double-column: 7.0×dynamic in.  Label offsets are proportional to
    x-range so they never overlap bar ends or each other.

    Args:
        metrics:   Metric names (y-axis)
        cohens_d:  Cohen's d values
        p_values:  Corresponding p-values
        ci_lower:  Optional lower bounds of 95% CI for each metric
        ci_upper:  Optional upper bounds of 95% CI for each metric
        save_path: Optional save path

    Returns:
        matplotlib Figure

    Example:
        >>> metrics  = ['Time', 'Accuracy', 'Compliance']
        >>> d_vals   = [3.8, 2.5, 1.9]
        >>> p_vals   = [0.0001, 0.001, 0.02]
        >>> fig = plot_effect_sizes(metrics, d_vals, p_vals)
    """
    with figure_context('double') as PS:
        W = PS.COLUMN_WIDTHS['double']
        n = len(metrics)
        height = max(2.8, n * 0.52 + 1.2)

        fig, ax = plt.subplots(figsize=(W, height), constrained_layout=True)

        colors = [
            PS.COLORS['red']    if d > 4.0 else
            PS.COLORS['orange'] if d > 2.0 else
            PS.COLORS['blue']
            for d in cohens_d
        ]

        # Build xerr for CI bars
        xerr = None
        if ci_lower is not None and ci_upper is not None:
            xerr = [
                [max(0, d - lo) for d, lo in zip(cohens_d, ci_lower)],
                [max(0, hi - d) for d, hi in zip(cohens_d, ci_upper)],
            ]

        ax.barh(metrics, cohens_d,
                xerr=xerr,
                color=colors,
                alpha=0.85,
                edgecolor='black', linewidth=0.5,
                error_kw=dict(elinewidth=1.0, capsize=3, capthick=0.8,
                              ecolor='#333333'))

        # Threshold zones (axvspan)
        x_max = max(cohens_d) * 1.35
        ax.axvspan(0.8, 2.0, alpha=0.06, color=PS.COLORS['blue'],   zorder=0)
        ax.axvspan(2.0, 4.0, alpha=0.06, color=PS.COLORS['orange'], zorder=0)
        ax.axvspan(4.0, x_max, alpha=0.06, color=PS.COLORS['red'],  zorder=0)

        ax.axvline(x=0.8, color=PS.COLORS['gray'], linestyle='--',
                   linewidth=0.9, alpha=0.7, label='Large (d>0.8)')
        ax.axvline(x=2.0, color=PS.COLORS['orange'], linestyle='--',
                   linewidth=0.9, alpha=0.7, label='Very Large (d>2.0)')

        # Significance labels — proportional offset (2% of x-range)
        x_range = x_max
        offset = x_range * 0.02

        for i, (d, p) in enumerate(zip(cohens_d, p_values)):
            stars = (
                '***' if p < 0.001 else
                '**'  if p < 0.01  else
                '*'   if p < 0.05  else ''
            )
            ax.text(d + offset, i, f'{d:.2f} {stars}'.strip(),
                    va='center', ha='left', size=7, weight='bold')

        ax.set_xlabel("Cohen's d (Effect Size)", weight='bold')
        ax.set_title("Effect Sizes: Baseline vs Post-Implementation", weight='bold')
        ax.set_xlim(0, x_max)
        ax.legend(loc='lower right', fontsize=7)
        ax.grid(axis='x', which='major', alpha=0.30, linewidth=0.4)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig


# ============================================================================
# Module Metadata
# ============================================================================

__version__ = '2.0.0'
__all__ = [
    # Style classes / helpers
    'PublicationStyle',
    'figure_context',
    'save_figure',
    'set_publication_style',
    # Color dicts
    'COLORS',
    'CATEGORY_COLORS',
    # Chart functions
    'plot_adli_radar',
    'plot_letci_radar',
    'plot_category_scores',
    'plot_ihi_trajectory',
    'plot_gap_priority_3d',
    'plot_scalability_analysis',
    'plot_framework_comparison_heatmap',
    'plot_effect_sizes',
]