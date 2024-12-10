import asyncio

from alembic import context
from sqlalchemy import create_engine

from app.core.config import settings
from app.core.database import Base

target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        # literal_binds=True,
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(
        settings.postgres_url.unicode_string(), future=True)

    with connectable.connect() as connection:
        do_run_migrations(connection)


run_migrations_online()
