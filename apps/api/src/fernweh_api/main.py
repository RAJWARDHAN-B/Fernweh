from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fernweh_api.errors import unhandled_exception_handler
from fernweh_api.logging import configure_logging
from fernweh_api.middleware import REQUEST_ID_HEADER, RequestContextMiddleware
from fernweh_api.routes import health
from fernweh_api.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    configure_logging(settings.log_level, json_output=settings.app_env != "local")

    app = FastAPI(
        title="Fernweh API",
        version="0.1.0",
        docs_url="/docs" if settings.expose_api_docs else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.expose_api_docs else None,
    )
    app.state.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_cors_origins,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Content-Type", REQUEST_ID_HEADER],
        expose_headers=[REQUEST_ID_HEADER],
    )
    app.add_middleware(RequestContextMiddleware)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(health.router)
    return app
