from datetime import datetime
from enum import Enum
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

def my_string_strip_filter(form, field):
    if field is not None and isinstance(field, str):
        return field.strip()

class UsStates(Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    DC = "DC"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VA = "VA"
    VT = "VT"
    WA = "WA"
    WI = "WI"
    WV = "WV"
    WY = "WY"
state_list = [state.value for state in UsStates]
state_choices = [(state.value, state.value) for state in UsStates]

class ShowForm(Form):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(Form):
    name = StringField("name", validators=[DataRequired()], filters=[lambda x: my_string_strip_filter(None, x)])
    city = StringField("city", validators=[DataRequired()], filters=[lambda x: my_string_strip_filter(None, x)])
    state = SelectField(
        "state",
        validators=[
            DataRequired(),
            AnyOf(state_list),
        ],
        choices=state_choices,
    )
    address = StringField("address", validators=[DataRequired()], filters=[lambda x: my_string_strip_filter(None, x)])
    phone = StringField("phone", validators=[Regexp(regex="^\\d{3}-\\d{3}-\\d{4}$", message="Must match pattern 000-000-0000")],
                        filters=[lambda x: my_string_strip_filter(None, x)])
    image_link = StringField("image_link", validators=[Optional(), URL()], filters=[lambda x: my_string_strip_filter(None, x)])
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired(), my_genre_check],
        choices=[genre.value for genre in Genre],
    )
    facebook_link = StringField("facebook_link", validators=[Optional(), URL()], filters=[lambda x: my_string_strip_filter(None, x)])
    website_link = StringField("website_link", validators=[Optional(), URL()], filters=[lambda x: my_string_strip_filter(None, x)])

    seeking_talent = BooleanField("seeking_talent")

    seeking_description = StringField("seeking_description", filters=[lambda x: my_string_strip_filter(None, x)])

class ArtistForm(Form):
    name = StringField("name", validators=[DataRequired()], filters=[lambda x: my_string_strip_filter(None, x)])

    city = StringField("city", validators=[DataRequired()], filters=[lambda x: my_string_strip_filter(None, x)])

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
        validators=[Regexp(regex="^\\d{3}-\\d{3}-\\d{4}$", message="Must match pattern 000-000-0000")],
        filters=[lambda x: my_string_strip_filter(None, x)]
    )

    image_link = StringField("image_link", validators=[Optional(), URL()], filters=[lambda x: my_string_strip_filter(None, x)])

    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired(), my_genre_check],
        choices=[genre.value for genre in Genre],
    )

    facebook_link = StringField("facebook_link", validators=[Optional(), URL()], filters=[lambda x: my_string_strip_filter(None, x)])

    website_link = StringField("website_link", validators=[Optional(), URL()], filters=[lambda x: my_string_strip_filter(None, x)])

    seeking_venue = BooleanField("seeking_venue")

    seeking_description = StringField("seeking_description", filters=[lambda x: my_string_strip_filter(None, x)])
