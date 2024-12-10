from typing import Tuple

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

from sqlalchemy.schema import Sequence, CreateSequence


def create_new_sequence(sequence_name) -> None:
    op.execute(
        CreateSequence(
            Sequence(sequence_name),
        )
    )


def date_fields() -> Tuple[
    sa.Column,
    sa.Column
]:
    return (
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            nullable=True,
            server_default=func.now(),
            onupdate=func.current_timestamp(),
        )
    )


def drop_table(table_name) -> None:
    op.drop_table(table_name)


def drop_sequence(sequence_name) -> None:
    op.execute(f'drop sequence {sequence_name}')


def drop_foreign_key(foreign_key, table_name) -> None:
    op.drop_constraint(
        foreign_key,
        table_name,
        type_='foreignkey'
    )


def drop_index(index_name, table_name) -> None:
    op.drop_index(op.f(index_name),
                  table_name=table_name)
