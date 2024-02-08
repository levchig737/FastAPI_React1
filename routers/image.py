from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from auth.auth import auth_backend
from auth.manager import get_user_manager
from database import get_db
from models.user import User

from services import image as ImageService
from dto import image as ImageDTO

router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.post('/', tags=["image"])
async def create(data: ImageDTO.Image = None, db: Session = Depends(get_db)):
    return ImageService.create_image(data, db)


@router.get('/{id}', tags=["image"])
async def get_image_by_id(id: int = None, db: Session = Depends(get_db)):
    return ImageService.get_image_by_id(id, db)


@router.get('/', tags=["image"])
async def get_images(db: Session = Depends(get_db)):
    return ImageService.get_images(db)


@router.put('/{id}', tags=["image"])
async def update(id: int = None, data: ImageDTO.Image = None, db: Session = Depends(get_db)):
    return ImageService.update(id, data, db)


@router.delete('/{id}', tags=["image"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return ImageService.remove(id, db)
