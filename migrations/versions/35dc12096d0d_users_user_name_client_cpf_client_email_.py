"""users.user_name , client.cpf, client.email unique in db

Revision ID: 35dc12096d0d
Revises: 5e898fcf4e5d
Create Date: 2022-02-15 17:35:04.932001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35dc12096d0d'
down_revision = '5e898fcf4e5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'clients', ['email'])
    op.create_unique_constraint(None, 'clients', ['cpf'])
    op.add_column('users', sa.Column('email', sa.String(length=100), nullable=False))
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['user_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'email')
    op.drop_constraint(None, 'clients', type_='unique')
    op.drop_constraint(None, 'clients', type_='unique')
    # ### end Alembic commands ###
