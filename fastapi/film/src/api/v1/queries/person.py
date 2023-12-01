from core.config import Settings

CONFIG = Settings().dict()


def query_person() -> dict:
    return {
        "size": CONFIG["ELASTIC_SCROLL_SIZE"],
        "query": {"match_all": {}},
    }
