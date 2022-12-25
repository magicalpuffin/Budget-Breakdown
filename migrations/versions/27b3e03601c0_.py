"""empty message

Revision ID: 27b3e03601c0
Revises: c0fc34829382
Create Date: 2022-12-25 14:26:34.050822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27b3e03601c0'
down_revision = 'c0fc34829382'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ledger',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('amount', sa.Numeric(precision=8, scale=2), nullable=False),
    sa.Column('source', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('type_table',
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('type_table')
    op.drop_table('ledger')
    # ### end Alembic commands ###