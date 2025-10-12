# models/user.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, JSON
from models.db import Base
from typing import Optional

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    preferences: Mapped[Optional[dict]] = mapped_column(JSON, default=[])

