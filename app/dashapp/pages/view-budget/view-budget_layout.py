from dash import html, dcc, dash_table
from dash import register_page
import dash_bootstrap_components as dbc

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
        dbc.Row([
            dbc.Label("Time Range", width= 1),
            dbc.Col(
                dcc.DatePickerRange(
                    id= page_id('input-date-range'), 
                ),
                width= 2
            ),
            dbc.Label("Time Bin", width= 1),
            dbc.Col(
                dcc.Dropdown(
                    value= 'Month', 
                    options= [
                        'Week', 
                        'Month', 
                        'Quarter', 
                        'Year'
                    ],
                    clearable= False,
                    id= page_id('input-time-dropdown')
                ),
                width= 2
            )
        ]),
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


