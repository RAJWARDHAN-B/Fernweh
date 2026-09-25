import pytest
from pydantic import ValidationError

from fernweh_domain import ErrorCode, ErrorEnvelope


def test_error_envelope_serializes_code_as_string() -> None:
    envelope = ErrorEnvelope(code=ErrorCode.UPSTREAM_TIMEOUT, message="Weather timed out")

    assert envelope.model_dump(mode="json") == {
        "code": "upstream_timeout",
        "message": "Weather timed out",
        "retryable": False,
        "request_id": None,
    }


def test_error_envelope_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ErrorEnvelope.model_validate({"code": "internal", "message": "x", "stack": "leak"})


def test_error_envelope_rejects_empty_message() -> None:
    with pytest.raises(ValidationError):
        ErrorEnvelope(code=ErrorCode.INTERNAL, message="")


def test_error_envelope_rejects_unknown_code() -> None:
    with pytest.raises(ValidationError):
        ErrorEnvelope.model_validate({"code": "teapot", "message": "x"})
