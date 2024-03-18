from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    """
    Передача данных между слоями приложения (database-services/product, database-routers/product)
    """
    title: str
    description: str
    count: int
    category_id: int
    brand_id: int
    price: float


class ProductRead(BaseModel):
    """
    Передача данных между слоями приложения (database-services/product, database-routers/product)
    """
    title: str
    description: str
    count: int
    category_id: int
    brand_id: int
    images: List[int] = []


class ProductBuy(BaseModel):
    """
    Передача данных между слоями приложения (database-services/product, database-routers/product)
    """
    count: int
