from tkinter.tix import COLUMN
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publish_date = db.Column(db.DateTime)
    retrieval_date = db.Column(db.DateTime)
    url = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    summary = db.Column(db.String(255))
