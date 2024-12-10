"""0007_alter_table_types_add_field_content_type

Revision ID: 9d9338d053fb
Revises: ff90dbda2b7e
Create Date: 2024-07-15 18:28:08.877801

"""
from migrations.utils import (
    op, sa, date_fields,
    drop_table
)


# revision identifiers, used by Alembic.
revision = '9d9338d053fb'
down_revision = 'ff90dbda2b7e'
branch_labels = None
depends_on = None


def alter_table_types() -> None:
    op.add_column(
        'types',
        sa.Column(
            'content_type',
            sa.VARCHAR(length=50),
            nullable=True,
        ),
    )

def upgrade():
    alter_table_types()


def downgrade():
    op.drop_column('types', 'content_type')