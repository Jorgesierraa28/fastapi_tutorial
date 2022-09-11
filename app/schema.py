from datetime import datetime
from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseModel,EmailStr


class BasePost(BaseModel):
    title: str
    content: str
    publish: bool = True

class CreatePost(BasePost):
    pass

class UserOut(BaseModel):
    id: int 
    email:EmailStr
    created_at: datetime 

    class Config: 
        orm_mode = True

class PostResponse(BasePost):
    id: int 
    created_at: datetime
    owner_id: int 
    owner: UserOut

    class Config: 
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str 



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class tokenData(BaseModel):
    id: Optional[str]