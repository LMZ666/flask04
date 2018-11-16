"""empty message

Revision ID: 5ba4c5052589
Revises: 
Create Date: 2018-11-16 21:29:47.134899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ba4c5052589'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('token', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('passwd', sa.String(length=100), nullable=True),
    sa.Column('img', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###