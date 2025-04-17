from sqlalchemy import Boolean, Column, Integer, String
from passlib.context import CryptContext
from modules.common.db import Base

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)
    
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password) 