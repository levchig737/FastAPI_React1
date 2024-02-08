from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from auth.auth import auth_backend
from auth.manager import get_user_manager
from database import get_db
from models.user import User

from services import brand as BrandService
from dto import brand as BrandDTO

router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.post('/', tags=["brand"])
async def create(data: BrandDTO.Brand = None, db: Session = Depends(get_db)):
    return BrandService.create_brand(data, db)


@router.get('/{id}', tags=["brand"])
async def get_brand_by_id(id: int = None, db: Session = Depends(get_db)):
    return BrandService.get_brand_by_id(id, db)


@router.get('/', tags=["brand"])
async def get_products(db: Session = Depends(get_db)):
    return BrandService.get_brands(db)


@router.put('/{id}', tags=["brand"])
async def update(id: int = None, data: BrandDTO.Brand = None, db: Session = Depends(get_db)):
    return BrandService.update(id, data, db)


@router.delete('/{id}', tags=["brand"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return BrandService.remove(id, db)
