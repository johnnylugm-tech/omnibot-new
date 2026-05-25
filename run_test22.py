#!/usr/bin/env python3
import subprocess, sys, os
env = {**os.environ, 'PYTHONPATH': os.path.join(os.getcwd(), '03-development', 'src')}
result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'tests/test_fr22.py', '-v', '--tb=short'],
    capture_output=True, text=True, timeout=60, env=env
)
with open('/Users/johnny/projects/omnibot-new/test_out.txt', 'w') as f:
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\n\nSTDERR:\n")
    f.write(result.stderr)
    f.write(f"\n\nRC: {result.returncode}")
print("Done")