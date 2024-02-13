from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from auth.auth import auth_backend
from auth.manager import get_user_manager
from database import get_db
from models.user import User

from services import product as ProductService
from dto import product as ProductDTO

router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.post('/', tags=["product"])
async def create(data: ProductDTO.Product = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin" and cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

    return ProductService.create_product(data, db)


@router.get('/{id}', tags=["product"])
async def get_product_by_id(id: int = None, db: Session = Depends(get_db)):
    product = ProductService.get_product(id, db)
    if not product:
        raise HTTPException(status_code=400, detail=f"Product with id {id} not exists")
    return product


@router.get('/', tags=["product"])
async def get_products(skip: int = 0, limit: int = 10, search_query: Optional[str] = None,
                       db: Session = Depends(get_db)):
    return ProductService.get_products(db, skip, limit, search_query)


@router.put('/{id}', tags=["product"])
async def update(id: int = None, data: ProductDTO.Product = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin" and cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

    return ProductService.update(id, data, db)


@router.delete('/{id}', tags=["product"])
async def delete(id: int = None, db: Session = Depends(get_db),
                 cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return ProductService.remove(id, db)


@router.put('/buy/{id}', tags=["product"])
async def buy_product(id: int = None, data: ProductDTO.ProductBuy = None, db: Session = Depends(get_db), cur_user: User = Depends(fastapi_users.current_user())):
    if cur_user.role != "admin" and cur_user.role != "user":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return ProductService.buy_product(id, data, db)
