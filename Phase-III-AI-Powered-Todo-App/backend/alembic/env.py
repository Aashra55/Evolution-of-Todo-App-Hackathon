import os
import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection

from alembic import context

# Add the project's root directory and src directory to sys.path
# to allow Alembic to find your models for autogenerate.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # Points to 'backend/'
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

# ADDED IMPORTS
from backend.src.services.database import DATABASE_URL # Import your DATABASE_URL
from backend.src.models.todo import Todo # Import your models for autogenerate
from sqlmodel import SQLModel # Import SQLModel


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ADDED: Set the SQLAlchemy URL from your database.py
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import Base
# target_metadata = Base.metadata
target_metadata = SQLModel.metadata # MODIFIED: Set target_metadata to SQLModel.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is additionally
    required if you want to consult metadata DDL.  By passing in
    the metadata here, we tell the context a proper
    metadata object is being used.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario, we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}), # Corrected: use get_section with current config_ini_section
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()