# Manuscript Figure Integration Guide

**Generated:** 2026-02-14
**Figures:** 15 files (6.0 MB total)
**Format:** PNG (300 DPI) + PDF (Type-2 fonts)

---

## LaTeX Integration Templates

### Figure 1a: ADLI Radar Chart (Single-column)

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/fig1a_adli_radar.pdf}
  \caption{ADLI process maturity profile for the top-performing department
           (Computer Science, n = 8 process items). The dashed circle marks
           the Baldrige excellence threshold (85\%). The dotted inner ring
           indicates the 95\% CI across all 25 departments. \textit{Integration}
           dimension shows largest gap (0.75 vs 0.85 threshold), driving the
           IHI improvement strategy.}
  \label{fig:adli_radar}
\end{figure}
```

### Figure 1b: LeTCI Radar Chart (Single-column)

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/fig1b_letci_radar.pdf}
  \caption{LeTCI results maturity profile. All four dimensions exceed the
           excellence threshold in the post-implementation period (Apr 2024--Mar 2025).
           \textit{Comparison} shows the narrowest margin (0.75), indicating that
           external benchmarking capability continues to develop.}
  \label{fig:letci_radar}
\end{figure}
```

### Figure 2: Category Score Comparison (Double-column)

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/fig2_category_scores.pdf}
  \caption{Baldrige category scores at baseline (Sept 2022) and post-implementation
           (Mar 2025), n = 25 departments. All seven categories exceed the Integrated
           level threshold (score $\geq$ 61) after implementation. Mean improvement:
           +29.9 points (66\% relative gain).}
  \label{fig:category_scores}
\end{figure*}
```

### Figure 3: IHI Trajectory (Double-column)

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/fig3_ihi_trajectory.pdf}
  \caption{Integration Health Index (IHI) trajectory over four assessment quarters
           (Apr 2024--Mar 2025), n = 25 departments. Shaded zones indicate integration
           strength bands (green: strong $>$0.75; amber: moderate 0.60--0.75; red: weak
           $<$0.60). IHI progresses from Moderate to Strong integration by Q4.
           Significance markers: ** \textit{p} $<$ 0.01, *** \textit{p} $<$ 0.001
           vs. Q1 baseline (paired \textit{t}-test). Error band: 95\% CI.}
  \label{fig:ihi_trajectory}
\end{figure*}
```

### Figure 4: 3D Gap Priority Matrix (Interactive)

**Note:** Use HTML for interactive version, PNG for print

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/fig4_gap_priority.png}
  \caption{Three-dimensional gap priority matrix for ten Baldrige assessment items
           (n = 25 departments). Axes: Gap Score (0--100, x), Baldrige Point Value (y),
           Deployment Urgency (0--1, z). Marker size and colour both encode the composite
           Priority Score (Equation 6). Items in the high-gap, high-point, high-urgency
           region represent critical improvement priorities; 7.1 Results and 1.1 Leadership
           rank highest. Interactive version: \url{supplementary/fig4_gap_priority.html}}
  \label{fig:gap_priority}
\end{figure}
```

### Figure 5: Scalability Analysis (Double-column)

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/fig5_scalability.pdf}
  \caption{Scalability performance of the EdcellenceTQM star-schema database across
           institution sizes (10--200 departments). \textit{Left}: query response time
           vs. department count; measured performance (solid blue) remains well below
           both theoretical O(n) (dashed) and O(n log n) (dash-dot) bounds, confirming
           sub-linear scaling attributed to query caching. \textit{Right}: relative
           response time increase vs. 10-department baseline; 200-department load yields
           only +374\% overhead, acceptable for real-time dashboard use (threshold: $<$5 s).}
  \label{fig:scalability}
\end{figure*}
```

### Figure 6: Framework Comparison Heatmap (Double-column)

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=0.9\textwidth]{figures/fig6_heatmap.pdf}
  \caption{Comparative feature matrix of six TQM software systems. Symbols:
           $\bullet$ full support, $\triangle$ partial support, $\circ$ absent.
           EdcellenceTQM is the only system providing native ADLI/LeTCI scoring,
           an Integration Health Index, and automated gap prioritisation---three
           capabilities directly linked to Baldrige Level 4--5 maturity advancement.}
  \label{fig:framework_comparison}
\end{figure*}
```

### Figure 7: Effect Sizes (Double-column)

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=0.9\textwidth]{figures/fig7_effect_sizes.pdf}
  \caption{Cohen's \textit{d} effect sizes for six operational metrics
           (n = 25 departments, pre- vs. post-implementation, paired \textit{t}-tests).
           Horizontal bars show 95\% CI. Zone shading: blue = large (d $>$ 0.8),
           amber = very large (d $>$ 2.0), red = extreme (d $>$ 4.0). All effects
           are statistically significant (*** \textit{p} $<$ 0.001 for top four metrics;
           ** \textit{p} $<$ 0.01 for remaining two), substantially exceeding the
           large-effect threshold (\textit{d} = 0.8) in every metric.}
  \label{fig:effect_sizes}
\end{figure*}
```

---

## Word/DOCX Integration

### Steps for Each Figure:

