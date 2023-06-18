import uuid
from dataclasses import asdict
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx

from src.api.request_models.request_base import OrderRequest

from src.api.response_models.sku_response import SKUResponseStatus, SKUResponseList

from src.api.dto.order import SKU

from src.api.dto.order import Order

ordering_router = APIRouter(prefix="/order", tags=["SKU"])


@ordering_router.post("/", response_model=SKUResponseList)
async def create_order(order: OrderRequest):
    # Проверяем статус наличия товаров в warehouse_service
    sku_list = []
    for item in order.items:
        sku: SKU = SKU(**dict(item))
        sku_list.append(sku)
    order_info: Order = Order(str(uuid.uuid4()), sku_list)

    check_skus_url = "http://127.0.0.1:8080/check_skus/status/"
    skus_request = {"items": [asdict(item, dict_factory=lambda d: {k: v for k, v in d if k == "count" or k == 'sku'}) for item in order_info.items]}

    async with httpx.AsyncClient() as client:
        response = await client.post(check_skus_url, json=skus_request)

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

    async with httpx.AsyncClient() as client:
        response = await client.post(get_sku_info_url,
                                     json=skus_request)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Status not OK")
    order_info.items = response.json()['items']

    if len(asdict(order_info)['items']) != len(order.items):
        # Получена неполная информация о товарах
        raise HTTPException(status_code=500,
                            detail="Incomplete SKU information")

    get_ml_info_url = "http://127.0.0.1:8000/pack/"
    get_ml_info_request = asdict(order_info)

    # async with httpx.AsyncClient() as client:
    #     headers = {"Content-Type": "application/json"}
    #     response = await client.get(get_ml_info_url, params=get_ml_info_request, headers=headers)
    #
    #
    # ml_info = response.json()
    ml_info = asdict(order_info)
    ml_info['package'] = 'YMA'
    print(ml_info)

    check_carton_url = "http://127.0.0.1:8080/check_carton/"
    check_carton_request = ml_info["package"]

    async with httpx.AsyncClient() as client:
        params = {"carton_type": check_carton_request}
        response = await client.get(check_carton_url, params=params)

    check_response = response.json()

    if response.status_code == HTTPStatus.NOT_FOUND:
        ml_info['carton_status'] = 'Not enough carton on warehouse'
        return {
            "status": 'Not enough carton on warehouse'
        }

    ml_info['carton_barcode'] = response.json()["barcode"]
    print(ml_info)

    end_url = "http://127.0.0.1:8081/api/v1/order/"

    async with httpx.AsyncClient() as client:
        await client.post(end_url, json=ml_info)

    return {
        "status": "OK"
    }





    # order_write_url = "http://127.0.0.1:8080/order/8081/api/v1/order/`"
    # order_request = {
    #     "orderId": order_info.orderId,
    #     "items": order_info.items
    # }
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(order_write_url,
    #                                  json=order_request)
    #
    # order_info = response.json()
    # # логика проверки response?
    # print(order_info)
    #
    #
    #
    # # Отправка данных в ml модель
    # ml_items = []
    # for item in sku_info['items']:
    #     ml_dict = dict()
    #     ml_dict["sku"] = item["sku"]
    #     for sku_item in sku_items:
    #         if sku_item["sku"] == item["sku"]:
    #             ml_dict["count"] = sku_item["count"]
    #             break
    #     ml_dict["size1"] = item["length"]
    #     ml_dict["size2"] = item["width"]
    #     ml_dict["size3"] = item["height"]
    #     ml_dict["weight"] = item["weight"]
    #     ml_dict["types"] = item["cargotypes"]
    #     ml_items.append(ml_dict)
    #
    # get_ml_info_url = "http://127.0.0.1:8080/order/"
    # get_ml_info_request = {
    #     "orderId": order.orderId,
    #     "items": ml_items
    # }
    #
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(get_ml_info_url,
    #                                  json=get_ml_info_request)
    #
    # ml_info = response.json()
    # # логика проверки response?
    # print(ml_info)



