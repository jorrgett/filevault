"""0002_create_table_apps

Revision ID: bbfb7d8a0e02
Revises: a8b6b2ec95ff
Create Date: 2024-01-16 09:51:19.970369

"""
from migrations.utils import (
    op, sa, date_fields,
    drop_table
)

# revision identifiers, used by Alembic.
revision = 'bbfb7d8a0e02'
down_revision = 'a8b6b2ec95ff'
branch_labels = None
depends_on = None


TABLE_NAME = "apps"


def create_table_apps() -> None:
    op.create_table(
        TABLE_NAME,
        sa.Column(
            'id',
            sa.BIGINT(),
            sa.Identity(
                always=False,
                start=1,
                increment=1
            ),
            autoincrement=True,
            nullable=False,
            unique=True
        ),
        sa.Column(
            'code',
            sa.VARCHAR(
                length=50,
            ),
            unique=True,
            nullable=False
        ),
        sa.Column(
            'secret',
            sa.VARCHAR(
                length=225,
            ),
            nullable=False
        ),
        sa.Column(
            'name',
            sa.VARCHAR(
                length=100,
            ),
            nullable=False
        ),
        sa.Column(
            'bucket_name',
            sa.VARCHAR(
                length=100,
            ),
            nullable=False
        ),
        sa.Column(
            'bucket_key_id',
            sa.VARCHAR(
                length=250,
            ),
            nullable=False
        ),
        sa.Column(
            'bucket_secret_key',
            sa.VARCHAR(
                length=250,
            ),
            nullable=False
        ),
        sa.Column(
            'bucket_region',
            sa.VARCHAR(
                length=20,
            ),
            nullable=False
        ),
        *date_fields(),
        sa.PrimaryKeyConstraint('id')
    )


def upgrade():
    create_table_apps()


def downgrade():
    drop_table(TABLE_NAME)
