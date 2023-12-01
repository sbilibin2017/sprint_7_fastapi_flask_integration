from pydantic import BaseModel


class GenreDetailSchema(BaseModel):
    id: str
    name: str
    film: list[dict]
