"""0004_create_table_user_password_tokens

Revision ID: c52af99eda94
Revises: af415cac288e
Create Date: 2024-01-16 17:55:48.210785

"""
from sqlalchemy import func
from migrations.utils import (
    op, sa, drop_foreign_key,
    drop_table
)


# revision identifiers, used by Alembic.
revision = 'c52af99eda94'
down_revision = 'af415cac288e'
branch_labels = None
depends_on = None

TABLE_NAME = 'user_password_tokens'


def create_table_user_password_recovery() -> None:
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
            unique=True,
        ),
        sa.Column(
            'user_id',
            sa.BIGINT(),
            sa.ForeignKey(
                'users.id',
                name="FK_user_password_tokens__users",
            ),
            autoincrement=False,
            nullable=False
        ),
        sa.Column('code',
                  sa.VARCHAR(length=50),
                  autoincrement=False,
                  nullable=True
                  ),
        sa.Column(
            "expire_date",
            sa.DateTime,
            nullable=False,
            server_default=func.now(),
        ),
        sa.PrimaryKeyConstraint('id')
    )


def upgrade():
    create_table_user_password_recovery()


def downgrade():
    drop_foreign_key(
        'FK_user_password_tokens__users',
        TABLE_NAME
    )
    drop_table(TABLE_NAME)
