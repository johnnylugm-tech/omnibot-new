#!/bin/bash
cd /Users/johnny/projects/omnibot-new
export PYTHONPATH=03-development/src
python3 -m pytest tests/test_fr11.py -v --tb=short 2>&1