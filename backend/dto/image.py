from pydantic import BaseModel


class Image(BaseModel):
    name: str
    product_id: int
