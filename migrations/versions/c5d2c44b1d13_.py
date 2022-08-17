"""empty message

Revision ID: c5d2c44b1d13
Revises: ff4ba030ef45
Create Date: 2022-08-16 17:43:03.913396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5d2c44b1d13'
down_revision = 'ff4ba030ef45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'seeking_venue')
    # ### end Alembic commands ###