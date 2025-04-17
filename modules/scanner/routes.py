from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json
import re
import datetime
from pathlib import Path
from modules.common.db import get_db
from modules.auth.security import get_current_user
from modules.scanner.scanner import calculate_score, simulate_vulnerability_scan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

RESULT_PATH = Path("results/results.json")
RESULT_PATH.parent.mkdir(exist_ok=True)

@router.post("/scan")
async def scan(
    request: Request, 
    domain: str = Form(...), 
    scan_type: str = Form("full"),
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
    
    # Validate domain format
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$', domain):
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "results": json.loads(RESULT_PATH.read_text()) if RESULT_PATH.exists() else [],
            "message": f"Invalid domain format: {domain}",
            "user": user
        })
    
    # Simulate a scan
    scan_results = simulate_vulnerability_scan(domain, scan_type)
    
    # Create a complete result object
    current_time = datetime.datetime.now().isoformat()
    result = {
        "domain": domain,
        "status": "done",
        "date": current_time,
        "scan_type": scan_type,
        "score": calculate_score(1000),
        "vulnerabilities": scan_results["vulnerabilities"],
        "paths": scan_results["paths"],
        "high_risk": scan_results["high_risk"],
        "medium_risk": scan_results["medium_risk"],
        "low_risk": scan_results["low_risk"],
        "risk_score": scan_results["risk_score"],
        "user": user.username
    }
    
    # Save to JSON
    results = []
    if RESULT_PATH.exists():
        results = json.loads(RESULT_PATH.read_text())
    results.append(result)
    RESULT_PATH.write_text(json.dumps(results, indent=2))

    # Calculate overall metrics
    high_risk = sum(item.get("high_risk", 0) for item in results)
    medium_risk = sum(item.get("medium_risk", 0) for item in results)
    low_risk = sum(item.get("low_risk", 0) for item in results)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "results": results,
        "message": f"Scan complete for {domain}",
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "user": user
    }) 