from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
# Original DATABASE_URL
# DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://username:password@localhost/databasename?charset=utf8mb4&ssl_disabled=true")
# DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin:admin@db/taskscheduler?charset=utf8mb4")

# DATABASE_URL = (
#     f"mysql+pymysql://{os.getenv('MARIADB_INITDB_USERNAME')}:{os.getenv('MARIADB_INITDB_PASSWORD')}"
#     f"@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
#     "?charset=utf8mb4&ssl_disabled=true"
# )
# print(DATABASE_URL)

DATABASE_URL = os.getenv("MARIADB_URI")
# print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
