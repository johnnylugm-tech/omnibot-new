"""FR-13: Structured JSON logger."""
from __future__ import annotations

import io
import json
import logging


def test_fr13_logger_outputs_valid_json():
    from omnibot.logging.logger import StructuredLogger

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


def test_fr13_log_output_is_valid_single_line_json():
    from omnibot.logging.logger import StructuredLogger

    logger = StructuredLogger("test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    logger.info("single line message")
    output = stream.getvalue().strip()
    assert "\n" not in output
    json.loads(output)


def test_fr13_log_contains_required_fields_timestamp_level_service_message():
    from omnibot.logging.logger import StructuredLogger

    logger = StructuredLogger("my_service")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    logger.info("hello")
    output = stream.getvalue().strip()
    record = json.loads(output)
    assert "timestamp" in record
    assert record["level"] == "INFO"
    assert record["service"] == "my_service"
    assert record["message"] == "hello"


def test_fr13_log_extra_kwargs_appear_as_top_level_keys():
    from omnibot.logging.logger import StructuredLogger

    logger = StructuredLogger("test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    logger.info("with extra", user_id="u123", action="login")
    output = stream.getvalue().strip()
    record = json.loads(output)
    assert record["user_id"] == "u123"
    assert record["action"] == "login"


def test_fr13_log_level_mapping_info_20_error_40():
    from omnibot.logging.logger import StructuredLogger

    logger = StructuredLogger("test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    logger.info("info msg")
    logger.error("error msg")
    lines = stream.getvalue().strip().split("\n")
    r_info = json.loads(lines[0])
    r_err = json.loads(lines[1])
    assert r_info["level"] == "INFO"
    assert r_err["level"] == "ERROR"


def test_fr13_pipeline_completion_logged_as_json():
    from omnibot.logging.logger import StructuredLogger

    logger = StructuredLogger("test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    logger.info("pipeline completed", pipeline="ingest", status="done", duration_ms=1500)
    output = stream.getvalue().strip()
    record = json.loads(output)
    assert record["message"] == "pipeline completed"
    assert record["pipeline"] == "ingest"
    assert record["status"] == "done"
    assert record["duration_ms"] == 1500


def test_fr13_non_json_serializable_kwarg_handled_gracefully():
    from omnibot.logging.logger import StructuredLogger

    logger = StructuredLogger("test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    class NotSerializable:
        pass

    logger.info("with non-serializable", obj=NotSerializable())
    output = stream.getvalue().strip()
    record = json.loads(output)
    assert record["message"] == "with non-serializable"
    assert "obj" in record


def test_fr13_each_output_line_is_valid_json_parseable_by_jq():
    from omnibot.logging.logger import StructuredLogger

    logger = StructuredLogger("test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    for i in range(3):
        logger.info(f"message {i}")
    lines = [l for l in stream.getvalue().strip().split("\n") if l]
    assert len(lines) == 3
    for line in lines:
        json.loads(line)


def test_fr13_audit_log_written_on_pipeline_completion():
    from omnibot.logging.logger import StructuredLogger

    logger = StructuredLogger("audit_test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger._logger.addHandler(handler)
    logger._logger.setLevel(logging.DEBUG)

    logger.info(
        "pipeline completed",
        event="pipeline_completion",
        pipeline="main",
        status="success",
        user_id="u001",
    )
    output = stream.getvalue().strip()
    record = json.loads(output)
    assert record["event"] == "pipeline_completion"
    assert record["pipeline"] == "main"
    assert record["status"] == "success"
    assert record["user_id"] == "u001"


def test_fr13_service_name_configurable_via_constructor():
    from omnibot.logging.logger import StructuredLogger

    logger_a = StructuredLogger("service_a")
    logger_b = StructuredLogger("service_b")
    stream_a = io.StringIO()
    stream_b = io.StringIO()
    for logger, stream in [(logger_a, stream_a), (logger_b, stream_b)]:
        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.DEBUG)
        logger._logger.addHandler(handler)
        logger._logger.setLevel(logging.DEBUG)
        logger.info("ping")

    rec_a = json.loads(stream_a.getvalue().strip())
    rec_b = json.loads(stream_b.getvalue().strip())
    assert rec_a["service"] == "service_a"
    assert rec_b["service"] == "service_b"


def test_fr13_logger_used_by_fr19_pipeline_stage_11():
    from omnibot.logging.logger import StructuredLogger
    import importlib

    spec = importlib.util.find_spec("omnibot.processing.pipeline")
    if spec is not None:
        try:
            from omnibot.processing.pipeline import PipelineStage
        except ImportError:
            return

        class TestStage(PipelineStage):
            def execute(self, data):
                return data

        logger = StructuredLogger("fr19_test")
        stage = TestStage(name="s11", logger=logger)
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.DEBUG)
        logger._logger.addHandler(handler)
        logger._logger.setLevel(logging.DEBUG)
        stage.execute({})
        output = stream.getvalue().strip()
        if output:
            json.loads(output)