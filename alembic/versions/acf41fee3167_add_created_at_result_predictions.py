"""add_created_at_result_predictions

Revision ID: acf41fee3167
Revises: bd904b6f75b1
Create Date: 2024-11-27 10:57:32.326339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acf41fee3167'
down_revision: Union[str, None] = 'bd904b6f75b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_result_predictions', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_result_predictions', 'created_at')
    # ### end Alembic commands ###
