#!/usr/bin/env python3
"""Run pytest and capture output."""
import subprocess, sys

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_fr22.py", "-v", "--tb=line"],
    capture_output=True, text=True, cwd="/Users/johnny/projects/omnibot-new"
)
# Print everything
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:2000])
print(f"EXIT: {result.returncode}")

# Also look for SKIPPED
for line in result.stdout.splitlines():
    if "SKIP" in line or "skip" in line.lower() or line.startswith("=="):
        print(">>>", line)
