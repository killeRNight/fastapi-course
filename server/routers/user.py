"""

User routes.

"""


from typing import List
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Add a new User"""

    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    user_obj = db.query(models.User).all()
    return user_obj


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by id"""

    user_obj = db.query(models.User).filter(models.User.id == user_id).first()
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {user_obj} was not found"
        )

    return user_obj
