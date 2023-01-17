from dash import html, dcc, dash_table
from dash import register_page
import dash_bootstrap_components as dbc
import pandas as pd

from app.models import Ledger, TypeTable
import sqlalchemy as sa

from utils.dashboard_functions import *

from app import db

register_page(
    __name__,
    path= '/view-budget',
    title= 'View Budget',
)

page_id = id_factory('view-budget')

maxdate = db.session.execute(sa.select(sa.func.max(Ledger.date))).first()[0]

layout = html.Div(
    [
        html.H1('View Budget', id= page_id('header-main')),
        dbc.Row([
            dbc.Label("Time Range", width= 1),
            dbc.Col(
                dcc.DatePickerRange(
                    id= page_id('input-date-range'), 
                    start_date= maxdate - pd.DateOffset(years= 1),
                    end_date= maxdate,
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
            ),
            dbc.Label("Category", width= 1),
            dbc.Col(
                dcc.Dropdown(
                    value= 'Type',
                    options= [
                        'Type'
                    ],
                    id= page_id('input-category-dropdown')
                ),
                width= 2,
            ),
        ]),
        dcc.Graph(id= page_id('figure-budget')),
        html.H1("Selected Data"),
        dbc.Button("Reset", id= page_id('button-reset'), class_name= 'mb-2'),
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
    ], className= 'mx-4',
)


