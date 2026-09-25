from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ErrorCode(StrEnum):
    INVALID_INPUT = "invalid_input"
    NOT_FOUND = "not_found"
    UPSTREAM_TIMEOUT = "upstream_timeout"
    UPSTREAM_UNAVAILABLE = "upstream_unavailable"
    RATE_LIMITED = "rate_limited"
    GUARD_REJECTED = "guard_rejected"
    INTERNAL = "internal"


class ErrorEnvelope(BaseModel):
    """Error shape shared by the API and every MCP server."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    code: ErrorCode
    message: str = Field(min_length=1, max_length=500)
    retryable: bool = False
    request_id: str | None = None
