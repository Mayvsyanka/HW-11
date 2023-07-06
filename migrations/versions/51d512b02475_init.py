"""'Init'

Revision ID: 51d512b02475
Revises: bb084aa83da3
Create Date: 2023-07-04 20:48:39.363347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51d512b02475'
down_revision = 'bb084aa83da3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
