"""Game.result column

Revision ID: 081a8948fc4c
Revises: 23bf5929695f
Create Date: 2019-10-07 16:05:28.570063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '081a8948fc4c'
down_revision = '23bf5929695f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('result', sa.String(length=16), nullable=True))
    op.create_index(op.f('ix_game_result'), 'game', ['result'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game_result'), table_name='game')
    op.drop_column('game', 'result')
    # ### end Alembic commands ###