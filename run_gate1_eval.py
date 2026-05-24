#!/usr/bin/env python3
"""Gate 1 evaluation runner for FR-02"""
import subprocess
import json
import sys

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd or "/Users/johnny/projects/omnibot-new")
    return result.returncode, result.stdout, result.stderr

# Ruff
print("Running ruff...")
rc, out, err = run_cmd("ruff check 03-development/src/")
print(f"Ruff exit: {rc}")
with open("/tmp/ruff_output.txt", "w") as f:
    f.write(out + err)
print(f"Ruff output: {out[:500] if out else 'empty'}{'...' if len(out) > 500 else ''}")

# Pyright
print("\nRunning pyright...")
rc, out, err = run_cmd("pyright 03-development/src/ --outputjson")
print(f"Pyright exit: {rc}")
with open("/tmp/pyright_output.json", "w") as f:
    f.write(out)
try:
    data = json.loads(out)
    summary = data.get("summary", {})
    print(f"Pyright: {summary.get('errorCount', 0)} errors")
except:
    print(f"Pyright raw: {out[:200]}")

# Pytest
print("\nRunning pytest...")
rc, out, err = run_cmd("PYTHONPATH=03-development/src/ python3 -m pytest tests/test_fr02.py -v --cov=03-development/src/omnibot --cov-report=term-missing 2>&1")
print(f"Pytest exit: {rc}")
with open("/tmp/pytest_output.txt", "w") as f:
    f.write(out + err)
print(f"Pytest output: {out[:500] if out else 'empty'}{'...' if len(out) > 500 else ''}")

print("\nDone. Files written to /tmp/{ruff_output.txt,pyright_output.json,pytest_output.txt}")