
from sqlalchemy import Column, Integer, String

from database import Base


class Brand(Base):
    """
    Таблица brands
    """
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name: String = Column(String, nullable=False)
