from sqlalchemy.dialects.postgresql import UUID
from src.databases.db import Base
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship, mapper
from datetime import datetime
from sqlalchemy import DateTime, String
from src.models import generate_uuid4, generate_now, user_role


class User(Base):
    __tablename__ = "user"

    # fields
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    login: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, unique=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, unique=False)

    # relations
    sessions: Mapped[list["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete", passive_deletes=True
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary=user_role,
        back_populates="users",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __init__(self, login, password):
        dt_now = generate_now()
        self.id = generate_uuid4()
        self.login = login
        self.password = generate_password_hash(password, "scrypt")
        self.created_at = dt_now
        self.updated_at = dt_now

    def is_password_valid(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.login}>"


