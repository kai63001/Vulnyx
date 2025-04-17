from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json
from pathlib import Path
from modules.common.db import get_db
from modules.auth.security import get_current_user, is_first_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

RESULT_PATH = Path("results/results.json")
RESULT_PATH.parent.mkdir(exist_ok=True)

@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request, 
    db: Session = Depends(get_db)
):
    # Check if user is logged in
    token = request.cookies.get("auth_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        user = await get_current_user(token, db)
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    # Check if first user exists, if not redirect to registration
    first_user = await is_first_user(db)
    if first_user:
        return RedirectResponse(url="/register", status_code=303)
    
    # Load scan results
    if RESULT_PATH.exists():
        data = json.loads(RESULT_PATH.read_text())
    else:
        data = []
    
    # Calculate risk metrics for display
    high_risk = sum(item.get("high_risk", 0) for item in data)
    medium_risk = sum(item.get("medium_risk", 0) for item in data)
    low_risk = sum(item.get("low_risk", 0) for item in data)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "results": data,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "user": user
    }) 