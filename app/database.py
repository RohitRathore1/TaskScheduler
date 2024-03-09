from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

# Original DATABASE_URL
# DATABASE_URL = "postgresql://admin:admin@localhost/taskscheduler"

# Modify the DATABASE_URL to use 'host.docker.internal' if running on Docker Desktop
# or use the actual IP address or hostname of the PostgreSQL server if necessary
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@host.docker.internal/taskscheduler")

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
