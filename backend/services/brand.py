from typing import Type

from sqlalchemy.orm import Session
from backend.dto import brand as BrandDTO
from backend.models.brand import Brand


def create_brand(data: Brand, db: Session) -> Brand:
    """
    Создание бренда
    :param data: данные о бренде
    :param db: бд сессии
    :return: Созданный бренд
    """

    brand = Brand(**data.dict())

    try:
        db.add(brand)
        db.commit()
        db.refresh(brand)
    except Exception as e:
        print(e)

    return brand


def get_brand_by_id(id: int, db: Session) -> Brand | None:
    """
    Получение 1 бренда по id
    :param id: id бренда
    :param db: бд сессия
    :return: Полученный бренд
    """

    return (
        db.query(Brand)
        .filter(Brand.id == id)
        .first()
    )


def get_brands(db: Session) -> list[Type[Brand]]:
    """
    Получение списка брендов
    :param db: бд, сессия
    :return: список брендов
    """

    return db.query(Brand).all()


def update(id: int, data: BrandDTO.Brand, db: Session) -> Brand | None:
    """
    Обновление информации о бренде по id
    :param id: id бренде
    :param data: данные бренда
    :param db: бд, сессия
    :return: бренд, если она существует, в ином случае - None
    """

    brand = get_brand_by_id(id, db)
    # Проверка соответствия нового статуса
    if brand:
        # Обновляем только те поля, которые присутствуют в data
        for field, value in data.dict(exclude_unset=True).items():
            setattr(brand, field, value)

        db.commit()
        db.refresh(brand)

        return brand
    return None


def remove(id: int, db: Session) -> int | None:
    """
    Удаляем бренд по id
    :param id: id бренда
    :param db: сессия/бд
    :return: кол-во удаленных строк, если бренд существует, иначе None
    """
    brand = db.query(Brand).filter(Brand.id == id).first()

    if brand:
        db.delete(brand)
        db.commit()

    return brand

