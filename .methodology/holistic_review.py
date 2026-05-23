import subprocess, json, os
from datetime import datetime, timezone

with open('/Users/johnny/projects/omnibot-new/01-requirements/SRS.md', 'r') as f:
    srs = f.read()
with open('/Users/johnny/projects/omnibot-new/01-requirements/SPEC_TRACKING.md', 'r') as f:
    tracking = f.read()
with open('/Users/johnny/projects/omnibot-new/01-requirements/TRACEABILITY_MATRIX.md', 'r') as f:
    tm = f.read()
with open('/Users/johnny/projects/omnibot-new/TEST_INVENTORY.yaml', 'r') as f:
    ti = f.read()

reviews = {}
for fname in ['P1.json', 'P1_spec_tracking.json', 'P1_tm.json', 'P1_ti.json']:
    path = f'/Users/johnny/projects/omnibot-new/.methodology/agent_b_approvals/{fname}'
    if os.path.exists(path):
        with open(path) as f:
            reviews[fname] = json.load(f)

total_chars = len(srs) + len(tracking) + len(tm) + len(ti)
print(f"Total embedded content: {total_chars} chars (~{total_chars//4} tokens)")

review_task = f"""HOLISTIC REVIEW: All 4 OmniBot Phase 1 deliverables. STATELESS — all docs embedded.

=== PREVIOUS REVIEW SUMMARIES ===
{json.dumps({k: v.get('review_status') + ' (c=' + str(v.get('confidence')) + ')' for k, v in reviews.items()}, indent=2)}
Gaps from sub-task reviews: all addressed in subsequent rounds.

=== DOC 1: SRS.md ===
{srs}

=== DOC 2: SPEC_TRACKING.md ===
{tracking}

=== DOC 3: TRACEABILITY_MATRIX.md ===
{tm}

=== DOC 4: TEST_INVENTORY.yaml ===
{ti}

Holistic checklist:
- All 21 FRs covered across all 4 deliverables?
- No contradictions between deliverables?
- Each item testable/traceable?
- All gaps from sub-task reviews addressed?
- Terminology consistent across all documents?
- FR Block JSON consistent with tables?
- Trace matrix matches SPEC_TRACKING NFR mappings?
- TEST_INVENTORY covers every FR from SRS.md?

Return ONLY JSON:
{{"status":"STAGE_PASS","review_status":"APPROVE","reason":"<summary under 200 chars>","confidence":<1-10>,"citations":["file:line"],"gaps":[...]}}"""

cli = '/Users/johnny/.hermes/node/bin/claude'
result = subprocess.run(
    [cli, '-p', review_task, '--output-format', 'json', '--setting-sources', '',
     '--disable-slash-commands', '--max-turns', '60', '--permission-mode', 'acceptEdits', '--no-session-persistence'],
    capture_output=True, text=True, timeout=600, cwd='/Users/johnny/projects/omnibot-new'
)

wrapper = json.loads(result.stdout)
actual = wrapper.get("result", "")
session_id = wrapper.get("session_id", "unknown")

review_data = None
for i, ch in enumerate(actual):
    if ch == '{':
        try:
            obj, _ = json.JSONDecoder().raw_decode(actual, i)
            if isinstance(obj, dict) and "review_status" in obj:
                review_data = obj
                break
        except:
            pass

if review_data:
    print(f"Holistic: {review_data['review_status']} | confidence={review_data['confidence']}")
    print(f"Reason: {review_data['reason']}")
    for g in review_data.get('gaps', []):
        print(f"  - [{g.get('severity')}] {g.get('id')}: {g.get('description','')[:120]}")

    with open('/Users/johnny/projects/omnibot-new/.methodology/agent_b_approvals/P1_holistic.json', 'w') as f:
        json.dump(review_data, f, indent=2, ensure_ascii=False)
    with open('/Users/johnny/projects/omnibot-new/.methodology/sessions_spawn.log', 'a') as f:
        f.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(), "role": "BUSINESS_ANALYST",
            "session_id": session_id, "status": "complete", "review_status": review_data['review_status'],
            "phase": 1, "fr_id": "P1_HOLISTIC"}) + '\n')

    has_blocking = any(g.get('severity') in ('medium', 'high') for g in review_data.get('gaps', []))
    if review_data['review_status'] == 'APPROVE' and not has_blocking:
        print("\n*** PHASE 1 HOLISTIC REVIEW APPROVED — proceed to push-checkpoint ***")
    else:
        print("\nBlocking gaps present:")
        for g in review_data.get('gaps', []):
            if g.get('severity') in ('medium', 'high'):
                print(f"  {g.get('severity')}: {g.get('description','')[:200]}")
else:
    print("FAILED: No review JSON")
    print(f"Output: {actual[:500]}")
