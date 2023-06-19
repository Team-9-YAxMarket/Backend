import uuid
from dataclasses import asdict
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
import httpx

from src.api.request_models.request_base import OrderRequest

from src.api.response_models.sku_response import SKUStatusResponse

from src.api.dto.order import SKU

from src.api.dto.order import Order

ordering_router = APIRouter(prefix="/order", tags=["SKU"])


@ordering_router.post("/", response_model=SKUStatusResponse)
async def create_order(order: OrderRequest):
    # Проверяем статус наличия товаров в warehouse_service
    sku_list = []
    for item in order.items:
        sku: SKU = SKU(**dict(item))
        sku_list.append(sku)
    order_info: Order = Order(str(uuid.uuid4()), sku_list)

    check_skus_url = "http://127.0.0.1:8080/check_skus/status/"
    skus_request = {
        "items": [
            asdict(
                item,
                dict_factory=lambda d: {
                    k: v for k, v in d if k == "count" or k == "sku"
                },
            )
            for item in order_info.items
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(check_skus_url, json=skus_request)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Status not OK"
        )
    sku_status = response.json()

    if sku_status.get("status") == "FAULT":
        # Отсутствует какой-то товар
        raise HTTPException(
            status_code=400,
            detail="Товаров на складе недостаточно для формирования заказа",
        )

    # Получаем информацию о товарах из warehouse_service
    get_sku_info_url = "http://127.0.0.1:8080/check_skus/"

    async with httpx.AsyncClient() as client:
        response = await client.post(get_sku_info_url, json=skus_request)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Status not OK"
        )
    order_info.items = response.json()["items"]
    if len(asdict(order_info)["items"]) != len(order.items):
        # Получена неполная информация о товарах
        raise HTTPException(
            status_code=500, detail="Неполная информация о SKU"
        )

    get_ml_available_url = "http://127.0.0.1:8000/health/"

    async with httpx.AsyncClient(timeout=10) as client:
        # Проверка доступности сервиса модели
        response = await client.get(get_ml_available_url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Модель недоступна"
        )
    post_ml_info_url = "http://127.0.0.1:8000/pack/"
    get_ml_info_request = asdict(order_info)

    async with httpx.AsyncClient(timeout=10) as client:
        # Запрос в сервис модели для получения рекомендуемой упаковки
        response = await client.post(
            post_ml_info_url, json=get_ml_info_request
        )
    ml_info = response.json()

    check_carton_url = "http://127.0.0.1:8080/check_carton/"
    check_carton_request = ml_info["package"]

    async with httpx.AsyncClient() as client:
        # проверка наличия коробки на складе
        params = {"carton_type": check_carton_request}
        response = await client.get(check_carton_url, params=params)

    if response.status_code == HTTPStatus.NOT_FOUND:
        ml_info["carton_status"] = "Not enough carton on warehouse"
        return {"status": "Not enough carton on warehouse"}

    ml_info["carton_barcode"] = response.json()["barcode"]
    print(ml_info)

    summary_order_url = "http://127.0.0.1:8081/api/v1/order/"

    async with httpx.AsyncClient() as client:
        # отправляется запрос на создание заказа с обогащенными данными
        response = await client.post(summary_order_url, json=ml_info)

    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code,
            detail="Не удалось сформировать заказ",
        )
    return {"status": "OK"}
