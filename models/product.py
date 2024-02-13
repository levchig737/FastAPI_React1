from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    """
    Таблица products
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title: String = Column(String, nullable=False)
    description: String = Column(String, nullable=False)
    count: Integer = Column(Integer, nullable=False)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Category", backref="products")

    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=False)
    brand = relationship("Brand", backref="products")

    images = relationship("Image", back_populates="product")
