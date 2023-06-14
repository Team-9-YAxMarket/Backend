from fastapi import FastAPI


from src.core.settings import settings

from src.api.routers import sku_router


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG, root_path=settings.WAREHOUSE_ROOT_PATH)
    app.include_router(sku_router.router_sku)

    return app
