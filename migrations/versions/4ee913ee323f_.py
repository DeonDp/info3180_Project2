"""empty message

Revision ID: 4ee913ee323f
Revises: 7264edfc87d7
Create Date: 2017-04-24 14:27:27.750115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ee913ee323f'
down_revision = '7264edfc87d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wish_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wish_title', sa.String(length=80), nullable=True),
    sa.Column('wish_des', sa.String(length=80), nullable=True),
    sa.Column('UserProfile_id', sa.Integer(), nullable=True),
    sa.Column('wish_link', sa.String(length=255), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['UserProfile_id'], [u'user_profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wish_item')
    # ### end Alembic commands ###