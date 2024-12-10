"""0006_alter_table_apps

Revision ID: ff90dbda2b7e
Revises: 06ea38c3e3c0
Create Date: 2024-03-20 14:21:27.424688

"""
from migrations.utils import (
    op, sa, date_fields,
    drop_table
)


# revision identifiers, used by Alembic.
revision = 'ff90dbda2b7e'
down_revision = '06ea38c3e3c0'
branch_labels = None
depends_on = None

def alter_table_apps() -> None:
    op.add_column(
        'apps',
        sa.Column(
            'bucket_invalidation_code',
            sa.VARCHAR(length=25),
            nullable=True,
        ),
    )

def upgrade():
    alter_table_apps()


def downgrade():
    op.drop_column('apps', 'bucket_invalidation_code')