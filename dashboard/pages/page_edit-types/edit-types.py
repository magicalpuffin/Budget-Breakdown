from ast import Store
import dash
from dash import html, dcc, dash_table
from dash import callback, Input, Output, State

import pandas as pd

from analyze_data import *

# Page for editing the types used to categorized the ledger
dash.register_page(
    __name__,
    path= '/edit-types',
    title= 'Edit Types'
)

layout = html.Div(
    [
        html.Div(children= 
        [
            html.H5("Types"),
            dash_table.DataTable(
                id= 'types-table', 
                columns= [{'name': i, 'id': i} for i in pd.read_csv('dashboard/data/types.csv').columns],
                style_table={'overflowY': 'auto'},
                page_size=50,
                filter_action= 'native',
                sort_action= 'native',
                editable= True,
                data= pd.read_csv('dashboard/data/types.csv').to_dict('records')),
            dcc.Store('types-data')
        ], style={'padding': 10, 'flex': 1}),
        html.Div(children=
        [
            html.H5("Uncategorized Types"),
            dash_table.DataTable(
                id= 'uncategorized-types-table',
                columns= [{'name': i, 'id': i} for i in pd.read_csv('dashboard/data/types.csv').columns],
                style_table={'overflowY': 'auto'},
                page_size=50,
                filter_action= 'native',
                sort_action= 'native',
                editable= True,
                data= pd.read_csv('dashboard/data/uncategorized.csv').to_dict('records')),
            html.Button("Update Types", id= 'update-types-button'),
        ], style={'padding': 10, 'flex': 1}),
    ], 
    style={'display': 'flex', 'flex-direction': 'row'}
)

# Table 2 updates when table 1 is edited
# Button 2 updated table 1
# Button 1 updates csv using table 1

# When the update types button is pressed, the table is saved to csv
# The dcc.Store is updated to match what was in the csv
# At initialization, only what is in csv is used
# @callback(
#     Output('types-data', 'data'),
#     Input('update-types-button', 'n_clicks'),
#     State('types-table', 'data')
# )
# def update_types(n_clicks, types_df):
#     if n_clicks != None:
#         types_df = pd.DataFrame.from_records(types_df)
#         types_df.to_csv('dashboard/data/types.csv')

#     return pd.read_csv('dashboard/data/types.csv').to_json(date_format= 'iso', orient= 'split')

# Whenever the dcc.Store is updated, the table is updated to match
# Allows for read/write. Functions should edit the dcc.Store
@callback(
    Output('types-table', 'data'),
    Input('types-data', 'data')
)
def refresh_types(types_data):
    return pd.read_json(types_data, orient= 'split').to_dict('records')

# Updates uncategorized types table depending on types table
# Compares to credit ledger
@callback(
    Output('uncategorized-types-table', 'data'),
    Input('types-table', 'data')
)
def update_uncategorized(types_df):
    if types_df == None:
        return None
    else:
        types_df = pd.DataFrame.from_records(types_df)
        credit_ledger = pd.read_csv('dashboard/data/credit_ledger.csv')

        ledger_categorized, uncategorized_types_df = add_types(credit_ledger, types_df)

        # exports for debugging purposes
        ledger_categorized.to_csv('dashboard/data/credit_categorized.csv', index= False)
        # uncategorized_types_df.to_csv('dasboard/data/uncategorized.csv')

        return uncategorized_types_df.to_dict('records')

# When the button is pressed, append to the types table
# Outputs to dcc.Store due to limitations on read/writting in callback
@callback(
    Output('types-data', 'data'),
    Input('update-types-button', 'n_clicks'),
    State('types-table', 'data'),
    State('uncategorized-types-table', 'data')
)
def update_categorized(n_clicks, types_df, uncategorized_types_df):
    if n_clicks == None:
        return pd.read_csv('dashboard/data/types.csv').to_json(date_format= 'iso', orient= 'split')
    else:
        uncategorized_types_df = pd.DataFrame.from_records(uncategorized_types_df)
        types_df = pd.DataFrame.from_records(types_df)
        types_df = pd.concat([types_df, uncategorized_types_df])
        types_df = types_df.dropna()
        types_df = types_df[~types_df["Name"].duplicated()]
        types_df.to_csv('dashboard/data/types.csv', index= False)
                
        return pd.read_csv('dashboard/data/types.csv').to_json(date_format= 'iso', orient= 'split')
