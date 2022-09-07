from cmath import exp
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from . import schema, database

#secret key
#algorithm 
#experiation time 

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = '4ono42n34on23o452435124k1ok3no1j4n5o1'
ALGORITHM = 'HS256'
ACCES_TOKEN_EXPIRATION_TIME = 30 

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
    

def get_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'could not validate credentials', headers={"WWW-Aunthenticate": "Bearer"})
    return verify_acces_token(token,credentials_exception)