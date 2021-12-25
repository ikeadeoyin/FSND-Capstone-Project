import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json

from dotenv import load_dotenv
load_dotenv()

database_path = os.getenv('DATABASE_UR')
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()




#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

casting= db.Table("casting",
db.Column("Movie_id", db.Integer, db.ForeignKey('Movie.id'), primary_key=True),
db.Column("Actor_id", db.Integer, db.ForeignKey('Actor.id'), primary_key=True))


class Movie(db.Model):
    __tablename__ = "Movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    release_date = db.Column(db.DateTime, nullable=False)
    length = db.Column(db.Integer())

    def __init__(self, title, release_date, length):
        self.title = title
        self.release_date = release_date
        self.length = length
        

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
     return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
      'length': self.length, 
      'actors': [x.name for x in self.Actor],         
    }

class Actor(db.Model):
    __tablename__ = "Actor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    movies = db.relationship('Movie', secondary= casting, backref=db.backref('Actor', lazy=True))

    def __init__(self, name, gender, movies):
        self.name = name
        self.gender = gender
        self.movies = movies
        

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
     return {
      'id': self.id,
      'name': self.name,
      'gender': self.gender,
      'movies': [x.title for x in self.movies]           
    }



# '''
# Person
# Have title and release year
# '''
# class Person(db.Model):  
#   __tablename__ = 'People'

#   id = Column(Integer, primary_key=True)
#   name = Column(String)
#   catchphrase = Column(String)

#   def __init__(self, name, catchphrase=""):
#     self.name = name
#     self.catchphrase = catchphrase

#   def format(self):
#     return {
#       'id': self.id,
#       'name': self.name,
#       'catchphrase': self.catchphrase}
