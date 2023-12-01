from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from settings import settings
from utils.logger import logger
from utils.state import State


async def gendata(es_cur: AsyncElasticsearch, data: list[dict], index: str, to_update: bool) -> dict:
    for row in data:
        if not to_update:
            yield {"_index": index, "_type": "_doc", "_id": row['id'], "_source": row}
        else:
            mask = await es_cur.exists(index=index, id=row['id'])
            if mask:
                for film in row['film']:
                    yield {
                        "_op_type": "update",
                        "_index": index,
                        "_id": row['id'],
                        "upsert": {"film": film},
                        "script": {
                            "source": "ctx._source.film.add(params.film)",
                            "lang": "painless",
                            "params": {"film": film}
                        }
                    }
            else:
                yield {"_index": index, "_type": "_doc", "_id": row['id'], "_source": row}


async def load(
    data_film: list[dict],
    data_genre: list[dict],
    data_actor: list[dict],
    data_writer: list[dict],
    data_director: list[dict],
    new_ids: list[str],
    es_cur: AsyncElasticsearch,
    state: State,
) -> None:
    """Loads transformed data to elasticsearch index."""
    await async_bulk(es_cur, gendata(es_cur, data_film, index=settings.ELASTIC_FILM_INDEX, to_update=False))
    await async_bulk(es_cur, gendata(es_cur, data_film, index=settings.ELASTIC_SEARCH_INDEX, to_update=False))
    await async_bulk(es_cur, gendata(es_cur, data_genre, index=settings.ELASTIC_GENRE_INDEX, to_update=True))
    await async_bulk(es_cur, gendata(es_cur, data_actor, index=settings.ELASTIC_ACTOR_INDEX, to_update=True))
    await async_bulk(es_cur, gendata(es_cur, data_writer, index=settings.ELASTIC_WRITER_INDEX, to_update=True))
    await async_bulk(es_cur, gendata(es_cur, data_director, index=settings.ELASTIC_DIRECTOR_INDEX, to_update=True))
    await state.set_state(settings.REDIS_FILM_STATE, new_ids)
    logger.info(f"\t[LOAD] new_state:{len(new_ids)}")
