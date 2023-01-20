from dash import html, dcc, dash_table
from dash import register_page
import dash_bootstrap_components as dbc

import pandas as pd
import datetime
from app.models import Ledger, TypeTable
import sqlalchemy as sa

from utils.dashboard_functions import *

from app import db

register_page(
    __name__,
    path= '/2022-report',
    title= '2022 Report',
)

page_id = id_factory('2022-report')

# Page ideas
# Include rent with spending, monthly expense
# Include after tax earnings, bi monthly, check in fidelity
# Percentage breakdown of yearly expenses
# Savings and saving rate?

qstmnt = sa.select(
    Ledger.id, 
    Ledger.date, 
    Ledger.name, 
    Ledger.amount, 
    Ledger.source, 
    TypeTable.type).join_from(
        Ledger, 
        TypeTable, 
        Ledger.name == TypeTable.name).where(
            (Ledger.date >= datetime.date(2022, 1, 1)) &
            (Ledger.date < datetime.date(2023, 1, 1))
        )

cledger_dict = db.session.execute(qstmnt).all()
cldeger_df = pd.DataFrame.from_records(cledger_dict)
cldeger_df.columns =['id', 'date', 'name', 'amount', 'source', 'type']

# Manually concat of rent spending. Other fields left na.
rent_df = pd.DataFrame({
    'date': pd.date_range(start= '2022-01-01', end= '2023-01-01', freq= '1M'), 
    'amount': [-1800]*12, 
    'type': ['Rent']*12,
})
cldeger_df = pd.concat([cldeger_df, rent_df])

layout = html.Div(
    [
        html.H1('2022 Report', id= page_id('header-main')),
        dbc.Row([
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
        dbc.Row([
            dbc.Col(
                dcc.Graph(id= page_id('figure-pie')),
                width= 6,
            ),
            dbc.Col(
                dcc.Graph(id= page_id('figure-bar')),
                width= 6,
            ),
        ]),
        dcc.Store(
            id= page_id('store-cledger'),
            data= cldeger_df.to_dict('records')
        )
    ], className= 'mx-4',
)


