from sqlalchemy.dialects.postgresql import UUID
from src.databases.db import Base
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import DateTime, String
from src.models import generate_uuid4, generate_now
from sqlalchemy.orm import Mapped, mapped_column, relationship, mapper


class Session(Base):
    __tablename__ = "session"

    # fields
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user_agent: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    authenticated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, unique=False
    )

    # relations
    user: Mapped["User"] = relationship(back_populates="sessions")
    tokens: Mapped[list["Token"]] = relationship(
        back_populates="session", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, user_id, user_agent):
        self.id = generate_uuid4()
        self.user_id = user_id
        self.user_agent = user_agent
        self.authenticated_at = generate_now()

    def __repr__(self):
        return f"<Session {self.id}>"



