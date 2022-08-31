

from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for, abort
from model.models import Venue, Artist
# from flask_wtf import Form
from datetime import datetime
from forms import VenueForm
from model.models import db
import json

STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','MD','MA','MI','MN','MS','MO','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

def venues():
    # TODO: replace with real venues data.
    # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    for venue in Venue.query.with_entities(Venue.city, Venue.state).order_by(Venue.state).distinct():
        venueMetaData = {
            "city": venue[0],
            "state": venue[1],
        }
        tempVenues = []
        for fullVenue in Venue.query.filter_by(city=venue[0], state=venue[1]).all():
            tempVenue = {
                "id": fullVenue.id,
                "name": fullVenue.name,
            }
            for show in fullVenue.shows:
                counter = 0
                if(show.start_time > datetime.now()):
                    counter += 1
                tempVenue['num_upcoming_shows'] = counter
            tempVenues.append(tempVenue)
        venueMetaData['venues'] = tempVenues
        print(venueMetaData)
        data.append(venueMetaData)
    return render_template('pages/venues.html', areas=data)

def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    searchTerm = request.form.get('search_term', '')
    search = "%{}%".format(searchTerm)
    venues = Venue.query.filter(Venue.name.ilike(search)).all()

    counter = 0
    data = {
        "count": len(venues),
        "data": []
    }
    for venue in venues:
        for show in venue.shows:
            counter = 0
            if(show.start_time > datetime.now()):
                counter += 1
        tempData = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": counter
        }
        data["data"].append(tempData)
    
    return render_template('pages/search_venues.html', results=data, search_term=request.form.get('search_term', ''))

def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    specificVenue = Venue.query.get(venue_id)
    
    data = {
        "id": venue_id,
        "name": specificVenue.name,
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": specificVenue.address,
        "city": specificVenue.city,
        "state": specificVenue.state,
        "phone": specificVenue.phone,
        "website": "https://www.themusicalhop.com",
        "facebook_link": specificVenue.facebook_link,
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": specificVenue.image_link,
        "upcoming_shows_count": 0,
        "upcoming_shows": [],
        "past_shows": []
    }

    counter = 0
    for show in specificVenue.shows:
        artist = Artist.query.get(show.artist_id)
        if(show.start_time > datetime.now()):
            data["upcoming_shows"].append({
                "artist_id": show.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time
            })
            counter += 1
        else:
            data["past_shows"].append({
                "artist_id": show.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time
            })
        data['upcoming_shows_count'] = counter
    
    return render_template('pages/show_venue.html', venue=data)

def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  req = request.form
  if req['state'] not in STATES:
      abort(422)
  try:
      venue = Venue(name=req['name'],
                  city=req['city'],
                  state=req['state'],
                  address=req['address'],
                  phone=req['phone'],
                  genres=req['genres'],
                  facebook_link=req['facebook_link'],
                  image_link='https://via.placeholder.com/335x500.png')
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + req['name'] + ' was successfully listed!')
  except Exception:
      flash('An error occurred. Venue ' + req['name'] + ' could not be listed.')
  finally:
      db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage
        return jsonify({'success': True})




def edit_venue(venue_id):
  form = VenueForm()
  specificVenue = Venue.query.get(venue_id)

  venue = {
    "id": venue_id,
    "name": specificVenue.name,
    "genres": specificVenue.genres,
    "address": specificVenue.address,
    "city": specificVenue.city,
    "state": specificVenue.state,
    "phone": specificVenue.phone,
    "website": "https://www.themusicalhop.com",
    "facebook_link": specificVenue.facebook_link,
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": specificVenue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  req = request.form

  if req['state'] not in STATES:
    abort(422)
        
  try:
      venue = Venue.query.get(venue_id)
      venue.name = req['name']
      venue.city = req['city']
      venue.state = req['state']
      venue.address = req['address']
      venue.phone = req['phone']
      venue.genres = req['genres']
      venue.facebook_link = req['facebook_link']
      venue.image_link = 'https://via.placeholder.com/335x500.png'
      db.session.commit()
      flash('Venue ' + req['name'] + ' was successfully changed!')
  except Exception:
      flash('An error occurred. Venue ' + req['name'] + ' could not be changed.')
  finally:
      db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))




