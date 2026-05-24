#!/usr/bin/env python3
import sys
sys.path.insert(0, '03-development/src')
import hashlib, hmac, time

BOT_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
BODY = b'{"update_id":123,"message":{"text":"hello"}}'
SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode('utf-8')).digest()
VALID_SIGNATURE = hmac.new(SECRET_KEY, BODY, hashlib.sha256).hexdigest()

from omnibot.security import TelegramWebhookVerifier

v = TelegramWebhookVerifier(BOT_TOKEN)

r1 = v.verify(BODY, VALID_SIGNATURE)
print(f'T1 valid sig: {r1} (expect True)')

r2 = v.verify(b'{"update_id":999}', VALID_SIGNATURE)
print(f'T2 tampered: {r2} (expect False)')

r3 = v.verify(BODY, 'deadbeef')
print(f'T3 wrong sig: {r3} (expect False)')

import inspect
src = inspect.getsource(TelegramWebhookVerifier.verify)
print(f'T4 compare_digest: {"compare_digest" in src} (expect True)')

iters = 100
start = time.perf_counter()
for _ in range(iters):
    v.verify(BODY, 'a' * 64)
elapsed = (time.perf_counter() - start) / iters * 1000
print(f'T5 timing ms/call: {elapsed:.3f}')