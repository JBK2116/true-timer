from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from backend.db import alembic_connection_url
from backend.db import Base  # Import Base from backend.models when models are prepared

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# CRITICAL: Use Base.metadata for autogenerate to work
# Base allows alembic to make migrations automatically via the current SQL ALCHEMY SCHEMA defined in db.py
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = alembic_connection_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    config.set_main_option("sqlalchemy.url", alembic_connection_url)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()