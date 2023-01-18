from app import create_app, db
from app.models import Ledger, TypeTable

import pandas as pd
import datetime
import plotly.graph_objects as go

from sqlalchemy import select

# Debugging the transforms needed for displaying the custom data in table
# Basic query of everything from databse
# Could be used later to test other queries

testapp = create_app()
testapp.app_context().push()

qstmnt = select(
    Ledger.id, 
    Ledger.date, 
    Ledger.name, 
    Ledger.amount, 
    Ledger.source, 
    TypeTable.type).join_from(
        Ledger, 
        TypeTable, 
        Ledger.name == TypeTable.name).where(
            (Ledger.date >= datetime.date(2022, 1, 1)) &
            (Ledger.date < datetime.date(2023, 1, 1))
        )
        
full_list = db.session.execute(qstmnt).all()
cldeger_df = pd.DataFrame.from_records(full_list)

cldeger_df.columns =['id', 'date', 'name', 'amount', 'source', 'type']
cldeger_df['date'] = pd.to_datetime(cldeger_df['date'])

# Seems to be the best way to group ids?
# cledgergrouped = cldeger_df.groupby([pd.Grouper(key= 'date', freq= '1M'), pd.Grouper(key= 'id')]).first()
cledgergrouped = cldeger_df.groupby(pd.Grouper(key= 'date', freq= '1M'))['id'].apply(lambda x: [x])
temp = cledgergrouped.map(lambda x: x[0])

# Testing grouping types
typesum = -cldeger_df.groupby(pd.Grouper(key= 'type'))['amount'].sum()

typesum = pd.concat([typesum[typesum >= 500], pd.Series({'Other': typesum[typesum < 500].sum()})])