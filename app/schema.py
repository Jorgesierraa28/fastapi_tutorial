from datetime import datetime
from xmlrpc.client import boolean
from pydantic import BaseModel,EmailStr


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

class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserOut(BaseModel):
    id: int 
    email:EmailStr
    created_at: datetime 

    class Config: 
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str