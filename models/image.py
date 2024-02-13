
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Image(Base):
    """
    Таблица images
    """
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name: String = Column(String, unique=True, nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship("Product", back_populates="images")
