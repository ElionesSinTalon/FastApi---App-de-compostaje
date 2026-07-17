import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


#----- Configuración de la base de datos

def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Railway puede proporcionar una URL con el esquema "postgres://"
        if database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        return database_url

    use_postgres = os.getenv("USE_POSTGRES", "").strip().lower() in {"1", "true", "yes", "on"}
    if use_postgres:
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "tu_password")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "compostaje_db")
        return (
            f"postgresql+psycopg2://"
            f"{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

    # Respaldo para pruebas locales
    return "sqlite:///./compostaje.db"


DATABASE_URL = get_database_url()


#----- Engine
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args,
)

#----- Sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()