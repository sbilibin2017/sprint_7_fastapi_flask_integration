from pydantic import BaseModel


class PersonDetailSchema(BaseModel):
    id: str
    full_name: str
    film: list[dict]
