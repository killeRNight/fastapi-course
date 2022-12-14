"""

Vote routes.

"""


from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, Response, APIRouter

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/vote", tags=['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def update_vote(
        vote: schemas.Vote,
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    """Vote for post"""

    found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not found_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.post_id} does not exist"
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id,
    )

    found_vote = vote_query.first()

    if vote.direction:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}"
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "added vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exists"
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "deleted vote"}
