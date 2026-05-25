#!/usr/bin/env python3
import subprocess, sys, os

env = {**os.environ, 'PYTHONPATH': os.path.join(os.getcwd(), '03-development', 'src')}
result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'tests/test_fr22.py', '-v', '--tb=short'],
    capture_output=True, text=True, timeout=120, env=env
)
print('STDOUT:', result.stdout[:5000])
print('STDERR:', result.stderr[:2000])
print('RC:', result.returncode)