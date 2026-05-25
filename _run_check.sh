#!/bin/bash
cd /Users/johnny/projects/omnibot-new
ruff check 03-development/src/ > /tmp/ruff_result.txt 2>&1
echo "RUFF_EXIT: $?" >> /tmp/ruff_result.txt
python3 -m pytest tests/test_fr18.py -v >> /tmp/pytest_result.txt 2>&1
echo "PYTEST_EXIT: $?" >> /tmp/pytest_result.txt
