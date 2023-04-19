from flask_login import UserMixin
from sqlalchemy import Table, Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


def set_password(password):
    return generate_password_hash(password)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1200), unique=True)
    password = db.Column(db.String(1200))
    UUID = db.Column(db.String(1200), unique=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1200), unique=True)
    desc = db.Column(db.String(1200))
    owner = db.Column(db.String(1200), db.ForeignKey(User.name))
    date = db.Column(db.TIMESTAMP)
    file = db.Column(db.BLOB)


