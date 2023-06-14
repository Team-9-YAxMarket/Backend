from fastapi import FastAPI

from src.api.routers import session_router, carton_router, prompt_router
from src.core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG, root_path=settings.PACKING_ROOT_PATH)

    # app.include_router(user_router.router)
    app.include_router(carton_router.router)
    app.include_router(prompt_router.router)

    return app
