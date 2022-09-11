from fastapi import FastAPI
from fastapi.params import Body
from . import models
from .database import engine
from .routers import posts, users, auth
from pydantic import BaseSettings



models.Base.metadata.create_all(bind=engine)



app = FastAPI() #incicializa la API app 

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)





