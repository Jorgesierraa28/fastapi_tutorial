from cmath import exp
from jose import JWTError, jwt
from datetime import datetime, timedelta

#secret key
#algorithm 
#experiation time 

SECRET_KEY = '4ono42n34on23o452435124k1ok3no1j4n5o1'
ALGORITHM = 'HS256'
ACCES_TOKEN_EXPIRATION_TIME = 30 

def create_acces_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCES_TOKEN_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt
