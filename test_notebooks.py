#!/usr/bin/env python3
"""
Jupyter Notebook Testing Script
Tests all notebooks for execution errors and output generation.
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime


class NotebookTester:
    """Test Jupyter notebooks for execution errors."""

    def __init__(self, notebooks_dir='notebooks'):
        self.notebooks_dir = Path(notebooks_dir)
        self.results = []

    def test_notebook(self, notebook_path):
        """Test a single notebook execution."""
        print(f"\nTesting: {notebook_path.name}")
        print("-" * 60)

        start_time = datetime.now()

        try:
            # Execute notebook using nbconvert
            cmd = [
                sys.executable, '-m', 'jupyter', 'nbconvert',
                '--to', 'notebook',
                '--execute',
                '--ExecutePreprocessor.timeout=300',
                '--output', f'{notebook_path.stem}_executed.ipynb',
                str(notebook_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )

            duration = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                print(f"  ✓ PASS ({duration:.1f}s)")
                # Check output file
                output_file = notebook_path.parent / f'{notebook_path.stem}_executed.ipynb'
                if output_file.exists():
                    # Count cells with outputs
                    with open(output_file) as f:
                        nb = json.load(f)
                        cells_with_output = sum(
                            1 for cell in nb.get('cells', [])
                            if cell.get('outputs') and len(cell['outputs']) > 0
                        )
                    print(f"  Cells with output: {cells_with_output}")
                    output_file.unlink()  # Clean up

                self.results.append({
                    'notebook': notebook_path.name,
                    'status': 'PASS',
                    'duration': duration,
                    'cells_with_output': cells_with_output
                })
                return True

            else:
                print(f"  ✗ FAIL ({duration:.1f}s)")
                error_msg = result.stderr[-500:] if result.stderr else "Unknown error"
                print(f"  Error: {error_msg}")
                self.results.append({
                    'notebook': notebook_path.name,
                    'status': 'FAIL',
                    'duration': duration,
                    'error': error_msg
                })
                return False

        except subprocess.TimeoutExpired:
            print(f"  ✗ TIMEOUT (>10 minutes)")
            self.results.append({
                'notebook': notebook_path.name,
                'status': 'TIMEOUT',
                'duration': 600
            })
            return False

        except Exception as e:
            print(f"  ✗ ERROR: {str(e)}")
            self.results.append({
                'notebook': notebook_path.name,
                'status': 'ERROR',
                'error': str(e)
            })
            return False

    def test_all_notebooks(self):
        """Test all notebooks in the directory."""
        notebooks = sorted(self.notebooks_dir.glob('*.ipynb'))

        if not notebooks:
            print(f"No notebooks found in {self.notebooks_dir}")
            return False

        print("=" * 80)
        print(f"Testing {len(notebooks)} Jupyter Notebooks")
        print("=" * 80)

        for notebook in notebooks:
            self.test_notebook(notebook)

        # Summary
        print("\n" + "=" * 80)
        print("NOTEBOOK TEST SUMMARY")
        print("=" * 80)

        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = len(self.results) - passed
        total_time = sum(r['duration'] for r in self.results)

        print(f"Total:    {len(self.results)}")
        print(f"Passed:   {passed}")
        print(f"Failed:   {failed}")
        print(f"Duration: {total_time:.1f}s")
        print()

        if failed > 0:
            print("FAILED NOTEBOOKS:")
            for r in self.results:
                if r['status'] != 'PASS':
                    print(f"  ✗ {r['notebook']}: {r['status']}")
        else:
            print("✓ ALL NOTEBOOKS PASSED")

        print("=" * 80)

        return failed == 0

    def generate_report(self, output_file='notebook_test_report.json'):
        """Generate JSON report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total': len(self.results),
            'passed': sum(1 for r in self.results if r['status'] == 'PASS'),
            'failed': len(self.results) - sum(1 for r in self.results if r['status'] == 'PASS'),
            'results': self.results
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nReport saved: {output_file}")


def main():
    """Run notebook tests."""
    # Check if jupyter is installed
    try:
        subprocess.run(
            [sys.executable, '-m', 'jupyter', '--version'],
            capture_output=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: Jupyter not installed. Install with: pip install jupyter nbconvert")
        return 1

    tester = NotebookTester()
    success = tester.test_all_notebooks()
    tester.generate_report()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
