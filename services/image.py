from typing import Type

from sqlalchemy.orm import Session
from dto import image as ImageDTO
from models.image import Image


def create_image(data: Image, db: Session) -> Image:
    """
    Создание изображения
    :param data: данные об изображении
    :param db: бд сессии
    :return: Созданное изображение
    """

    image = Image(**data.dict())

    try:
        db.add(image)
        db.commit()
        db.refresh(image)
    except Exception as e:
        print(e)

    return image


def get_image_by_id(id: int, db: Session) -> Image | None:
    """
    Получение 1 изображения по id
    :param id: id изображения
    :param db: бд сессия
    :return: Полученное изображение
    """

    return (
        db.query(Image)
        .filter(Image.id == id)
        .first()
    )


def get_images(db: Session) -> list[Type[Image]]:
    """
    Получение списка изображений
    :param db: бд, сессия
    :return: список изображений
    """

    return db.query(Image).all()


def update(id: int, data: ImageDTO.Image, db: Session) -> Image | None:
    """
    Обновление информации об изображении по id
    :param id: id изображении
    :param data: данные изображения
    :param db: бд, сессия
    :return: изображение, если оно существует, в ином случае - None
    """

    image = get_image_by_id(id, db)
    # Проверка соответствия нового статуса
    if image:
        # Обновляем только те поля, которые присутствуют в data
        for field, value in data.dict(exclude_unset=True).items():
            setattr(image, field, value)

        db.commit()
        db.refresh(image)

        return image
    return None


def remove(id: int, db: Session) -> int | None:
    """
    Удаляем изображение по id
    :param id: id изображения
    :param db: сессия/бд
    :return: кол-во удаленных строк, если изображение существует, иначе None
    """
    image = db.query(Image).filter(Image.id == id).first()

    if image:
        db.delete(image)
        db.commit()

    return image

