import sys
from pathlib import Path

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from modules.common.db import Base, engine
from modules.auth.routes import router as auth_router
from modules.scanner.routes import router as scanner_router
from modules.dashboard.routes import router as dashboard_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vulnyx Scanner", description="Web Security Scanner Tool")
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="public"), name="static")

# Include routers
app.include_router(auth_router)
app.include_router(scanner_router)
app.include_router(dashboard_router)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Vulnyx Scanner starting at http://localhost:8080")
    uvicorn.run("main:app", host="0.0.0.0", port=8080)