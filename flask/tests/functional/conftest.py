import pytest
from app import app as aplication
from config import redis, config
from config import config
from src.databases.db import db_session, add_admin_and_roles
from app import models
# from app.src.models.role import Role
# from app.src.models.user import User
from src.repositories.cache import CacheRepository
from src.services.session import session_service
from src.services.user import user_crud_service
from src.helpers.request_user_agent import get_user_agent


@pytest.fixture()
def app():
    model_user = models['user']
    model_role = models['role']
    add_admin_and_roles(aplication, model_user, model_role)
    aplication.config.update({
        "TESTING": True,
    })

    yield aplication


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

