from dash import register_page, callback, Input, Output, State
# Need to import register_page for dash to import these callbacks
# Might be a better way, importing from the layout page

import pandas as pd
import base64
import io

from app import debugsession
from app.models import Ledger, TypeTable
from utils.dashboard_functions import *

from sqlalchemy import select

page_id = id_factory('append-budget')

@callback(
    Output(page_id('table-upload'), 'data'),
    Input(page_id('file-upload'), 'contents'),
    State(page_id('file-upload'), 'filename')
)
def displayupload(contents, filename):
    '''
    Displays the csv file uploaded in the upload table
    '''

    if contents:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8'))
            )
            df = clean_import(df)

        return df.to_dict('records')
    else:
        return None

@callback(
    Output(page_id('table-added'), 'data'),
    Input(page_id('table-upload'), 'data'),
)
def displayadded(upload_dict):
    '''
    Compares what is in the upload table with what is in the database.
    Displays what would be added based on new id
    '''
    if upload_dict:
        upload_df = pd.DataFrame.from_records(upload_dict)
        # Should use the sqlachemy way
        ledger_df = pd.read_sql("SELECT * FROM ledger", debugsession.connection())

        added_df = upload_df[~upload_df['Id'].isin(ledger_df['id'])]

        return added_df.to_dict('records')
    else:
        return None

# Writes the current stored ledger to pdf
# Outputs a status confirming it was appended
@callback(
    Output(page_id('header-append-status'), 'children'),
    Input(page_id('button-append'), 'n_clicks'),
    State(page_id('table-added'), 'data'),
)
def appenddata(n_clicks, added_dict):
    '''
    Commits what is in the added table to the database. 
    Returns a basic message of the upload being completed
    '''
    if n_clicks:
        added_df = pd.DataFrame.from_records(added_dict)

        type_list = debugsession.execute(select(TypeTable)).all()
        type_df = pd.DataFrame.from_records([item[0].as_dict() for item in type_list])

        new_type_list = []
        for name in added_df[~added_df['Name'].isin(type_df['name'])]['Name'].unique():
            new_type_list.append(
                TypeTable(
                    name = name
                )
            )

        # This could be a function
        ledger_list = []
        for i in range(len(added_df)):
            ledger_list.append(
                Ledger(
                    id = added_df.iloc[i]['Id'],
                    date = added_df.iloc[i]['Date'],
                    name = added_df.iloc[i]['Name'],
                    amount = added_df.iloc[i]['Amount'],
                    source = added_df.iloc[i]['Source'],
                )
            )
        
        debugsession.bulk_save_objects(ledger_list)
        debugsession.bulk_save_objects(new_type_list)
        debugsession.commit()

        # The returned message should be more useful
        return "Appended"