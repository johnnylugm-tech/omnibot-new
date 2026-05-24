#!/bin/bash
cd /Users/johnny/projects/omnibot-new
/opt/homebrew/bin/python3 -m pytest tests/test_fr02.py -q --tb=short
exit $?