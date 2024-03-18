from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from backend.auth.auth import auth_backend
from backend.auth.manager import get_user_manager
from backend.database import get_db
from backend.models.user import User

from backend.services import category as CategoryService
from backend.dto import category as CategoryDTO

router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.post('/', tags=["category"])
async def create(data: CategoryDTO.Category = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin" and cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return CategoryService.create_category(data, db)


@router.get('/{id}', tags=["category"])
async def get_category_by_id(id: int = None, db: Session = Depends(get_db)):
    category = CategoryService.get_category(id, db)
    if not category:
        raise HTTPException(status_code=400, detail=f"Category with id {id} not exists")
    return category


@router.get('/', tags=["category"])
async def get_categories(db: Session = Depends(get_db)):
    return CategoryService.get_categories(db)


@router.put('/{id}', tags=["category"])
async def update(id: int = None, data: CategoryDTO.Category = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return CategoryService.update(id, data, db)


@router.delete('/{id}', tags=["category"])
async def delete(id: int = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return CategoryService.remove(id, db)
