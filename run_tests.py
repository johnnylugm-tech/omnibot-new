#!/usr/bin/env python3
import sys
import os

# Set up the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '03-development', 'src'))

# Import the test module
import importlib.util
spec = importlib.util.spec_from_file_location("test_fr11", "tests/test_fr11.py")
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

# Print what we have
print("Test module loaded successfully")
print("Functions:", [name for name in dir(test_module) if name.startswith('test_')])