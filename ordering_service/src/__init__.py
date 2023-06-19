from fastapi import FastAPI

from src.api.routers.sku_router_with_dto import ordering_router


def create_app() -> FastAPI:
    app = FastAPI(debug=False, root_path="")
    app.include_router(ordering_router)

    return app
