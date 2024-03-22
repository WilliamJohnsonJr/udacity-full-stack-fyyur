"""empty message

Revision ID: 477e3f4dcedc
Revises: a998e91d35e9
Create Date: 2024-03-22 18:36:46.936992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '477e3f4dcedc'
down_revision = 'a998e91d35e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###