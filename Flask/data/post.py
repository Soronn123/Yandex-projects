import datetime
import sqlalchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase, UserMixin):
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    crat_content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.String,
                                     default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = relationship('User')
    comments = relationship("Comments", back_populates='post')