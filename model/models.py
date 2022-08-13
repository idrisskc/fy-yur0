
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

Shows = db.Table('Shows',
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(120), nullable = True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120),default = True)
    phone = db.Column(db.String(120), nullable = True)
    image_link = db.Column(db.String(500),default = True)
    facebook_link = db.Column(db.String(120), default = True)
    website = db.Column(db.String(120), default = True)
    seeking_description = db.Column(db.String(500), default = True)
    artist_name = db.Column(db.String(120))
    start_time = db.Column(db.DateTime(), default = datetime.utcnow)
    artist = db.relationship('Product', secondary = Shows, backref = db.backref('venues', lazy = True))
        
    def __repr__(self):
        return f'{self.name}:{self.id}'
    
    
class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    city = db.Column(db.String(120))
    website = db.Column(db.String(120), default=True)
    state = db.Column(db.String(120), nullable = True)
    phone = db.Column(db.String(120), nullable = True)
    genres = db.Column(db.String(120), nullable = True)
    image_link = db.Column(db.String(500), default=True)
    facebook_link = db.Column(db.String(120), default=True)
    seeking_description = db.Column(db.String(500), default=True)
    
    def __repr__(self):
        return f'{self.name}:{self.id}'
    



# data = [
#     {
#        'name':'The Musical Hop'
#        'genres':'diaz'
#        'city':'San Francisco'
#        'state':'CA' 
#     },
#     {
#        'name':'Park Square Live Music & Coffee'
#        'genres':'diaz'
#        'city':'San Francisco'
#        'state':'CA' 
#     },
#     {
#        'name':'The Dueling Pianos Bar'
#        'genres':'rock'
#        'city':'New York'
#        'state':'NY'   
#     }
# ]
# venue_insert = insert(Venue).values(data)    

# venue_insert = Venue(name='The Musical Hop',genres='rock', city='San Francisco', state='CA' )
# db.session.add(venue_insert)
# db.session.commit()