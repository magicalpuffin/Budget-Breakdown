from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Ledger(db.Model):
    __tablename__ = 'ledger'
    id = db.Column(db.String(64), primary_key = True)
    date = db.Column(db.Date, nullable = False)
    name = db.Column(db.String(64), nullable = False)
    amount = db.Column(db.Numeric(8,2), nullable = False)
    source = db.Column(db.String(64), nullable = False)
    
    # def __repr__(self):
    #     return '<Ledger {}>'.format(self.name)

class TypeTable(db.Model):
    __tablename__ = 'type_table'
    name = db.Column(db.String(64), primary_key = True)
    type = db.Column(db.String(64))

    def as_dict(self):
        return {
            'name': self.name,
            'type': self.type,
        }