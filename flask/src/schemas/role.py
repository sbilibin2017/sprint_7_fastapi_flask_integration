from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models.role import Role
from src.databases.db import db_session


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True
        sqla_session = db_session

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
