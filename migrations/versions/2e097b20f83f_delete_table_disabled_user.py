"""delete table disabled user

Revision ID: 2e097b20f83f
Revises: 46a92d992acf
Create Date: 2022-04-01 21:25:17.147191

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2e097b20f83f'
down_revision = '46a92d992acf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('disabled')
    op.alter_column('orders_has_products', 'sale_value',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
    op.alter_column('products', 'cost_value',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
    op.alter_column('products', 'sale_value_varejo',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
    op.alter_column('products', 'sale_value_atacado',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
    op.alter_column('products', 'sale_value_promotion',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'sale_value_promotion',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('products', 'sale_value_atacado',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('products', 'sale_value_varejo',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('products', 'cost_value',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('orders_has_products', 'sale_value',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.create_table('disabled',
    sa.Column('id_disabled', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('date_disabled', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('id_user', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], name='disabled_id_user_fkey'),
    sa.PrimaryKeyConstraint('id_disabled', name='disabled_pkey')
    )
    # ### end Alembic commands ###
