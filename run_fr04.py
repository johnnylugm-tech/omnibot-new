#!/usr/bin/env python3
import sys
sys.path.insert(0, '03-development/src')
import hashlib, hmac

BOT_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
BODY = b'{"update_id":123,"message":{"text":"hello"}}'
SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode('utf-8')).digest()
VALID_SIGNATURE = hmac.new(SECRET_KEY, BODY, hashlib.sha256).hexdigest()

from omnibot.security import TelegramWebhookVerifier

v = TelegramWebhookVerifier(BOT_TOKEN)
r1 = v.verify(BODY, VALID_SIGNATURE)
print('Test 1 (valid sig):', r1)

r2 = v.verify(b'{"update_id":999}', VALID_SIGNATURE)
print('Test 2 (tampered):', r2)

r3 = v.verify(BODY, 'deadbeef')
print('Test 3 (wrong sig):', r3)

import inspect
src = inspect.getsource(TelegramWebhookVerifier.verify)
r4 = 'compare_digest' in src
print('Test 4 (compare_digest):', r4)

v1 = TelegramWebhookVerifier(BOT_TOKEN)
v2 = TelegramWebhookVerifier('other_token')
r5a = v1.verify(BODY, VALID_SIGNATURE)
r5b = v2.verify(BODY, VALID_SIGNATURE)
print('Test 5a (same token):', r5a)
print('Test 5b (diff token):', r5b)

all_pass = all([r1==True, r2==False, r3==False, r4==True, r5a==True, r5b==False])
print()
print('ALL PASS' if all_pass else 'SOME FAILED')
sys.exit(0 if all_pass else 1)