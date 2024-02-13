from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from enum import Enum as BaseEnum


class Base(DeclarativeBase):
    pass


# Перечисление для типа роли
class UserRole(str, BaseEnum):
    admin = "admin"  # Все права
    manager = "manager"  # CRUD для: продукты, категории, изображения, бренды
    user = "user"  # Получить данные (get) для продуктов, категорий, изображений, брендов, купить продукт


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    role: UserRole = Column(String, nullable=False)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
