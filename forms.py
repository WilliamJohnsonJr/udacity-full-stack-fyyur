from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Optional

from models import Genre

def my_genre_check(form, field):
    for genre in field.data:
        if genre not in [g.value for g in Genre]:
            raise ValidationError('Value must be one or more of: ' + ', '.join([genre.value for genre in Genre]))

state_list = [
                    "AL",
                    "AK",
                    "AZ",
                    "AR",
                    "CA",
                    "CO",
                    "CT",
                    "DE",
                    "DC",
                    "FL",
                    "GA",
                    "HI",
                    "ID",
                    "IL",
                    "IN",
                    "IA",
                    "KS",
                    "KY",
                    "LA",
                    "ME",
                    "MT",
                    "NE",
                    "NV",
                    "NH",
                    "NJ",
                    "NM",
                    "NY",
                    "NC",
                    "ND",
                    "OH",
                    "OK",
                    "OR",
                    "MD",
                    "MA",
                    "MI",
                    "MN",
                    "MS",
                    "MO",
                    "PA",
                    "RI",
                    "SC",
                    "SD",
                    "TN",
                    "TX",
                    "UT",
                    "VT",
                    "VA",
                    "WA",
                    "WV",
                    "WI",
                    "WY"
                ]
state_choices = [
            ("AL", "AL"),
            ("AK", "AK"),
            ("AZ", "AZ"),
            ("AR", "AR"),
            ("CA", "CA"),
            ("CO", "CO"),
            ("CT", "CT"),
            ("DE", "DE"),
            ("DC", "DC"),
            ("FL", "FL"),
            ("GA", "GA"),
            ("HI", "HI"),
            ("ID", "ID"),
            ("IL", "IL"),
            ("IN", "IN"),
            ("IA", "IA"),
            ("KS", "KS"),
            ("KY", "KY"),
            ("LA", "LA"),
            ("ME", "ME"),
            ("MT", "MT"),
            ("NE", "NE"),
            ("NV", "NV"),
            ("NH", "NH"),
            ("NJ", "NJ"),
            ("NM", "NM"),
            ("NY", "NY"),
            ("NC", "NC"),
            ("ND", "ND"),
            ("OH", "OH"),
            ("OK", "OK"),
            ("OR", "OR"),
            ("MD", "MD"),
            ("MA", "MA"),
            ("MI", "MI"),
            ("MN", "MN"),
            ("MS", "MS"),
            ("MO", "MO"),
            ("PA", "PA"),
            ("RI", "RI"),
            ("SC", "SC"),
            ("SD", "SD"),
            ("TN", "TN"),
            ("TX", "TX"),
            ("UT", "UT"),
            ("VT", "VT"),
            ("VA", "VA"),
            ("WA", "WA"),
            ("WV", "WV"),
            ("WI", "WI"),
            ("WY", "WY"),
        ]

class ShowForm(Form):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state",
        validators=[
            DataRequired(),
            AnyOf(state_list),
        ],
        choices=state_choices,
    )
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone")
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired(), my_genre_check],
        choices=[genre.value for genre in Genre],
    )
    facebook_link = StringField("facebook_link", validators=[URL()])
    website_link = StringField("website_link")

    seeking_talent = BooleanField("seeking_talent")

    seeking_description = StringField("seeking_description")

class ArtistForm(Form):
    name = StringField("name", validators=[DataRequired()])
    def filter_name(form, field):
        if field is not None and isinstance(field, str):
            return field.strip()

    city = StringField("city", validators=[DataRequired()])
    def filter_city(form, field):
        if field is not None and isinstance(field, str):
            return field.strip()

    state = SelectField(
        "state",
        validators=[
            DataRequired(),
            AnyOf(state_list),
        ],
        choices=state_choices,
    )

    phone = StringField(
        "phone",
        validators=[Regexp(regex="^\\d{3}-\\d{3}-\\d{4}$", message="Must match pattern 000-000-0000")]
    )
    def filter_phone(form, field):
        if field is not None and isinstance(field, str):
            return field.strip()

    image_link = StringField("image_link", validators=[Optional(), URL()])
    def filter_image_link(form, field):
        if field is not None and isinstance(field, str):
            return field.strip()

    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired(), my_genre_check],
        choices=[genre.value for genre in Genre],
    )

    facebook_link = StringField("facebook_link", validators=[Optional(), URL()])
    def filter_facebook_link(form, field):
        if field is not None and isinstance(field, str):
            return field.strip()

    website_link = StringField("website_link", validators=[Optional(), URL()])
    def filter_website_link(form, field):
        if field is not None and isinstance(field, str):
            return field.strip()

    seeking_venue = BooleanField("seeking_venue")

    seeking_description = StringField("seeking_description")
    def filter_seeking_description(form, field):
        if field is not None and isinstance(field, str):
            return field.strip()
