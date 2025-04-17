from fastapi import APIRouter, Request, Depends, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from modules.common.db import get_db
from modules.auth.models import User
from modules.auth.security import authenticate_user, create_access_token, is_first_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Login page
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    # Check if user is already logged in
    token = request.cookies.get("auth_token")
    if token:
        try:
            from modules.auth.security import get_current_user
            user = await get_current_user(token, db)
            # If token is valid, redirect to dashboard
            return RedirectResponse(url="/", status_code=303)
        except:
            # Token is invalid, continue to login page
            pass
    
    # Check if registration is allowed (only if no users exist)
    first_user = await is_first_user(db)
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "can_register": first_user
    })

@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request, 
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Incorrect username or password",
            "can_register": await is_first_user(db)
        })
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    # Set cookie
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="auth_token", 
        value=access_token,
        httponly=True,
        max_age=1800,  # 30 minutes
        path="/"
    )
    
    return response

# Register page
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, db: Session = Depends(get_db)):
    # Check if registration is allowed (only if no users exist)
    first_user = await is_first_user(db)
    if not first_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "disabled": True,
            "is_first_user": False
        })
    
    return templates.TemplateResponse("register.html", {
        "request": request,
        "is_first_user": first_user
    })

@router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if registration is allowed
    first_user = await is_first_user(db)
    if not first_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "disabled": True,
            "is_first_user": False
        })
    
    # Validate input
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Passwords do not match",
            "is_first_user": first_user
        })
    
    # Check if username exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username already exists",
            "is_first_user": first_user
        })
    
    # Check if email exists
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Email already exists",
            "is_first_user": first_user
        })
    
    # Create user (first user is admin)
    hashed_password = User.get_password_hash(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_admin=first_user
    )
    db.add(user)
    db.commit()
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "message": "Registration successful. You can now log in.",
        "can_register": False
    })

# Logout
@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="auth_token", path="/")
    return response 