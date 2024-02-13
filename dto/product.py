from typing import List

from pydantic import BaseModel

from models.category import Category


class Product(BaseModel):
    """
    Передача данных между слоями приложения (database-services/product, database-routers/product)
    """
    title: str
    description: str
    count: int
    category_id: int
    brand_id: int


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
