from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from enum import Enum

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.ForeignKey("venues.id"), nullable=False)
    artist_id = db.Column(db.ForeignKey("artists.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    artist = db.relationship("Artist", back_populates="shows")
    venue = db.relationship("Venue", back_populates="shows")
    venue_name = association_proxy("venue", "name")
    venue_image_link = association_proxy("venue", "image_link")
    artist_name = association_proxy("artist", "name")
    artist_image_link = association_proxy("artist", "image_link")

class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(2083), nullable=True)
    facebook_link = db.Column(db.String(2083), nullable=True)
    website = db.Column(db.String(2083), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship("Show", back_populates="venue")
    genres = db.relationship("VenueGenre", lazy=True)

    @property
    def past_shows(self):
        current_time = datetime.now()
        return [show for show in self.shows if show.start_time < current_time]

    @property
    def past_shows_count(self):
        current_time = datetime.now()
        return len([show for show in self.shows if show.start_time < current_time])

    @property
    def upcoming_shows(self):
        current_time = datetime.now()
        return [show for show in self.shows if show.start_time >= current_time]

    @property
    def upcoming_shows_count(self):
        current_time = datetime.now()
        return len([show for show in self.shows if show.start_time >= current_time])

    def __repr__(self):
        return f"<Venue {self.id}, {self.name}>"


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(2083), nullable=True)
    facebook_link = db.Column(db.String(2083), nullable=True)
    website = db.Column(db.String(2083), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship("Show", back_populates="artist")
    genres = db.relationship("ArtistGenre", lazy=True)

    @property
    def past_shows(self):
        current_time = datetime.now()
        return [show for show in self.shows if show.start_time < current_time]

    @property
    def past_shows_count(self):
        current_time = datetime.now()
        return len([show for show in self.shows if show.start_time < current_time])

    @property
    def upcoming_shows(self):
        current_time = datetime.now()
        return [show for show in self.shows if show.start_time >= current_time]

    @property
    def upcoming_shows_count(self):
        current_time = datetime.now()
        return len([show for show in self.shows if show.start_time >= current_time])

    def __repr__(self):
        return f"<Artist {self.id}, {self.name}>"

class Genre(Enum):
    ALTERNATIVE = 'Alternative'
    BLUES = 'Blues'
    CLASSICAL = 'Classical'
    COUNTRY = 'Country'
    ELECTRONIC = 'Electronic'
    FOLK = 'Folk'
    FUNK = 'Funk'
    HIP_HOP = 'Hip-Hop'
    HEAVY_METAL = 'Heavy Metal'
    INSTRUMENTAL = 'Instrumental'
    JAZZ = 'Jazz'
    MUSICAL_THEATRE = 'Musical Theatre'
    POP = 'Pop'
    PUNK = 'Punk'
    R_AND_B = 'R&B'
    REGGAE = 'Reggae'
    ROCK_N_ROLL = 'Rock n Roll'
    SOUL = 'Soul'
    SWING = 'Swing'
    OTHER = 'Other'

class ArtistGenre(db.Model):
    __tablename__ = "artist_genre"

    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), primary_key=True)
    genre = db.Column(db.Enum(Genre, values_callable=lambda x: [e.value for e in x], name='genre'), primary_key=True)

class VenueGenre(db.Model):
    __tablename__ = "venue_genre"

    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), primary_key=True)
    genre = db.Column(db.Enum(Genre, values_callable=lambda x: [e.value for e in x], name='genre'), primary_key=True)
