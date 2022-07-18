"""empty message

Revision ID: 31211f1eef1e
Revises: c39df59a8e98
Create Date: 2022-07-17 08:13:08.271773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '31211f1eef1e'
down_revision = 'c39df59a8e98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ordertable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('usd', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('rub', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    op.drop_table('order')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('usd', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('rub', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='order_pkey'),
    sa.UniqueConstraint('order_id', name='order_order_id_key')
    )
    op.drop_table('ordertable')
    # ### end Alembic commands ###
