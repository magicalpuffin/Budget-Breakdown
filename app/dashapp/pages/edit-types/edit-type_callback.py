from dash import register_page, callback, Input, Output, State

import pandas as pd

from app import db
from app.models import TypeTable
from utils.dashboard_functions import *

from sqlalchemy import select

page_id = id_factory('edit-type')

# store-types -> table-types -> button-update-types -> store types

# Dash callbacks can't self reference, therefore a temp store is used
@callback(
    Output(page_id('table-types'), 'data'),
    Input(page_id('store-types'), 'data')
)
def refresh_types(types_data):
    return types_data

# When the button is pressed, the types table is used to update the database
# Afterwards, to the types store is updated based on the database
# Uses header-main as input to load when page is loaded. I don't remember why this work around is needed.
@callback(
    Output(page_id('store-types'), 'data'),
    Input(page_id('button-update-types'), 'n_clicks'),
    Input(page_id('header-main'), 'children'),
    State(page_id('table-types'), 'data'),
)
def update_categorized(n_clicks, header_text, types_df):
    # Query database for TypeTable, need to make objects persistent
    type_list = db.session.execute(select(TypeTable)).all()
    type_df = pd.DataFrame.from_records([item[0].as_dict() for item in type_list])
    
    # If clicked
    if n_clicks != None:
        types_df = pd.DataFrame.from_records(types_df)
        edited_df = type_df.compare(types_df)

        # Uses the index to update, must keep the datatable and list in sync
        # Woudl probably be better to use name to avoid desync issues
        for i in edited_df.index:
            type_list[i][0].type = types_df.loc[i, 'type']
        db.session.commit()

        # It might not be necessary to re-query?
        # Would need to ensure everything is correctly persistent before next commit
        type_list = db.session.execute(select(TypeTable)).all()
        type_df = pd.DataFrame.from_records([item[0].as_dict() for item in type_list])


    return type_df.to_dict('records')