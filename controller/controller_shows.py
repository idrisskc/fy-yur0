from flask import Flask, render_template, request, Response, flash, redirect, url_for
from model.models import Artist, Venue, Show
from flask_sqlalchemy import SQLAlchemy
from forms import *

app = Flask(__name__)
db = SQLAlchemy(app)

def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
    req = request.form
    try:
        show = Show(venue_id=req['venue_id'],
                    artist_id=req['artist_id'],
                    start_time=req['start_time']
                    )
        db.session.add(show)
        db.session.commit()
        flash('Show Successfully Added')
    except Exception:
        flash('An error occurred. Show could not be created')
    finally:
        db.session.close()
     # TODO: on unsuccessful db insert, flash an error instead.
     # e.g., flash('An error occurred. Show could not be listed.')
     # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    data = []
    for show in Show.query.all():
        artist = Artist.query.get(show.artist_id)
        venue = Artist.query.get(show.venue_id)
        data.append({
            "venue_id": show.venue_id,
            "venue_name": venue.name,
            "artist_id": show.artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time
        })

    return render_template('pages/shows.html', shows=data)  