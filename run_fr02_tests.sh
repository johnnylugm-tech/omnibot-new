#!/bin/bash
set -e
cd /Users/johnny/projects/omnibot-new
/opt/homebrew/bin/python3 -m pytest tests/test_fr02.py -q --tb=short 2>&1
echo "EXIT_CODE: $?"
git add tests/test_fr02.py
git commit -m "test(RED): failing test for FR-02"