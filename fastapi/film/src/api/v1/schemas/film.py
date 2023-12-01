from pydantic import BaseModel


class FilmDetailSchema(BaseModel):
    id: str
    imdb_rating: float
    title: str
    genre_name: list[str]
    director: list[dict]
    actor: list[dict]
    writer: list[dict]
