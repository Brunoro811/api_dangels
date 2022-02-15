"""create table orders, clients and add column in sellers

Revision ID: fbd3a7fbe9b5
Revises: b1526b64f018
Create Date: 2022-02-15 15:46:39.224026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbd3a7fbe9b5'
down_revision = 'b1526b64f018'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id_client', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('street', sa.String(length=100), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('zip_code', sa.String(length=9), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('country', sa.String(length=2), nullable=False),
    sa.Column('phone', sa.String(length=14), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('birthdate', sa.DateTime(), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.PrimaryKeyConstraint('id_client')
    )
    op.create_table('orders',
    sa.Column('id_order', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('id_seller', sa.Integer(), nullable=False),
    sa.Column('id_client', sa.Integer(), nullable=False),
    sa.Column('id_store', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_client'], ['clients.id_client'], ),
    sa.ForeignKeyConstraint(['id_seller'], ['sellers.id_seller'], ),
    sa.ForeignKeyConstraint(['id_store'], ['stores.id_store'], ),
    sa.PrimaryKeyConstraint('id_order')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('clients')
    # ### end Alembic commands ###