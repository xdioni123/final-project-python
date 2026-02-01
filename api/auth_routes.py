from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db
from models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------
# Schemas
# ---------
class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# ---------
# Register
# ---------
@router.post("/register")
def register(data: RegisterRequest):
    db = get_db()

    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=data.username)
    user.set_password(data.password)

    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}

# ---------
# Login
# ---------
@router.post("/login")
def login(data: LoginRequest):
    db = get_db()

    user = db.query(User).filter(User.username == data.username).first()
    if not user or not user.check_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "username": user.username,
        "is_admin": user.is_admin
    }
