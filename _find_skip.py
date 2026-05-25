import subprocess, sys
result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_fr22.py", "--collect-only", "-q"], capture_output=True, text=True)
for line in result.stdout.splitlines() + result.stderr.splitlines():
    if "SKIP" in line or "skip" in line.lower() or "===" in line:
        print(line)