1. **Insert Figure:**
   - Insert → Picture
   - Navigate to: `D:\2026-Journal\Rung\GitHub\EdcellenceTQM\figures\publication\`
   - Select PNG file (300 DPI for high quality)

2. **Format Size:**
   - Right-click → Format Picture → Size
   - Lock aspect ratio: ✅
   - Width:
     - Single-column: 3.5 inches (Fig 1a, 1b, 4)
     - Double-column: 7.0 inches (Fig 2, 3, 5, 6, 7)

3. **Add Caption:**
   - References → Insert Caption
   - Label: Figure
   - Position: Below selected item
   - Paste caption text from templates above

### Figure Captions for Word:

**Figure 1a.** ADLI process maturity profile for the top-performing department (Computer Science, n = 8 process items). The dashed circle marks the Baldrige excellence threshold (85%). The dotted inner ring indicates the 95% CI across all 25 departments. *Integration* dimension shows largest gap (0.75 vs 0.85 threshold), driving the IHI improvement strategy.

**Figure 1b.** LeTCI results maturity profile. All four dimensions exceed the excellence threshold in the post-implementation period (Apr 2024–Mar 2025). *Comparison* shows the narrowest margin (0.75), indicating that external benchmarking capability continues to develop.

**Figure 2.** Baldrige category scores at baseline (Sept 2022) and post-implementation (Mar 2025), n = 25 departments. All seven categories exceed the Integrated level threshold (score ≥ 61) after implementation. Mean improvement: +29.9 points (66% relative gain).

**Figure 3.** Integration Health Index (IHI) trajectory over four assessment quarters (Apr 2024–Mar 2025), n = 25 departments. Shaded zones indicate integration strength bands (green: strong >0.75; amber: moderate 0.60–0.75; red: weak <0.60). IHI progresses from Moderate to Strong integration by Q4. Significance markers: ** *p* < 0.01, *** *p* < 0.001 vs. Q1 baseline (paired *t*-test). Error band: 95% CI.

**Figure 4.** Three-dimensional gap priority matrix for ten Baldrige assessment items (n = 25 departments). Axes: Gap Score (0–100, x), Baldrige Point Value (y), Deployment Urgency (0–1, z). Marker size and colour both encode the composite Priority Score (Equation 6). Items in the high-gap, high-point, high-urgency region represent critical improvement priorities; 7.1 Results and 1.1 Leadership rank highest.

**Figure 5.** Scalability performance of the EdcellenceTQM star-schema database across institution sizes (10–200 departments). *Left*: query response time vs. department count; measured performance (solid blue) remains well below both theoretical O(n) (dashed) and O(n log n) (dash-dot) bounds, confirming sub-linear scaling attributed to query caching. *Right*: relative response time increase vs. 10-department baseline; 200-department load yields only +374% overhead, acceptable for real-time dashboard use (threshold: <5 s).

**Figure 6.** Comparative feature matrix of six TQM software systems. Symbols: ● full support, △ partial support, ○ absent. EdcellenceTQM is the only system providing native ADLI/LeTCI scoring, an Integration Health Index, and automated gap prioritisation—three capabilities directly linked to Baldrige Level 4–5 maturity advancement.

**Figure 7.** Cohen's *d* effect sizes for six operational metrics (n = 25 departments, pre- vs. post-implementation, paired *t*-tests). Horizontal bars show 95% CI. Zone shading: blue = large (d > 0.8), amber = very large (d > 2.0), red = extreme (d > 4.0). All effects are statistically significant (*** *p* < 0.001 for top four metrics; ** *p* < 0.01 for remaining two), substantially exceeding the large-effect threshold (*d* = 0.8) in every metric.

---

## File Specifications

| Figure | Filename | Format | Size (inches) | Resolution | File Size |
|--------|----------|--------|---------------|------------|-----------|
| Fig 1a | fig1a_adli_radar | PNG + PDF | 3.5 × 3.5 | 300 DPI | 142 KB (PNG) |
| Fig 1b | fig1b_letci_radar | PNG + PDF | 3.5 × 3.5 | 300 DPI | 148 KB (PNG) |
| Fig 2 | fig2_category_scores | PNG + PDF | 7.0 × 4.5 | 300 DPI | 109 KB (PNG) |
| Fig 3 | fig3_ihi_trajectory | PNG + PDF | 7.0 × 3.5 | 300 DPI | 145 KB (PNG) |
| Fig 4 | fig4_gap_priority | HTML + PNG | Variable | Interactive | 4.7 MB (HTML) |
| Fig 5 | fig5_scalability | PNG + PDF | 7.0 × 3.8 | 300 DPI | 162 KB (PNG) |
| Fig 6 | fig6_heatmap | PNG + PDF | 7.0 × dynamic | 300 DPI | 107 KB (PNG) |
| Fig 7 | fig7_effect_sizes | PNG + PDF | 7.0 × dynamic | 300 DPI | 111 KB (PNG) |

**Total:** 15 files, 6.0 MB

---

## Quality Checklist

✅ **Resolution:** All PNG files at 300 DPI
✅ **Fonts:** PDF files use Type-2 embedded fonts (IEEE compliant)
✅ **Sizes:** IEEE column widths (3.5" single, 7.0" double)
✅ **Colors:** Wong 2011 colorblind-safe palette
✅ **Layout:** No overlapping elements (28 anti-overlap features)
✅ **Standards:** IEEE/Springer publication-ready

---

## Supplementary Materials

**Interactive Figure 4:**
- Upload `fig4_gap_priority.html` as supplementary material
- Reference in caption: "Interactive version available online"
- Readers can rotate 3D view and inspect individual data points

**Code Repository:**
- GitHub: https://github.com/ChatchaiTritham/EdcellenceTQM
- DOI: (Create via Zenodo after upload)
- Reference: "Implementation code available at [DOI]"

---

**Generated:** 2026-02-14
**Status:** Ready for JKSU-CIS submission
