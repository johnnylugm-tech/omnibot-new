#!/usr/bin/env python3
"""Check pytest skip status for test_fr22."""
import subprocess
import sys

result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'tests/test_fr22.py', '-v', '--tb=no'],
    capture_output=True,
    text=True,
    cwd='/Users/johnny/projects/omnibot-new',
    env={**subprocess.os.environ, 'PYTHONPATH': '03-development/src'},
)
output = result.stdout + result.stderr
for line in output.split('\n'):
    if 'SKIPPED' in line or 'skip' in line.lower() or 'passed' in line or 'failed' in line:
        print(line)
print('---RC---', result.returncode)