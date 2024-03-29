"""set all test data

Revision ID: 3f0bad9b18fd
Revises: 93ff86dfa96c
Create Date: 2024-03-28 03:09:00.796476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f0bad9b18fd'
down_revision = '93ff86dfa96c'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    op.execute("""
        DELETE FROM artist_genre;
    """)
    op.execute("""
        DELETE FROM venue_genre;
    """)
    op.execute("""
        DELETE FROM shows;
    """)
    op.execute("""
        DELETE FROM venues;
    """)
    op.execute("""
        DELETE FROM artists;
    """)
