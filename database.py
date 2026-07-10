import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


#----- Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Railway puede proporcionar una URL con el esquema "postgres://"
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1
        )
else:
    # Configuración para desarrollo local
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "tu_password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "compostaje_db")

    # Si existe al menos el usuario de PostgreSQL se utiliza PostgreSQL local.
    if DB_USER:
        DATABASE_URL = (
            f"postgresql+psycopg2://"
            f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        # Respaldo para pruebas locales
        DATABASE_URL = "sqlite:///./compostaje.db"


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