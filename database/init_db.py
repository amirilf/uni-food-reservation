from sqlalchemy import create_engine
from database.connection import Base 


DATABASE_URL = "sqlite:///./db.sqlite"

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    init_db()