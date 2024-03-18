from typing import Type

from sqlalchemy.orm import Session
from backend.dto import category as CategoryDTO
from backend.models.category import Category


def create_category(data: Category, db: Session) -> Category:
    """
    Создание категории
    :param data: данные об категории
    :param db: бд сессии
    :return: Созданная категория
    """

    category = Category(**data.dict())

    try:
        db.add(category)
        db.commit()
        db.refresh(category)
    except Exception as e:
        print(e)

    return category


def get_category(id: int, db: Session) -> Category | None:
    """
    Получение 1 категории по id
    :param id: id категории
    :param db: бд сессия
    :return: Полученная категория
    """

    return (
        db.query(Category)
        .filter(Category.id == id)
        .first()
    )


def get_categories(db: Session) -> list[Type[Category]]:
    """
    Получение списка категорий
    :param db: бд, сессия
    :return: список категорий
    """

    return db.query(Category).all()


def update(id: int, data: CategoryDTO.Category, db: Session) -> Category | None:
    """
    Обновление информации о категории по id
    :param id: id категории
    :param data: данные категории
    :param db: бд, сессия
    :return: категория, если она существует, в ином случае - None
    """

    category = get_category(id, db)
    # Проверка соответствия нового статуса
    if category:
        # Обновляем только те поля, которые присутствуют в data
        for field, value in data.dict(exclude_unset=True).items():
            setattr(category, field, value)

        db.commit()
        db.refresh(category)

        return category
    return None


def remove(id: int, db: Session) -> int | None:
    """
    Удаляем category по id
    :param id: id category
    :param db: сессия/бд
    :return: кол-во удаленных строк, если продукт существует, иначе None
    """
    category = db.query(Category).filter(Category.id == id).first()

    if category:
        db.delete(category)
        db.commit()

    return category

