from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    carton_router,
    order_router,
    prompt_router,
    session_router,
)
from src.core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG, root_path=settings.PACKING_ROOT_PATH)

    app.include_router(carton_router.router)
    app.include_router(prompt_router.router)
    app.include_router(order_router.router)
    app.include_router(session_router.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
