from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.auth import auth_backend
from models.user import User
from auth.manager import get_user_manager
from database import get_db
from services import user as UserService
from dto.user import UserCreate, UserUpdate
from fastapi_users import FastAPIUsers

router = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


# @router.post('/register', tags=["user"])
# async def register_user(data: UserCreate, db: Session = Depends(get_db)):
#     existing_user = UserService.get_user_by_username(data.username, db)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return UserService.create_user(data, db)


@router.get('/{id}', tags=["user"])
async def get_user(id: int, cur_user: User = Depends(fastapi_users.current_user()), db: Session = Depends(get_db)):
    if cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

    user_db = UserService.get_user_by_id(id, db)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db


@router.put('/{id}', tags=["user"])
async def update_user(id: int, data: UserUpdate, db: Session = Depends(get_db), cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

    user = UserService.update_user(id, data, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete('/{id}', tags=["user"])
async def delete_user(id: int, db: Session = Depends(get_db), cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

    user = UserService.delete_user(id, db)
    if user == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
