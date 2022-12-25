import dash
from dash import html

import dash_bootstrap_components as dbc
from .components.navbar import navbar

from config import Config

import os

dirname = os.path.dirname(__file__)

APP_ID = 'budgetbreakdown'
# URL_BASE = '/fullpage/budgetbreakdown/'
URL_BASE = '/'

# Function used to add the dash app to the flask app
def add_app(server):
    '''
    Runs the dash app on the same server as the main flask app
    '''
    app = dash.Dash(
        server = server,
        url_base_pathname = URL_BASE,
        use_pages = True,
        suppress_callback_exceptions = True,
        pages_folder = os.path.join(dirname, 'pages'),
        assets_folder = os.path.join(dirname, 'assets'),
    )

    app.layout = html.Div(children=
        [
            navbar(URL_BASE),
            dash.page_container
        ]
    )

    return server

# Adding the app location to the sys.path
import sys
sys.path.append('C:\\Users\\Mealted.Lemon\\Documents\\GitHub\\Budget-Breakdown\\app\\dashapp')

# class TestConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_DEBUG1')

# Run the app as a module
# py -m app.dashapp.app
if __name__ == '__main__':
    # Trying to do this in order for debug but I guess it doesn't work
    # Most likely related to app context that I can't figure out, probably another work around
    app = dash.Dash(
        __name__,
        use_pages= True,
        suppress_callback_exceptions=True,
        title= "Budget Breakdown"
    )

    app.layout = html.Div(children=
        [
            navbar('/'),
            dash.page_container,
        ]
    )

    sever = app.server
    app.run_server(debug = True)