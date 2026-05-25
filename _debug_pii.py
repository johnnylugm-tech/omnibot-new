#!/usr/bin/env python3
import sys
sys.path.insert(0, '03-development/src')
from omnibot.processing.pii import PIIMasker

# Test address regex
addr = '台北市大安區忠孝東路'
print(f'Address: {addr}')
print(f'Address match: {PIIMasker.TAIWAN_ADDRESS_RE.findall(addr)}')
print(f'Address masked: {PIIMasker.mask(addr)}')

# Test email
email = 'john@example.com'
print(f'\nEmail: {email}')
print(f'Email match: {PIIMasker.EMAIL_RE.findall(email)}')
print(f'Email masked: {PIIMasker.mask(email)}')

# Test phone
phone = '0912345678'
print(f'\nPhone: {phone}')
print(f'Phone match: {PIIMasker.PHONE_RE.findall(phone)}')
print(f'Phone masked: {PIIMasker.mask(phone)}')

# None
print(f'\nmask(None) = {PIIMasker.mask(None)!r}')
print(f'mask_count(None) = {PIIMasker.mask_count(None)}')
print(f'should_escalate(None) = {PIIMasker.should_escalate(None)}')