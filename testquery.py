from app import create_app, db
from app.models import Ledger, TypeTable

import pandas as pd
import datetime

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

cledgergrouped['2022-01-31'][0]

cldeger_df.set_index(['date']).groupby(pd.Grouper(key= 'id')).resample('1M').apply(lambda x:x)

# messing with reindexing
pd.date_range(start= cldeger_df['date'].min(), end= cldeger_df['date'].max(), freq= '1M')
cldeger_df.set_index('date').reindex(pd.date_range(start= cldeger_df['date'].min(), end= cldeger_df['date'].max(), freq= '1M'))

cldeger_df.set_index(['date']).asfreq('1M')
cldeger_df.set_index(['date', 'id']).groupby(pd.Grouper(level=0, freq= '1M'))['amount'].sum()

test_df = pd.DataFrame({
    'date': pd.date_range(start= '2022-01-01', end= '2023-01-01', freq= '1M'), 
    'amount': [-1800]*12, 
    'type': ['Rent']*12,
})

pd.concat([cldeger_df, test_df])