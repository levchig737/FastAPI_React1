import os
from typing import Type

from fastapi import HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from backend.dto import image as ImageDTO
from backend.models.image import Image
from backend.services.product import get_product


def validate_image(image: Image, db) -> bool:
    # Проверяем существование продукта
    product = get_product(image.product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {image.product_id} does not exist")

    # Проверка типа файла
    allowed_extensions = {".jpg", ".jpeg", ".png"}  # Разрешенные расширения файлов
    _, file_extension = os.path.splitext(str(image.name))  # Получаем расширение файла из имени

    if file_extension.lower() not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Not allowed type of file")

    # Проверка уникальности имени файла
    existing_image = db.query(Image).filter(Image.name == image.name).first()
    if existing_image:
        raise HTTPException(status_code=400, detail=f"File already exists")

    # Проверка существования файла
    # Получаем абсолютный путь к файлу относительно текущей директории проекта
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к текущему файлу
    file_path = os.path.join(base_dir, "../..", "react", "React-shop", "public", "img", str(image.name))  # Путь к изображению
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail=f"File not exists")
    return True


def create_image(data: Image, db: Session) -> Image:
    """
    Создание изображения
    :param data: данные об изображении
    :param db: бд сессии
    :return: Созданное изображение
    """

    validate_image(data, db)

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


def upload_image(file: UploadFile = File(...)) -> None:
    # Получаем абсолютный путь к файлу относительно текущей директории проекта
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к текущему файлу
    file_path = os.path.join(base_dir, "../..", "react", "React-shop", "public", "img",
                             str(file.filename))  # Путь к изображению

    # Проверки
    if not os.path.exists(os.path.join(base_dir, "../..", "react", "React-shop", "public", "img")):
        raise HTTPException(status_code=400, detail=f"Path not exists")

        # Проверка типа файла
    allowed_extensions = {".jpg", ".jpeg", ".png"}  # Разрешенные расширения файлов
    _, file_extension = os.path.splitext(str(file.filename))  # Получаем расширение файла из
    if file_extension.lower() not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Not allowed type of file")

    # Проверка уникальности имени файла
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail=f"File already exists")

    # Сохраняем файл в папку public/img с тем же именем, что у файла
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

