from fastapi import APIRouter, HTTPException
from API.database import SessionDep
from API.models.users import User

router = APIRouter()

@router.get("/user/{user_id}")
async def read_users(user_id: int, session: SessionDep)->User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user")
async def create_user(user: User, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.put("/user/{user_id}")
async def update_user(user_id: int, user: User, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_db.name = user.name
    user_db.username = user.username
    user_db.password = user.password
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@router.delete("/user/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}