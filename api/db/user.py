

import uuid
from sqlmodel import Session, select

from api.db.models import User
from api.user.schema import UserLogin, UserRead


def get_user_by_id(id: uuid.UUID, db_session: Session) -> UserRead | None:
    user = db_session.exec(
        select(User).where(User.id == id)
    ).first()
    return user

def get_user_by_email(email: str, db_session: Session) -> User | None:
    user = db_session.exec(
        select(User).where(User.email == email)
    ).first()
    return user

def get_users(db_session: Session) -> list[UserRead]:
    users = db_session.exec(select(User)).all()
    return users

def create_user(user: User, db_session: Session) -> UserRead:
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def update_user(user: User, db_session: Session) -> UserRead:
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def delete_user(user: User, db_session: Session) -> UserRead:
    db_session.delete(user)
    db_session.commit()
    return user

def login_user(user: UserLogin, db_session: Session) -> bool:
    temp_user = get_user_by_email(user.email, db_session)
    if temp_user is None:
        return False
    if temp_user.password != user.password:
        return False
    return True