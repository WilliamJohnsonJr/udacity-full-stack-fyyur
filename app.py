# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
from dateutil import parser
import babel
from flask import Flask, abort, jsonify, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import ArtistGenre, Genre, VenueGenre, db, Show, Venue, Artist
from sqlalchemy import func

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    if isinstance(value, datetime):
        date = value
    else:
        date = parser.parse(value)
    
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # Adapted from the Udacity Knowledge Center post here: https://knowledge.udacity.com/questions/145968#148233

    areas = (
        db.session.query(Venue.city, Venue.state)
        .distinct(Venue.city, Venue.state)
        .order_by(Venue.state)
        .all()
    )
    data = []
    for area in areas:
        venue_list = []
        venues = Venue.query.filter(Venue.city == area.city, Venue.state == area.state)
        for venue in venues:
            venue_list.append(
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": venue.upcoming_shows_count,
                }
            )
        data.append({
            "city": area.city,
            "state": area.state,
            "venues": venue_list
        })
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  past_shows = venue.past_shows
  upcoming_shows = venue.upcoming_shows
  genre_names = [genre.genre.value for genre in venue.genres]
  venue_dict = venue.__dict__
  venue_dict["genres"] = genre_names
  venue_dict["past_shows"] = past_shows
  venue_dict["past_shows_count"] = venue.past_shows_count
  venue_dict["upcoming_shows"] = upcoming_shows
  venue_dict["upcoming_shows_count"] = venue.upcoming_shows_count
  return render_template('pages/show_venue.html', venue=venue_dict)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # Adapted from this answer on Udacity Knowledge: https://knowledge.udacity.com/questions/627743
    form = VenueForm(request.form, meta={"csrf": False})
    if not form.validate_on_submit():
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors " + str(message))
        return render_template("forms/new_venue.html", form=form)
    # called upon submitting the new venue listing form
    venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        address=form.address.data,
        image_link=form.image_link.data,
        website=form.website_link.data,
        facebook_link=form.facebook_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data,
    )
    db.session.add(venue)
    try:
        db.session.flush()
        selected_genres = form.genres.data
        if len(selected_genres):
            data = list(
                map(lambda g: {"venue_id": venue.id, "genre": g}, selected_genres)
            )
            for item in data:
                new_ag = VenueGenre(venue_id=item["venue_id"], genre=item["genre"])
                db.session.add(new_ag)
        db.session.commit()
        db.session.close()
        # on successful db insert, flash success
        flash("Venue " + request.form["name"] + " was successfully listed!")
        return redirect(url_for('index'))
    except Exception as error:
        print('Error:', error)
        # We rollback in case of an error. Even though there is the possibility of an venue ID
        # being orphaned in a rollback due to the flush above, this is not a concern.
        db.session.rollback()
        flash(
            "An error occurred. Venue "
            + request.form["name"]
            + " could not be listed."
        )
        db.session.close()
        abort(400)
    # No finally block here since we must return or abort (which auto-raises) in the try and except blocks.


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    if not venue:
        abort(400)
    try:
        db.session.delete(venue)
        db.session.commit()
        db.session.close()

    except Exception as error:
        print("Error:", error)
        db.session.rollback()
        db.session.close()
        abort(400)

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    
    artist = Artist.query.filter_by(id=artist_id).first()
    past_shows = artist.past_shows
    upcoming_shows = artist.upcoming_shows
    genre_names = [genre.genre.value for genre in artist.genres]
    artist_dict = artist.__dict__
    artist_dict["genres"] = genre_names
    artist_dict["past_shows"] = past_shows
    artist_dict["past_shows_count"] = artist.past_shows_count
    artist_dict["upcoming_shows"] = upcoming_shows
    artist_dict["upcoming_shows_count"] = artist.upcoming_shows_count
    return render_template('pages/show_artist.html', artist=artist_dict)

def fetch_and_build_venue(venue_id: int):
    venue = Venue.query.filter_by(id=venue_id).first()  # We use filter_by here because get is deprecated
    genre_names = [genre.genre.value for genre in venue.genres]
    venue_dict = venue.__dict__
    venue_dict["genres"] = genre_names
    return venue_dict

def add_genres_to_venue(venue_id: int, genres: list):
    selected_genres = genres
    if len(selected_genres):
        data = list(
            map(lambda g: {"venue_id": venue_id, "genre": g}, selected_genres)
        )
        for item in data:
            new_vg = VenueGenre(venue_id=item["venue_id"], genre=item["genre"])
            db.session.add(new_vg)

def fetch_and_build_artist(artist_id: int):
    artist = Artist.query.filter_by(id=artist_id).first()  # We use filter_by here because get is deprecated
    genre_names = [genre.genre.value for genre in artist.genres]
    artist_dict = artist.__dict__
    artist_dict["genres"] = genre_names
    return artist_dict

