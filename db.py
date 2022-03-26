from __main__ import *
#SQL Alchemy
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'
db = SQLAlchemy(app)


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mal_id = db.Column(db.Integer)
    sources = db.Column(db.String)
    image_url = db.Column(db.String)
    title = db.Column(db.String)
    airing = db.Column(db.String)
    synopsis = db.Column(db.String)
    type = db.Column(db.String)
    planned_episodes = db.Column(db.String)
    score = db.Column(db.Float)
    episodes = db.relationship('Episode')
    add_date = db.Column(db.Date, server_default=db.func.current_date())
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment')
    tags = db.relationship('Tag')
    pinned = db.relationship('Pinned')
    synonyms = db.Column(db.String)
    rated = db.Column(db.String)
    orginal_url = db.Column(db.String)


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime = db.Column(db.Integer, db.ForeignKey('anime.id'))
    title = db.Column(db.String)
    url = db.Column(db.String)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean)
    comments = db.relationship("Comment")
    animes = db.relationship("Anime")
    pinned = db.relationship('Pinned')
    registry_date=db.Column(db.Date, server_default=db.func.current_date())


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String)
    anime = db.Column(db.Integer, db.ForeignKey('anime.id'))
    add_date=db.Column(db.Date, server_default=db.func.current_date())


class Pinned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    anime = db.Column(db.Integer, db.ForeignKey(Anime.id))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)
    anime = db.Column(db.Integer, db.ForeignKey('anime.id'))

db.create_all()