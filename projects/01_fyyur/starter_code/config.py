import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL

# ADD local databse url link
SQLALCHEMY_DATABASE_URI = 'postgresql://purvi@localhost:5432/fyyurDB'

# CSRF disable to test form_validate
WTF_CSRF_ENABLED = False