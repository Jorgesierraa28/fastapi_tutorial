from logging import raiseExceptions
from os import stat
from sqlite3 import Cursor
from turtle import update
from sqlalchemy.orm import Session
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import  List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from .. import models,schema
from .. import utils
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password 

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'this id: {id} doesnt exist')
    return user 