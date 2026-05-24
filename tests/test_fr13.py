"""FR-13: Structured JSON logger."""
from __future__ import annotations

import json


def test_fr13_logger_outputs_valid_json():
    from omnibot.logging.logger import StructuredLogger
    import io
    import logging

    logger = StructuredLogger("test_service")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    logger.info("test message", extra_field="value")
    output = stream.getvalue().strip()
    assert output
    record = json.loads(output)
    assert record["level"] == "INFO"
    assert record["message"] == "test message"
    assert record["extra_field"] == "value"
    assert record["service"] == "test_service"


def test_fr13_logger_warning_and_error_levels():
    from omnibot.logging.logger import StructuredLogger
    import io
    import logging

    logger = StructuredLogger("test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    logger.warning("warn")
    logger.error("err")
    lines = stream.getvalue().strip().split("\n")
    assert len(lines) == 2
    assert json.loads(lines[0])["level"] == "WARNING"
    assert json.loads(lines[1])["level"] == "ERROR"
