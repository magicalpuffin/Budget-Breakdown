from dash import register_page, callback, Input, Output, State

import pandas as pd

from app import debugsession
from app.models import TypeTable
from utils.dashboard_functions import *

from sqlalchemy import select

page_id = id_factory('edit-type')

# store-types -> table-types -> button-update-types -> store types


# Should switch to just one types table with the option to filter only ones with missing data
# Needs to display join with left merge and only show unique
# Append the 

# Dash callbacks can't self reference, therefore a temp store is used
# The types table is set to the types store
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
    type_list = debugsession.execute(select(TypeTable)).all()
    type_df = pd.DataFrame.from_records([item[0].as_dict() for item in type_list])

    # If clicked
    if n_clicks != None:
        types_df = pd.DataFrame.from_records(types_df)
        edited_df = type_df.compare(types_df)

        # Uses the index to update, must keep the datatable and list in sync
        for i in edited_df.index:
            type_list[i][0].type = types_df.loc[i, 'type']
        debugsession.commit()

        # It might not be necessary to re-query?
        # Would need to ensure everything is correctly persistent before next commit
        type_list = debugsession.execute(select(TypeTable)).all()
        type_df = pd.DataFrame.from_records([item[0].as_dict() for item in type_list])


    return type_df.to_dict('records')