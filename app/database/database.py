from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import metadata
from app.core.config import settings

# SQLite Database URL
DATABASE_URL = settings.DATABASE_URL

# Create Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create the database tables
def init_db():
    metadata.create_all(bind=engine)
