from dash import html, dcc, dash_table
from dash import register_page, callback, Input, Output, State, ctx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

from app.models import Ledger, TypeTable
import sqlalchemy as sa

from utils.dashboard_functions import *

from app import db

page_id = id_factory('view-budget')

# Manualy set colors for consistency
typecolor_dict = {
    'Amazon' : '#FF9900',
    'Auto' : '#4e4e4e',
    'Consumer Staples' : '#E31837',
    'Entertainment' : '#FFC107',
    'Gas' : '#00FF99',
    'Healthcare' : '#006BA6',
    'Hobby' : '#1F3B4D',
    'Misc' : '#6610F2',
    'Restaurant' : '#6610F2',
    'Transportation' : '#009ad9',
    'Utilities' : '#026937',
}

@callback(
    Output(page_id('store-cledger'), 'data'),
    Input(page_id('header-main'), 'children'),
    Input(page_id('input-date-range'), "start_date"),
    Input(page_id('input-date-range'), "end_date"),
)
def updatestore(header_text, start_date, end_date):
    qstmnt = sa.select(
        Ledger.id, 
        Ledger.date, 
        Ledger.name, 
        Ledger.amount, 
        Ledger.source, 
        TypeTable.type).join_from(
            Ledger, 
            TypeTable, 
            Ledger.name == TypeTable.name)

    cledger_dict = db.session.execute(qstmnt).all()
    cldeger_df = pd.DataFrame.from_records(cledger_dict)
    cldeger_df.columns =['id', 'date', 'name', 'amount', 'source', 'type']

    cldeger_df = cldeger_df[
        (cldeger_df['date'] >= pd.to_datetime(start_date, utc= True)) &
        (cldeger_df['date'] <= (pd.to_datetime(end_date, utc= True)))
    ]

    return cldeger_df.to_dict('records')


# Weird work around to load the figure everytime the link is opened
# Maybe switching to an anctual database would help
@callback(
    Output(page_id('figure-budget'), 'figure'),
    Input(page_id('store-cledger'), 'data'),
    Input(page_id('input-time-dropdown'), 'value'),
    Input(page_id('input-category-dropdown'), 'value'),
)
def load_fig(cledger_dict, time_group, filter_category):
    cledger_df = pd.DataFrame.from_records(cledger_dict)
    cledger_df["date"] = pd.to_datetime(cledger_df["date"])

    binsize_dict = {
        'Week': 604800000.0,
        'Month': 'M1',
        'Quarter': 'M3',
        'Year': 'M12'
    }
    binsize = binsize_dict[time_group]

    scattersize_dict = {
        'Week': '1W',
        'Month': '1M',
        'Quarter': '1Q',
        'Year': '1Y'        
    }
    scattersize = scattersize_dict[time_group]

    if filter_category == 'Type':

        # Create figure
        fig = go.Figure()
        for type_val in cledger_df['type'].unique():
            type_df = cledger_df[cledger_df['type'] == type_val]
            fig.add_trace(go.Histogram(
                name= type_val,
                x= type_df['date'],
                y= type_df['amount'],
                xbins= dict(size= binsize),
                histfunc= 'sum',
                customdata= type_df['id'],
                texttemplate= "%{y}",
                marker= dict(color = typecolor_dict[type_val]),
            ))

        fig.update_layout(
            title= ("<b>Total Spending Over Time</b><br>" + 
                    "<i>Spending by Type</i>"),
            barmode= 'stack', 
            bargap = 0.1,
            height= 800
        )
        fig.update_yaxes(
            title_text = "Cost ($)",
        )
        fig.update_xaxes(
            dtick = binsize,
            ticklabelmode = 'period'
        )

    else:
        # Creates scatter plot
        # Currently issues with getting data to display in the table
        fig = go.Figure()
        scatter_df = cledger_df.groupby(pd.Grouper(key= 'date', freq= scattersize))['amount'].sum()
        # print(cledger_df.groupby(cledger_df["date"].to_period('1M')))
        scatter_df.index = scatter_df.index.map(lambda x: x.replace(day= month_mid(x)))
        
        fig.add_trace(go.Scatter(
            name = "Total Spending Over Time",
            x= scatter_df.index,
            y= scatter_df.values,
            mode= 'lines+markers+text',
            texttemplate= "%{y}",
            textposition= "top center",
            customdata= cledger_df,
            # textfont= dict(size = 24),
            ), 
            # secondary_y= False
        )
        fig.update_yaxes(
            title_text = "Cost ($)",
            rangemode = 'tozero',
        )
        fig.update_xaxes(
            dtick = binsize,
            ticklabelmode = 'period'
        )
    
    return fig

@callback(
    Output(page_id('table-budget'), 'data'),
    Input(page_id('figure-budget'), 'clickData'),
    Input(page_id('store-cledger'), 'data'),
    Input(page_id('button-reset'), 'n_clicks'),
)
def display_click_data(clickData, cledger_dict, n_clicks):
    print(clickData)
    
    # Currently commented out due to issues with getting the scatter to display correctly
    # Testing on a separate file for grouping data
    # if cledger_dict:
    #     cledger_df = pd.DataFrame.from_records(cledger_dict)
    #     cledger_df["date"] = pd.to_datetime(cledger_df["date"])

    #     if clickData and (page_id('button-reset') != ctx.triggered_id):
    #         clickData = clickData['points'][0]['customdata']
    #         cledger_df = cledger_df[cledger_df['id'].isin(clickData)]

    #     cledger_df = cledger_df.to_dict('records')
        
    #     return cledger_df
    return