from fastapi import APIRouter
from typing import List

from app.schemas.user import UserCreate, UserOut

router = APIRouter()

# tiny in-memory store for example purposes
_db = []


@router.get("/users", response_model=List[UserOut])
def list_users():
    return _db


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate):
    user = {"id": len(_db) + 1, "email": payload.email, "full_name": payload.full_name}
    _db.append(user)
    return user
