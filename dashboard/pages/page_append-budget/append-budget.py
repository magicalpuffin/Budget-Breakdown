import dash
from dash import html, dcc, dash_table
from dash import callback, Input, Output, State

import pandas as pd
import base64
import io

from analyze_data import *

dash.register_page(
    __name__,
    path= '/append-budget',
    title= 'Append Budget'
)

layout = html.Div(
    [
        html.H5("Import File"),
        dcc.Upload(
            id= 'file-upload', 
            children= html.Div(['Drag and Drop or Select File']), 
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
        }),
        html.H5("Imported Data"),
        dash_table.DataTable(
            id= 'import-table', 
            style_table={'height': '300px', 'overflowY': 'auto'},
            page_size=20,
            fixed_rows={'headers': True}),
        html.Button('Append', id= 'append-button'),
        html.H5("Added Data"),
        dash_table.DataTable(
            id= 'added-table', 
            style_table={'height': '300px', 'overflowY': 'auto'},
            page_size=20,
            fixed_rows={'headers': True}),
        html.H5("", id= 'append-status'),
        dcc.Store('credit-ledger')
    ]
)

@callback(
    Output('import-table', 'data'),
    Input('file-upload', 'contents'),
    State('file-upload', 'filename')
)
def displayimport(contents, filename):
    if contents:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8'))
            )
            df = clean_import(df)
        return df.to_dict('records')

@callback(
    Output('added-table', 'data'),
    Output('credit-ledger', 'data'),
    Input('import-table', 'data')
)
def displayadded(importdata):
    if importdata:
        importdata = pd.DataFrame.from_records(importdata)

        credit_ledger_df = pd.read_csv('dashboard/data/credit_ledger.csv')

        newledger, added = append_ledger(credit_ledger_df, importdata)

        newledger = newledger.to_json(date_format= 'iso', orient= 'split')
        return added.to_dict('records'), newledger
    else:
        return None, None

@callback(
    Output('append-status', 'children'),
    Input('append-button', 'n_clicks'),
    State('credit-ledger', 'data'),
)
def appenddata(n_clicks, newledger):
    if n_clicks:
        newledger = pd.read_json(newledger, orient= 'split', dtype= False)
        newledger.to_csv('dashboard/data/credit_ledger.csv', index= False)
        return "Appended"