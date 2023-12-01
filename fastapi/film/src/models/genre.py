from uuid import UUID

import orjson
from pydantic import BaseModel
from utils.orjson import orjson_dumps


class Genre(BaseModel):
    id: UUID
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
