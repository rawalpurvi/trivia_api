"""empty message

Revision ID: e85b61424ac4
Revises: 74adcf5d23bd
Create Date: 2020-12-22 14:35:41.248720

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e85b61424ac4'
down_revision = '74adcf5d23bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show_details', sa.Column('show_start_time', sa.DateTime(), nullable=True))
    op.drop_column('show_details', 'start_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show_details', sa.Column('start_time', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column('show_details', 'show_start_time')
    # ### end Alembic commands ###