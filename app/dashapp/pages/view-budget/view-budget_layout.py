from dash import html, dcc, dash_table
from dash import register_page, callback, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

from utils.dashboard_functions import *

# Creates a figure and displays in web app
# Should switch to a database

register_page(
    __name__,
    path= '/view-budget',
    title= 'View Budget',
)

page_id = id_factory('view-budget')

# Consider adding filtering by date
# Could also prototype the datetimegrouping callback thing, dcc.store with xbin change callback

layout = html.Div(
    [
        html.H1('Budget Breakdown Figure', id= page_id('header-main')),
        dcc.Graph(id= page_id('figure-budget')),
        dash_table.DataTable(
            id = page_id('table-budget'),
            columns = [
                {'name': 'Id', 'id': 'id'},
                {'name': 'Date', 'id': 'date'},
                {'name': 'Name', 'id': 'name'},
                {'name': 'Amount', 'id': 'amount'},
                {'name': 'Source', 'id': 'source'},
                {'name': 'Type', 'id': 'type'},
            ], 
            page_size=20,
            fixed_rows={'headers': True}
        ),
        dcc.Store(id= page_id('store-cledger'))
    ]
)


