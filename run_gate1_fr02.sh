#!/bin/bash
# Gate 1 evaluation script for FR-02

echo "=== RUFF LINTING ==="
ruff check 03-development/src/ 2>&1
echo ""

echo "=== PYRIGHT TYPE CHECKING ==="
pyright 03-development/src/ --outputjson 2>&1
echo ""

echo "=== PYTEST FR-02 TESTS ==="
PYTHONPATH=03-development/src/ python3 -m pytest tests/test_fr02.py -v --cov=03-development/src/omnibot --cov-report=term-missing 2>&1
echo ""

echo "=== COVERAGE SUMMARY ==="
PYTHONPATH=03-development/src/ python3 -m coverage report --rcfile=.coveragerc 2>&1 | head -30