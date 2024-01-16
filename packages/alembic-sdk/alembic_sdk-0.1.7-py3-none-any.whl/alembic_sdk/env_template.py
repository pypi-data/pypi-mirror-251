# fmt: off
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from sqlmodel import Field, SQLModel

SQLModel.metadata.clear()

### INSERT NEW MODELS below ###
def load_or_reload_modules_from_import_statements(lines="""

"""):
    import re
    lines = lines.split('\n')

    module_names = []

    # Regular expression to match import statements
    # This version excludes the imported objects and only captures the module names
    pattern = r'import\s+([a-zA-Z0-9_.]+)|from\s+([a-zA-Z0-9_.]+)\s+import'

    for line in lines:
        matches = re.findall(pattern, line)
        for match in matches:
            # Either the first group (import statement) or the second group (from ... import statement)
            module_name = match[0] if match[0] else match[1]
            if module_name:
                module_names.append(module_name)
    
    return module_names


module_names = load_or_reload_modules_from_import_statements()


if not any([module_name in sys.modules for module_name in module_names]):
    for module_name in module_names:
        if module_name not in sys.modules:
            exec(f"import {module_name}")
else:
    # remove all modules from sys.modules
    for module_name in module_names:
        if module_name in sys.modules:
            del sys.modules[module_name]
            
    import warnings

    from sqlalchemy import exc as sa_exc

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        for module_name in module_names:
            if module_name not in sys.modules:
                exec(f"import {module_name}")
        


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = SQLModel.metadata
metadata.naming_convention = convention
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata, 
            compare_type=True, 
            render_as_batch=True,
            )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
