from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from auth.auth import auth_backend
from auth.manager import get_user_manager
from database import get_db
from models.user import User

from services import category as CategoryService
from dto import category as CategoryDTO

router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.post('/', tags=["category"])
async def create(data: CategoryDTO.Category = None, db: Session = Depends(get_db)):
    return CategoryService.create_category(data, db)


@router.get('/{id}', tags=["category"])
async def get_category_by_id(id: int = None, db: Session = Depends(get_db)):
    return CategoryService.get_category(id, db)


@router.get('/', tags=["category"])
async def get_products(db: Session = Depends(get_db)):
    return CategoryService.get_categories(db)


@router.put('/{id}', tags=["category"])
async def update(id: int = None, data: CategoryDTO.Category = None, db: Session = Depends(get_db)):
    return CategoryService.update(id, data, db)


@router.delete('/{id}', tags=["category"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return CategoryService.remove(id, db)
