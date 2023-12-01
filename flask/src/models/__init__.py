from datetime import datetime
from uuid import uuid4
from src.databases.db import Base
from sqlalchemy import ForeignKey, Column, Table


def generate_now():
    return datetime.now()


def generate_uuid4():
    return uuid4()



user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
)

