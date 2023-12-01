from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models.token import Token
from src.databases.db import db_session


class TokenSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Token
        include_fk = True
        sqla_session = db_session

token_schema = TokenSchema()
tokens_schema = TokenSchema(many=True)



