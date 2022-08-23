from xmlrpc.client import boolean
from pydantic import BaseModel


class BasePost(BaseModel):
    title: str
    content: str
    publish: bool = True

class CreatePost(BasePost):
    pass

class PostResponse(BasePost):
    id: int 

    class Config: 
        orm_mode = True