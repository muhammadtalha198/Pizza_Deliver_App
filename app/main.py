from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging

from app.routes.health import router as health_router
from app.routes.user_routes import router as auth_router

from app.routes.auth_routes import router as protected_router


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title=settings.APP_NAME)
    app.include_router(health_router, prefix="/api")
    app.include_router(auth_router, prefix="/auth")
    app.include_router(protected_router, prefix="/me", tags=["protected"])
    return app


app = create_app()
