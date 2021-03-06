"""empty message

Revision ID: 36bd0d276b66
Revises: 7c3f50c10e89
Create Date: 2020-12-27 13:36:48.535703

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '36bd0d276b66'
down_revision = '7c3f50c10e89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('show_name', sa.String(), nullable=True),
    sa.Column('show_start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('show_details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show_details',
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('show_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('show_start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('show_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], name='show_details_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], name='show_details_venue_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('artist_id', 'venue_id', name='show_details_pkey')
    )
    op.drop_table('show')
    # ### end Alembic commands ###
