from sqlalchemy import Column, Integer, BigInteger, String, Enum
from database.connection import Base
from database.enums import UserStage

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    
    t_id = Column(BigInteger, unique=True, nullable=False)
    t_fullname = Column(String(100), nullable=False)
    
    username = Column(String(50), nullable=True)
    password = Column(String(100), nullable=True)
    fullname = Column(String(100), nullable=True)
    gender = Column(String(10), nullable=True)
    national_number = Column(String(20), nullable=True)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    faculty = Column(String(50), nullable=True)
    cookie = Column(String(300), nullable=True)
    
    user_stage = Column(Enum(UserStage), nullable=False, default=UserStage.NEW)
