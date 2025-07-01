"""Initial migration

Revision ID: 0001_initial
Revises:
Create Date: 2025-07-01 00:00:00.000000

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # --- Создаём таблицу buildings ---
    op.create_table(
        'buildings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
    )

    # --- Создаём таблицу activities ---
    op.create_table(
        'activities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('activities.id'), nullable=True),
    )

    # --- Создаём таблицу organizations ---
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('phone_numbers', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('building_id', sa.Integer(), sa.ForeignKey('buildings.id'), nullable=False),
    )

    # --- Создаём таблицу связи many-to-many organization_activities ---
    op.create_table(
        'organization_activities',
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), primary_key=True),
        sa.Column('activity_id', sa.Integer(), sa.ForeignKey('activities.id'), primary_key=True),
    )


def downgrade():
    # Откатываем в обратном порядке
    op.drop_table('organization_activities')
    op.drop_table('organizations')
    op.drop_table('activities')
    op.drop_table('buildings')
