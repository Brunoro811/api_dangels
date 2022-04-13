"""remove column id_type_sale of orders_has_products and add in orders

Revision ID: 7051bafb2862
Revises: dcd3b49e97f8
Create Date: 2022-04-13 12:01:07.433658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7051bafb2862'
down_revision = 'dcd3b49e97f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('id_type_sale', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'orders', 'types_sales', ['id_type_sale'], ['id_type_sale'])
    op.alter_column('orders_has_products', 'sale_value',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)
    op.drop_constraint('orders_has_products_id_type_sale_fkey', 'orders_has_products', type_='foreignkey')
    op.drop_column('orders_has_products', 'id_type_sale')
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
    op.add_column('orders_has_products', sa.Column('id_type_sale', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('orders_has_products_id_type_sale_fkey', 'orders_has_products', 'types_sales', ['id_type_sale'], ['id_type_sale'])
    op.alter_column('orders_has_products', 'sale_value',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'id_type_sale')
    # ### end Alembic commands ###