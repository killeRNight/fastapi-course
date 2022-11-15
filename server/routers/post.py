"""

Post routes.

"""


from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, Response, APIRouter

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,          # used for pagination
        search: Optional[str] = "",
):
    """Get all Posts"""

    posts = db.query(models.Post).filter(
      models.Post.title.contains(search)
    ).offset(skip).limit(limit).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
      models.Post.title.contains(search)
    ).offset(skip).limit(limit).all()

    return results


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """Get single Post by id"""

    post_obj = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(models.Post.id == post_id).first()

    if post_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} was not found"
        )

    return post_obj


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
        payload: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """Add a new Post"""

    new_post = models.Post(owner_id=current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{post_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_post(
        post_id: int, updated_post: schemas.PostBase,
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """Update specified Post object"""

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_obj = post_query.first()

    if post_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} was not found"
        )

    if post_obj.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """Delete single Post by id"""

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_obj = post_query.first()

    if post_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} was not found"
        )

    if post_obj.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
