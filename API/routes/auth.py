from fastapi import APIRouter, HTTPException
from API.database import SessionDep
from API.models.users import User
from sqlmodel import select

router = APIRouter()

@router.get("/auth")
async def auth(username: str, password: str, session: SessionDep):
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password == password:
        return user.user_id
    else:
        return {"status": "fail"}