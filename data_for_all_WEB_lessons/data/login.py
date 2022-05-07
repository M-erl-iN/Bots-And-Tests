import datetime

import sqlalchemy
from flask_login import LoginManager

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    email = sqlalchemy.Column(
        sqlalchemy.VARCHAR, index=True, unique=True, nullable=True
    )
    hashed_password = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    status = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    level_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    words = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
