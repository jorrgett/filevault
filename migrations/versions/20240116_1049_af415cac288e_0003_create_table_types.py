"""0003_create_table_types

Revision ID: af415cac288e
Revises: bbfb7d8a0e02
Create Date: 2024-01-16 10:49:23.859604

"""
from migrations.utils import (
    op, sa, date_fields,
    drop_table, drop_foreign_key
)


# revision identifiers, used by Alembic.
revision = 'af415cac288e'
down_revision = 'bbfb7d8a0e02'
branch_labels = None
depends_on = None

TABLE_NAME = 'types'


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
            'app_id',
            sa.BIGINT(),
            sa.ForeignKey(
                'apps.id',
                name="FK_types__apps",
                onupdate="CASCADE",
                ondelete="CASCADE"
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
            'width',
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            'height',
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            'size',
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            'file_format',
            sa.VARCHAR(
                length=25,
            ),
            nullable=False
        ),
        *date_fields(),
        sa.PrimaryKeyConstraint('id')
    )


def upgrade():
    create_table_apps()


def downgrade():
    drop_foreign_key('FK_types__apps', TABLE_NAME)
    drop_table(TABLE_NAME)
