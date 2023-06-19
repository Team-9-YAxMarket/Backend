from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional


@dataclass
class SKU:
    sku: Optional[str] = ""
    barcode: Optional[str] = ""
    img: Optional[str] = ""
    count: Optional[int] = None
    length: Optional[Decimal] = None
    width: Optional[Decimal] = None
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    cargotypes: Optional[List[str]] = None


@dataclass()
class Order:
    orderId: Optional[str]
    items: List[SKU]
    package: Optional[str] = ""
