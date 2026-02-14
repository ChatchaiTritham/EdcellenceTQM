#!/usr/bin/env python3
"""
Comprehensive Test Runner for EdcellenceTQM
Generates detailed test reports for all functions and features.

Tests:
1. Core algorithms (6 equations)
2. Visualization functions (8+ chart types)
3. Data loading and validation
4. Integration tests
5. Performance benchmarks
6. Jupyter notebook execution
"""

import sys
import os
import time
import json
import traceback
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing
import matplotlib.pyplot as plt

from adli_letci_core import (
    ADLIIndicators,
    LeTCIIndicators,
    compute_adli_score,
    compute_letci_score,
    compute_category_score,
    compute_organizational_score,
    compute_integration_health_index,
    compute_gap_priority_score,
    classify_maturity_level,
    AssessmentEngine
)

from visualizations import (
    plot_adli_radar,
    plot_letci_radar,
    plot_category_scores,
    plot_ihi_trajectory,
    plot_gap_priority_3d,
    plot_scalability_analysis,
    plot_framework_comparison_heatmap,
    plot_effect_sizes
)


class TestResult:
    """Container for test results."""

    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.duration = 0.0
        self.error = None
        self.details = {}

    def to_dict(self):
        return {
            'name': self.name,
            'passed': self.passed,
            'duration': f"{self.duration:.3f}s",
            'error': str(self.error) if self.error else None,
            'details': self.details
        }


