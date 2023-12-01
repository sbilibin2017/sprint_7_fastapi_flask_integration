from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.services.user import user_crud_service
from src.services.session import session_service
from src.services.role import role_crud_service
from src.schemas.user import users_schema,user_schema
from src.schemas.session import sessions_schema
from src.decorators.auth import auth_required
from config import config
from src.helpers.request_body import get_request_body
from src.helpers.request_user_agent import get_user_agent
from src.dataclasses.auth import AuthDataclass
from src.repositories.cache import cache_repository

bp_auth = Blueprint("auth", __name__)
from src.databases.cache import cache


@bp_auth.route('/auth/register', methods=["POST"])
def register():
    body = get_request_body()
    auth_data = AuthDataclass(**body)
    role = role_crud_service.get_by_name('user')
    user_crud_service.create({'login':auth_data.login, 'password':auth_data.password}, roles = [role.name])
    return jsonify(msg="Registered successfully!", status=HTTPStatus.OK)


@bp_auth.route("/auth/login", methods=["POST"])
def login():
    body = get_request_body()
    auth_data = AuthDataclass(**body)
    auth_data.user_agent = get_user_agent()
    user = user_crud_service.get_by_login(auth_data.login)
    user_id = user.id
    cache_repository.check(user_id)
    access_token, refresh_token = session_service.create(
        {"user_id": user_id, "user_agent": auth_data.user_agent}
    )   
    cache_repository.set(user_id, access_token)
    return jsonify(
        access_token=access_token, refresh_token=refresh_token, status=HTTPStatus.OK
    )


@bp_auth.route("/auth/logout", methods=["DELETE"])
@auth_required(roles=['admin','user'], is_refresh=False)
def logout(current_user):
    session_service.deactivate_refresh(current_user["session_id"])   
    cache_repository.block(current_user["user_id"])
    return jsonify(msg="Bye!", status=HTTPStatus.OK)