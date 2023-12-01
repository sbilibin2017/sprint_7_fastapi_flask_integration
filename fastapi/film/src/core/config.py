from logging import config as logging_config
from pathlib import Path

from core.logger import LOGGING
from dotenv import dotenv_values
from pydantic import BaseSettings

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

config = dotenv_values(BASE_DIR / ".env")

dev = bool(int(config["DEV"]))
if dev:
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


class Settings(BaseSettings):
    PROJECT_NAME = api_config["PROJECT_NAME"]

    REDIS_HOST = docker_config["REDIS_HOST"]
    REDIS_PORT = redis_config["REDIS_PORT"]

    ELASTIC_HOST = docker_config["ELASTIC_HOST"]
    ELASTIC_PORT = elastic_config["ELASTIC_PORT"]
    ELASTIC_URL = f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"
    ELASTIC_FILM_INDEX = elastic_config["ELASTIC_FILM_INDEX"]
    ELASTIC_GENRE_INDEX = elastic_config["ELASTIC_GENRE_INDEX"]
    ELASTIC_ACTOR_INDEX = elastic_config["ELASTIC_ACTOR_INDEX"]
    ELASTIC_WRITER_INDEX = elastic_config["ELASTIC_WRITER_INDEX"]
    ELASTIC_DIRECTOR_INDEX = elastic_config["ELASTIC_DIRECTOR_INDEX"]

    ELASTIC_SCROLL = "2s"
    ELASTIC_SCROLL_SIZE = 100

    CACHE_EXPIRE_IN_SECONDS = 60 * 5

    DEV = dev
