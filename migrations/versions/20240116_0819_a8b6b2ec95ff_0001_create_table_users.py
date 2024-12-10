"""0001_create_table_users

Revision ID: a8b6b2ec95ff
Revises: 
Create Date: 2024-01-16 08:19:14.207176

"""
from migrations.utils import (
    op, sa, date_fields,
    drop_table
)

# revision identifiers, used by Alembic.
revision = 'a8b6b2ec95ff'
down_revision = None
branch_labels = None
depends_on = None

TABLE_NAME = "users"


def create_table_users() -> None:
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
            'full_name',
            sa.VARCHAR(
                length=50,
            ),
            nullable=False
        ),
        sa.Column(
            'email',
            sa.VARCHAR(
                length=50,
            ),
            nullable=False,
            unique=True
        ),
        sa.Column(
            'password',
            sa.VARCHAR(
                length=225,
            ),
            nullable=False
        ),
        *date_fields(),
        sa.PrimaryKeyConstraint('id')
    )


def upgrade():
    create_table_users()


def downgrade():
    drop_table(TABLE_NAME)
