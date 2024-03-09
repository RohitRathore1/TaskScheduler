from sqlalchemy import Column, Integer, String, DateTime, create_engine, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError
from datetime import datetime
import enum
import os

Base = declarative_base()
schema_name = "task_schema"

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
    __table_args__ = {'schema': schema_name}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    scheduled_time = Column(DateTime, nullable=False)
    # Add a column for recurrence frequency
    recurrence = Column(Enum(RecurrenceFrequency), nullable=True)
    
# Database connection settings - adjust as needed
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost/taskscheduler")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_schema(engine, schema_name):
    try:
        # Obtain a connection from the engine
        with engine.connect() as connection:
            # Begin a transaction
            with connection.begin():
                connection.execute(CreateSchema(schema_name))
    except ProgrammingError:
        # Schema already exists
        print(f"Schema '{schema_name}' already exists.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")

# Function to create tables in the database
def create_tables():
    create_schema(engine, schema_name)  # Ensure the schema exists
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    create_tables()
