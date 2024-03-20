"""empty message

Revision ID: ff7262246378
Revises: 4a0d73fc2017
Create Date: 2024-03-08 18:10:48.930469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff7262246378'
down_revision = '4a0d73fc2017'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('characther_name', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('characther_description', sa.String(length=250), nullable=True))
        batch_op.drop_column('caracther_description')
        batch_op.drop_column('caracther_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('caracther_name', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('caracther_description', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
        batch_op.drop_column('characther_description')
        batch_op.drop_column('characther_name')

    # ### end Alembic commands ###
