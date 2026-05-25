#!/usr/bin/env python3
import sys
import os
import subprocess

# Set up path
os.environ['PYTHONPATH'] = os.path.join(os.path.dirname(__file__), '03-development', 'src')

# Run pytest
result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'tests/test_fr19.py', '-q'],
    capture_output=True,
    text=True,
    timeout=120,
    env={**os.environ, 'PYTHONPATH': os.path.join(os.path.dirname(__file__), '03-development', 'src')}
)

# Write output to file
with open('/Users/johnny/projects/omnibot-new/test_output.txt', 'w') as f:
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\nSTDERR:\n")
    f.write(result.stderr)
    f.write("\nRETURN CODE:\n")
    f.write(str(result.returncode))

print("Output written to test_output.txt")
print(f"Return code: {result.returncode}")