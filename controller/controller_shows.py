import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from model.models import Artist, Venue, Show
from flask_sqlalchemy import SQLAlchemy
from forms import *

app = Flask(__name__)
db = SQLAlchemy(app)

def create_shows():
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)

def create_show_submission():
    form = ShowForm()

    if form.validate():
        try:
            show = Show(
                venue_id=request.form.get("venue_id"),
                artist_id=request.form.get("artist_id"),
                start_time=request.form.get("start_time"),
            )
            db.session.add(show)
            db.session.commit()
            flash(f"Show was successfully listed!")
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash("An error occurred. Show could not be listed.")
        finally:
            db.session.close()

        return redirect(url_for("index"))

    return render_template("forms/new_show.html", form=form)

def shows():
    data = []
    shows = Show.query.order_by(Show.start_time).all()

    for show in shows:
        data.append(
            {
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "artist_id": show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time,
            }
        )

    return render_template("pages/shows.html", shows=data)