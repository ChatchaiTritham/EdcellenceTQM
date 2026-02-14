#!/usr/bin/env python3
"""
EdcellenceTQM Environment Setup (Cross-Platform)

This script provides a cross-platform Python-based setup for EdcellenceTQM.
Works on Windows, Linux, and macOS.

Usage:
    python setup_environment.py
    python setup_environment.py --jupyter  # Also launch Jupyter
    python setup_environment.py --test     # Run tests after setup
"""

import sys
import subprocess
import platform
import os
from pathlib import Path

# ANSI color codes (work on most terminals)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def disable():
        """Disable colors for Windows cmd (if needed)"""
        Colors.GREEN = Colors.YELLOW = Colors.RED = ''
        Colors.BLUE = Colors.BOLD = Colors.END = ''

# Disable colors on Windows cmd (keep for PowerShell)
if platform.system() == 'Windows' and 'TERM' not in os.environ:
    Colors.disable()


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    symbol = "[OK]" if platform.system() == 'Windows' else "✓"
    print(f"{Colors.GREEN}{symbol} {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    symbol = "[ERROR]" if platform.system() == 'Windows' else "✗"
    print(f"{Colors.RED}{symbol} {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    symbol = "[WARN]" if platform.system() == 'Windows' else "⚠"
    print(f"{Colors.YELLOW}{symbol} {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    symbol = "[INFO]" if platform.system() == 'Windows' else "ℹ"
    print(f"{Colors.BLUE}{symbol} {text}{Colors.END}")


def check_python_version():
    """Check if Python version is >= 3.8"""
    print_info("Checking Python version...")
    version = sys.version_info

    if version < (3, 8):
        print_error(f"Python 3.8+ required. Found: {version.major}.{version.minor}.{version.micro}")
        return False

    print_success(f"Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_venv(venv_dir="venv-tqm"):
    """Create virtual environment"""
    venv_path = Path(venv_dir)

    if venv_path.exists():
        print_warning(f"Virtual environment already exists: {venv_dir}")
        response = input("Recreate it? (y/n): ").strip().lower()
        if response == 'y':
            print_info("Removing existing environment...")
            import shutil
            shutil.rmtree(venv_path)
        else:
            print_info("Using existing environment")
            return venv_path

    print_info(f"Creating virtual environment: {venv_dir}")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print_success("Virtual environment created")
        return venv_path
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return None


def get_venv_python(venv_path):
    """Get path to Python executable in venv"""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def upgrade_pip(python_exe):
    """Upgrade pip in virtual environment"""
    print_info("Upgrading pip...")
    try:
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
            check=True,
            capture_output=True
        )
        print_success("pip upgraded")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to upgrade pip: {e}")
        return False


def install_dependencies(python_exe):
    """Install requirements.txt"""
    print_info("Installing EdcellenceTQM dependencies...")
    print_info("(This may take 2-3 minutes)")

    try:
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True
        )
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False


def verify_installation(python_exe):
    """Verify package installation"""
    print_info("Verifying installation...")

    packages = [
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("matplotlib", "Matplotlib"),
        ("plotly", "Plotly"),
        ("scipy", "SciPy"),
        ("seaborn", "Seaborn")
    ]

    all_ok = True
    for pkg_import, pkg_name in packages:
        try:
            result = subprocess.run(
                [str(python_exe), "-c", f"import {pkg_import}; print({pkg_import}.__version__)"],
                check=True,
                capture_output=True,
                text=True
            )
            version = result.stdout.strip()
            print(f"  {Colors.GREEN}✓{Colors.END} {pkg_name} {version}")
        except subprocess.CalledProcessError:
            print(f"  {Colors.RED}✗{Colors.END} {pkg_name} - import failed")
            all_ok = False

    # Test core module
    try:
        subprocess.run(
            [str(python_exe), "-c", "from src.adli_letci_core import ADLIIndicators"],
            check=True,
            capture_output=True
        )
        print(f"  {Colors.GREEN}✓{Colors.END} EdcellenceTQM core module")
    except subprocess.CalledProcessError:
        print(f"  {Colors.RED}✗{Colors.END} EdcellenceTQM core module - import failed")
        all_ok = False

    if all_ok:
        print_success("All packages verified")
    return all_ok


def run_quick_test(python_exe):
    """Run quick functionality test"""
    print_info("Running quick functionality test...")

    test_code = """
from src.adli_letci_core import ADLIIndicators, compute_adli_score
indicators = ADLIIndicators(0.8, 0.7, 0.6, 0.75)
score = compute_adli_score(indicators)
expected = 72.5
if abs(score - expected) < 0.01:
    print(f"ADLI Score: {score:.2f} (expected: {expected})")
else:
    print(f"Test failed: got {score:.2f}, expected {expected}")
    exit(1)
"""

    try:
        result = subprocess.run(
            [str(python_exe), "-c", test_code],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"  {Colors.GREEN}✓{Colors.END} {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Test failed: {e}")
        return False


def run_tests(python_exe):
    """Run pytest unit tests"""
    print_info("Running unit tests...")

    try:
        result = subprocess.run(
            [str(python_exe), "-m", "pytest", "tests/", "-v", "--tb=short"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print_success("All tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print_warning("Some tests failed (may be normal if test data incomplete)")
        return False


def launch_jupyter(python_exe):
    """Launch Jupyter notebook server"""
    print_info("Launching Jupyter notebook server...")
    print_info("Press Ctrl+C to stop the server")

    try:
        subprocess.run(
            [str(python_exe), "-m", "jupyter", "notebook", "notebooks/"],
            check=True
        )
    except KeyboardInterrupt:
        print_info("\nJupyter server stopped")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to launch Jupyter: {e}")


def print_next_steps(venv_dir):
    """Print next steps for user"""
    print_header("Setup Complete!")

    print("Your EdcellenceTQM environment is ready.\n")
    print(f"{Colors.BOLD}Next steps:{Colors.END}\n")

    # Activation command
    if platform.system() == "Windows":
        activate_cmd = f"{venv_dir}\\Scripts\\activate.bat"
    else:
        activate_cmd = f"source {venv_dir}/bin/activate"

    print(f"  1. Activate environment (in new terminals):")
    print(f"     {Colors.GREEN}{activate_cmd}{Colors.END}\n")

    print(f"  2. Launch Jupyter notebooks:")
    print(f"     {Colors.GREEN}jupyter notebook notebooks/{Colors.END}\n")

    print(f"  3. Run example assessment:")
    print(f"     {Colors.GREEN}python -c \"from src.adli_letci_core import *; "
          f"print(compute_adli_score(ADLIIndicators(0.8,0.7,0.6,0.75)))\"{Colors.END}\n")

    print(f"  4. Run tests:")
    print(f"     {Colors.GREEN}pytest tests/ -v{Colors.END}\n")

    print(f"  5. Deactivate environment when done:")
    print(f"     {Colors.GREEN}deactivate{Colors.END}\n")

    print("For more information, see README.md")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")


def main():
    """Main setup routine"""
    import argparse

    parser = argparse.ArgumentParser(description="EdcellenceTQM Environment Setup")
    parser.add_argument("--jupyter", action="store_true", help="Launch Jupyter after setup")
    parser.add_argument("--test", action="store_true", help="Run tests after setup")
    parser.add_argument("--venv-dir", default="venv-tqm", help="Virtual environment directory name")
    args = parser.parse_args()

    print_header("EdcellenceTQM Environment Setup")
    print_info(f"Platform: {platform.system()} {platform.release()}")

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create virtual environment
    venv_path = create_venv(args.venv_dir)
    if not venv_path:
        sys.exit(1)

    # Get venv Python executable
    python_exe = get_venv_python(venv_path)
    if not python_exe.exists():
        print_error(f"Virtual environment Python not found: {python_exe}")
        sys.exit(1)

    # Upgrade pip
    if not upgrade_pip(python_exe):
        print_warning("pip upgrade failed, continuing anyway...")

    # Install dependencies
    if not install_dependencies(python_exe):
        sys.exit(1)

    # Verify installation
    if not verify_installation(python_exe):
        print_warning("Some packages failed verification")

    # Run quick test
    run_quick_test(python_exe)

    # Run full tests if requested
    if args.test:
        run_tests(python_exe)

    # Print next steps
    print_next_steps(args.venv_dir)

    # Launch Jupyter if requested
    if args.jupyter:
        launch_jupyter(python_exe)


if __name__ == "__main__":
    main()
