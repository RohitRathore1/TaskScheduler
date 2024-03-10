from sqlalchemy import Column, Integer, String, DateTime, create_engine, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
import enum
import os

Base = declarative_base()

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

# Update DATABASE_URL to use MariaDB connection details
# Adjust the URL according to your MariaDB configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin:admin@localhost/taskscheduler?charset=utf8mb4")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    create_tables()
