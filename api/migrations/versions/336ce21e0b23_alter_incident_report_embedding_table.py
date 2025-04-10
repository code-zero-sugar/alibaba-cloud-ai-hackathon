"""Alter incident report embedding table

Revision ID: 336ce21e0b23
Revises: 4fe22985229b
Create Date: 2025-04-09 09:20:49.860234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '336ce21e0b23'
down_revision: Union[str, None] = '4fe22985229b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incident_report_embedding', sa.Column('content', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('incident_report_embedding', 'content')
    # ### end Alembic commands ###
