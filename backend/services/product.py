from typing import Optional, Type, Tuple, List

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.dto import product as ProductDTO
from backend.models.product import Product

from backend.services.category import get_category
from backend.services.brand import get_brand_by_id


def validate_product(product: Product, db) -> bool:
    if int(product.count) < 0:
        raise HTTPException(status_code=400, detail="Count should be >= 0")

    if int(product.price) <= 0:
        raise HTTPException(status_code=400, detail="Price should be > 0")

    # Проверяем существование категории
    category = get_category(product.category_id, db)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {product.category_id} does not exist")

    # Проверяем существование брендов
    brand = get_brand_by_id(product.brand_id, db)
    if not brand:
        raise HTTPException(status_code=404, detail=f"Brand with id {product.brand_id} does not exist")

    return True


def create_product(data: ProductDTO.Product, db: Session) -> Product:
    """
    Создание продукта
    :param data: данные об
    :param db: бд сессия
    :return: Созданный продукт
    """

    # Проверка данных о продукте
    validate_product(data, db)

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
    # joinedload, чтобы вывести список images, которые ссылаются на этот продукт
    product = db.query(Product).options(joinedload(Product.images)).filter(Product.id == id).first()
    return product


def get_products(db: Session, skip: int = 0, limit: int = 10, search_query: Optional[str] = None) -> Tuple[
    List[Type[Product]], int]:
    """
    Получение списка продуктов
    :param search_query: Поиск по строке в названии
    :param limit: Конец пагинации
    :param skip: Начало пагинации
    :param db: бд, сессия
    :return: список товаров
    """
    query = db.query(Product).options(joinedload(Product.images))

    if search_query:
        query = query.filter(Product.title.ilike(f"%{search_query}%"))

    total_count = query.count()  # Получаем общее количество товаров

    products = query.offset(skip).limit(limit).all()

    items = []
    for i in range(skip+1, limit+1):
        item = get_product(i, db)
        if item:
            items.append(item)
        else: break

    return items, total_count


def get_count_products(db: Session) -> int:
    """
    Получение количества продуктов
    :param db: бд, сессия
    :return: количество товаров
    """
    query = db.query(Product)

    total_count = query.count()  # Получаем общее количество товаров

    return total_count


def update(id: int, data: ProductDTO.Product, db: Session) -> Product | None:
    """
    Обновление информации о продукте по id
    :param id: id продукта
    :param data: данные продукта
    :param db: бд, сессия
    :return: Продукт, если он существует, в ином случае - None
    """
    validate_product(data, db)

    product = get_product(id, db)

    # Проверка условий на соответствие роли пользователя со статусом задачи
    # performer = get_user_by_id(data.performer_id, db)
    # validate_data(performer, data)

    # Проверка существования продукта
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

    # Удаляем каждое изображение из базы данных
    for image in product.images:
        if image:
            db.delete(image)
            db.commit()

    if product:
        db.delete(product)
        db.commit()

    return product


def buy_product(id: int, data: ProductDTO.ProductBuy, db: Session) -> Product | None:
    """
    Покупка продукта
    :param id: id продукта
    :param count: Количество, которое покупает пользователь
    :param db: бд, сессия
    :return: Купленный продукт или None, если продукта не существует
    """
    product = get_product(id, db)

    # Проверка существования продукта
    if product:
        product.count -= data.count

        # Проверяем корректность данных
        validate_product(product, db)

        db.commit()
        db.refresh(product)

        return product
    return None
