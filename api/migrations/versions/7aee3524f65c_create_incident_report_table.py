"""Create incident report table

Revision ID: 7aee3524f65c
Revises: 
Create Date: 2025-04-08 14:26:27.716479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7aee3524f65c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('incident_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('desc', sa.String(), nullable=False),
    sa.Column('action', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incident_report_id'), 'incident_report', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_incident_report_id'), table_name='incident_report')
    op.drop_table('incident_report')
    # ### end Alembic commands ###
