"""0005_alter_table_apps

Revision ID: 06ea38c3e3c0
Revises: c52af99eda94
Create Date: 2024-03-11 15:48:37.243120

"""
from migrations.utils import (
    op, sa, date_fields,
    drop_table
)


# revision identifiers, used by Alembic.
revision = '06ea38c3e3c0'
down_revision = 'c52af99eda94'
branch_labels = None
depends_on = None

def alter_table_apps() -> None:
    op.add_column(
        'apps',
        sa.Column(
            'cloudfront_url',
            sa.VARCHAR(length=100),
            nullable=True,
        ),
    )

def upgrade():
    alter_table_apps()


def downgrade():
    op.drop_column('apps', 'cloudfront_url')