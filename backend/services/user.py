from sqlalchemy.orm import Session
from backend.models.user import User
from backend.dto.user import UserUpdate


# def create_user(data: UserCreate, db: Session) -> User:
#     user = User(**data.dict())
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user


def get_user_by_id(id: int, db: Session) -> User | None:

    return db.query(User).filter(User.id == id).first()


def update_user(id: int, data: UserUpdate, db: Session) -> User | None:
    user = get_user_by_id(id, db)
    if user:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user
    return None


def delete_user(id: int, db: Session) -> int:
    user = db.query(User).filter(User.id == id).delete()
    db.commit()
    return user
