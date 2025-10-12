# models/crud.py
from sqlalchemy.orm import Session
from models.user import User


def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def create_user(db: Session, telegram_id: int, name: str):
    user = User(telegram_id=telegram_id, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_preferences(db: Session, telegram_id: int, preferences: dict):
    user = get_user_by_telegram_id(db=db, telegram_id=telegram_id)
    if not user:
        return None
    user.preferences = preferences
    db.commit()
    db.refresh(user)
    return user

def get_preferences(db: Session, telegram_id: int):
    user = get_user_by_telegram_id(db=db, telegram_id=telegram_id)
    if not user:
        return None
    return user.preferences
