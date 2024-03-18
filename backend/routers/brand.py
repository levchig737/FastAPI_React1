from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from backend.auth.auth import auth_backend
from backend.auth.manager import get_user_manager
from backend.database import get_db
from backend.models.user import User

from backend.services import brand as BrandService
from backend.dto import brand as BrandDTO

router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.post('/', tags=["brand"])
async def create(data: BrandDTO.Brand = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin" and cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return BrandService.create_brand(data, db)


@router.get('/{id}', tags=["brand"])
async def get_brand_by_id(id: int = None, db: Session = Depends(get_db)):
    brand = BrandService.get_brand_by_id(id, db)
    if not brand:
        raise HTTPException(status_code=400, detail=f"Brand with id {id} not exists")
    return brand


@router.get('/', tags=["brand"])
async def get_brands(db: Session = Depends(get_db)):
    return BrandService.get_brands(db)


@router.put('/{id}', tags=["brand"])
async def update(id: int = None, data: BrandDTO.Brand = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin" and cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return BrandService.update(id, data, db)


@router.delete('/{id}', tags=["brand"])
async def delete(id: int = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return BrandService.remove(id, db)
