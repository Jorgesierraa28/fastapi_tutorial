from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr
from pydantic.types import conint


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

class Vote(BaseModel):
    post_id: int 
    dir: conint(le=1)

class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class PostOut(BasePost):
    Post: PostResponse
    votes: int 

    class Config: 
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class tokenData(BaseModel):
    id: Optional[str]