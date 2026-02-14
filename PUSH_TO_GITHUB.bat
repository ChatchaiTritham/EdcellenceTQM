@echo off
REM Auto-push to GitHub after repository creation
cd /d "D:\2026-Journal\Rung\GitHub\EdcellenceTQM"

echo ========================================
echo  Pushing EdcellenceTQM to GitHub
echo ========================================
echo.
echo Repository: https://github.com/ChatchaiTritham/EdcellenceTQM
echo Commit: 68c2f1e (34 files, 9,906 insertions)
echo.
echo Files to upload:
echo - 15 publication figures (PNG + PDF, 300 DPI)
echo - JKSU-CIS submission checklist
echo - Manuscript integration templates
echo - Test outputs (21/21 passing)
echo.
echo Pushing now...
echo.

git push -u origin master

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo  SUCCESS! Repository uploaded
    echo ========================================
    echo.
    echo View at: https://github.com/ChatchaiTritham/EdcellenceTQM
    echo.
    echo Next steps:
    echo 1. Insert figures into manuscript
    echo 2. Submit to JKSU-CIS journal
    echo.
) else (
    echo ========================================
    echo  PUSH FAILED
    echo ========================================
    echo.
    echo Make sure you created the repository at:
    echo https://github.com/new
    echo.
)

pause
