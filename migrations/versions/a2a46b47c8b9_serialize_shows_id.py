"""serialize shows id

Revision ID: a2a46b47c8b9
Revises: b9f6f6950da4
Create Date: 2024-03-28 03:06:32.976814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2a46b47c8b9'
down_revision = 'b9f6f6950da4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE SEQUENCE shows_id_seq')
    op.execute('ALTER TABLE shows ALTER COLUMN id SET DEFAULT nextval(\'shows_id_seq\')')


def downgrade():
    op.execute('ALTER TABLE shows ALTER COLUMN id DROP DEFAULT')
    op.execute('DROP SEQUENCE shows_id_seq')