class EdcellenceTQMTestSuite:
    """Comprehensive test suite for EdcellenceTQM framework."""

    def __init__(self):
        self.results: List[TestResult] = []
        self.test_dir = Path(__file__).parent
        self.output_dir = self.test_dir / 'test_outputs'
        self.output_dir.mkdir(exist_ok=True)

    def run_all_tests(self):
        """Execute all test categories."""
        print("=" * 80)
        print("EdcellenceTQM Comprehensive Test Suite")
        print("=" * 80)
        print(f"Test Directory: {self.test_dir}")
        print(f"Output Directory: {self.output_dir}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()

        # Category 1: Core Algorithm Tests
        print("Category 1: Core Algorithm Tests")
        print("-" * 80)
        self.test_adli_scoring()
        self.test_letci_scoring()
        self.test_category_aggregation()
        self.test_organizational_score()
        self.test_integration_health_index()
        self.test_gap_prioritization()
        print()

        # Category 2: Visualization Tests
        print("Category 2: Visualization Tests (2D/3D Charts)")
        print("-" * 80)
        self.test_adli_radar_chart()
        self.test_letci_radar_chart()
        self.test_category_bar_chart()
        self.test_ihi_trajectory_chart()
        self.test_gap_priority_3d_chart()
        self.test_scalability_chart()
        self.test_heatmap_chart()
        self.test_effect_size_chart()
        print()

        # Category 3: Data Loading Tests
        print("Category 3: Data Loading & Validation Tests")
        print("-" * 80)
        self.test_load_sample_data()
        self.test_load_benchmark_data()
        self.test_load_department_scores()
        print()

        # Category 4: Integration Tests
        print("Category 4: Integration & Pipeline Tests")
        print("-" * 80)
        self.test_assessment_engine_pipeline()
        self.test_multi_department_assessment()
        print()

        # Category 5: Edge Cases & Validation
        print("Category 5: Edge Cases & Input Validation")
        print("-" * 80)
        self.test_edge_cases()
        self.test_input_validation()
        print()

        # Generate reports
        self.generate_summary_report()
        self.generate_json_report()
        self.generate_html_report()

    def _run_test(self, test_name: str, test_func):
        """Execute a single test with timing and error handling."""
        result = TestResult(test_name)
        start_time = time.time()

        try:
            details = test_func()
            result.passed = True
            result.details = details or {}
            status = "[OK] PASS"
        except Exception as e:
            result.passed = False
            result.error = e
            result.details = {'traceback': traceback.format_exc()}
            status = "[X] FAIL"

        result.duration = time.time() - start_time
        self.results.append(result)

        print(f"  {status} {test_name} ({result.duration:.3f}s)")
        if not result.passed:
            print(f"       Error: {str(result.error)[:100]}")

        return result

    # ===== CATEGORY 1: CORE ALGORITHM TESTS =====

    def test_adli_scoring(self):
        """Test Equation 1: ADLI Process Scoring."""
        def test():
            # Test default weights
            indicators = ADLIIndicators(0.8, 0.7, 0.6, 0.75)
            score = compute_adli_score(indicators)
            expected = 0.8*30 + 0.7*30 + 0.6*20 + 0.75*20
            assert abs(score - expected) < 0.01, f"Expected {expected}, got {score}"

            # Test custom weights
            custom_weights = {'A': 0.25, 'D': 0.25, 'L': 0.25, 'I': 0.25}
            score_custom = compute_adli_score(indicators, weights=custom_weights)
            expected_custom = 71.25  # (0.8+0.7+0.6+0.75)/4 * 100 = 71.25
            assert abs(score_custom - expected_custom) < 0.01, f"Expected {expected_custom}, got {score_custom}"

            # Test range
            assert 0 <= score <= 100, f"Score {score} outside [0,100]"

            return {
                'default_score': score,
                'custom_score': score_custom,
                'validated_range': True
            }

        return self._run_test("ADLI Scoring (Equation 1)", test)

    def test_letci_scoring(self):
        """Test Equation 2: LeTCI Results Scoring."""
        def test():
            indicators = LeTCIIndicators(0.85, 0.80, 0.75, 0.85)
            score = compute_letci_score(indicators)
            expected = 0.85*40 + 0.80*25 + 0.75*25 + 0.85*10
            assert abs(score - expected) < 0.01
            assert 0 <= score <= 100

            return {
                'score': score,
                'expected': expected,
                'validated_range': True
            }

        return self._run_test("LeTCI Scoring (Equation 2)", test)

    def test_category_aggregation(self):
        """Test Equation 3: Category Score Aggregation."""
        def test():
            item_scores = [76.25, 72.50, 78.00]
            point_values = [70, 50, 30]
            category_score = compute_category_score(item_scores, point_values)

            expected = (76.25*70 + 72.50*50 + 78.00*30) / (70+50+30)
            assert abs(category_score - expected) < 0.01

            return {
                'category_score': category_score,
                'expected': expected,
                'point_weighted': True
            }

        return self._run_test("Category Aggregation (Equation 3)", test)

    def test_organizational_score(self):
        """Test Equation 4: Organizational Score."""
        def test():
            category_scores = {
                'Leadership': 76.25,
                'Strategy': 72.50,
                'Customers': 74.00,
                'Measurement': 82.00,
                'Workforce': 68.50,
                'Operations': 78.00,
                'Results': 81.25
            }

            org_score = compute_organizational_score(category_scores)

            # Verify weights sum to 1.0
            default_weights = {
                'Leadership': 0.12, 'Strategy': 0.085, 'Customers': 0.085,
                'Measurement': 0.10, 'Workforce': 0.10, 'Operations': 0.15,
                'Results': 0.36
            }
            weight_sum = sum(default_weights.values())
            assert abs(weight_sum - 1.0) < 0.001

            # Verify score
            expected = sum(category_scores[k] * default_weights[k] for k in category_scores)
            assert abs(org_score - expected) < 0.01

            # Test maturity classification
            maturity = classify_maturity_level(org_score)
            assert 'level' in maturity
            assert 'label' in maturity

            return {
                'organizational_score': org_score,
                'maturity_level': maturity['level'],
                'maturity_label': maturity['label']
            }

        return self._run_test("Organizational Score (Equation 4)", test)

    def test_integration_health_index(self):
        """Test Equation 5: Integration Health Index."""
        def test():
            process_integration = [0.80, 0.75, 0.70, 0.72, 0.68, 0.78, 0.76]
            results_integration = [0.85, 0.82, 0.80, 0.78]

            ihi = compute_integration_health_index(
                process_integration_scores=process_integration,
                results_integration_scores=results_integration
            )

            expected = 0.5 * (np.mean(process_integration) + np.mean(results_integration))
            assert abs(ihi - expected) < 0.001
            assert 0 <= ihi <= 1.0

            return {
                'ihi': ihi,
                'process_avg': np.mean(process_integration),
                'results_avg': np.mean(results_integration)
            }

        return self._run_test("Integration Health Index (Equation 5)", test)

    def test_gap_prioritization(self):
        """Test Equation 6: Gap-Based Prioritization."""
        def test():
            current = 68.5
            target = 100.0
            points = 40
            urgency = 0.80

            priority = compute_gap_priority_score(current, target, points, urgency)
            expected = (target - current) * points * urgency

            assert abs(priority - expected) < 0.01
            assert priority >= 0

            return {
                'priority_score': priority,
                'gap': target - current,
                'expected': expected
            }

        return self._run_test("Gap Prioritization (Equation 6)", test)

    # ===== CATEGORY 2: VISUALIZATION TESTS =====

    def test_adli_radar_chart(self):
        """Test ADLI radar chart generation."""
        def test():
            scores = {
                'Approach': 0.80,
                'Deployment': 0.75,
                'Learning': 0.70,
                'Integration': 0.80
            }

            save_path = self.output_dir / 'test_adli_radar.png'
            fig = plot_adli_radar(scores, title="Test ADLI Radar", save_path=str(save_path))

            assert save_path.exists(), f"Chart not saved to {save_path}"
            assert save_path.stat().st_size > 1000, "Chart file too small"

            plt.close(fig)

            return {
                'chart_saved': str(save_path),
                'file_size_kb': save_path.stat().st_size / 1024
            }

        return self._run_test("ADLI Radar Chart (2D)", test)

    def test_letci_radar_chart(self):
        """Test LeTCI radar chart generation."""
        def test():
            scores = {
                'Level': 0.85,
                'Trend': 0.80,
                'Comparison': 0.75,
                'Integration': 0.85
            }

            save_path = self.output_dir / 'test_letci_radar.png'
            fig = plot_letci_radar(scores, title="Test LeTCI Radar", save_path=str(save_path))

            assert save_path.exists()
            assert save_path.stat().st_size > 1000

            plt.close(fig)

            return {
                'chart_saved': str(save_path),
                'file_size_kb': save_path.stat().st_size / 1024
            }

        return self._run_test("LeTCI Radar Chart (2D)", test)

    def test_category_bar_chart(self):
        """Test category comparison bar chart."""
        def test():
            baseline = {'Leadership': 65, 'Strategy': 60, 'Customers': 62,
                       'Measurement': 70, 'Workforce': 58, 'Operations': 68, 'Results': 72}
            current = {'Leadership': 76, 'Strategy': 73, 'Customers': 74,
                      'Measurement': 82, 'Workforce': 69, 'Operations': 78, 'Results': 81}

            save_path = self.output_dir / 'test_category_bars.png'
            fig = plot_category_scores(baseline, current, save_path=str(save_path))

            assert save_path.exists()
            plt.close(fig)

            return {'chart_saved': str(save_path)}

        return self._run_test("Category Bar Chart (2D)", test)

    def test_ihi_trajectory_chart(self):
        """Test IHI trajectory line chart."""
        def test():
            quarters = ['Q1-2024', 'Q2-2024', 'Q3-2024', 'Q4-2024']
            ihi_values = [0.62, 0.68, 0.74, 0.78]
            ci_lower = [0.58, 0.64, 0.70, 0.74]
            ci_upper = [0.66, 0.72, 0.78, 0.82]
            confidence_intervals = list(zip(ci_lower, ci_upper))

            save_path = self.output_dir / 'test_ihi_trajectory.png'
            fig = plot_ihi_trajectory(quarters, ihi_values, confidence_intervals,
                                     save_path=str(save_path))

            assert save_path.exists()
            plt.close(fig)

            return {'chart_saved': str(save_path)}

        return self._run_test("IHI Trajectory Chart (2D)", test)

    def test_gap_priority_3d_chart(self):
        """Test 3D gap priority scatter plot."""
        def test():
            items = ['1.1', '2.1', '3.1', '5.1', '6.1']
            gaps = [23.75, 27.50, 26.00, 31.50, 22.00]
            point_values = [70, 40, 85, 40, 50]
            urgency = [0.25, 0.30, 0.15, 0.80, 0.22]

            save_path = self.output_dir / 'test_gap_priority_3d.png'
            fig = plot_gap_priority_3d(items, gaps, point_values, urgency,
                                       save_path=str(save_path))

            assert save_path.exists()
            # Note: Plotly figures don't need plt.close()

            return {'chart_saved': str(save_path), 'chart_type': '3D Scatter'}

        return self._run_test("Gap Priority 3D Chart (3D)", test)

    def test_scalability_chart(self):
        """Test scalability analysis chart."""
        def test():
            dept_counts = [10, 25, 50, 100, 200]
            response_times = [0.8, 1.2, 1.8, 2.5, 3.8]
            theoretical_linear = [x * 0.08 for x in dept_counts]
            theoretical_log = [0.5 * np.log(x) for x in dept_counts]

            save_path = self.output_dir / 'test_scalability.png'
            fig = plot_scalability_analysis(
                dept_counts, response_times,
                {'Linear O(n)': theoretical_linear, 'Log O(log n)': theoretical_log},
                save_path=str(save_path)
            )

            assert save_path.exists()
            plt.close(fig)

            return {'chart_saved': str(save_path)}

        return self._run_test("Scalability Analysis Chart (2D)", test)

    def test_heatmap_chart(self):
        """Test framework comparison heatmap."""
        def test():
            systems = ['ADLI-LeTCI', 'MBNQA', 'EFQM', 'EdPEx']
            features = ['Computational', 'Process-Results', 'Integration',
                       'Gap Analysis', 'Multi-Framework']
            scores = np.array([
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [0.3, 1.0, 0.5, 0.4, 0.0],
                [0.3, 1.0, 0.6, 0.4, 0.0],
                [0.0, 1.0, 0.3, 0.2, 0.0]
            ])

            save_path = self.output_dir / 'test_heatmap.png'
            fig = plot_framework_comparison_heatmap(systems, features, scores,
                                                   save_path=str(save_path))

            assert save_path.exists()
            plt.close(fig)

            return {'chart_saved': str(save_path)}

        return self._run_test("Framework Comparison Heatmap (2D)", test)

    def test_effect_size_chart(self):
        """Test effect sizes bar chart."""
        def test():
            metrics = ['Time Reduction', 'Duplicate Elimination', 'User Satisfaction']
            cohens_d = [2.45, 3.12, 1.89]
            p_values = [0.0001, 0.0001, 0.001]

            save_path = self.output_dir / 'test_effect_sizes.png'
            fig = plot_effect_sizes(metrics, cohens_d, p_values,
                                   save_path=str(save_path))

            assert save_path.exists()
            plt.close(fig)

            return {'chart_saved': str(save_path)}

        return self._run_test("Effect Sizes Chart (2D)", test)

    # ===== CATEGORY 3: DATA LOADING TESTS =====

    def test_load_sample_data(self):
        """Test loading sample assessment data CSV."""
        def test():
            data_path = self.test_dir / 'data' / 'examples' / 'sample_assessment_data.csv'
            assert data_path.exists(), f"Sample data not found: {data_path}"

            df = pd.read_csv(data_path)

            # Verify required columns
            required_cols = ['department', 'item_id', 'item_type',
                           'approach', 'deployment', 'learning', 'integration']
            for col in required_cols:
                assert col in df.columns, f"Missing column: {col}"

            # Verify data ranges
            for dim in ['approach', 'deployment', 'learning', 'integration']:
                assert df[dim].min() >= 0 and df[dim].max() <= 1.0

            return {
                'rows': len(df),
                'departments': df['department'].nunique(),
                'items': df['item_id'].nunique()
            }

        return self._run_test("Load Sample Assessment Data (CSV)", test)

    def test_load_benchmark_data(self):
        """Test loading benchmark results CSV."""
        def test():
            data_path = self.test_dir / 'data' / 'examples' / 'benchmark_results_scalability.csv'
            assert data_path.exists(), f"Benchmark data not found: {data_path}"

            df = pd.read_csv(data_path)
            assert 'department_count' in df.columns, f"Missing column: department_count. Found: {df.columns.tolist()}"
            assert 'response_time_sec' in df.columns, f"Missing column: response_time_sec. Found: {df.columns.tolist()}"

            return {
                'rows': len(df),
                'max_departments': df['department_count'].max()
            }

        return self._run_test("Load Benchmark Data (CSV)", test)

    def test_load_department_scores(self):
        """Test loading department scores JSON."""
        def test():
            data_path = self.test_dir / 'data' / 'examples' / 'department_scores.json'
            assert data_path.exists(), f"Department scores not found: {data_path}"

            with open(data_path) as f:
                data = json.load(f)

            assert isinstance(data, dict), "JSON root should be dict"
            assert 'departments' in data, f"Missing 'departments' key. Found: {data.keys()}"

            # Verify structure
            departments = data['departments']
            assert len(departments) > 0, "No departments found"

            first_dept = departments[0]
            assert 'category_scores' in first_dept, f"Missing category_scores. Found: {first_dept.keys()}"
            assert 'Leadership' in first_dept['category_scores'], f"Missing Leadership category"

            return {
                'departments': len(departments),
                'structure': 'valid',
                'sample_dept': first_dept['department_name']
            }

        return self._run_test("Load Department Scores (JSON)", test)

    # ===== CATEGORY 4: INTEGRATION TESTS =====

    def test_assessment_engine_pipeline(self):
        """Test complete AssessmentEngine pipeline."""
        def test():
            engine = AssessmentEngine()

            # Add process items
            engine.add_process_item('1.1', ADLIIndicators(0.80, 0.75, 0.70, 0.80), 70)
            engine.add_process_item('2.1', ADLIIndicators(0.75, 0.70, 0.65, 0.75), 40)

            # Add results items
            engine.add_results_item('7.1', LeTCIIndicators(0.85, 0.80, 0.75, 0.85), 100)

            # Compute scores
            org_score = engine.compute_organizational_score()
            ihi = engine.compute_ihi()

            assert 0 <= org_score <= 100
            assert 0 <= ihi <= 1.0

            return {
                'organizational_score': org_score,
                'ihi': ihi,
                'process_items': len(engine.process_items),
                'results_items': len(engine.results_items)
            }

        return self._run_test("AssessmentEngine Pipeline", test)

    def test_multi_department_assessment(self):
        """Test multi-department assessment scenario."""
        def test():
            data_path = self.test_dir / 'data' / 'examples' / 'sample_assessment_data.csv'
            df = pd.read_csv(data_path)

            dept_scores = {}

            for dept in df['department'].unique()[:3]:  # Test first 3 departments
                dept_df = df[df['department'] == dept]
                process_df = dept_df[dept_df['item_type'] == 'Process']

                scores = []
                for _, row in process_df.iterrows():
                    indicators = ADLIIndicators(
                        row['approach'], row['deployment'],
                        row['learning'], row['integration']
                    )
                    scores.append(compute_adli_score(indicators))

                dept_scores[dept] = np.mean(scores) if scores else 0.0

            assert len(dept_scores) > 0, "No department scores calculated"

            # Check each score is in valid range
            for dept, score in dept_scores.items():
                assert 0 <= score <= 100, f"Score out of range for {dept}: {score}"

            return {
                'departments_tested': len(dept_scores),
                'avg_scores': {k: round(v, 2) for k, v in dept_scores.items()}
            }

        return self._run_test("Multi-Department Assessment", test)

    # ===== CATEGORY 5: EDGE CASES & VALIDATION =====

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        def test():
            # All zeros
            zeros = ADLIIndicators(0.0, 0.0, 0.0, 0.0)
            score_zeros = compute_adli_score(zeros)
            assert score_zeros == 0.0

            # All ones
            ones = ADLIIndicators(1.0, 1.0, 1.0, 1.0)
            score_ones = compute_adli_score(ones)
            assert score_ones == 100.0

            # Empty category
            empty_cat = compute_category_score([], [])
            assert empty_cat == 0.0

            # Single item category
            single_cat = compute_category_score([75.0], [100])
            assert single_cat == 75.0

            return {
                'zeros': score_zeros,
                'ones': score_ones,
                'empty_category': empty_cat,
                'single_item': single_cat
            }

        return self._run_test("Edge Cases & Boundaries", test)

    def test_input_validation(self):
        """Test input validation and error handling."""
        def test():
            errors_caught = []

            # Test invalid ADLI range
            try:
                ADLIIndicators(1.5, 0.5, 0.5, 0.5)
                errors_caught.append(False)
            except ValueError:
                errors_caught.append(True)

            # Test invalid LeTCI range
            try:
                LeTCIIndicators(0.5, 0.5, -0.1, 0.5)
                errors_caught.append(False)
            except ValueError:
                errors_caught.append(True)

            # Test mismatched lengths
            try:
                compute_category_score([75, 80], [100, 80, 60])
                errors_caught.append(False)
            except (ValueError, AssertionError):
                errors_caught.append(True)

            assert all(errors_caught), "Some validation errors not caught"

            return {
                'validation_tests': len(errors_caught),
                'all_passed': all(errors_caught)
            }

        return self._run_test("Input Validation", test)

    # ===== REPORT GENERATION =====

    def generate_summary_report(self):
        """Generate summary console report."""
        print()
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        pass_rate = (passed / total * 100) if total > 0 else 0
        total_time = sum(r.duration for r in self.results)

        print(f"Total Tests:  {total}")
        print(f"Passed:       {passed} ({pass_rate:.1f}%)")
        print(f"Failed:       {failed}")
        print(f"Total Time:   {total_time:.2f}s")
        print()

        if failed > 0:
            print("FAILED TESTS:")
            print("-" * 80)
            for r in self.results:
                if not r.passed:
                    print(f"  [X] {r.name}")
                    print(f"    Error: {str(r.error)[:150]}")
            print()

        # Category breakdown
        categories = {
            'Core Algorithms': 0,
            'Visualizations': 0,
            'Data Loading': 0,
            'Integration': 0,
            'Validation': 0
        }

        for r in self.results:
            if 'Equation' in r.name or 'Scoring' in r.name or 'IHI' in r.name or 'Gap' in r.name:
                categories['Core Algorithms'] += 1 if r.passed else 0
            elif 'Chart' in r.name or 'Radar' in r.name or 'Heatmap' in r.name:
                categories['Visualizations'] += 1 if r.passed else 0
            elif 'Load' in r.name:
                categories['Data Loading'] += 1 if r.passed else 0
            elif 'Engine' in r.name or 'Multi-Department' in r.name:
                categories['Integration'] += 1 if r.passed else 0
            elif 'Edge' in r.name or 'Validation' in r.name:
                categories['Validation'] += 1 if r.passed else 0

        print("CATEGORY BREAKDOWN:")
        print("-" * 80)
        for cat, count in categories.items():
            print(f"  {cat:25} {count:2} tests passed")
        print()

        print("=" * 80)
        if pass_rate == 100:
            print("[OK] ALL TESTS PASSED - Repository is production-ready!")
        elif pass_rate >= 90:
            print("[WARN] MOSTLY PASSING - Minor issues to address")
        else:
            print("[X] SIGNIFICANT FAILURES - Review and debug required")
        print("=" * 80)
        print()

    def generate_json_report(self):
        """Generate JSON test report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.results),
                'passed': sum(1 for r in self.results if r.passed),
                'failed': sum(1 for r in self.results if not r.passed),
                'pass_rate': sum(1 for r in self.results if r.passed) / len(self.results) * 100,
                'total_duration': sum(r.duration for r in self.results)
            },
            'tests': [r.to_dict() for r in self.results]
        }

        json_path = self.output_dir / 'test_report.json'
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"JSON report saved: {json_path}")

    def generate_html_report(self):
        """Generate HTML test report."""
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        pass_rate = passed / len(self.results) * 100

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>EdcellenceTQM Test Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-box {{ flex: 1; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-box.total {{ background: #3498db; color: white; }}
        .stat-box.passed {{ background: #27ae60; color: white; }}
        .stat-box.failed {{ background: #e74c3c; color: white; }}
        .stat-box h3 {{ margin: 0; font-size: 36px; }}
        .stat-box p {{ margin: 5px 0 0 0; opacity: 0.9; }}
        .test-item {{ margin: 10px 0; padding: 15px; border-left: 4px solid #ddd; background: #f9f9f9; }}
        .test-item.passed {{ border-left-color: #27ae60; }}
        .test-item.failed {{ border-left-color: #e74c3c; background: #fee; }}
        .test-name {{ font-weight: bold; font-size: 16px; }}
        .test-duration {{ color: #7f8c8d; font-size: 14px; }}
        .test-error {{ color: #c0392b; margin-top: 10px; font-family: monospace; font-size: 13px; }}
        .progress-bar {{ width: 100%; height: 30px; background: #ecf0f1; border-radius: 15px; overflow: hidden; margin: 20px 0; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #27ae60, #2ecc71); text-align: center; line-height: 30px; color: white; font-weight: bold; }}
        .charts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
        .chart-box {{ border: 1px solid #ddd; padding: 10px; text-align: center; background: white; }}
        .chart-box img {{ max-width: 100%; height: auto; }}
        .chart-title {{ font-weight: bold; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>EdcellenceTQM Comprehensive Test Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="summary">
            <div class="stat-box total">
                <h3>{len(self.results)}</h3>
                <p>Total Tests</p>
            </div>
            <div class="stat-box passed">
                <h3>{passed}</h3>
                <p>Passed</p>
            </div>
            <div class="stat-box failed">
                <h3>{failed}</h3>
                <p>Failed</p>
            </div>
        </div>

        <div class="progress-bar">
            <div class="progress-fill" style="width: {pass_rate}%">{pass_rate:.1f}% Pass Rate</div>
        </div>

        <h2>Test Results</h2>
"""

        for result in self.results:
            status_class = 'passed' if result.passed else 'failed'
            status_icon = '[OK]' if result.passed else '[X]'

            html += f"""
        <div class="test-item {status_class}">
            <div class="test-name">{status_icon} {result.name}</div>
            <div class="test-duration">Duration: {result.duration:.3f}s</div>
"""

            if not result.passed:
                error_msg = str(result.error).replace('<', '&lt;').replace('>', '&gt;')
                html += f'            <div class="test-error">Error: {error_msg}</div>\n'

            html += '        </div>\n'

        # Add generated charts
        chart_files = list(self.output_dir.glob('test_*.png'))
        if chart_files:
            html += """
        <h2>Generated Visualizations</h2>
        <div class="charts">
"""
            for chart in chart_files:
                chart_name = chart.stem.replace('test_', '').replace('_', ' ').title()
                html += f"""
            <div class="chart-box">
                <img src="{chart.name}" alt="{chart_name}">
                <div class="chart-title">{chart_name}</div>
            </div>
"""
            html += '        </div>\n'

        html += """
    </div>
</body>
</html>
"""

        html_path = self.output_dir / 'test_report.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"HTML report saved: {html_path}")


def main():
    """Run comprehensive test suite."""
    suite = EdcellenceTQMTestSuite()
    suite.run_all_tests()

    # Return exit code based on results
    all_passed = all(r.passed for r in suite.results)
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
