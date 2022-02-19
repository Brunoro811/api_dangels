"""add table group_products

Revision ID: 29e665d1dc2e
Revises: de054e99c4ea
Create Date: 2022-02-14 19:20:17.686144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29e665d1dc2e'
down_revision = 'de054e99c4ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group_products',
    sa.Column('id_group', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_product_one', sa.Integer(), nullable=False),
    sa.Column('id_product_two', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id_group'),
    sa.UniqueConstraint('id_product_one'),
    sa.UniqueConstraint('id_product_two')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group_products')
    # ### end Alembic commands ###