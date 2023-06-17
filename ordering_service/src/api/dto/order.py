from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional


@dataclass
class SKU:
    sku: Optional[str]
    barcode: Optional[str]
    img: Optional[str]
    count: Optional[int]
    length: Optional[Decimal]
    width: Optional[Decimal]
    height: Optional[Decimal]
    weight: Optional[Decimal]
    cargotypes: Optional[List[str]]

@dataclass()
class Order:
    orderId: Optional[str]
    items: List[SKU]