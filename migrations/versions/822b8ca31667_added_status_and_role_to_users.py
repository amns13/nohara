"""added status and role to users

Revision ID: 822b8ca31667
Revises: 6da9d87b7c88
Create Date: 2020-11-01 17:23:23.588330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '822b8ca31667'
down_revision = '6da9d87b7c88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('status', sa.Integer(), nullable=True))
    op.execute("UPDATE user SET role = 1, status = 2 WHERE status is NULL")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    op.drop_column('user', 'role')
    # ### end Alembic commands ###