from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio raíz del proyecto al PYTHONPATH
# Suponiendo que 'alembic' está en la raíz junto a 'app' y 'alembic.ini'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
database_url = os.getenv('DATABASE_URL')

# Configuración de Alembic
config = context.config
# Actualizar la URL de la base de datos en la configuración de Alembic
config.set_main_option('sqlalchemy.url', database_url)

# Importar los modelos para que Alembic pueda detectar la metadata
from app.models.competition import Competition
from app.models.user import User
from app.models.match import Match
from app.models.registration import Registration
from app.models.reservation import Reservation
from app.models.room import Room
from app.models.score import Score
from app.models.team import Team

# Importar Base desde app/database.py
from app.database import Base

# Establecer la metadata de la clase Base para autogenerar migraciones
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
