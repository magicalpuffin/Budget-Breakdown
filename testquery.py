from app import create_app, db
from app.models import Ledger, TypeTable

import pandas as pd

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
        Ledger.name == TypeTable.name)
full_list = db.session.execute(qstmnt).all()
cldeger_df = pd.DataFrame.from_records(full_list)

cldeger_df.columns =['id', 'date', 'name', 'amount', 'source', 'type']
cldeger_df['date'] = pd.to_datetime(cldeger_df['date'])

cldeger_df.groupby(pd.Grouper(key= 'date', freq= '1M'))['amount'].sum()
cldeger_df.set_index(['date']).groupby(pd.Grouper(key= 'id')).resample('1M').apply(lambda x:x)

pd.date_range(start= cldeger_df['date'].min(), end= cldeger_df['date'].max(), freq= '1M')

cldeger_df.set_index('date').reindex(pd.date_range(start= cldeger_df['date'].min(), end= cldeger_df['date'].max(), freq= '1M'))