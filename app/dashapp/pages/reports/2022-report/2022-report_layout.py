from dash import html, dcc, dash_table
from dash import register_page
import dash_bootstrap_components as dbc

from utils.dashboard_functions import *

# Creates a figure and displays in web app
# Should switch to a database

register_page(
    __name__,
    path= '/2022-report',
    title= '2022 Report',
)

page_id = id_factory('2022-report')

layout = html.Div([])