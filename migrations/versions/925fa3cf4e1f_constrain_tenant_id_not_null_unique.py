"""constrain_tenant_id_not_null_unique

Revision ID: 925fa3cf4e1f
Revises: 551091d80e6c
Create Date: 2026-02-12 04:09:56.922161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '925fa3cf4e1f'
down_revision: Union[str, Sequence[str], None] = '551091d80e6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('emails', schema=None) as batch_op:
        # 1. Enforce NOT NULL
        batch_op.alter_column('tenant_id', nullable=False, existing_type=sa.String())
        
        # 2. Drop old index on provider_message_id (Global)
        batch_op.drop_index('ix_emails_provider_message_id')
        
        # 3. Create Tenant-Scoped Unique Constraint (Acts as Composite Index)
        batch_op.create_unique_constraint(
            'uq_emails_tenant_provider',
            ['tenant_id', 'provider_message_id']
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('emails', schema=None) as batch_op:
        # 1. Drop Unique Constraint
        batch_op.drop_constraint('uq_emails_tenant_provider', type_='unique')
        
        # 2. Restore Old Index
        batch_op.create_index('ix_emails_provider_message_id', ['provider_message_id'], unique=False)
        
        # 3. Make tenant_id Nullable again
        batch_op.alter_column('tenant_id', nullable=True, existing_type=sa.String())
