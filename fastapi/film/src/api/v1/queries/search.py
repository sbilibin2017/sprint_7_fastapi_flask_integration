from core.config import Settings

CONFIG = Settings().dict()


# def query_film_by_title(title: str) -> dict:
#     return {"query": {"match": {"title": {"query": title, "fuzziness": "AUTO"}}}}


def query_film_by_title(title: str) -> dict:
    return {"query": {"fuzzy": {"title": {"value": title}}}}
