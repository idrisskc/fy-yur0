import sys
from flask_moment import Moment
from flask import render_template, request, flash, redirect, url_for, abort
from model.models import Artist, Show, Venue
from forms import *
# from ..app import app
from model.models import db

# STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','MD','MA','MI','MN','MS','MO','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

# @app.route('/')
def artists():
    form = SearchForm()
    data = Artist.query.with_entities(Artist.id, Artist.name).all()

    return render_template("pages/artists.html", artists=data, form=form)


def search_artists():
    form = SearchForm()
    search_term = request.form.get("search_term")

    artists = (
        Artist.query.with_entities(Artist.id, Artist.name)
        .filter(Artist.name.ilike(f"%{search_term}%"))
        .all()
    )

    data = {
        "count": len(artists),
        "data": [
            {
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": Show.query.filter(
                    db.and_(
                        Show.artist_id == artist.id, Show.start_time > datetime.now()
                    )
                ).count(),
            }
            for artist in artists
        ],
    }

    return render_template(
        "pages/search_artists.html",
        results=data,
        search_term=request.form.get("search_term", ""),
        form=form,
    )

def show_artist(artist_id):
    form = SearchForm()

    artist = Artist.query.get(artist_id)

    if artist:
        past_shows = []
        upcoming_shows = []

        for show in artist.shows:
            venue = {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time,
            }

            if show.start_time < datetime.now():
                past_shows.append(venue)
            else:
                upcoming_shows.append(venue)

        data = {
            **artist.__dict__,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }

        return render_template("pages/show_artist.html", artist=data, form=form)

    return render_template("errors/404.html", form=form)


# @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = (
        Artist.query.with_entities(Artist.name, Artist.id)
        .filter(Artist.id == artist_id)
        .one_or_none()
    )

    if artist:
        return render_template("forms/edit_artist.html", form=form, artist=artist)

    return render_template("errors/404.html", form=form)

def edit_artist_submission(artist_id):
    form = ArtistForm()

    if form.validate():
        try:
            db.session.query(Artist).filter(Artist.id == artist_id).update(
                {
                    "name": request.form.get("name"),
                    "city": request.form.get("city"),
                    "state": request.form.get("state"),
                    "phone": request.form.get("phone"),
                    "image_link": request.form.get("image_link"),
                    "facebook_link": request.form.get("facebook_link"),
                    "website": request.form.get("website"),
                    "seeking_venue": True
                    if request.form.get("seeking_venue")
                    else False,
                    "seeking_description": request.form.get("seeking_description"),
                    "genres": request.form.getlist("genres"),
                }
            )
            db.session.commit()
            flash(f"Artist was successfully edited!")
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash(f"An error occurred. Artist could not be edited.")
        finally:
            db.session.close()

        return redirect(url_for("show_artist", artist_id=artist_id))

    artist = (
        Artist.query.with_entities(Artist.name, Artist.id)
        .filter(Artist.id == artist_id)
        .one_or_none()
    )

    return render_template("forms/edit_artist.html", form=form, artist=artist)

def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


def create_artist_submission():
    form = ArtistForm()

    if form.validate():
        try:
            artist = Artist(
                name=request.form.get("name"),
                city=request.form.get("city"),
                state=request.form.get("state"),
                phone=request.form.get("phone"),
                image_link=request.form.get("image_link"),
                facebook_link=request.form.get("facebook_link"),
                website=request.form.get("website"),
                seeking_venue=True if request.form.get("seeking_venue") else False,
                seeking_description=request.form.get("seeking_description"),
                genres=request.form.getlist("genres "),
            )

            db.session.add(artist)
            db.session.commit()

            artist_name = artist.name
            flash(f"Artist {artist_name} was successfully listed!")
        except:
            db.session.rollback()
            print(sys.exc_info())

            artist_name = request.form.get("name")
            flash(f"An error occurred. Artist {artist_name} could not be listed.")
        finally:
            db.session.close()

        return redirect(url_for("index"))

    return render_template("forms/new_artist.html", form=form)
