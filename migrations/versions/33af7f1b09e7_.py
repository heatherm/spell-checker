"""empty message

Revision ID: 33af7f1b09e7
Revises: 77a965ec1375
Create Date: 2019-11-17 14:42:06.240285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33af7f1b09e7'
down_revision = '77a965ec1375'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('admin', sa.Boolean(), default=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'admin')
    # ### end Alembic commands ###
