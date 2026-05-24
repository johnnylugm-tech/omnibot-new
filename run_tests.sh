#!/bin/bash
cd /Users/johnny/projects/omnibot-new
PYTHONPATH=03-development/src python3 -m pytest tests/test_fr04.py -v 2>&1
echo "EXIT_CODE: $?"