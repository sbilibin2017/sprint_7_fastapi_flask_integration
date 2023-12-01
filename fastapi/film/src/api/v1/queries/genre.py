from core.config import Settings

CONFIG = Settings().dict()


def query_genre() -> dict:
    return {
        "size": CONFIG["ELASTIC_SCROLL_SIZE"],
        "query": {"match_all": {}},
    }
