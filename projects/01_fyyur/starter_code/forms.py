from datetime import datetime
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError, InputRequired
from enum import Enum
import phonenumbers
from flask import Flask, flash

# Implement Enum class for Genres
class GenresName(Enum):
            ALTERNATIVE = 'Alternative'
            BLUES = 'Blues'
            CLASSICAL ='Classical'
            COUNTRY = 'Country'
            ELECTRONIC = 'Electronic'
            FOLK = 'Folk'
            FUNK = 'Funk'
            HIPHOP = 'Hip-Hop'
            HEAVYMETAL = 'Heavy Metal'
            INSTRUMENTAL = 'Instrumental'
            JAZZ = 'Jazz'
            MUSICALTHEATRE = 'Musical Theatre'
            POP = 'Pop'
            PUNK = 'Punk'
            RANDB = 'R&B'
            REGGAE = 'Reggae'
            ROCKNROLL = 'Rock n Roll'
            SOUL = 'Soul'
            OTHER = 'Other'
    
def __str__(self):
    return self.name

@classmethod
def choices(cls):
    return [(choice.name, choice.value) for choice in cls]

# Phone Validatoin for US Phone numbers
def validate_phone(form, field):
    if len(field.data) > 16:
        flash('Phone number is too long.')
        raise ValidationError("Phone number is too long.")
    input_number = phonenumbers.parse(field.data,"US")
    if not (phonenumbers.is_valid_number(input_number)):
        flash('Invalid phone number.')
        raise ValidationError("Invalid phone number.")
    
# Implement Enum class for Facebook link check
class FacebookLink(Enum):
            HTTP = 'http'
            FACEBOOK ='facebook'

# Facebook link Validatoin using FacebookLink Enum Class
def validate_facebook_link(form,field):
    for checkValue in FacebookLink:
        if checkValue.value not in field.data:
            flash("Facebook link is not valid")
            raise ValidationError("Facebook link is not valid")        

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):

    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        # TODO implement validation logic for state
        # Use Phonenumbers field to validate phone number for state
        # Add validate_phone function to validate phone number for state
        'phone', validators=[DataRequired(),validate_phone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        # Get string choices  from Enum Class GenresName
        'genres', validators=[DataRequired()], choices = [(choice.name, choice.value) for choice in GenresName], coerce=str
    )
    facebook_link = StringField(
         # TODO implement enum restriction
         # Add validate_facebook_link function to check facebook link using FacebookLink Enum class
        'facebook_link', validators=[URL(),validate_facebook_link]
    )    
    website = StringField(
        'website'
    )
    seeking_talent = SelectField(
        'seeking_talent', validators = None,
        choices = [
            ('No', 'No'),
            ('Yes', 'Yes'),
        ]
    )
    seeking_description = StringField(
        'seeking_description'    
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        # Use Phonenumbers field to validate phone number for state
        # Add validate_phone function to validate phone number for state
        'phone' , validators=[DataRequired(),validate_phone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        # Get string choices  from Enum Class GenresName
        'genres', validators=[DataRequired()], choices = [(choice.name, choice.value) for choice in GenresName], coerce=str
    )

    facebook_link = StringField(
        # TODO implement enum restriction
        # Add validate_facebook_link function to check facebook link using FacebookLink Enum class
        'facebook_link', validators=[URL(),validate_facebook_link]
    )
    website = StringField(
        'website'
    )
    seeking_venue = SelectField(
        'seeking_venue', validators = None,
        choices = [
            ('No', 'No'),
            ('Yes', 'Yes'),
        ]
    )
    seeking_description = StringField(
        'seeking_description'
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM

# ADD New Artist Form and add seeking_venue and seeking_discription field

class NewArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        # Use Phonenumbers field to validate phone number for state
        # Add validate_phone function to validate phone number for state
        'phone' , validators=[DataRequired(),validate_phone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        # Get string choices  from Enum Class GenresName
        'genres', validators=[DataRequired()], choices = [(choice.name, choice.value) for choice in GenresName], coerce=str
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        # Add validate_facebook_link function to check facebook link using FacebookLink Enum class
        'facebook_link', validators=[URL(),validate_facebook_link]
    )
    website = StringField(
        'website'
    )
    seeking_venue = SelectField(
        'seeking_venue', validators = None,
        choices = [
            ('No', 'No'),
            ('Yes', 'Yes'),
        ]
    )
    seeking_description = StringField(
        'seeking_description'
    )
    
# Add New Show Form    

class NewShowForm(Form):
    show_name = StringField(
        'show_name', validators=[DataRequired()]
    )
    artist_id = SelectField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = SelectField(
        'venue_id', validators=[DataRequired()]
    )
    show_start_time = DateTimeField(
        'show_start_time', validators=[DataRequired()], default= datetime.today()
    )