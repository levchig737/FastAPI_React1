from typing import Optional, Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from dto import product as ProductDTO
from models.product import Product

from services.category import get_category
from services.brand import get_brand_by_id


def create_product(data: Product, db: Session) -> Product:
    """
    Создание продукта
    :param data: данные об
    :param db: бд сессия
    :return: Созданный продукт
    """

    # Проверяем существование категории
    category = get_category(data.category_id, db)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {data.category_id} does not exist")

    # Проверяем существование брендов
    brand = get_brand_by_id(data.brand_id, db)
    if not brand:
        raise HTTPException(status_code=404, detail=f"Brand with id {data.brand_id} does not exist")

    product = Product(**data.dict())

    try:
        db.add(product)
        db.commit()
        db.refresh(product)
    except Exception as e:
        print(e)

    return product


def get_product(id: int, db: Session) -> Product | None:
    """
    Получение 1 продукта по id
    :param id: id продукта
    :param db: бд сессия
    :return: Полученный продукт
    """
    return (
        db.query(Product)
        .filter(Product.id == id)
        .first()
    )


def get_products(db: Session, skip: int = 0, limit: int = 10, search_query: Optional[str] = None) -> list[Type[Product]]:
    """
    Получение списка продуктов
    :param search_query: Поиск по строке в названии
    :param limit: Конец пагинации
    :param skip: Начало пагинации
    :param db: бд, сессия
    :return: список товаров
    """
    query = db.query(Product)

    if search_query:
        query = query.filter(Product.title.ilike(f"%{search_query}%"))

    return query.offset(skip).limit(limit).all()


def update(id: int, data: ProductDTO.Product, db: Session) -> Product | None:
    """
    Обновление информации о продукте по id
    :param id: id продукта
    :param data: данные продукта
    :param db: бд, сессия
    :return: Продукт, если он существует, в ином случае - None
    """

    product = get_product(id, db)

    # Проверка условий на соответствие роли пользователя со статусом задачи
    # performer = get_user_by_id(data.performer_id, db)
    # validate_data(performer, data)

    # Проверка соответствия нового статуса
    if product:
        # Обновляем только те поля, которые присутствуют в data
        for field, value in data.dict(exclude_unset=True).items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)

        return product
    return None


def remove(id: int, db: Session) -> int | None:
    """
    Удаляем product по id
    :param id: id product
    :param db: сессия/бд
    :return: кол-во удаленных строк, если продукт существует, иначе None
    """
    product = db.query(Product).filter(Product.id == id).first()

    if product:
        db.delete(product)
        db.commit()

    return product

