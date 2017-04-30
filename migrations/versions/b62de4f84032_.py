"""empty message

Revision ID: b62de4f84032
Revises: 4ee913ee323f
Create Date: 2017-04-24 14:43:13.655362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b62de4f84032'
down_revision = '4ee913ee323f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('uname', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'uname')
    # ### end Alembic commands ###
