#!/usr/bin/env python3
import sys
sys.path.insert(0, '03-development/src')
from omnibot.processing.pii import PIIMasker

tests = [
    ('02-1234-5678', 'dashed phone'),
    ('0912345678', 'continuous phone'),
    ('john@example.com', 'email'),
    ('台北市大安區忠孝東路', 'address'),
]
for text, name in tests:
    result = PIIMasker.mask(text)
    print(f'{name}: "{text}" -> "{result}"')

# Test None
print(f'None input: mask={PIIMasker.mask(None)!r}, count={PIIMasker.mask_count(None)}')