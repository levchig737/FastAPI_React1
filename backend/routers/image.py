from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from backend.auth.auth import auth_backend
from backend.auth.manager import get_user_manager
from backend.database import get_db
from backend.models.user import User

from backend.services import image as ImageService
from backend.dto import image as ImageDTO

router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.post('/', tags=["image"])
async def create(data: ImageDTO.Image = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin" and cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return ImageService.create_image(data, db)


@router.get('/{id}', tags=["image"])
async def get_image_by_id(id: int = None, db: Session = Depends(get_db)):
    image = ImageService.get_image_by_id(id, db)
    if not image:
        raise HTTPException(status_code=400, detail=f"Image with id {id} not exists")
    return image


@router.get('/', tags=["image"])
async def get_images(db: Session = Depends(get_db)):
    return ImageService.get_images(db)


@router.put('/{id}', tags=["image"])
async def update(id: int = None, data: ImageDTO.Image = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin" and cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return ImageService.update(id, data, db)


@router.delete('/{id}', tags=["image"])
async def delete(id: int = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return ImageService.remove(id, db)
