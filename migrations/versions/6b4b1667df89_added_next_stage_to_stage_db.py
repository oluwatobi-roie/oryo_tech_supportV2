"""added next stage to stage db

Revision ID: 6b4b1667df89
Revises: b08608f04571
Create Date: 2025-01-29 08:32:01.847909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b4b1667df89'
down_revision = 'b08608f04571'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stage', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stage_next', sa.String(length=30), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stage', schema=None) as batch_op:
        batch_op.drop_column('stage_next')

    # ### end Alembic commands ###
