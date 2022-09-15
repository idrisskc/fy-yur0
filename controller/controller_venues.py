

import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for, abort
from model.models import Show, Venue, Artist
# from flask_wtf import Form
from datetime import datetime
from forms import SearchForm, VenueForm
from model.models import db
import json

# STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','MD','MA','MI','MN','MS','MO','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

def venues():
    form = SearchForm()

    venues = (
        Venue.query.with_entities(Venue.id, Venue.name, Venue.state, Venue.city)
        .order_by(Venue.city, Venue.state)
        .all()
    )

    data = []
    previous_location = None
    i = -1

    for venue in venues:
        current_location = f"{venue.city}, {venue.state}"

        if previous_location != current_location:
            # Designing "container" object for the grouping of venues by location
            data.append({"city": venue.city, "state": venue.state, "venues": []})

            i += 1
            previous_location = current_location

        # Adding venue to "grouped-by-location" object container
        data[i]["venues"].append(
            {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": Show.query.filter(
                    db.and_(Show.venue_id == venue.id, Show.start_time > datetime.now())
                ).count(),
            }
        )

    return render_template("pages/venues.html", areas=data, form=form)

def search_venues():
    form = SearchForm()
    search_term = request.form.get("search_term")

    venues = (
        Venue.query.with_entities(Venue.id, Venue.name)
        .filter(Venue.name.ilike(f"%{search_term}%"))
        .all()
    )

    data = {
        "count": len(venues),
        "data": [
            {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": Show.query.filter(
                    db.and_(Show.venue_id == venue.id, Show.start_time > datetime.now())
                ).count(),
            }
            for venue in venues
        ],
    }

    return render_template(
        "pages/search_venues.html",
        results=data,
        search_term=request.form.get("search_term", ""),
        form=form,
    )

def show_venue(venue_id):
    form = SearchForm()

    venue = Venue.query.get(venue_id)

    if venue:
        past_shows = []
        upcoming_shows = []

        for show in venue.shows:
            artist = {
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time,
            }

            if show.start_time < datetime.now():
                past_shows.append(artist)
            else:
                upcoming_shows.append(artist)

        data = {
            **venue.__dict__,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }

        return render_template("pages/show_venue.html", venue=data, form=form)

    return render_template("errors/404.html", form=form)

def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

def create_venue_submission():
    form = VenueForm()

    if form.validate():
        try:
            venue = Venue(
                name=request.form.get("name"),
                city=request.form.get("city"),
                state=request.form.get("state"),
                address=request.form.get("address"),
                phone=request.form.get("phone"),
                image_link=request.form.get("image_link"),
                facebook_link=request.form.get("facebook_link"),
                website=request.form.get("website"),
                seeking_talent=True if request.form.get("seeking_talent") else False,
                seeking_description=request.form.get("seeking_description"),
                genres=request.form.getlist("genres"),
            )
            db.session.add(venue)
            db.session.commit()

            venue_name = venue.name
            flash(f"Venue {venue_name} was successfully listed!")
        except:
            db.session.rollback()
            print(sys.exc_info())

            venue_name = request.form.get("name")
            flash(f"An error occurred. Venue {venue_name} could not be listed.")
        finally:
            db.session.close()

        return redirect(url_for("index"))

    return render_template("forms/new_venue.html", form=form)


def delete_venue(venue_id):
    try:
        venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
        db.session.delete(venue)
        db.session.commit()

        flash(f"Venue {venue.name} was successfully deleted.")
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash(f"An error occurred. Venue {venue.name} could not be deleted.")
    finally:
        db.session.close()

    return redirect(url_for("index"))

def edit_venue(venue_id):
    form = VenueForm()
    venue = (
        Venue.query.with_entities(Venue.name, Venue.id)
        .filter(Venue.id == venue_id)
        .one_or_none()
    )

    if venue:
        return render_template("forms/edit_venue.html", form=form, venue=venue)

    return render_template("errors/404.html", form=form)

def edit_venue_submission(venue_id):
    form = VenueForm()

    if form.validate():
        try:
            db.session.query(Venue).filter(Venue.id == venue_id).update(
                {
                    "name": request.form.get("name"),
                    "city": request.form.get("city"),
                    "state": request.form.get("state"),
                    "address": request.form.get("address"),
                    "phone": request.form.get("phone"),
                    "image_link": request.form.get("image_link"),
                    "facebook_link": request.form.get("facebook_link"),
                    "website": request.form.get("website"),
                    "seeking_talent": request.form.get("seeking_talent", False),
                    "seeking_description": request.form.get("seeking_description"),
                    "genres": request.form.getlist("genres"),
                }
            )
            db.session.commit()
            flash(f"Venue was successfully edited!")
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash(f"An error occurred. Venue could not be edited.")
        finally:
            db.session.close()

        return redirect(url_for("show_venue", venue_id=venue_id))

    venue = (
        Venue.query.with_entities(Venue.name, Venue.id)
        .filter(Venue.id == venue_id)
        .one_or_none()
    )

    return render_template("forms/edit_venue.html", form=form, venue=venue)


