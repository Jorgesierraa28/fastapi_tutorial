from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from . import schema, database, models
from sqlalchemy.orm import Session
from .config import settings

#secret key
#algorithm 
#experiation time 

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCES_TOKEN_EXPIRATION_TIME = settings.acces_token_expire_minutes

def create_acces_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def verify_acces_token(token: str, credentials_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schema.tokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    

def get_current_user(token: str = Depends(oath2_scheme), db: Session =Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'could not validate credentials', headers={"WWW-Aunthenticate": "Bearer"})
    token = verify_acces_token(token,credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user 