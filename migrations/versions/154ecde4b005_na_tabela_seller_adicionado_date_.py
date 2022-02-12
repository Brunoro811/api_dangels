"""na tabela seller adicionado date_creation e date_resignation

Revision ID: 154ecde4b005
Revises: 934bd3b7ef94
Create Date: 2022-02-11 20:02:45.385733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '154ecde4b005'
down_revision = '934bd3b7ef94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sellers', sa.Column('date_creation', sa.DateTime(), nullable=True))
    op.add_column('sellers', sa.Column('date_resignation', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sellers', 'date_resignation')
    op.drop_column('sellers', 'date_creation')
    # ### end Alembic commands ###
