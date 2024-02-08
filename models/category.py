
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    """
    Таблица categories
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name: String = Column(String, nullable=False)
