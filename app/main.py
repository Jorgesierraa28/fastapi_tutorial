from os import stat
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI() #incicializa la API app 

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
    return {"data": mypost}

@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    mypost.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post_id = find_post(id)
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'this id:{id} was not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': 'this id was not found'}
    return{"this is the post": post_id}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index == None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'this id:{id} doesnt exist')
    mypost.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post (id: int, post: Post):
    index = find_index(id)
    print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'this id:{id} doesnt exist')
    post_dict = post.dict()
    post_dict['id'] = id  
    mypost[index] = post_dict
    return {"the new post": post_dict}
    