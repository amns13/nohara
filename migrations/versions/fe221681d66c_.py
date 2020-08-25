"""empty message

Revision ID: fe221681d66c
Revises: 610f3404fac0
Create Date: 2020-08-25 07:22:32.715103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe221681d66c'
down_revision = '610f3404fac0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('template_id', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'template_id')
    # ### end Alembic commands ###
