import orjson
from pydantic import BaseModel
from utils.mixin import DataMixin
from utils.orjson import orjson_dumps


class Film(BaseModel):
    id: str
    imdb_rating: float
    genre: list[DataMixin]
    genre_name: list[str]
    title: str
    description: str
    director: list[str]
    director_name: list[DataMixin]
    actor_name: list[str]
    actor: list[DataMixin]
    writer_name: list[str]
    writer: list[DataMixin]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
