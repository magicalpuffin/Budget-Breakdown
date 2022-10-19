from dash import html, dcc, dash_table
from dash import register_page, callback, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

from utils.dashboard_functions import *

# Creates a figure and displays in web app
# Should switch to a database

register_page(
    __name__,
    # path= '/view-budget',
    title= 'View Budget',
)

page_id = id_factory('view-budget')

# credit_categorized_df is the primary data set which includes the entire credit ledger categorized
credit_categorized_df = pd.read_csv('dashboard/data/credit_categorized.csv')
credit_categorized_df["Date"] = pd.to_datetime(credit_categorized_df["Date"])

# Consider adding filtering by date
# Could also prototype the datetimegrouping callback thing, dcc.store with xbin change callback

layout = html.Div(
    [
        html.Div(
            [
                html.H1('Budget Breakdown Figure', id= page_id('header-main')),
                dcc.Graph(id= page_id('figure-budget')),
                dash_table.DataTable(
                    id = page_id('table-budget'),
                    data = credit_categorized_df.to_dict('records'), 
                    columns = [{"name": i, "id": i} for i in credit_categorized_df.columns], 
                    page_size=20,
                    fixed_rows={'headers': True}
                ),
            ]
        ),
    ]
)


# Weird work around to load the figure everytime the link is opened
# Not sure but without this, the figure only loads once, even if data is changed
# Maybe switching to an anctual database would help
@callback(
    Output(page_id('figure-budget'), 'figure'),
    Input(page_id('header-main'), 'children')
)
def load_fig(header_text):
    # Refresh to load most recent data
    credit_categorized_df = pd.read_csv('dashboard/data/credit_categorized.csv')
    credit_categorized_df["Date"] = pd.to_datetime(credit_categorized_df["Date"])

    # Create figure
    fig = go.Figure()
    for type_val in credit_categorized_df['Type'].unique():
        type_df = credit_categorized_df[credit_categorized_df['Type'] == type_val]
        fig.add_trace(go.Histogram(
            name= type_val,
            x= type_df['Date'],
            y= type_df['Amount'],
            xbins= dict(size= 'M1'),
            histfunc= 'sum',
            customdata= type_df['Id'],
            texttemplate= "%{y}"
        ))

    fig.update_layout(barmode= 'stack', bargap = 0.2)
    fig.update_xaxes(ticklabelmode = 'period')
    
    return fig

@callback(
    Output(page_id('table-budget'), 'data'),
    Input(page_id('figure-budget'), 'clickData')
)
def display_click_data(clickData):
    
    filter_df = credit_categorized_df
    if clickData:
        clickData = clickData['points'][0]['customdata']
        filter_df = filter_df[filter_df['Id'].isin(clickData)]

    filter_df = filter_df.to_dict('records')
    
    return filter_df