from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ETLSettings(BaseSettings):

    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_URL: str

    ELASTIC_FILM_MAPPING_FILENAME: str
    ELASTIC_GENRE_MAPPING_FILENAME: str
    ELASTIC_ACTOR_MAPPING_FILENAME: str
    ELASTIC_WRITER_MAPPING_FILENAME: str
    ELASTIC_DIRECTOR_MAPPING_FILENAME: str
    ELASTIC_SEARCH_MAPPING_FILENAME: str

    ELASTIC_FILM_INDEX: str
    ELASTIC_GENRE_INDEX: str
    ELASTIC_DIRECTOR_INDEX: str
    ELASTIC_WRITER_INDEX: str
    ELASTIC_ACTOR_INDEX: str
    ELASTIC_SEARCH_INDEX: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_FILM_STATE: str
    REDIS_GENRE_STATE: str
    REDIS_ACTOR_STATE: str
    REDIS_WRITER_STATE: str
    REDIS_DIRECTOR_STATE: str

    DB_NAME: str
    DB_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_CHUNK_SIZE: int

    SLEEP: int


config = dotenv_values(BASE_DIR / ".env")
if bool(int(config['DEV'])):
    api_config = dotenv_values(BASE_DIR / "env/api/.env.dev")
    redis_config = dotenv_values(BASE_DIR / "env/redis/.env.dev")
    elastic_config = dotenv_values(BASE_DIR / "env/elasticsearch/.env.dev")
    docker_config = dotenv_values(BASE_DIR / "env/docker/.env.dev")
    postgres_config = dotenv_values(BASE_DIR / "env/postgres/.env.dev")
else:
    api_config = dotenv_values(BASE_DIR / "env/api/.env")
    redis_config = dotenv_values(BASE_DIR / "env/redis/.env")
    elastic_config = dotenv_values(BASE_DIR / "env/elasticsearch/.env")
    docker_config = dotenv_values(BASE_DIR / "env/docker/.env")
    postgres_config = dotenv_values(BASE_DIR / "env/postgres/.env")


settings = ETLSettings(

    ELASTIC_HOST=docker_config["ELASTIC_HOST"],
    ELASTIC_PORT=elastic_config["ELASTIC_PORT"],
    ELASTIC_URL="http://{}:{}".format(
        docker_config["ELASTIC_HOST"], elastic_config["ELASTIC_PORT"]),

    ELASTIC_FILM_MAPPING_FILENAME=elastic_config["ELASTIC_FILM_MAPPING_FILENAME"],
    ELASTIC_SEARCH_MAPPING_FILENAME=elastic_config["ELASTIC_SEARCH_MAPPING_FILENAME"],
    ELASTIC_GENRE_MAPPING_FILENAME=elastic_config["ELASTIC_GENRE_MAPPING_FILENAME"],
    ELASTIC_ACTOR_MAPPING_FILENAME=elastic_config["ELASTIC_ACTOR_MAPPING_FILENAME"],
    ELASTIC_WRITER_MAPPING_FILENAME=elastic_config["ELASTIC_WRITER_MAPPING_FILENAME"],
    ELASTIC_DIRECTOR_MAPPING_FILENAME=elastic_config["ELASTIC_DIRECTOR_MAPPING_FILENAME"],

    ELASTIC_FILM_INDEX=elastic_config["ELASTIC_FILM_INDEX"],
    ELASTIC_SEARCH_INDEX=elastic_config["ELASTIC_SEARCH_INDEX"],
    ELASTIC_GENRE_INDEX=elastic_config["ELASTIC_GENRE_INDEX"],
    ELASTIC_DIRECTOR_INDEX=elastic_config["ELASTIC_DIRECTOR_INDEX"],
    ELASTIC_WRITER_INDEX=elastic_config["ELASTIC_WRITER_INDEX"],
    ELASTIC_ACTOR_INDEX=elastic_config["ELASTIC_ACTOR_INDEX"],

    REDIS_HOST=docker_config["REDIS_HOST"],
    REDIS_PORT=redis_config["REDIS_PORT"],
    REDIS_FILM_STATE=redis_config["REDIS_FILM_STATE"],
    REDIS_GENRE_STATE=redis_config["REDIS_GENRE_STATE"],
    REDIS_ACTOR_STATE=redis_config["REDIS_ACTOR_STATE"],
    REDIS_WRITER_STATE=redis_config["REDIS_WRITER_STATE"],
    REDIS_DIRECTOR_STATE=redis_config["REDIS_DIRECTOR_STATE"],

    DB_NAME=postgres_config["DB_NAME"],
    DB_USER=postgres_config["DB_USER"],
    POSTGRES_PASSWORD=postgres_config["POSTGRES_PASSWORD"],
    POSTGRES_HOST=docker_config["POSTGRES_HOST"],
    POSTGRES_PORT=postgres_config["POSTGRES_PORT"],
    POSTGRES_CHUNK_SIZE=postgres_config["POSTGRES_CHUNK_SIZE"],

    SLEEP=2
)
