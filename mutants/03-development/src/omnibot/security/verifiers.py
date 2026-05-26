"""Webhook signature verification — FR-04 (Telegram) + FR-05 (LINE)."""

import base64
import hashlib
import hmac
from abc import ABC, abstractmethod
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class WebhookVerifier(ABC):
    """Abstract base for webhook signature verification."""

    @abstractmethod
    def verify(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""


class TelegramWebhookVerifier(WebhookVerifier):
    """Verify Telegram webhook request signatures."""

    def xǁTelegramWebhookVerifierǁ__init____mutmut_orig(self, bot_token: str):
        """Initialize with Telegram bot token."""
        self.secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()

    def xǁTelegramWebhookVerifierǁ__init____mutmut_1(self, bot_token: str):
        """Initialize with Telegram bot token."""
        self.secret_key = None

    def xǁTelegramWebhookVerifierǁ__init____mutmut_2(self, bot_token: str):
        """Initialize with Telegram bot token."""
        self.secret_key = hashlib.sha256(None).digest()

    def xǁTelegramWebhookVerifierǁ__init____mutmut_3(self, bot_token: str):
        """Initialize with Telegram bot token."""
        self.secret_key = hashlib.sha256(bot_token.encode(None)).digest()

    def xǁTelegramWebhookVerifierǁ__init____mutmut_4(self, bot_token: str):
        """Initialize with Telegram bot token."""
        self.secret_key = hashlib.sha256(bot_token.encode("XXutf-8XX")).digest()

    def xǁTelegramWebhookVerifierǁ__init____mutmut_5(self, bot_token: str):
        """Initialize with Telegram bot token."""
        self.secret_key = hashlib.sha256(bot_token.encode("UTF-8")).digest()
    
    xǁTelegramWebhookVerifierǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTelegramWebhookVerifierǁ__init____mutmut_1': xǁTelegramWebhookVerifierǁ__init____mutmut_1, 
        'xǁTelegramWebhookVerifierǁ__init____mutmut_2': xǁTelegramWebhookVerifierǁ__init____mutmut_2, 
        'xǁTelegramWebhookVerifierǁ__init____mutmut_3': xǁTelegramWebhookVerifierǁ__init____mutmut_3, 
        'xǁTelegramWebhookVerifierǁ__init____mutmut_4': xǁTelegramWebhookVerifierǁ__init____mutmut_4, 
        'xǁTelegramWebhookVerifierǁ__init____mutmut_5': xǁTelegramWebhookVerifierǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTelegramWebhookVerifierǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTelegramWebhookVerifierǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTelegramWebhookVerifierǁ__init____mutmut_orig)
    xǁTelegramWebhookVerifierǁ__init____mutmut_orig.__name__ = 'xǁTelegramWebhookVerifierǁ__init__'

    def xǁTelegramWebhookVerifierǁverify__mutmut_orig(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_1(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is not None:
            return False
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_2(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return True
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_3(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = None
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_4(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(None, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_5(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, None, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_6(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, body, None).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_7(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_8(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_9(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, body, ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_10(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(None, signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_11(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, None)

    def xǁTelegramWebhookVerifierǁverify__mutmut_12(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature)

    def xǁTelegramWebhookVerifierǁverify__mutmut_13(self, body: bytes, signature: str) -> bool:
        """Return True if the request signature matches the body."""
        if signature is None:
            return False
        expected = hmac.new(self.secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, )
    
    xǁTelegramWebhookVerifierǁverify__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTelegramWebhookVerifierǁverify__mutmut_1': xǁTelegramWebhookVerifierǁverify__mutmut_1, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_2': xǁTelegramWebhookVerifierǁverify__mutmut_2, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_3': xǁTelegramWebhookVerifierǁverify__mutmut_3, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_4': xǁTelegramWebhookVerifierǁverify__mutmut_4, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_5': xǁTelegramWebhookVerifierǁverify__mutmut_5, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_6': xǁTelegramWebhookVerifierǁverify__mutmut_6, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_7': xǁTelegramWebhookVerifierǁverify__mutmut_7, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_8': xǁTelegramWebhookVerifierǁverify__mutmut_8, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_9': xǁTelegramWebhookVerifierǁverify__mutmut_9, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_10': xǁTelegramWebhookVerifierǁverify__mutmut_10, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_11': xǁTelegramWebhookVerifierǁverify__mutmut_11, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_12': xǁTelegramWebhookVerifierǁverify__mutmut_12, 
        'xǁTelegramWebhookVerifierǁverify__mutmut_13': xǁTelegramWebhookVerifierǁverify__mutmut_13
    }
    
    def verify(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTelegramWebhookVerifierǁverify__mutmut_orig"), object.__getattribute__(self, "xǁTelegramWebhookVerifierǁverify__mutmut_mutants"), args, kwargs, self)
        return result 
    
    verify.__signature__ = _mutmut_signature(xǁTelegramWebhookVerifierǁverify__mutmut_orig)
    xǁTelegramWebhookVerifierǁverify__mutmut_orig.__name__ = 'xǁTelegramWebhookVerifierǁverify'


class LineWebhookVerifier(WebhookVerifier):
    """Verify LINE Messaging API webhook request signatures."""

    def xǁLineWebhookVerifierǁ__init____mutmut_orig(self, channel_secret: str):
        """Initialize with LINE channel secret."""
        self.channel_secret = channel_secret.encode("utf-8")

    def xǁLineWebhookVerifierǁ__init____mutmut_1(self, channel_secret: str):
        """Initialize with LINE channel secret."""
        self.channel_secret = None

    def xǁLineWebhookVerifierǁ__init____mutmut_2(self, channel_secret: str):
        """Initialize with LINE channel secret."""
        self.channel_secret = channel_secret.encode(None)

    def xǁLineWebhookVerifierǁ__init____mutmut_3(self, channel_secret: str):
        """Initialize with LINE channel secret."""
        self.channel_secret = channel_secret.encode("XXutf-8XX")

    def xǁLineWebhookVerifierǁ__init____mutmut_4(self, channel_secret: str):
        """Initialize with LINE channel secret."""
        self.channel_secret = channel_secret.encode("UTF-8")
    
    xǁLineWebhookVerifierǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLineWebhookVerifierǁ__init____mutmut_1': xǁLineWebhookVerifierǁ__init____mutmut_1, 
        'xǁLineWebhookVerifierǁ__init____mutmut_2': xǁLineWebhookVerifierǁ__init____mutmut_2, 
        'xǁLineWebhookVerifierǁ__init____mutmut_3': xǁLineWebhookVerifierǁ__init____mutmut_3, 
        'xǁLineWebhookVerifierǁ__init____mutmut_4': xǁLineWebhookVerifierǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLineWebhookVerifierǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁLineWebhookVerifierǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁLineWebhookVerifierǁ__init____mutmut_orig)
    xǁLineWebhookVerifierǁ__init____mutmut_orig.__name__ = 'xǁLineWebhookVerifierǁ__init__'

    def xǁLineWebhookVerifierǁverify__mutmut_orig(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_1(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is not None:
            return False
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_2(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return True
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_3(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = None
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_4(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(None, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_5(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, None, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_6(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, None).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_7(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_8(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_9(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, ).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_10(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = None
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_11(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(None).decode()
        return hmac.compare_digest(expected, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_12(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(None, signature)

    def xǁLineWebhookVerifierǁverify__mutmut_13(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, None)

    def xǁLineWebhookVerifierǁverify__mutmut_14(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(signature)

    def xǁLineWebhookVerifierǁverify__mutmut_15(self, body: bytes, signature: str) -> bool:
        """Return True if the LINE webhook signature matches the body."""
        if signature is None:
            return False
        digest = hmac.new(self.channel_secret, body, hashlib.sha256).digest()
        expected = base64.b64encode(digest).decode()
        return hmac.compare_digest(expected, )
    
    xǁLineWebhookVerifierǁverify__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLineWebhookVerifierǁverify__mutmut_1': xǁLineWebhookVerifierǁverify__mutmut_1, 
        'xǁLineWebhookVerifierǁverify__mutmut_2': xǁLineWebhookVerifierǁverify__mutmut_2, 
        'xǁLineWebhookVerifierǁverify__mutmut_3': xǁLineWebhookVerifierǁverify__mutmut_3, 
        'xǁLineWebhookVerifierǁverify__mutmut_4': xǁLineWebhookVerifierǁverify__mutmut_4, 
        'xǁLineWebhookVerifierǁverify__mutmut_5': xǁLineWebhookVerifierǁverify__mutmut_5, 
        'xǁLineWebhookVerifierǁverify__mutmut_6': xǁLineWebhookVerifierǁverify__mutmut_6, 
        'xǁLineWebhookVerifierǁverify__mutmut_7': xǁLineWebhookVerifierǁverify__mutmut_7, 
        'xǁLineWebhookVerifierǁverify__mutmut_8': xǁLineWebhookVerifierǁverify__mutmut_8, 
        'xǁLineWebhookVerifierǁverify__mutmut_9': xǁLineWebhookVerifierǁverify__mutmut_9, 
        'xǁLineWebhookVerifierǁverify__mutmut_10': xǁLineWebhookVerifierǁverify__mutmut_10, 
        'xǁLineWebhookVerifierǁverify__mutmut_11': xǁLineWebhookVerifierǁverify__mutmut_11, 
        'xǁLineWebhookVerifierǁverify__mutmut_12': xǁLineWebhookVerifierǁverify__mutmut_12, 
        'xǁLineWebhookVerifierǁverify__mutmut_13': xǁLineWebhookVerifierǁverify__mutmut_13, 
        'xǁLineWebhookVerifierǁverify__mutmut_14': xǁLineWebhookVerifierǁverify__mutmut_14, 
        'xǁLineWebhookVerifierǁverify__mutmut_15': xǁLineWebhookVerifierǁverify__mutmut_15
    }
    
    def verify(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLineWebhookVerifierǁverify__mutmut_orig"), object.__getattribute__(self, "xǁLineWebhookVerifierǁverify__mutmut_mutants"), args, kwargs, self)
        return result 
    
    verify.__signature__ = _mutmut_signature(xǁLineWebhookVerifierǁverify__mutmut_orig)
    xǁLineWebhookVerifierǁverify__mutmut_orig.__name__ = 'xǁLineWebhookVerifierǁverify'
