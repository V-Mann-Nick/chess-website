"""Game.timestamp column

Revision ID: 3b10f3899fb6
Revises: 081a8948fc4c
Create Date: 2019-10-08 09:25:35.471294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b10f3899fb6'
down_revision = '081a8948fc4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_game_timestamp'), 'game', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game_timestamp'), table_name='game')
    op.drop_column('game', 'timestamp')
    # ### end Alembic commands ###