import uuid
from datetime import datetime

import pandas as pd

from utils.logger import logger
from utils.validator import FilmElastic, GenreElastic, PersonElastic

DEFAULT_NUM = -1.0
DEFAULT_DATE = '1777-07-07'
DEFAULT_STR = ""
DEFAULT_LIST = []
DEFAULT_DICT = {}


def build_film_data(
    filmwork_id: uuid.UUID, df: pd.DataFrame, df_fwg: pd.DataFrame, df_fwp: pd.DataFrame
) -> tuple[dict, datetime]:
    """Prepare json data."""

    df_sub = df[df["id"] == filmwork_id]
    df_fwg_sub = df_fwg[df_fwg["id"] == filmwork_id]
    df_fwp_sub = df_fwp[df_fwp["id"] == filmwork_id]

    d = {}
    d["id"] = filmwork_id
    d["title"] = df_sub["title"].iloc[0]
    d["imdb_rating"] = df_sub["imdb_rating"].iloc[0]
    d['creation_date'] = df_sub['creation_date'].iloc[0]
    d["type"] = df_sub["type"].iloc[0]
    d["description"] = df_sub["description"].iloc[0]
    if len(df_fwg_sub) > 0:
        d["genre__name"] = df_fwg_sub["name"].values.tolist()
        d["genre"] = df_fwg_sub[["genre_id", "name"]].rename(
            columns={'genre_id': 'id'}).to_dict("records")
    else:
        d["genre__name"] = DEFAULT_LIST
        d["genre"] = DEFAULT_LIST
    for key in ["director", "actor", "writer"]:
        subdf = df_fwp_sub[df_fwp_sub["role"] == key]
        if len(subdf) > 0:
            d[f"{key}__full_name"] = subdf["full_name"].values.tolist()
            d[key] = subdf[["person_id", "full_name"]].rename(
                columns={'person_id': 'id'}).to_dict("records")
        else:
            d[f"{key}__full_name"] = DEFAULT_LIST
            d[key] = DEFAULT_LIST
    d_validated = FilmElastic(**d).dict()
    return d_validated


async def transform(df: pd.DataFrame, df_fwg: pd.DataFrame, df_fwp: pd.DataFrame) -> tuple[list[dict], datetime]:
    """Transforms extracted data."""
    logger.info("\t[TRANSFORM]")
    data_film, data_genre, data_actor, data_writer, data_director \
        = [], [], [], [], []

    for film_id in df["id"].values:
        film = build_film_data(film_id, df, df_fwg, df_fwp)
        data_film.append(film)

    for genre_id, subdf in df_fwg.groupby('genre_id'):
        genre = GenreElastic(**{'id': genre_id, 'name': subdf['name'].iloc[0],
                                'film': subdf[['id']].to_dict('records')}).dict()
        data_genre.append(genre)

    for role, data_role in zip(['actor', 'writer', 'director'], [data_actor, data_writer, data_director]):
        subdf = df_fwp[df_fwp['role'] == role]
        for person_id, subsubdf in subdf.groupby('person_id'):
            genre = PersonElastic(**{
                'id': person_id,
                'full_name': subsubdf['full_name'].iloc[0],
                'film': subsubdf[['id']].to_dict('records')
            }).dict()
            data_role.append(genre)

    return data_film, data_genre, data_actor, data_writer, data_director
