from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from effective_mobile_task import db

ADMIN_ROLE = 20

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[int] = mapped_column(default=1)

class RefreshToken(db.Model):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    token: Mapped[str] = mapped_column()
    expires_at: Mapped[int] = mapped_column(TIMESTAMP)
    revoked: Mapped[bool] = mapped_column(default=False)

class RolePermission(db.Model):
    __tablename__ = "role_permission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    role_id: Mapped[int] = mapped_column()