import os
from dotenv import load_dotenv

# Sets enviornment variables based on a .env file
# Assumes .env file is at root
load_dotenv()

class Config(object):
    # Add more info here
    # There should not be any commas
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_DEBUG1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    # SQLALCHEMY_ECHO = True