#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate 
from sqlalchemy import func
import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
# ADD: connect to local postgresql database in config.py

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Implement many-to-many relationship using show_details with Artist and Venue tables

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete="CASCADE"), nullable=False)
    show_name = db.Column(db.String)
    show_start_time = db.Column(db.DateTime(), nullable = False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Show {self.show_name} {self.show_start_time}>'

  

   # TODO: implement any missing fields, as a database migration using Flask-Migrate
   # ADD: implement seeking venue and seeking venue description into Artist table

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, unique=False)
    seeking_description = db.Column(db.String(1024))
    shows = db.relationship('Show', backref='artist', lazy=True)   

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, unique=False)
    seeking_description = db.Column(db.String(1024))
    shows = db.relationship('Show', cascade="all, delete", backref='venues', lazy=True)    

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # ADD: implement seeking talent and seeking talent description into Venue table

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# ADD Implement repalationship with model and import flask_migrate to do migration


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  #Show recenty listed Artist and Venue
  artists = Artist.query.with_entities(Artist.id,Artist.name).order_by(Artist.id.desc()).limit(10).all()
  venues = Venue.query.with_entities(Venue.id,Venue.name).order_by(Venue.id.desc()).limit(10).all()

  data={
    "artists": artists,
    "venues": venues
  }
  return render_template('pages/home.html', lists=data)

