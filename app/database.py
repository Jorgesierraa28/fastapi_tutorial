from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time 
from psycopg2.extras import RealDictCursor


#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Jorge95i28s@localhost/fastapi"

# while True:
#     try: 
#        conn = psycopg2.connect(host='localhost', database='fastapi', user= 'postgres', password = 'Jorge95i28s', cursor_factory = RealDictCursor)
#        cursor = conn.cursor()
#        print('database connection was succesfully')
#        break
#     except Exception as error: 
#        print('Conecting to database fail')
#        print('error: ',error)
#        time.sleep(2)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()