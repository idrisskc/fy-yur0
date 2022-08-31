from flask_moment import Moment
from flask import render_template, request, flash, redirect, url_for, abort
from model.models import Artist, Venue
from forms import *
# from ..app import app
from model.models import db

STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','MD','MA','MI','MN','MS','MO','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

# @app.route('/')
def artists():
  # TODO: replace with real data returned from querying the database
  # data = Artist.query.all() 
  data = []
  for artist in Artist.query.all():
      singleArtist = {
          "id": artist.id,
          "name": artist.name
      }
      data.append(singleArtist)
  return render_template('pages/artists.html', artists=data)

def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    searchTerm = request.form.get('search_term', '')
    search = "%{}%".format(searchTerm)
    artists = Artist.query.filter(Artist.name.ilike(search)).all()

    counter = 0
    data = {
        "count": len(artists),
        "data": []
    }
    for artist in artists:
        for show in artist.shows:
            counter = 0
            if(show.start_time > datetime.now()):
                counter += 1
        tempData = {
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": counter
        }
        data["data"].append(tempData)
    return render_template('pages/search_artists.html', results=data, search_term=request.form.get('search_term', ''))


def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    specificArtist = Artist.query.get(artist_id)
   
    data = {
        "id": artist_id,
        "name": specificArtist.name,
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "city": specificArtist.city,
        "state": specificArtist.state,
        "phone": specificArtist.phone,
        "website": "https://www.themusicalhop.com",
        "facebook_link": specificArtist.facebook_link,
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": specificArtist.image_link,
        "upcoming_shows_count": 0,
        "upcoming_shows": [],
        "past_shows": []
    }

    counter = 0
    for show in specificArtist.shows:
        venue = Venue.query.get(show.venue_id)
        if(show.start_time > datetime.now()):
            data["upcoming_shows"].append({
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time
            })
            counter += 1
        else:
            data["past_shows"].append({
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time
            })
        data['upcoming_shows_count'] = counter

    return render_template('pages/show_artist.html', artist=data)

# @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    specificArtist = Artist.query.get(artist_id)

    artist = {
      "id": artist_id,
      "name": specificArtist.name,
      "genres": specificArtist.genres,
      "city": specificArtist.city,
      "state": specificArtist.state,
      "phone": specificArtist.phone,
      "website": "https://www.themusicalhop.com",
      "facebook_link": specificArtist.facebook_link,
      "seeking_talent": True,
      "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
      "image_link": specificArtist.image_link
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    req = request.form
    if req['state'] not in STATES:
        abort(422)
    try:
        artist = Artist.query.get(artist_id)
        artist.name = req['name']
        artist.city = req['city']
        artist.state = req['state']
        artist.phone = req['phone']
        artist.genres = req['genres']
        artist.facebook_link = req['facebook_link']
        artist.image_link = 'https://via.placeholder.com/335x500.png'
        db.session.commit()
        flash('Artist ' + req['name'] + ' was successfully changed!')
    except Exception:
        flash('An error occurred. Artist ' + req['name'] + ' could not be changed.')
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  # on successful db insert, flash success
    req = request.form
    if req['state'] not in STATES:
        abort(422)
    try:
        artist = Artist(name=req['name'],
                    city=req['city'],
                    state=req['state'],
                    phone=req['phone'],
                    genres=req['genres'],
                    facebook_link=req['facebook_link'],
                    image_link='https://via.placeholder.com/335x500.png')
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + req['name'] + ' was successfully listed!')
    except Exception:
        flash('An error occurred. Artist ' + req['name'] + ' could not be listed.')
    finally:
        db.session.close()
     # TODO: on unsuccessful db insert, flash an error instead.
     # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
