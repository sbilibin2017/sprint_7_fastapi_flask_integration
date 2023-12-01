from flask import Flask
from src.databases.db import db_session, add_admin_and_roles
from src.models.user import User
from src.models.role import Role
from src.models import user_role
from src.models.session import Session
from src.models.token import Token
from uuid import UUID

from src.api.v1.admin.user import bp_admin_user
from src.api.v1.admin.role import bp_admin_role
from src.api.v1.auth import bp_auth
from src.api.v1.token import bp_token
from config import config

# init app
app = Flask(__name__)
app.config["SECRET_KEY"] = config.flask.secret_key

# models
models ={
    'user':User, 
    'role':Role, 
    'user_role':user_role, 
    'session':Session, 
    'token':Token
}

# add roles and admin
add_admin_and_roles(app, User, Role)

# add routers
app.register_blueprint(bp_admin_user)
app.register_blueprint(bp_admin_role)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_token)

