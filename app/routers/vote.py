from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import database, models, schema, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = '/vote',
    tags= ["votes"]
)

# @router.post('/',status_code=status.HTTP_201_CREATED)
# def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
#     vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
#     found_vote = vote_query.first()
#     if(vote.dir==1):
#         if found_vote:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already vote on post {vote.post_id}")
#         new_vote = models.Votes(user_id = current_user.id, post_id = vote.post_id)
#         db.add(new_vote)
#         db.commit()
#         return {"message": "succesfully added a vote"}
#     else:
#         if not found_vote:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {vote.post_id} doesn exist")
#         else:
#             vote_query.delete(synchronize_session=False)
#             db.commit()
#             return {"message": "succesfully deleted post"}

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    post_find = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_find: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {vote.post_id} doesn exist")
    else: 
        if(vote.dir==1):
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already vote on post {vote.post_id}")
            new_vote = models.Votes(user_id = current_user.id, post_id = vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"message": "succesfully added a vote"}
        else:
            if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote doesnt exists")
            else:
                vote_query.delete(synchronize_session=False)
                db.commit()
                return {"message": "succesfully deleted post"}
