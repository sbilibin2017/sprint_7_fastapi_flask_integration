from datetime import datetime

import numpy as np
import pandas as pd
import pydantic
from psycopg import AsyncConnection

from settings import settings
from utils.logger import logger
from utils.validator import Film, Film4Genre, Film4Person


def get_query(current_state: tuple[str]) -> tuple[str, datetime]:
    """Creates filmwork query with respect of current etl state."""
    if len(current_state) != 0:
        query = f"""
                    SELECT *
                    FROM film
                    WHERE id NOT IN {current_state}
                    ORDER BY updated_at DESC
                """
    else:
        query = """
                    SELECT *
                    FROM film
                    ORDER BY updated_at DESC
                """
    return query


def get_film_chunk(FilmworkPydantic: pydantic.BaseModel, chunk: list[dict]) -> pd.DataFrame:
    """Creatres dataframe for filmwork."""
    columns = list(FilmworkPydantic.__fields__)
    df = pd.DataFrame.from_records(chunk)[columns]
    df['id'] = df['id'].astype(str)
    return df.replace({np.nan: None})


async def get_film4genre_chunk(
    FilmworkGenrePydantic: pydantic.BaseModel, cursor: AsyncConnection.cursor, df: pd.DataFrame
) -> pd.DataFrame:
    """Creatres dataframe for filmwork genres."""
    film_idxs = tuple(df["id"].values.tolist())
    columns = list(FilmworkGenrePydantic.__fields__)
    query = f"""
                SELECT *
                FROM film4genre fwg
                LEFT JOIN genre g
                    ON fwg.genre_id = g.id
                WHERE film_id in {film_idxs}
            """
    await cursor.execute(query)
    rows = await cursor.fetchall()
    df = pd.DataFrame.from_records(rows)[columns]\
        .drop('id', axis=1).rename(columns={"film_id": "id"})
    df[['id', 'genre_id']] = df[['id', 'genre_id']].astype(str)
    return df.replace({np.nan: None})


async def get_film4person_chunk(FilmworkPersonPydantic: pydantic.BaseModel, cursor: AsyncConnection.cursor, df):
    """Creatres dataframe for filmwork persons."""
    film_idxs = tuple(df["id"].values.tolist())
    columns = list(FilmworkPersonPydantic.__fields__)
    query = f"""
                SELECT *
                FROM film4person fwp
                    LEFT JOIN person p
                    ON fwp.person_id = p.id
                WHERE film_id in {film_idxs}
            """
    await cursor.execute(query)
    rows = await cursor.fetchall()
    df = pd.DataFrame.from_records(rows)[columns]\
        .drop('id', axis=1).rename(columns={"film_id": "id"})
    df[['id', 'person_id']] = df[['id', 'person_id']].astype(str)
    return df.replace({np.nan: None})


async def get_dataframes(
    cursor: AsyncConnection.cursor,
    chunk: int,
    Film: pydantic.BaseModel,
    Film4Genre: pydantic.BaseModel,
    Film4Person: pydantic.BaseModel
) -> tuple[pd.DataFrame]:
    df = get_film_chunk(Film, chunk)
    df_fwg = await get_film4genre_chunk(Film4Genre, cursor, df)
    df_fwp = await get_film4person_chunk(Film4Person, cursor, df)
    return df, df_fwg, df_fwp, df['id'].values.tolist()


async def execute_film_query(postgres_cur: AsyncConnection.cursor, current_state: tuple[str]):
    query = get_query(current_state)
    await postgres_cur.execute(query)
    chunk = await postgres_cur.fetchmany(settings.POSTGRES_CHUNK_SIZE)
    return chunk


async def extract(postgres_cur: AsyncConnection.cursor, current_state: tuple[str]) -> tuple[dict]:
    """Extracts data from postgres."""
    logger.info("\t[EXTRACT] getting current state ...")
    try:
        chunk = await execute_film_query(postgres_cur, current_state)
        df, df_fwg, df_fwp, new_ids = await get_dataframes(
            postgres_cur, chunk, Film, Film4Genre, Film4Person
        )
        return df, df_fwg, df_fwp, new_ids
    except Exception as e:
        logger.info(e)
        return None, None, None, None
