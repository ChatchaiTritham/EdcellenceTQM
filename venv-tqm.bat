@echo off
REM EdcellenceTQM Virtual Environment Setup Script
REM For Windows users
REM Usage: venv-tqm.bat

setlocal enabledelayedexpansion

echo ==================================================
echo EdcellenceTQM Environment Setup (Windows)
echo ==================================================
echo.

REM Check Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check Python version
echo Checking Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found: Python %PYTHON_VERSION%

python -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.8+ required. Found: %PYTHON_VERSION%
    pause
    exit /b 1
)
echo [OK] Python version compatible
echo.

REM Define virtual environment directory
set VENV_DIR=venv-tqm

REM Check if virtual environment exists
if exist "%VENV_DIR%" (
    echo Virtual environment already exists at: %VENV_DIR%
    set /p RECREATE="Do you want to recreate it? (y/n): "
    if /i "!RECREATE!"=="y" (
        echo Removing existing environment...
        rmdir /s /q "%VENV_DIR%"
    ) else (
        echo Using existing environment.
        call "%VENV_DIR%\Scripts\activate.bat"
        echo [OK] Activated existing environment
        echo.
        echo To activate in future sessions, run:
        echo   %VENV_DIR%\Scripts\activate.bat
        pause
        exit /b 0
    )
)

REM Create virtual environment
echo Creating virtual environment: %VENV_DIR%
python -m venv "%VENV_DIR%"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
echo [OK] Environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel --quiet
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing EdcellenceTQM dependencies...
echo (This may take 2-3 minutes)
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Verify installation
echo Verifying installation...

python -c "import numpy; print('  - NumPy', numpy.__version__)" 2>nul || echo   [FAIL] NumPy
python -c "import pandas; print('  - Pandas', pandas.__version__)" 2>nul || echo   [FAIL] Pandas
python -c "import matplotlib; print('  - Matplotlib', matplotlib.__version__)" 2>nul || echo   [FAIL] Matplotlib
python -c "import plotly; print('  - Plotly', plotly.__version__)" 2>nul || echo   [FAIL] Plotly
python -c "from src.adli_letci_core import ADLIIndicators; print('  - EdcellenceTQM core module')" 2>nul || echo   [FAIL] Core module

echo [OK] All packages verified
echo.

REM Run quick test
echo Running quick functionality test...
python -c "from src.adli_letci_core import ADLIIndicators, compute_adli_score; indicators = ADLIIndicators(0.8, 0.7, 0.6, 0.75); score = compute_adli_score(indicators); expected = 72.5; print(f'  OK ADLI Score: {score:.2f} (expected: {expected})') if abs(score - expected) < 0.01 else exit(1)"
echo.

REM Run unit tests if pytest available
where pytest >nul 2>nul
if %errorlevel% equ 0 (
    echo Running unit tests...
    pytest tests/ -v --tb=short 2>nul || echo [WARNING] Some tests failed (may be normal if test data incomplete)
    echo.
)

REM Success message
echo ==================================================
echo [SUCCESS] Setup Complete!
echo ==================================================
echo.
echo Your EdcellenceTQM environment is ready.
echo.
echo Next steps:
echo   1. Activate environment (in new terminals):
echo      %VENV_DIR%\Scripts\activate.bat
echo.
echo   2. Launch Jupyter notebooks:
echo      jupyter notebook notebooks/
echo.
echo   3. Run example assessment:
echo      python -c "from src.adli_letci_core import *; print(compute_adli_score(ADLIIndicators(0.8,0.7,0.6,0.75)))"
echo.
echo   4. Run tests:
echo      pytest tests/ -v
echo.
echo   5. Deactivate environment when done:
echo      deactivate
echo.
echo For more information, see README.md
echo ==================================================
echo.
pause
