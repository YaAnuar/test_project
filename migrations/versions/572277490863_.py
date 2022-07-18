"""empty message

Revision ID: 572277490863
Revises: 31211f1eef1e
Create Date: 2022-07-18 04:00:57.280380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '572277490863'
down_revision = '31211f1eef1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ordertable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('usd', sa.Integer(), nullable=True),
    sa.Column('time', sa.Date(), nullable=True),
    sa.Column('rub', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ordertable')
    # ### end Alembic commands ###