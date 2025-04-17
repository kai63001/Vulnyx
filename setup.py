import sys
from pathlib import Path

# Add the current directory to the Python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from modules.common.db import Base, engine
from modules.auth.models import User

def setup():
    """Initialize the database and create necessary directories"""
    # Create database tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create result directory if it doesn't exist
    result_dir = ROOT_DIR / "results"
    result_dir.mkdir(exist_ok=True)
    print(f"Created result directory: {result_dir}")
    
    print("Setup completed successfully!")

if __name__ == "__main__":
    setup() 