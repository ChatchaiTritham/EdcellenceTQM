#!/bin/bash
# EdcellenceTQM — Quick GitHub Upload Script
# Run this script to upload all changes to GitHub

cd "D:\2026-Journal\Rung\GitHub\EdcellenceTQM"

echo "=================================="
echo "EdcellenceTQM GitHub Upload"
echo "=================================="

# Stage all important files
echo ""
echo "[1/5] Staging modified files..."
git add src/visualizations.py
git add src/adli_letci_core.py
git add requirements.txt
git add README.md

echo "[2/5] Staging notebooks..."
git add notebooks/

echo "[3/5] Staging documentation..."
git add INSTALLATION.md
git add TESTING_REPORT.md
git add VISUALIZATION_VERIFICATION.md
git add PRODUCTION_READY_SUMMARY.md
git add GITHUB_UPLOAD_GUIDE.md

echo "[4/5] Staging test suite..."
git add test_runner.py
git add setup_environment.py
git add data/

# Remove deprecated files
git rm -f DEPLOYMENT_GUIDE.md 2>/dev/null || true

echo "[5/5] Showing status..."
git status

echo ""
echo "=================================="
echo "Ready to commit!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Review changes above"
echo "2. Run: git commit -m 'Commercial-grade upgrade for IEEE/Springer standards'"
echo "3. Run: git push origin master"
echo ""
echo "Or use the full commit message from GITHUB_UPLOAD_GUIDE.md"
