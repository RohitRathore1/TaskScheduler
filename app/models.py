from sqlalchemy import Column, Integer, String, DateTime, create_engine, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import enum
import os

Base = declarative_base()

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# print(dotenv_path)
load_dotenv(dotenv_path)

# Define an Enum for task recurrence frequencies
class RecurrenceFrequency(enum.Enum):
    ONCE = 'once'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    BIWEEKLY = 'biweekly'
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    YEARLY = 'yearly'

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)  # Specify a length for String type
    scheduled_time = Column(DateTime, nullable=False)
    recurrence = Column(Enum(RecurrenceFrequency), nullable=True)

# Original DATABASE_URL
# DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://username:password@localhost/databasename?charset=utf8mb4&ssl_disabled=true")
# DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin:admin@db/taskscheduler?charset=utf8mb4")
# DATABASE_URL = (
#     f"mysql+pymysql://{os.getenv('MARIADB_INITDB_USERNAME')}:{os.getenv('MARIADB_INITDB_PASSWORD')}"
#     f"@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
#     "?charset=utf8mb4&ssl_disabled=true"
# )

DATABASE_URL = os.getenv("MARIADB_URI")
# print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    create_tables()