#----------------------------------------------------------------------------#
#  Venues
#----------------------------------------------------------------------------#

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  # Data from database
  data = Venue.query.with_entities(Venue.id, Venue.name, Venue.city, Venue.state).order_by(Venue.city, Venue.state).all()

  return render_template('pages/venues.html', venues=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  # Serch venue from the Venue table
  search = request.form.get('search_term')
  data = Venue.query.with_entities(Venue.id, Venue.name, Venue.city, Venue.state).filter(Venue.name.ilike("%" + search + "%") | Venue.city.ilike("%" + search + "%") | Venue.state.ilike("%" + search + "%")).order_by('id').all()

  # Set data and lenght to the respose variable
  response={
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  # Fetch venue information and past and future shows information 
  venue_details = Venue.query.filter_by(id=venue_id).first()
  artists = db.session.query(Artist.id, Artist.name, Artist.image_link, Show.show_name, Show.show_start_time).filter(Show.venue_id == venue_id, Artist.id == Show.artist_id).order_by(Artist.id).all()

  # Convert Geners String into List
  genres_value = venue_details.genres
  genres_array = genres_value.replace("}","").replace("{","")
  genres_list = list(genres_array.split(","))


  #  Check Past and Upcoming Shows  
  past_shows = []
  upcoming_shows = []
  past_shows_count = 0
  upcoming_shows_count = 0
  for artist in artists:
      if artist.show_start_time < datetime.datetime.now():
        past_shows.append({
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(artist.show_start_time)
        })
        past_shows_count = past_shows_count + 1
      elif artist.show_start_time > datetime.datetime.now():
        upcoming_shows.append({
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(artist.show_start_time)
        })
        upcoming_shows_count = upcoming_shows_count + 1
  
  # Set all the information to Data
  data = {
    "id": venue_details.id,
    "name": venue_details.name,
    "genres": genres_list,
    "address": venue_details.address,
    "city": venue_details.city,
    "state": venue_details.state,
    "phone": venue_details.phone,
    "website": venue_details.website,
    "facebook_link": venue_details.facebook_link,
    "seeking_talent": venue_details.seeking_talent,
    "seeking_description": venue_details.seeking_description,
    "image_link": venue_details.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count":upcoming_shows_count
  }

  return render_template('pages/show_venue.html', venue=data)

#  ----------------------------------------------------------------
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # Check all the validation in form
  form = VenueForm()
  if form.validate_on_submit():
    # Take Seeking Vanue value into Falg variable
    if (request.form['seeking_talent'] == 'Yes'):
      Flag = True
    else:
      Flag = False  

    genres_value = request.form.getlist('genres')

    # Get all the values from Artist Form
    venue_create = Venue(name= request.form['name'], 
                          city=request.form['city'],
                          state= request.form['state'],
                          phone = request.form['phone'],
                          address = request.form['address'],
                          genres = genres_value,
                          website = request.form['website'],
                          image_link = request.form['image_link'],
                          facebook_link = request.form['facebook_link'],
                          seeking_talent = Flag,
                          seeking_description = request.form['seeking_description']
                        )

    # on successful db insert, flash success
    # flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    try:
          db.session.add(venue_create)
          db.session.commit()
    except:
          db.session.rollback()
          flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
          db.session.close()
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return redirect(url_for('index'))
  else:
    return render_template('forms/new_venue.html', form=form)

#  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  Delete Venue
#  ----------------------------------------------------------------

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  # Get Venue name for venue table using venue_id
  venue = Venue.query.get(venue_id)
  venue_name = venue.name
  
  # Set Variable for check delete
  error_on_delete = False

  # Delete Venue from Venue and Show table 
  try:
        db.session.delete(venue)
        db.session.commit()
  except:
        error_on_delete = True
        db.session.rollback()
        #flash('An error occurred. Venue ' + venue_name + ' could not be deleted.')
        #return render_template('pages/home.html')
  finally:
        db.session.close()
        #flash('Venue ' + venue_name + ' was successfully deleted with all the shows!')
        #return render_template('pages/home.html')


  if error_on_delete:
      flash('An error occurred. Venue ' + venue_name + ' could not be deleted.')
      return jsonify({
              'message': 'An error occurred. Venue ' + venue_name + ' could not be deleted.',
              'success': False,
              'url': url_for('venues')
      })
  else:
      flash('Venue ' + venue_name + ' was successfully deleted with all the shows!')
      return jsonify({
              'message': 'Venue ' + venue_name + ' was successfully deleted with all the shows!',
              'success': True,
              'url': url_for('index')
      })

  #return render_template('pages/home.html')
 

#  ----------------------------------------------------------------
#  Update Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  venue = Venue.query.filter_by(id=venue_id).first()
  geners_value = venue.genres

  # Convert Geners String into List
  geners_array = geners_value.replace("}","").replace("{","")
  g_list = list(geners_array.split(",")) 
  #flash(str(g_list))

  #Set all the values from database
  form = VenueForm()
  form.state.default = venue.state
  form.genres.coerce = str
  form.genres.default = g_list
  if(venue.seeking_talent == False):
    form.seeking_talent.default = 'No'
  else:  
    form.seeking_talent.default = 'Yes'
  form.process()
  
  #Render edit_artist html with database data

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  # Check all the validation for form
  form = VenueForm()
  if form.validate_on_submit():
    # Take Seeking Vanue value into Falg variable
    if (request.form['seeking_talent'] == 'Yes'):
      Flag = True
    else:
      Flag = False  

    # Get all the values for genres to the variable
    genres_value = request.form.getlist('genres')

    # Get artist value from database to update

    try:
      venue_update = Venue.query.get(venue_id)
      # Update values for Venue
      venue_update.name = request.form['name'] 
      venue_update.city = request.form['city']
      venue_update.state = request.form['state']
      venue_update.phone = request.form['phone']
      venue_update.address = request.form['address']
      venue_update.genres = genres_value
      venue_update.website = request.form['website']
      venue_update.image_link = request.form['image_link']
      venue_update.facebook_link = request.form['facebook_link']
      venue_update.seeking_talent = Flag
      venue_update.seeking_description = request.form['seeking_description']
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    return redirect(url_for('edit_venue', venue_id=venue_id))
 

#------------------------------------------------------------------
#  Artists
#------------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  # Retrive Artist Name and Id from database
  data = Artist.query.with_entities(Artist.name, Artist.id).order_by('id').all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # Serch venue from the Venue table
  search = request.form.get('search_term')
  data = Artist.query.with_entities(Artist.id, Artist.name, Artist.city, Artist.state).filter(Artist.name.ilike("%" + search + "%") | Artist.city.ilike("%" + search + "%") | Artist.state.ilike("%" + search + "%")).order_by('id').all()

  response={
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the Artist page with the given artist_id
  # TODO: replace with real venue data from the artist table, using artist_id

  # Fetch Artist information and past and future shows information 

  artist_details = Artist.query.filter_by(id=artist_id).first()
  venues = db.session.query(Venue.id, Venue.name, Venue.image_link, Show.show_name, Show.show_start_time).filter(Show.artist_id == artist_id, Venue.id == Show.venue_id).order_by(Venue.id).all()

  # Convert Geners String into List
  genres_value = artist_details.genres
  genres_array = genres_value.replace("}","").replace("{","")
  genres_list = list(genres_array.split(","))


  #  Check Past and Upcoming Shows  
  past_shows = []
  upcoming_shows = []
  past_shows_count = 0
  upcoming_shows_count = 0
  for venue in venues:
      if venue.show_start_time < datetime.datetime.now():
        past_shows.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": str(venue.show_start_time)
        })
        past_shows_count = past_shows_count + 1
      elif venue.show_start_time > datetime.datetime.now():
        upcoming_shows.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": str(venue.show_start_time)
        })
        upcoming_shows_count = upcoming_shows_count + 1
  
  # Set all the information to the data 
  data = {
    "id": artist_details.id,
    "name": artist_details.name,
    "genres": genres_list,
    "city": artist_details.city,
    "state": artist_details.state,
    "phone": artist_details.phone,
    "website": artist_details.website,
    "facebook_link": artist_details.facebook_link,
    "seeking_venue": artist_details.seeking_venue,
    "seeking_description": artist_details.seeking_description,
    "image_link": artist_details.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count":upcoming_shows_count
  }

  return render_template('pages/show_artist.html', artist=data)

