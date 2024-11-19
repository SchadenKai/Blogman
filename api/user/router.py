from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from api.database import get_session
from api.db.user import create_user, get_user_by_email, login_user, update_user
from user.schema import UserCreate, UserLogin, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])


# signup
@router.post("/signup")
def user_signup(user: UserCreate, db_session: Session = Depends(get_session)) -> None:
    temp_user = get_user_by_email(user.email, db_session)
    if temp_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    create_user(user)
    

# signin 
@router.post("/signin")
def user_signin(user: UserLogin, db_session: Session = Depends(get_session)) -> None:
    if login_user(user, db_session):
        return {"message": "Login successful"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

# update profile
@router.put("")
def profile_update(user: UserUpdate, db_session: Session = Depends(get_session)) -> None:
    update_user(user, db_session)

# delete profile

# change password

# inspect user profile

# follow user 

# unfollow user

# get all followers

# get all following