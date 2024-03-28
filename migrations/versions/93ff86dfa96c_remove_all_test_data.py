"""remove all test data

Revision ID: 93ff86dfa96c
Revises: a2a46b47c8b9
Create Date: 2024-03-28 03:07:25.937222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93ff86dfa96c'
down_revision = 'a2a46b47c8b9'
branch_labels = None
depends_on = None


def upgrade():
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


def downgrade():
    pass
