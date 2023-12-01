from uuid import UUID

from pydantic import BaseModel


class PersonMixin(BaseModel):
    id: UUID
    full_name: str
