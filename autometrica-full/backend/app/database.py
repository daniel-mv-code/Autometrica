from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:1234@localhost:5432/autometrica_db"

    # Configuración SMTP (Gmail / otros)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "AutoMétrica"
    SMTP_FROM_EMAIL: str = ""

    # Configuración SMS (Twilio)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # Configuración Resend (Envío de correos reales)
    RESEND_API_KEY: str = ""
    RESEND_FROM: str = "AutoMétrica <onboarding@resend.dev>"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

# Configurar motor con fallback automático a SQLite si PostgreSQL no responde
try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        pass
    print("[Base de Datos] Conectado exitosamente a PostgreSQL.")
except Exception as e:
    print(f"[Base de Datos] No se pudo conectar a PostgreSQL: {e}")
    print("[Base de Datos] Activando fallback a base de datos SQLite local (autometrica_db.db)...")
    sqlite_url = "sqlite:///./autometrica_db.db"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

