from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(20)) # This will be 'admin' or 'member'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20))
    genre = db.Column(db.String(50))
    publisher = db.Column(db.String(100))
    year = db.Column(db.Integer)
    copies = db.Column(db.Integer)