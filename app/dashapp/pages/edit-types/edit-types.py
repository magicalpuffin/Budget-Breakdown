from dash import html, dcc, dash_table
from dash import register_page
import dash_bootstrap_components as dbc

from utils.dashboard_functions import *

# Page for editing the types used to categorized the ledger
register_page(
    __name__,
    path= "/edit-types",
    title= 'Edit Types',
)

page_id = id_factory('edit-type')

layout = html.Div(
    [
        html.H5("Types", id = page_id('header-main')),
        dbc.Row([
            dbc.Col([
                # For some reason, in order to copy paste into the table,
                # you must make the entire table editable and then set columns to false
                dash_table.DataTable(
                    id= page_id('table-types'), 
                    columns= [
                        {'name': 'Name', 'id': 'name', 'editable': False},
                        {'name': 'Type', 'id': 'type', 'editable': True}
                        ],
                    style_table= {'overflowY': 'auto'},
                    page_size= 25,
                    filter_action= 'native',
                    sort_action= 'native',
                    editable= True,
                    ),
            ], width= 6),
            dbc.Col([
                html.Button("Update Types", id= page_id('button-update-types')),
            ], width= 6),
        ]),
        dcc.Store(id= page_id('store-types')),
    ], style= {'padding': 10}
)


