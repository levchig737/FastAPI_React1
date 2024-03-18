
from fastapi_users import schemas

from backend.models.user import UserRole


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    name: str
    role: UserRole
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    email: str
    name: str
    password: str
    role: UserRole
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    email: str
    name: str
    password: str
    role: UserRole
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
