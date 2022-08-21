from os import stat
from sqlite3 import Cursor
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

app = FastAPI() #incicializa la API app 

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


mypost = [{
    "tittle": "tittle of post 1",
    "content": "content of post 1",
    "id": 1

},
{
    "tittle": "tittle of post 2",
    "content": "content of post 2",
    "id": 2


}
]

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None



def find_post(id): 
    for p in mypost:
        if p['id'] == id: 
            return p

def find_index(id):
    for i, p in enumerate(mypost):
        if p['id'] == id:
            return i

@app.get("/") #metodo http y direccion que el usuario tiene que ingresar para llamar la api, que debe hacer la funcion de la api app 
async def root():
    return{"message": "hello world 2"}

    ## uvicourn reload para re lanzar el servidos cuando haya un cambio

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, publish) VALUES (%s,%s,%s) RETURNING * """, (post.title,post.content,post.publish))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id)))
    post_id = cursor.fetchone()
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'this id:{id} was not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': 'this id was not found'}
    return{"this is the post": post_id}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'this id:{id} doesnt exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@app.put('/posts/{id}')
def update_post (id: int, post: Post):
    cursor.execute(""" UPDATE posts set title = %s, content= %s, publish = %s where id = %s RETURNING *""", (post.title,post.content,post.publish,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'this id:{id} doesnt exist')
    return {"the new post": updated_post}
    