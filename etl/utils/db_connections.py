import json
from http import HTTPStatus
from pathlib import Path

import backoff
import psycopg
import pydantic
from elasticsearch import AsyncElasticsearch
from psycopg.rows import dict_row
from redis.asyncio import Redis

from settings import settings
from utils.logger import logger
from utils.state import State
from utils.validator import ElasticPydantic, PostgresPydantic, RedisPydantic

BASE_DIR = Path(__file__).resolve().parent.parent


@backoff.on_exception(backoff.expo, psycopg.AsyncConnection.OperationalError, max_tries=5)
async def get_postgres_conn(PostgresConfig: pydantic.BaseModel) -> psycopg.AsyncConnection.cursor:
    """Get postgres params."""
    d = {
        "dbname": settings.DB_NAME,
        "user": settings.DB_USER,
        "password": settings.POSTGRES_PASSWORD,
        "host": settings.POSTGRES_HOST,
        "port": settings.POSTGRES_PORT
    }
    d = PostgresPydantic(**d).dict()
    try:
        conn = await psycopg.AsyncConnection.connect(**d, row_factory=dict_row)
        cur = conn.cursor()
        return cur
    except psycopg.AsyncConnection.OperationalError as error:
        logger.error(error)


@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def get_es_conn(EsPydantic: pydantic.BaseModel) -> AsyncElasticsearch:
    """Get elasticsearch instance."""
    d = {"host": settings.ELASTIC_HOST, "port": settings.ELASTIC_PORT}
    d = EsPydantic(**d).dict()
    try:
        conn = AsyncElasticsearch(retry_on_timeout=True, **d)
        return conn
    except Exception as e:
        logger.error(e)


@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def get_redis_conn(RedisPydantic: pydantic.BaseModel) -> Redis.client:
    """Get redis instance."""
    d = {"host": settings.REDIS_HOST, "port": settings.REDIS_PORT}
    d = RedisPydantic(**d).dict()
    try:
        conn = await Redis(**d)
        return conn
    except Exception as e:
        logger.error(e)


async def prepare_es_cursor(mapping: str, index: str, es_cur: AsyncElasticsearch) -> AsyncElasticsearch:
    with open(BASE_DIR / "utils/es_mapping" / mapping, "r") as f:
        mapping = json.load(f)
    indices = await es_cur.indices.get_alias()
    if index not in indices.keys():
        await es_cur.indices.create(index=index,
                                    ignore=HTTPStatus.BAD_REQUEST, body=mapping)
    await es_cur.indices.get_mapping(index)
    return es_cur


async def set_es_index(es_cur: AsyncElasticsearch) -> AsyncElasticsearch:
    """Set elasticsearch index."""
    for mapping, index in [
        (settings.ELASTIC_FILM_MAPPING_FILENAME, settings.ELASTIC_FILM_INDEX),
        (settings.ELASTIC_GENRE_MAPPING_FILENAME,
         settings.ELASTIC_GENRE_INDEX),
        (settings.ELASTIC_DIRECTOR_MAPPING_FILENAME,
         settings.ELASTIC_DIRECTOR_INDEX),
        (settings.ELASTIC_WRITER_MAPPING_FILENAME,
         settings.ELASTIC_WRITER_INDEX),
        (settings.ELASTIC_ACTOR_MAPPING_FILENAME,
         settings.ELASTIC_ACTOR_INDEX)
    ]:
        es_cur = await prepare_es_cursor(mapping, index, es_cur)
    return es_cur


async def setup_connections() -> list[psycopg.AsyncConnection.cursor, AsyncElasticsearch, Redis.client, State]:
    """Set connections to postgres, redis, elasticsearch, init state."""
    postgres_conn = await get_postgres_conn(PostgresPydantic)
    es_cur = await set_es_index(await get_es_conn(ElasticPydantic))
    redis_conn = await get_redis_conn(RedisPydantic)
    state = State(redis_conn)
    return postgres_conn, es_cur, redis_conn, state


async def get_film_total_count(postgres_cur: psycopg.AsyncConnection.cursor) -> dict:
    """Get min and max date from postgres."""
    await postgres_cur.execute("""SELECT count(id) as count FROM film""")
    data = await postgres_cur.fetchall()
    count = data[0]['count']
    return count


async def close_connections(postgres_cur, es_cur):
    await postgres_cur.close()
    await es_cur.transport.close()
