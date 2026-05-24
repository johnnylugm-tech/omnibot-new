"""FR-13: Structured JSON logger."""
from __future__ import annotations

import json
import logging
import time


class StructuredLogger:
    def __init__(self, service_name: str = "omnibot"):
        self._logger = logging.getLogger(service_name)
        self._service_name = service_name

    def info(self, message: str, **kwargs) -> None:
        self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self._log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self._log("ERROR", message, **kwargs)

    def _log(self, level: str, message: str, **kwargs) -> None:
        record = {"timestamp": time.time(), "level": level,
                  "service": self._service_name, "message": message, **kwargs}
        self._logger.log(getattr(logging, level), json.dumps(record))