#  ----------------------------------------------------------------
#  Update Artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  # Retruve Artist data from the artist table

  artist = Artist.query.filter_by(id=artist_id).first()
  geners_value = artist.genres

  # Convert Geners String into List
  geners_array = geners_value.replace("}","").replace("{","")
  g_list = list(geners_array.split(",")) 
  #flash(str(g_list))

  #Set all the values from database
  form = ArtistForm()
  form.state.default = artist.state
  form.genres.coerce = str
  form.genres.default = g_list
  if(artist.seeking_venue == False):
    form.seeking_venue.default = 'No'
  else:  
    form.seeking_venue.default = 'Yes'
  form.process()
  
  #Render edit_artist html with database data
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  # check validation for form
  form = ArtistForm()
  if form.validate_on_submit():
    # Take Seeking Vanue value into Falg variable
    if (request.form['seeking_venue'] == 'Yes'):
      Flag = True
    else:
      Flag = False  

    # Get all the values for genres to the variable
    genres_value = request.form.getlist('genres')

    # Get artist value from database to update

    try:
      artist_update = Artist.query.get(artist_id)
      # Update values for Artist
      artist_update.name = request.form['name'] 
      artist_update.city = request.form['city']
      artist_update.state = request.form['state']
      artist_update.phone = request.form['phone']
      artist_update.genres = genres_value
      artist_update.website = request.form['website']
      artist_update.image_link = request.form['image_link']
      artist_update.facebook_link = request.form['facebook_link']
      artist_update.seeking_venue = Flag
      artist_update.seeking_description = request.form['seeking_description']
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))
  else:  
    return redirect(url_for('edit_artist', artist_id=artist_id))


#  ----------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = NewArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # check validation for form
  form = ArtistForm()
  if form.validate_on_submit():
    # Take Seeking Vanue value into Falg variable
    if (request.form['seeking_venue'] == 'Yes'):
      Flag = True
    else:
      Flag = False  

    genres_value = request.form.getlist('genres')

    # Get all the values from Artist Form
    artist_create = Artist(name= request.form['name'], 
                          city=request.form['city'],
                          state= request.form['state'],
                          phone = request.form['phone'],
                          genres = genres_value,
                          website = request.form['website'],
                          image_link = request.form['image_link'],
                          facebook_link = request.form['facebook_link'],
                          seeking_venue = Flag,
                          seeking_description = request.form['seeking_description']
                          )

    # on successful db insert, flash success
    # flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    
    try:
          db.session.add(artist_create)
          db.session.commit()
    except:
          db.session.rollback()
          flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
          db.session.close()
          flash('Artist ' + request.form['name'] + ' was successfully listed!')

    return redirect(url_for('index'))
  else:
    return render_template('forms/new_artist.html', form=form)      

#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  # Get all the informations from Artist and Venue table for all the shows 
  data = db.session.query(Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link, Venue.id.label("venue_id"), Venue.name.label("venue_name"), Show.show_name, Show.show_start_time).filter(Artist.id == Show.artist_id , Venue.id == Show.venue_id ).order_by(Artist.id).all()
  
  # Render all the data to shows.html
  return render_template('pages/shows.html', shows=data)

#  ----------------------------------------------------------------
#  Search Show
#  ----------------------------------------------------------------


@app.route('/shows/search', methods=['POST'])
def search_shows():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  # Serch venue from the Venue table
  search = request.form.get('search_term')
  data = db.session.query(Show.show_name).filter(Show.show_name.ilike("%" + search + "%")).all()

  # Set data and lenght to the respose variable
  response={
    "count": len(data),
    "data": data
  }

  return render_template('pages/show.html', results=response, search_term=request.form.get('search_term', ''))
 

#  ----------------------------------------------------------------
#  Create Show
#  ----------------------------------------------------------------

@app.route('/shows/create')
def create_shows():
  
  # renders form. do not touch.
  form = NewShowForm()

  # Select all Artist and Venue names fot Create New Show
  artists_name = Artist.query.with_entities(Artist.id,Artist.name).order_by('id').all()
  venues_name = Venue.query.with_entities(Venue.id,Venue.name).order_by('id').all()


  # Set Artist and Venue Name and IDs to Select Field
  artists = [(artist.id, artist.name) for artist in artists_name]
  venues = [(venue.id, venue.name) for venue in venues_name]
  form.artist_id.choices = artists
  form.venue_id.choices = venues
  form.process()

  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # Insert Show information into DB table 

  # Get all the values from Artist Form
  show_create = Show(show_name= request.form['show_name'], 
                        artist_id = request.form['artist_id'],
                        venue_id = request.form['venue_id'],
                        show_start_time = request.form['show_start_time']
                      )


  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  try:
        db.session.add(show_create)
        db.session.commit()
  except:
        db.session.rollback()
        flash('An error occurred. Show ' + request.form['show_name'] + ' could not be listed.')
  finally:
        db.session.close()
        flash('Show ' + request.form['show_name'] + ' was successfully listed!')

  #return render_template('pages/home.html')
  return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
