from typing import List

from pydantic import BaseModel

from models.category import Category


class Product(BaseModel):
    """
    Передача данных между слоями приложения (database-services/product, database-routers/product)
    """
    title: str
    description: str
    category_id: int
    brand_id: int
    images: List[int] = []