def add_genres_to_artist(artist_id: int, genres: list):
    selected_genres = genres
    if len(selected_genres):
        data = list(
            map(lambda g: {"artist_id": artist_id, "genre": g}, selected_genres)
        )
        for item in data:
            new_ag = ArtistGenre(artist_id=item["artist_id"], genre=item["genre"])
            db.session.add(new_ag)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    artist_dict = fetch_and_build_artist(artist_id)
    form.process(data=artist_dict)  # Hydrate the form with the current data from the db
    return render_template("forms/edit_artist.html", form=form, artist=artist_dict)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form, meta={"csrf": False})
    if not form.validate_on_submit():
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors " + str(message))
        artist_dict = fetch_and_build_artist(artist_id)
        return render_template("forms/edit_artist.html", form=form, artist=artist_dict)
    artist: Artist | None = Artist.query.filter_by(id=artist_id).first()
    if not isinstance(artist, Artist):
        abort(400)
    try:
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.website = form.website_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        add_genres_to_artist(artist_id=artist.id, genres=form.genres.data)

        db.session.commit()
        db.session.close()
        flash("Artist " + form.name.data + " was successfully updated!")
        return redirect(url_for("show_artist", artist_id=artist_id))
    except Exception as error:
        print('Error:', error)
        db.session.rollback()
        db.session.close()
        flash("An error occurred. Artist " + form.name.data + " could not be updated.")
        abort(400)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue_dict = fetch_and_build_venue(venue_id)
    form.process(data=venue_dict)  # Hydrate the form with the current data from the db
    return render_template('forms/edit_venue.html', form=form, venue=venue_dict)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form, meta={"csrf": False})
    if not form.validate_on_submit():
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors " + str(message))
        venue_dict = fetch_and_build_venue(venue_id)
        return render_template("forms/edit_venue.html", form=form, venue=venue_dict)
    venue: Venue | None = Venue.query.filter_by(id=venue_id).first()
    if not isinstance(venue, Venue):
        print("Error:", "No Venue found")
        abort(400)
    try:
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.address = form.address.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.website = form.website_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        add_genres_to_venue(venue_id=venue.id, genres=form.genres.data)
        db.session.commit()
        db.session.close()
        flash("Venue " + form.name.data + " was successfully updated!")
        return redirect(url_for("show_venue", venue_id=venue_id))
    except Exception as error:
        print("Error:", error)
        db.session.rollback()
        db.session.close()
        flash("An error occurred. Venue " + form.name.data + " could not be updated.")
        abort(400)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # Adapted from this answer on Udacity Knowledge: https://knowledge.udacity.com/questions/627743
    form = ArtistForm(request.form, meta={'csrf': False})
    if not form.validate_on_submit():
        message = []
        for field, err in form.errors.items():
            message.append(field + ' ' + '|'.join(err))
        flash('Errors ' + str(message))
        return render_template('forms/new_artist.html', form=form)
    # called upon submitting the new artist listing form
    artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        image_link=form.image_link.data,
        website=form.website_link.data,
        facebook_link=form.facebook_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data,
    )
    db.session.add(artist)
    try:
        db.session.flush()
        add_genres_to_artist(artist_id=artist.id, genres=form.genres.data)
        db.session.commit()
        db.session.close()
        # on successful db insert, flash success
        flash("Artist " + form.name.data + " was successfully listed!")
        return redirect(url_for('index'))
    except Exception as error:
        print('Error:', error)
        # We rollback in case of an error. Even though there is the possibility of an artist ID
        # being orphaned in a rollback due to the flush above, this is not a concern.
        db.session.rollback()
        db.session.close()
        flash(
            "An error occurred. Artist "
            + form.name.data
            + " could not be listed."
        )
        abort(400)
    # No finally block here since we must return or abort (which auto-raises) in the try and except blocks.


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    data = Show.query.order_by("start_time").all()
    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    form = ShowForm(request.form, meta={'csrf': False})
    if not form.validate_on_submit():
        message = []
        for field, err in form.errors.items():
            message.append(field + ' ' + '|'.join(err))
        flash('Errors ' + str(message))
        return render_template("forms/new_show.html", form=form)
    show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
    )
    try:
        db.session.add(show)
        db.session.commit()
        db.session.close()
        # on successful db insert, flash success
        flash("Show was successfully listed!")
        return redirect(url_for('index'))
    except Exception as error:
        print('Error:', error)
        db.session.rollback()
        db.session.close()
        flash('An error occurred. Show could not be listed.')
        abort(400)


@app.errorhandler(400)
def handle_bad_request(error):
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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
