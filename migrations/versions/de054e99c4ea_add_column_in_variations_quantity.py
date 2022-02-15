"""add column in variations.quantity

Revision ID: de054e99c4ea
Revises: 7ffd71ed743f
Create Date: 2022-02-14 18:56:08.943703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de054e99c4ea'
down_revision = '7ffd71ed743f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('variations', sa.Column('quantity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('variations', 'quantity')
    # ### end Alembic commands ###