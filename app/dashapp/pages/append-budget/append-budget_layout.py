from dash import html, dcc, dash_table
from dash import register_page 
import dash_bootstrap_components as dbc

from utils.dashboard_functions import *

register_page(
    __name__,
    path= '/append-budget',
    title= 'Append Budget',
)

page_id = id_factory('append-budget')

# Page Sturcture:
# User uploads data
# Table displays what was uploaded
# Table displays what would be added to the database
# Append button commits the upload

layout = html.Div(
    [
        html.H1("Append Budget"),
        dbc.Row([
            html.H2("Import a File"),
            dbc.Col(dcc.Upload(
                id= page_id('file-upload'), 
                className= 'file-upload',
                children= html.Div(['Drag and Drop or Select File']), 
                style={
                    'height': '60px',
                    'lineHeight': '60px',
                }
            )),
        ]),
        html.Button('Append', id= page_id('button-append')),
        dbc.Row([
            dbc.Col([
                html.H2("Uploaded Data"),
                dash_table.DataTable(
                    id= page_id('table-upload'), 
                    fixed_rows={'headers': True}),
            ], width= 6), 
            dbc.Col([
                html.H2("Added Data"),
                dash_table.DataTable(
                    id= page_id('table-added'), 
                    fixed_rows={'headers': True}),
                html.H2("", id= page_id('header-append-status')),
            ], width= 6),
        ]),
    ], className= 'mx-4',
)