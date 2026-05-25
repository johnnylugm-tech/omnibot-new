#!/usr/bin/env python3
import subprocess, sys, os

env = {**os.environ, 'PYTHONPATH': os.path.join(os.getcwd(), '03-development', 'src')}

# Test each failing test individually
tests = [
    'test_fr22_fcr_phase1_target_50_percent_odd_query',
    'test_fr22_webhook_signature_replay_attack_blocked',
    'test_fr22_burst_1000_requests_at_least_900_get_429',
    'test_fr22_ruff_check_zero_violations_ci_gate',
]

for t in tests:
    r = subprocess.run(
        [sys.executable, '-m', 'pytest', f'tests/test_fr22.py::{t}', '-v', '--tb=long'],
        capture_output=True, text=True, timeout=60, env=env
    )
    with open(f'/Users/johnny/projects/omnibot-new/out_{t}.txt', 'w') as f:
        f.write(f"STDOUT:\n{r.stdout}\n\nSTDERR:\n{r.stderr}\n\nRC:{r.returncode}")
    print(f"Ran {t}, RC={r.returncode}")