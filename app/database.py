from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

# Original DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin:admin@localhost/taskscheduler?charset=utf8mb4&ssl_disabled=true")

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
