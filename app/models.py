from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    publish = Column(Boolean, server_default='TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"
    email = Column(String,nullable=False, unique= True)
    password = Column(String, nullable=False)
    id = Column(Integer,primary_key = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    phone_number = Column(String)

class Votes(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), primary_key = True, nullable = False)
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True, nullable = False)
    