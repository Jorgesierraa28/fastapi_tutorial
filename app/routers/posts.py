from logging import raiseExceptions
from os import stat
from sqlite3 import Cursor
from turtle import update
from sqlalchemy.orm import Session
from sqlalchemy import func
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import  List, Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from .. import models,schema, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

#@router.get("/",response_model=List[schema.PostOut] )
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schema.PostResponse)
def create_post(post: schema.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" INSERT INTO posts (title, content, publish) VALUES (%s,%s,%s) RETURNING * """, (post.title,post.content,post.publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#@router.get("/{id}", response_model= schema.PostOut)
@router.get("/{id}")
def get_post(id: int, response: Response,db: Session = Depends(get_db) ):
    # cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id)))
    # post_id = cursor.fetchone()
    #post_id = db.query(models.Post).filter(models.Post.id == id).first()
    post_id = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
             models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'this id:{id} was not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': 'this id was not found'}
    return post_id

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if not deleted_post:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'this id:{id} doesnt exist')
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to delete the post")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@router.put('/{id}', response_model=schema.PostResponse)
def update_post (id: int, post: schema.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts set title = %s, content= %s, publish = %s where id = %s RETURNING *""", (post.title,post.content,post.publish,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'this id:{id} doesnt exist')
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to update the post")

    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return  updated_post_query.first()