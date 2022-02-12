"""create table's users ,sellers and relationships

Revision ID: 934bd3b7ef94
Revises: bc9af93b9a91
Create Date: 2022-02-11 18:19:57.683744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '934bd3b7ef94'
down_revision = 'bc9af93b9a91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stores',
    sa.Column('id_store', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('adress', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id_store')
    )
    op.create_table('types',
    sa.Column('id_type_user', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('permission', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id_type_user')
    )
    op.create_table('sellers',
    sa.Column('id_seller', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('id_store', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_store'], ['stores.id_store'], ),
    sa.PrimaryKeyConstraint('id_seller')
    )
    op.create_table('users',
    sa.Column('id_user', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=30), nullable=False),
    sa.Column('id_desabled', sa.Integer(), nullable=True),
    sa.Column('id_type_user', sa.Integer(), nullable=True),
    sa.Column('id_seller', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_seller'], ['sellers.id_seller'], ),
    sa.ForeignKeyConstraint(['id_type_user'], ['types.id_type_user'], ),
    sa.PrimaryKeyConstraint('id_user')
    )
    op.create_table('disabled',
    sa.Column('id_disabled', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('date_disabled', sa.DateTime(), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_disabled')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('disabled')
    op.drop_table('users')
    op.drop_table('sellers')
    op.drop_table('types')
    op.drop_table('stores')
    # ### end Alembic commands ###
