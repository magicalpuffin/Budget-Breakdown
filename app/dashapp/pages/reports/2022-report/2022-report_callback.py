from dash import html, dcc, dash_table
from dash import register_page, callback, Input, Output, State, ctx
import pandas as pd
import plotly.graph_objects as go
import json
import os

from app.models import Ledger, TypeTable
import sqlalchemy as sa

from utils.dashboard_functions import *

from app import db

page_id = id_factory('2022-report')

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
    'Other' : '#6610F2',
    'Restaurant' : '#6610F2',
    'Transportation' : '#009ad9',
    'Utilities' : '#026937',
    'Rent' : '#FDFD96',
}

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
            title= ("<b>2022 Total Spending</b><br>" + 
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
        
        # Convoluted way to get a series indexed by date group with list of list of ids
        # pandas apply function returns lists in strange ways, to work around the list is nested in apply and select in map
        groupindexed = cledger_df.groupby(pd.Grouper(key= 'date', freq= scattersize))['id'].apply(lambda x: [x])
        idindate_df = groupindexed.map(lambda x: x[0])
        
        # Will need to create something to account for other time periods besides month
        # scatter_df.index = scatter_df.index.map(lambda x: x.replace(day= month_mid(x)))
        
        fig.add_trace(go.Scatter(
            name = "Total Spending Over Time",
            x= scatter_df.index,
            y= scatter_df.values,
            mode= 'lines+markers+text',
            texttemplate= "%{y}",
            textposition= "top center",
            customdata= idindate_df,
            # textfont= dict(size = 24),
            ), 
            # secondary_y= False
        )
        fig.update_layout(
            title = "<b>2022 Total Spending</b>"
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
    Output(page_id('figure-pie'), 'figure'),
    Input(page_id('store-cledger'), 'data'),
)
def load_piefig(cledger_dict):
    cledger_df = pd.DataFrame.from_records(cledger_dict)
    cledger_df["date"] = pd.to_datetime(cledger_df["date"])

    typecostsum = -cledger_df.groupby(pd.Grouper(key= 'type'))['amount'].sum()
    typecostsum = pd.concat([typecostsum[typecostsum >= 500], pd.Series({'Other': typecostsum[typecostsum < 500].sum()})])

    typecolors = [typecolor_dict[type_name] for type_name in typecostsum.index]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels= typecostsum.index,
        values= typecostsum.values,
        hole= 0.3,
        textinfo= 'label+percent+value',
        marker= {
            'colors': typecolors,
        },
    ))
    fig.update_layout(
        title= "<b>2022 Spending Pie Chart</b>",
        height= 600,
    )

    return fig

@callback(
    Output(page_id('figure-bar'), 'figure'),
    Input(page_id('store-cledger'), 'data'),
)
def load_barfig(cledger_dict):
    cledger_df = pd.DataFrame.from_records(cledger_dict)
    cledger_df["date"] = pd.to_datetime(cledger_df["date"])

    typecostsum = -cledger_df.groupby(pd.Grouper(key= 'type'))['amount'].sum()
    typecostprec = typecostsum/typecostsum.sum()*100


    fig = go.Figure()

    fig.add_trace(go.Bar(
        x= typecostsum.values,
        y= typecostsum.index,
        customdata= typecostprec.values,
        texttemplate= "$%{x:.2f} (%{customdata:.2f}%)",
        orientation= 'h',
    ))
    fig.update_yaxes(
        categoryorder = 'total ascending'
    )
    fig.update_xaxes(
        title = "Cost ($)",
    )
    fig.update_layout(
        title= "<b>2022 Spending Bar Chart</b>",
        height= 600,
    )

    return fig