from dash import html, dcc, dash_table
from dash import register_page, callback, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

from app import debugsession
from app.models import Ledger, TypeTable
from sqlalchemy import select

from utils.dashboard_functions import *

page_id = id_factory('view-budget')

# credit_categorized_df is the primary data set which includes the entire credit ledger categorized

@callback(
    Output(page_id('store-cledger'), 'data'),
    Input(page_id('header-main'), 'children')
)
def updatestore(header_text):
    qstmnt = select(
    Ledger.id, 
    Ledger.date, 
    Ledger.name, 
    Ledger.amount, 
    Ledger.source, 
    TypeTable.type).join_from(
        Ledger, 
        TypeTable, 
        Ledger.name == TypeTable.name)

    cledger_dict = debugsession.execute(qstmnt).all()
    cldeger_df = pd.DataFrame.from_records(cledger_dict)
    cldeger_df.columns =['id', 'date', 'name', 'amount', 'source', 'type']

    return cldeger_df.to_dict('records')


# Weird work around to load the figure everytime the link is opened
# Maybe switching to an anctual database would help
@callback(
    Output(page_id('figure-budget'), 'figure'),
    Input(page_id('store-cledger'), 'data')
)
def load_fig(cledger_dict):
    cledger_df = pd.DataFrame.from_records(cledger_dict)
    cledger_df["date"] = pd.to_datetime(cledger_df["date"])

    # Create figure
    fig = go.Figure()
    for type_val in cledger_df['type'].unique():
        type_df = cledger_df[cledger_df['type'] == type_val]
        fig.add_trace(go.Histogram(
            name= type_val,
            x= type_df['date'],
            y= type_df['amount'],
            xbins= dict(size= 'M1'),
            histfunc= 'sum',
            customdata= type_df['id'],
            texttemplate= "%{y}"
        ))

    fig.update_layout(
        barmode= 'stack', 
        bargap = 0.2,
        height= 800
    )
    fig.update_xaxes(ticklabelmode = 'period')
    
    return fig

@callback(
    Output(page_id('table-budget'), 'data'),
    Input(page_id('figure-budget'), 'clickData'),
    Input(page_id('store-cledger'), 'data'),
)
def display_click_data(clickData, cledger_dict):
    
    if cledger_dict:
        cledger_df = pd.DataFrame.from_records(cledger_dict)
        cledger_df["date"] = pd.to_datetime(cledger_df["date"])

        if clickData:
            clickData = clickData['points'][0]['customdata']
            cledger_df = cledger_df[cledger_df['id'].isin(clickData)]

        cledger_df = cledger_df.to_dict('records')
        
        return cledger_df
    return