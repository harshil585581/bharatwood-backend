"""Add origin column

Revision ID: d68dddd8ccd3
Revises: 608f6bba8514
Create Date: 2026-03-11 11:10:09.877712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd68dddd8ccd3'
down_revision: Union[str, Sequence[str], None] = '608f6bba8514'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('site_visits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('origin', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_site_visits_created_at'), 'site_visits', ['created_at'], unique=False)
    op.create_index(op.f('ix_site_visits_id'), 'site_visits', ['id'], unique=False)
    op.create_index(op.f('ix_site_visits_ip_address'), 'site_visits', ['ip_address'], unique=False)
    op.create_index(op.f('ix_site_visits_origin'), 'site_visits', ['origin'], unique=False)
    op.create_index(op.f('ix_site_visits_session_id'), 'site_visits', ['session_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_site_visits_session_id'), table_name='site_visits')
    op.drop_index(op.f('ix_site_visits_origin'), table_name='site_visits')
    op.drop_index(op.f('ix_site_visits_ip_address'), table_name='site_visits')
    op.drop_index(op.f('ix_site_visits_id'), table_name='site_visits')
    op.drop_index(op.f('ix_site_visits_created_at'), table_name='site_visits')
    op.drop_table('site_visits')
