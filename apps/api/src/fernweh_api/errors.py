from fastapi import Request
from fastapi.responses import JSONResponse

from fernweh_api.logging import get_logger
from fernweh_api.middleware import REQUEST_ID_HEADER
from fernweh_domain import ErrorCode, ErrorEnvelope

logger = get_logger(__name__)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id: str | None = getattr(request.state, "request_id", None)
    logger.exception("unhandled_exception", request_id=request_id, exc_info=exc)
    envelope = ErrorEnvelope(
        code=ErrorCode.INTERNAL,
        message="An unexpected error occurred.",
        request_id=request_id,
    )
    headers = {REQUEST_ID_HEADER: request_id} if request_id else None
    return JSONResponse(status_code=500, content=envelope.model_dump(mode="json"), headers=headers)
