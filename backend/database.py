import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import settings

<<<<<<< HEAD
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif DATABASE_URL.startswith("postgresql://") and "+psycopg2" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Support PostgreSQL (Supabase / Local) with graceful SQLite fallback
if not DATABASE_URL or DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL or "sqlite:///./krishisetu_demo.db", connect_args={"check_same_thread": False})
else:
    try:
        test_engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"connect_timeout": 3})
        # Test connection immediately
        with test_engine.connect() as conn:
            pass
        engine = test_engine
        print(f"[Krishisetu DB] Connected to PostgreSQL / Supabase successfully!")
    except Exception as e:
        print(f"[Krishisetu DB] PostgreSQL connection failed ({e}). Falling back to local SQLite.")
=======
logger = logging.getLogger("krishisetu.database")

DATABASE_URL = settings.sqlalchemy_database_url

# Support PostgreSQL as primary database, with graceful SQLite fallback if local PostgreSQL is not running
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        # Test actual connection on startup if fallback isn't disabled
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        logger.warning(f"PostgreSQL connection failed ({exc}). Falling back to local SQLite database for portable execution.")
>>>>>>> 3d189fbcd7a35f20565ff5c523577f33c19fe422
        fallback_url = "sqlite:///./krishisetu_demo.db"
        engine = create_engine(fallback_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

