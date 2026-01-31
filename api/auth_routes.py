from fastapi import APIRouter
from pydantic import BaseModel
from database import get_db
from models.user import User
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/auth")

class UserData(BaseModel):
    username: str
    password: str


@router.post("/register")
def register_user(data: UserData):
    db = get_db()

    user = User(username=data.username)
    user.set_password(data.password)

    try:
        db.add(user)
        db.commit()
        return {"status": "success"}
    except IntegrityError:
        db.rollback()
        return {"status": "error", "message": "Username already exists"}


@router.post("/login")
def login_user(data: UserData):
    db = get_db()
    user = db.query(User).filter(User.username == data.username).first()

    if user and user.check_password(data.password):
        return {
            "status": "success",
            "is_admin": user.is_admin
        }

    return {"status": "error"}
