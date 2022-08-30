from logging import raiseExceptions
from os import stat
from sqlite3 import Cursor
from turtle import update
from sqlalchemy.orm import Session
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import models,schema, utils
from .database import engine, get_db
from .routers import posts, users, auth


models.Base.metadata.create_all(bind=engine)



app = FastAPI() #incicializa la API app 

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

while True:
    try: 
       conn = psycopg2.connect(host='localhost', database='fastapi', user= 'postgres', password = 'Jorge95i28s', cursor_factory = RealDictCursor)
       cursor = conn.cursor()
       print('database connection was succesfully')
       break
    except Exception as error: 
       print('Conecting to database fail')
       print('error: ',error)
       time.sleep(2)



