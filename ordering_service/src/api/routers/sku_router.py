from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx

from src.api.request_models.request_base import OrderRequest

from src.api.response_models.sku_response import SKUResponseStatus, SKUResponseList

ordering_router = APIRouter(prefix="/order", tags=["SKU"])


@ordering_router.post("/", response_model=SKUResponseList)
async def create_order(order: OrderRequest):
    # Проверяем статус наличия товаров в warehouse_service

    check_skus_url = "http://127.0.0.1:8080/check_skus/status/"
    sku_items = [{"sku": item.sku, "count": item.count} for item in
                 order.items]
    check_skus_request = {"items": sku_items}

    async with httpx.AsyncClient() as client:
        response = await client.post(check_skus_url, json=check_skus_request)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Status not OK")
    sku_status = response.json()
    if sku_status.get("status") == "FAULT":
        # Отсутствует какой-то товар
        raise HTTPException(status_code=400,
                            detail="Товаров на складе недостаточно для формирования заказа")

    # Получаем информацию о товарах из warehouse_service
    get_sku_info_url = "http://127.0.0.1:8080/check_skus/"
    get_sku_info_request = {"items": sku_items}

    async with httpx.AsyncClient() as client:
        response = await client.post(get_sku_info_url,
                                     json=get_sku_info_request)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Status not OK")
    sku_info = response.json()
    if len(sku_info['items']) != len(order.items):
        print(len(sku_info), len(order.items))
        print(sku_info)
        # Получена неполная информация о товарах
        raise HTTPException(status_code=500,
                            detail="Incomplete SKU information")


    # отправка инофрмации для создания заказа
    order_items = []
    for item in sku_info['items']:
        order_dict = dict()
        order_dict["sku"] = item["sku"]
        order_dict["barcode"] = item["barcode"]
        order_dict["img"] = item["img"]
        for sku_item in sku_items:
            if sku_item["sku"] == item["sku"]:
                order_dict["count"] = sku_item["count"]
                break
        order_items.append(order_dict)

    order_write_url = "http://127.0.0.1:8080/order/8081/api/v1/order/`"
    order_request = {
        "orderId": order.orderId,
        "items": order_items
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(order_write_url,
                                     json=order_request)

    order_info = response.json()
    # логика проверки response?
    print(order_info)



    # Отправка данных в ml модель
    ml_items = []
    for item in sku_info['items']:
        ml_dict = dict()
        ml_dict["sku"] = item["sku"]
        for sku_item in sku_items:
            if sku_item["sku"] == item["sku"]:
                ml_dict["count"] = sku_item["count"]
                break
        ml_dict["size1"] = item["length"]
        ml_dict["size2"] = item["width"]
        ml_dict["size3"] = item["height"]
        ml_dict["weight"] = item["weight"]
        ml_dict["types"] = item["cargotypes"]
        ml_items.append(ml_dict)

    get_ml_info_url = "http://127.0.0.1:8080/order/"
    get_ml_info_request = {
        "orderId": order.orderId,
        "items": ml_items
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(get_ml_info_url,
                                     json=get_ml_info_request)

    ml_info = response.json()
    # логика проверки response?
    print(ml_info)



