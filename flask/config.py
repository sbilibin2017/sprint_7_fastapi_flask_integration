from pathlib import Path
from dotenv import dotenv_values
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent.parent

cfg = dotenv_values(BASE_DIR / ".env")

dev = bool(int(cfg["DEV"]))
sleep = int(cfg["SLEEP"])

if dev:
    redis = dotenv_values(BASE_DIR / "env/redis/.env.dev")
    postgres = dotenv_values(BASE_DIR / "env/postgres/.env.dev")
    flask = dotenv_values(BASE_DIR / "env/flask/.env.dev")
    jwt = dotenv_values(BASE_DIR / "env/jwt/.env.dev")
    admin = dotenv_values(BASE_DIR / "env/admin/.env.dev")
    docker = dotenv_values(BASE_DIR / "env/docker/.env.dev")
    test = dotenv_values(BASE_DIR / "env/test/.env.dev")
else:
    redis = dotenv_values(BASE_DIR / "env/redis/.env")
    postgres = dotenv_values(BASE_DIR / "env/postgres/.env")
    flask = dotenv_values(BASE_DIR / "env/flask/.env")
    jwt = dotenv_values(BASE_DIR / "env/jwt/.env")
    admin = dotenv_values(BASE_DIR / "env/admin/.env")
    docker = dotenv_values(BASE_DIR / "env/docker/.env")
    test = dotenv_values(BASE_DIR / "env/test/.env")


@dataclass
class Postgres:
    user: str = postgres["POSTGRES_USER"]
    password: str = postgres["POSTGRES_PASSWORD"]
    host: str = postgres["POSTGRES_HOST"]
    port: int = postgres["POSTGRES_PORT"]
    db: str = postgres["POSTGRES_DB"]


@dataclass
class Redis:
    host: str = redis["REDIS_HOST"]
    port: int = redis["REDIS_PORT"]
    db: int = redis["REDIS_DB"]


@dataclass
class Flask:
    secret_key: str = flask["SECRET_KEY"]


@dataclass
class JWT:
    secret_key: str = jwt["SECRET_KEY"]
    access_token_expires: int = jwt["ACCESS_TOKEN_EXPIRES"]
    refresh_token_expires: int = jwt["REFRESH_TOKEN_EXPIRES"]


@dataclass
class Admin:
    login: str = admin["LOGIN"]
    password: str = admin["PASSWORD"]
    all_roles: str = admin["ALL_ROLES"]
    admin_role: str = admin["ADMIN_ROLE"]


@dataclass
class Docker:
    postgres_host: str = docker["POSTGRES_HOST"]
    redis_host: str = docker["REDIS_HOST"]


@dataclass
class Test:
    n_samples: int = test["N_SAMPLES"]
    redis_test_db: int = test["REDIS_TEST_DB"]
    postgres_test_db: str = test["POSTGRES_TEST_DB"]


class Config:
    postgres: Postgres = Postgres()
    redis: Redis = Redis()
    flask: Flask = Flask()
    jwt: JWT = JWT()
    admin: Admin = Admin()
    docker: Docker = Docker()
    test: Test = Test()


config = Config()
