

from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import insert
from model.models import Venue
from flask_wtf import Form
from forms import VenueForm
from model.models import db
import json


def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = Venue.query.all()
  return render_template('pages/venues.html', areas=data)

def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  response = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Venue.query.get(venue_id)
  return render_template('pages/show_venue.html', venue=data)

def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None



def edit_venue(venue_id):
  form = VenueForm()
  venue =Venue.query.get(venue_id)
  venue.name = request.form.get('name')
  venue.city = request.form.get('city')
  venue.state = request.form.get('state')
  venue.phone = request.form.get('phone')
  venue.image_link = request.form.get('image_link')
  venue.facebook_link = request.form.get('facebook_link')
  venue.website = request.form.get('website')
  venue.genres = json.dumps(request.form.getlist('genres'))
  venue.seeking_venue = request.form.get('seeking_venue')
  venue.seeking_description = request.form.get('seeking_description')
  venue.seeking_talent = True if venue.seeking_talent == 'y' else False
  db.session.add(venue)
  db.session.commit()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  venue_id = Venue.query().filter(Venue.id==venue_id).get(Venue.id)
  return redirect(url_for('show_venue', venue_id=venue_id))




