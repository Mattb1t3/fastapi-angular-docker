# backend/api_backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carga variables del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Crea el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crea la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos ORM
Base = declarative_base()
