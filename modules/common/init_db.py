from modules.common.db import Base, engine
from modules.auth.models import User

def init_db():
    """Initialize the database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 