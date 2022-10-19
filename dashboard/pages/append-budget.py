from dash import html, dcc, dash_table
from dash import register_page, callback, Input, Output, State

import pandas as pd
import base64
import io

from utils.dashboard_functions import *

register_page(
    __name__,
    # path= '/append-budget',
    title= 'Append Budget',
)

page_id = id_factory('append-budget')

layout = html.Div(
    [
        html.H1("Append Budget"),
        html.H2("Import File"),
        dcc.Upload(
            id= page_id('file-upload'), 
            className= 'file-upload',
            children= html.Div(['Drag and Drop or Select File']), 
            style={
                'height': '60px',
                'lineHeight': '60px',
        }),
        html.H2("Imported Data"),
        dash_table.DataTable(
            id= page_id('table-import'), 
            style_table={'height': '300px', 'overflowY': 'auto'},
            page_size=20,
            fixed_rows={'headers': True}),
        html.Button('Append', id= page_id('button-append')),
        html.H2("Added Data"),
        dash_table.DataTable(
            id= page_id('table-added'), 
            style_table={'height': '300px', 'overflowY': 'auto'},
            page_size=20,
            fixed_rows={'headers': True}),
        html.H2("", id= page_id('header-append-status')),
        dcc.Store('credit-ledger')
    ]
)

# Maybe there is a better way for transfering data between dcc.Store and dash_table? Could create own function.
# Takes uploaded CSV and displays it in a table. Data is stored in the table
@callback(
    Output(page_id('table-import'), 'data'),
    Input(page_id('file-upload'), 'contents'),
    State(page_id('file-upload'), 'filename')
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

# There was some weirdness relating to calling the function at initial load.
# Loads the current credit ledger and appends the uploaded data.
# Displays data that would be added
# New ledger is temporarily stored
@callback(
    Output(page_id('table-added'), 'data'),
    Output('credit-ledger', 'data'),
    Input(page_id('table-import'), 'data')
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

# Writes the current stored ledger to pdf
# Outputs a status confirming it was appended
@callback(
    Output(page_id('header-append-status'), 'children'),
    Input(page_id('button-append'), 'n_clicks'),
    State('credit-ledger', 'data'),
)
def appenddata(n_clicks, newledger):
    if n_clicks:
        newledger = pd.read_json(newledger, orient= 'split', dtype= False)
        newledger.to_csv('dashboard/data/credit_ledger.csv', index= False)
        return "Appended"