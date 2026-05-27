"""[FR-13] Structured JSON logger."""
from __future__ import annotations

import json
import logging
import time
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


class StructuredLogger:
    def xǁStructuredLoggerǁ__init____mutmut_orig(self, service_name: str = "omnibot"):
        """Initialize structured logger with optional service name."""
        self._logger = logging.getLogger(service_name)
        self._service_name = service_name
    def xǁStructuredLoggerǁ__init____mutmut_1(self, service_name: str = "XXomnibotXX"):
        """Initialize structured logger with optional service name."""
        self._logger = logging.getLogger(service_name)
        self._service_name = service_name
    def xǁStructuredLoggerǁ__init____mutmut_2(self, service_name: str = "OMNIBOT"):
        """Initialize structured logger with optional service name."""
        self._logger = logging.getLogger(service_name)
        self._service_name = service_name
    def xǁStructuredLoggerǁ__init____mutmut_3(self, service_name: str = "omnibot"):
        """Initialize structured logger with optional service name."""
        self._logger = None
        self._service_name = service_name
    def xǁStructuredLoggerǁ__init____mutmut_4(self, service_name: str = "omnibot"):
        """Initialize structured logger with optional service name."""
        self._logger = logging.getLogger(None)
        self._service_name = service_name
    def xǁStructuredLoggerǁ__init____mutmut_5(self, service_name: str = "omnibot"):
        """Initialize structured logger with optional service name."""
        self._logger = logging.getLogger(service_name)
        self._service_name = None
    
    xǁStructuredLoggerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredLoggerǁ__init____mutmut_1': xǁStructuredLoggerǁ__init____mutmut_1, 
        'xǁStructuredLoggerǁ__init____mutmut_2': xǁStructuredLoggerǁ__init____mutmut_2, 
        'xǁStructuredLoggerǁ__init____mutmut_3': xǁStructuredLoggerǁ__init____mutmut_3, 
        'xǁStructuredLoggerǁ__init____mutmut_4': xǁStructuredLoggerǁ__init____mutmut_4, 
        'xǁStructuredLoggerǁ__init____mutmut_5': xǁStructuredLoggerǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredLoggerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁStructuredLoggerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁStructuredLoggerǁ__init____mutmut_orig)
    xǁStructuredLoggerǁ__init____mutmut_orig.__name__ = 'xǁStructuredLoggerǁ__init__'

    def xǁStructuredLoggerǁinfo__mutmut_orig(self, message: str, **kwargs) -> None:
        """Log an INFO-level structured JSON record."""
        self._log("INFO", message, **kwargs)

    def xǁStructuredLoggerǁinfo__mutmut_1(self, message: str, **kwargs) -> None:
        """Log an INFO-level structured JSON record."""
        self._log(None, message, **kwargs)

    def xǁStructuredLoggerǁinfo__mutmut_2(self, message: str, **kwargs) -> None:
        """Log an INFO-level structured JSON record."""
        self._log("INFO", None, **kwargs)

    def xǁStructuredLoggerǁinfo__mutmut_3(self, message: str, **kwargs) -> None:
        """Log an INFO-level structured JSON record."""
        self._log(message, **kwargs)

    def xǁStructuredLoggerǁinfo__mutmut_4(self, message: str, **kwargs) -> None:
        """Log an INFO-level structured JSON record."""
        self._log("INFO", **kwargs)

    def xǁStructuredLoggerǁinfo__mutmut_5(self, message: str, **kwargs) -> None:
        """Log an INFO-level structured JSON record."""
        self._log("INFO", message, )

    def xǁStructuredLoggerǁinfo__mutmut_6(self, message: str, **kwargs) -> None:
        """Log an INFO-level structured JSON record."""
        self._log("XXINFOXX", message, **kwargs)

    def xǁStructuredLoggerǁinfo__mutmut_7(self, message: str, **kwargs) -> None:
        """Log an INFO-level structured JSON record."""
        self._log("info", message, **kwargs)
    
    xǁStructuredLoggerǁinfo__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredLoggerǁinfo__mutmut_1': xǁStructuredLoggerǁinfo__mutmut_1, 
        'xǁStructuredLoggerǁinfo__mutmut_2': xǁStructuredLoggerǁinfo__mutmut_2, 
        'xǁStructuredLoggerǁinfo__mutmut_3': xǁStructuredLoggerǁinfo__mutmut_3, 
        'xǁStructuredLoggerǁinfo__mutmut_4': xǁStructuredLoggerǁinfo__mutmut_4, 
        'xǁStructuredLoggerǁinfo__mutmut_5': xǁStructuredLoggerǁinfo__mutmut_5, 
        'xǁStructuredLoggerǁinfo__mutmut_6': xǁStructuredLoggerǁinfo__mutmut_6, 
        'xǁStructuredLoggerǁinfo__mutmut_7': xǁStructuredLoggerǁinfo__mutmut_7
    }
    
    def info(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredLoggerǁinfo__mutmut_orig"), object.__getattribute__(self, "xǁStructuredLoggerǁinfo__mutmut_mutants"), args, kwargs, self)
        return result 
    
    info.__signature__ = _mutmut_signature(xǁStructuredLoggerǁinfo__mutmut_orig)
    xǁStructuredLoggerǁinfo__mutmut_orig.__name__ = 'xǁStructuredLoggerǁinfo'

    def xǁStructuredLoggerǁwarning__mutmut_orig(self, message: str, **kwargs) -> None:
        """Log a WARNING-level structured JSON record."""
        self._log("WARNING", message, **kwargs)

    def xǁStructuredLoggerǁwarning__mutmut_1(self, message: str, **kwargs) -> None:
        """Log a WARNING-level structured JSON record."""
        self._log(None, message, **kwargs)

    def xǁStructuredLoggerǁwarning__mutmut_2(self, message: str, **kwargs) -> None:
        """Log a WARNING-level structured JSON record."""
        self._log("WARNING", None, **kwargs)

    def xǁStructuredLoggerǁwarning__mutmut_3(self, message: str, **kwargs) -> None:
        """Log a WARNING-level structured JSON record."""
        self._log(message, **kwargs)

    def xǁStructuredLoggerǁwarning__mutmut_4(self, message: str, **kwargs) -> None:
        """Log a WARNING-level structured JSON record."""
        self._log("WARNING", **kwargs)

    def xǁStructuredLoggerǁwarning__mutmut_5(self, message: str, **kwargs) -> None:
        """Log a WARNING-level structured JSON record."""
        self._log("WARNING", message, )

    def xǁStructuredLoggerǁwarning__mutmut_6(self, message: str, **kwargs) -> None:
        """Log a WARNING-level structured JSON record."""
        self._log("XXWARNINGXX", message, **kwargs)

    def xǁStructuredLoggerǁwarning__mutmut_7(self, message: str, **kwargs) -> None:
        """Log a WARNING-level structured JSON record."""
        self._log("warning", message, **kwargs)
    
    xǁStructuredLoggerǁwarning__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredLoggerǁwarning__mutmut_1': xǁStructuredLoggerǁwarning__mutmut_1, 
        'xǁStructuredLoggerǁwarning__mutmut_2': xǁStructuredLoggerǁwarning__mutmut_2, 
        'xǁStructuredLoggerǁwarning__mutmut_3': xǁStructuredLoggerǁwarning__mutmut_3, 
        'xǁStructuredLoggerǁwarning__mutmut_4': xǁStructuredLoggerǁwarning__mutmut_4, 
        'xǁStructuredLoggerǁwarning__mutmut_5': xǁStructuredLoggerǁwarning__mutmut_5, 
        'xǁStructuredLoggerǁwarning__mutmut_6': xǁStructuredLoggerǁwarning__mutmut_6, 
        'xǁStructuredLoggerǁwarning__mutmut_7': xǁStructuredLoggerǁwarning__mutmut_7
    }
    
    def warning(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredLoggerǁwarning__mutmut_orig"), object.__getattribute__(self, "xǁStructuredLoggerǁwarning__mutmut_mutants"), args, kwargs, self)
        return result 
    
    warning.__signature__ = _mutmut_signature(xǁStructuredLoggerǁwarning__mutmut_orig)
    xǁStructuredLoggerǁwarning__mutmut_orig.__name__ = 'xǁStructuredLoggerǁwarning'

    def xǁStructuredLoggerǁerror__mutmut_orig(self, message: str, **kwargs) -> None:
        """Log an ERROR-level structured JSON record."""
        self._log("ERROR", message, **kwargs)

    def xǁStructuredLoggerǁerror__mutmut_1(self, message: str, **kwargs) -> None:
        """Log an ERROR-level structured JSON record."""
        self._log(None, message, **kwargs)

    def xǁStructuredLoggerǁerror__mutmut_2(self, message: str, **kwargs) -> None:
        """Log an ERROR-level structured JSON record."""
        self._log("ERROR", None, **kwargs)

    def xǁStructuredLoggerǁerror__mutmut_3(self, message: str, **kwargs) -> None:
        """Log an ERROR-level structured JSON record."""
        self._log(message, **kwargs)

    def xǁStructuredLoggerǁerror__mutmut_4(self, message: str, **kwargs) -> None:
        """Log an ERROR-level structured JSON record."""
        self._log("ERROR", **kwargs)

    def xǁStructuredLoggerǁerror__mutmut_5(self, message: str, **kwargs) -> None:
        """Log an ERROR-level structured JSON record."""
        self._log("ERROR", message, )

    def xǁStructuredLoggerǁerror__mutmut_6(self, message: str, **kwargs) -> None:
        """Log an ERROR-level structured JSON record."""
        self._log("XXERRORXX", message, **kwargs)

    def xǁStructuredLoggerǁerror__mutmut_7(self, message: str, **kwargs) -> None:
        """Log an ERROR-level structured JSON record."""
        self._log("error", message, **kwargs)
    
    xǁStructuredLoggerǁerror__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredLoggerǁerror__mutmut_1': xǁStructuredLoggerǁerror__mutmut_1, 
        'xǁStructuredLoggerǁerror__mutmut_2': xǁStructuredLoggerǁerror__mutmut_2, 
        'xǁStructuredLoggerǁerror__mutmut_3': xǁStructuredLoggerǁerror__mutmut_3, 
        'xǁStructuredLoggerǁerror__mutmut_4': xǁStructuredLoggerǁerror__mutmut_4, 
        'xǁStructuredLoggerǁerror__mutmut_5': xǁStructuredLoggerǁerror__mutmut_5, 
        'xǁStructuredLoggerǁerror__mutmut_6': xǁStructuredLoggerǁerror__mutmut_6, 
        'xǁStructuredLoggerǁerror__mutmut_7': xǁStructuredLoggerǁerror__mutmut_7
    }
    
    def error(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredLoggerǁerror__mutmut_orig"), object.__getattribute__(self, "xǁStructuredLoggerǁerror__mutmut_mutants"), args, kwargs, self)
        return result 
    
    error.__signature__ = _mutmut_signature(xǁStructuredLoggerǁerror__mutmut_orig)
    xǁStructuredLoggerǁerror__mutmut_orig.__name__ = 'xǁStructuredLoggerǁerror'

    def xǁStructuredLoggerǁ_log__mutmut_orig(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_1(self, level: str, message: str, **kwargs) -> None:
        record = None
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_2(self, level: str, message: str, **kwargs) -> None:
        record = {"XXtimestampXX": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_3(self, level: str, message: str, **kwargs) -> None:
        record = {"TIMESTAMP": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_4(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "XXlevelXX": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_5(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "LEVEL": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_6(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "XXserviceXX": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_7(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "SERVICE": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_8(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "XXmessageXX": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_9(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "MESSAGE": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_10(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(None, json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_11(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), None)
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_12(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_13(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), )
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_14(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(None, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_15(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, None), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_16(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_17(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, ), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_18(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(None))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_19(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = None
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_20(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(None)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_21(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = None
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_22(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = None
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_23(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(None)
            self._logger.log(getattr(logging, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_24(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(None, json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_25(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), None)

    def xǁStructuredLoggerǁ_log__mutmut_26(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_27(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), )

    def xǁStructuredLoggerǁ_log__mutmut_28(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(None, level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_29(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, None), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_30(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(level), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_31(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, ), json.dumps(serializable))

    def xǁStructuredLoggerǁ_log__mutmut_32(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        try:
            self._logger.log(getattr(logging, level), json.dumps(record))
        except TypeError:
            serializable = {}
            for k, v in record.items():
                try:
                    json.dumps(v)
                    serializable[k] = v
                except TypeError:
                    serializable[k] = repr(v)
            self._logger.log(getattr(logging, level), json.dumps(None))
    
    xǁStructuredLoggerǁ_log__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredLoggerǁ_log__mutmut_1': xǁStructuredLoggerǁ_log__mutmut_1, 
        'xǁStructuredLoggerǁ_log__mutmut_2': xǁStructuredLoggerǁ_log__mutmut_2, 
        'xǁStructuredLoggerǁ_log__mutmut_3': xǁStructuredLoggerǁ_log__mutmut_3, 
        'xǁStructuredLoggerǁ_log__mutmut_4': xǁStructuredLoggerǁ_log__mutmut_4, 
        'xǁStructuredLoggerǁ_log__mutmut_5': xǁStructuredLoggerǁ_log__mutmut_5, 
        'xǁStructuredLoggerǁ_log__mutmut_6': xǁStructuredLoggerǁ_log__mutmut_6, 
        'xǁStructuredLoggerǁ_log__mutmut_7': xǁStructuredLoggerǁ_log__mutmut_7, 
        'xǁStructuredLoggerǁ_log__mutmut_8': xǁStructuredLoggerǁ_log__mutmut_8, 
        'xǁStructuredLoggerǁ_log__mutmut_9': xǁStructuredLoggerǁ_log__mutmut_9, 
        'xǁStructuredLoggerǁ_log__mutmut_10': xǁStructuredLoggerǁ_log__mutmut_10, 
        'xǁStructuredLoggerǁ_log__mutmut_11': xǁStructuredLoggerǁ_log__mutmut_11, 
        'xǁStructuredLoggerǁ_log__mutmut_12': xǁStructuredLoggerǁ_log__mutmut_12, 
        'xǁStructuredLoggerǁ_log__mutmut_13': xǁStructuredLoggerǁ_log__mutmut_13, 
        'xǁStructuredLoggerǁ_log__mutmut_14': xǁStructuredLoggerǁ_log__mutmut_14, 
        'xǁStructuredLoggerǁ_log__mutmut_15': xǁStructuredLoggerǁ_log__mutmut_15, 
        'xǁStructuredLoggerǁ_log__mutmut_16': xǁStructuredLoggerǁ_log__mutmut_16, 
        'xǁStructuredLoggerǁ_log__mutmut_17': xǁStructuredLoggerǁ_log__mutmut_17, 
        'xǁStructuredLoggerǁ_log__mutmut_18': xǁStructuredLoggerǁ_log__mutmut_18, 
        'xǁStructuredLoggerǁ_log__mutmut_19': xǁStructuredLoggerǁ_log__mutmut_19, 
        'xǁStructuredLoggerǁ_log__mutmut_20': xǁStructuredLoggerǁ_log__mutmut_20, 
        'xǁStructuredLoggerǁ_log__mutmut_21': xǁStructuredLoggerǁ_log__mutmut_21, 
        'xǁStructuredLoggerǁ_log__mutmut_22': xǁStructuredLoggerǁ_log__mutmut_22, 
        'xǁStructuredLoggerǁ_log__mutmut_23': xǁStructuredLoggerǁ_log__mutmut_23, 
        'xǁStructuredLoggerǁ_log__mutmut_24': xǁStructuredLoggerǁ_log__mutmut_24, 
        'xǁStructuredLoggerǁ_log__mutmut_25': xǁStructuredLoggerǁ_log__mutmut_25, 
        'xǁStructuredLoggerǁ_log__mutmut_26': xǁStructuredLoggerǁ_log__mutmut_26, 
        'xǁStructuredLoggerǁ_log__mutmut_27': xǁStructuredLoggerǁ_log__mutmut_27, 
        'xǁStructuredLoggerǁ_log__mutmut_28': xǁStructuredLoggerǁ_log__mutmut_28, 
        'xǁStructuredLoggerǁ_log__mutmut_29': xǁStructuredLoggerǁ_log__mutmut_29, 
        'xǁStructuredLoggerǁ_log__mutmut_30': xǁStructuredLoggerǁ_log__mutmut_30, 
        'xǁStructuredLoggerǁ_log__mutmut_31': xǁStructuredLoggerǁ_log__mutmut_31, 
        'xǁStructuredLoggerǁ_log__mutmut_32': xǁStructuredLoggerǁ_log__mutmut_32
    }
    
    def _log(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredLoggerǁ_log__mutmut_orig"), object.__getattribute__(self, "xǁStructuredLoggerǁ_log__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _log.__signature__ = _mutmut_signature(xǁStructuredLoggerǁ_log__mutmut_orig)
    xǁStructuredLoggerǁ_log__mutmut_orig.__name__ = 'xǁStructuredLoggerǁ_log'
