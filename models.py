from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime


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
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship("Show", back_populates="venue")
    genres = db.relationship("Genre", secondary=lambda: venue_genre_table)

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
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship("Show", back_populates="artist")
    genres = db.relationship("Genre", secondary=lambda: artist_genre_table)

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


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __repr__(self):
        return f"<Genre {self.id}, {self.name}>"


artist_genre_table = db.Table(
    "artist_genre",
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True),
)

venue_genre_table = db.Table(
    "venue_genre",
    db.Column("venue_id", db.Integer, db.ForeignKey("venues.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True),
)
