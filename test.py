import unittest
from app import create_app, db
from app.models import Ledger, TypeTable
from config import Config
import os
from datetime import datetime
import re

import pandas as pd
from app.dashapp.utils.dashboard_functions import *

from sqlalchemy import select

# This should probably be deleted

testdata= pd.read_csv('debugdata\Credit Card - 9129_01-01-2022_12-21-2022.csv')
testdata= clean_import(testdata)

# testdata['Name'] =testdata['Name'].apply(lambda x: re.sub(r"\s+", " ", x))
# testdata['Id'] = testdata['Id'].apply(lambda x: re.split(r";", x)[0])

indata = pd.read_csv('August2022_8641.csv')
indata = clean_import(indata)

inobjlst = []

for i in range(len(indata)):
    inobjlst.append(
        Ledger(
            id = indata.iloc[i]['Id'],
            date = indata.iloc[i]['Date'],
            name = indata.iloc[i]['Name'],
            amount = indata.iloc[i]['Amount'],
            source = indata.iloc[i]['Source'],
        )
    )

typedata = pd.read_csv('types.csv')

typebojlst= []

for i in range(len(typedata)):
    typebojlst.append(
        TypeTable(
            name = typedata.iloc[i]['Name'],
            type = typedata.iloc[i]['Type']
        )
    )
# Models updated, actual database structure update, debug database created
# Should test if values get truncated

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_DEBUG1')

class LedgerModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


# -----
# For debugging directly in terminal
testapp = create_app(TestConfig)
testapp.app_context().push()
db.create_all()

db.session.bulk_save_objects(inobjlst)
db.session.bulk_save_objects(typebojlst)
db.session.commit()

outdata = pd.read_sql("SELECT * FROM ledger", db.session.connection())
outdata = pd.read_sql("SELECT ledger.id, ledger.date, ledger.name, ledger.amount, ledger.source, type_table.type FROM ledger INNER JOIN type_table on ledger.name=type_table.name", db.session.connection())
outdata['date']

selecttable = pd.read_sql(select(Ledger), db.session.connection())
pd.read_sql(select(TypeTable), db.session.connection())

db.session.add(TypeTable(
    name= "7-ELEVEN 34358 SAN DIEGO",
    type= "asdsdf"
))

for obj in db.session:
    print(obj)

ledgerlist = db.session.execute(select(Ledger)).all()

typelst = db.session.execute(select(TypeTable)).all()
db.session.execute(select(TypeTable)).first()

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
pd.DataFrame.from_records(full_list)

typedf = pd.DataFrame.from_records([item[0].as_dict() for item in typelst])



# I don't know why but it outputs objects in tuples?
# Needs to set object directly for the session to manage things correctly
typelst[0][0].type = 'aslddf'


for item in typelst:
    if item[0].name == '7-ELEVEN 34358 SAN DIEGO':
        item[0].type = 'Gas'


# Outputs the changes objects, can be directly commited to the database
db.session.dirty

db.session.commit()

# To apply this, the submit button would only issue the db session commit
# Can easily display, however, the edits to the types would need to be tracked
# Compare to identify the changes, would need to match from database to a typelst. Could use index if well controlled


db.session.rollback()
db.session.close()
db.session.remove()
db.drop_all()
testapp.app_context().pop()