import time
import random
from contextlib import contextmanager
from datetime import datetime, timedelta
from .crud import get_task_by_id, update_task, create_task
from .database import SessionLocal
from .models import RecurrenceFrequency
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define a context manager to handle the session's lifecycle
@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_next_run(scheduled_time, recurrence):
    """
    Calculates the next scheduled time for a task based on its recurrence frequency.

    Parameters:
    - scheduled_time (datetime): The initial scheduled time of the task.
    - recurrence (RecurrenceFrequency): The recurrence frequency of the task, which determines
      how often the task recurs. The `RecurrenceFrequency` is an enumeration that includes values like
      DAILY, WEEKLY, BIWEEKLY, MONTHLY, QUARTERLY, and YEARLY.

    Returns:
    - datetime: The next scheduled time of the task. Returns None if the recurrence frequency
      is not recognized, which should not happen with well-defined enums.

    Examples:
    - If the task is scheduled for 2023-01-01 and has a DAILY recurrence, the next scheduled
      time will be 2023-01-02.
    - If the task is scheduled for 2023-01-01 and has a WEEKLY recurrence, the next scheduled
      time will be 2023-01-08.
    """
    if recurrence == RecurrenceFrequency.DAILY:
        return scheduled_time + timedelta(days=1)
    elif recurrence == RecurrenceFrequency.WEEKLY:
        return scheduled_time + timedelta(weeks=1)
    elif recurrence == RecurrenceFrequency.BIWEEKLY:
        return scheduled_time + timedelta(weeks=2)
    elif recurrence == RecurrenceFrequency.MONTHLY:
        return scheduled_time + timedelta(weeks=4)
    elif recurrence == RecurrenceFrequency.QUARTERLY:
        return scheduled_time + timedelta(weeks=13)
    elif recurrence == RecurrenceFrequency.YEARLY:
        return scheduled_time + timedelta(weeks=52)
    else:  # Default case, should not occur for well-defined enums
        return None

def execute_task(task_id: int):
    """
    Simulates the execution of a task by sleeping for a random amount of time and then
    updating the task's details to indicate it has been executed. If the task is recurrent,
    it schedules the next occurrence.

    This function is meant to simulate work being done for the task. It sleeps for a random
    duration to represent the task's execution time. After "executing" the task, it updates
    the task's name to include the execution time and handles the scheduling of the next
    occurrence if the task is recurrent.

    Parameters:
    - task_id (int): The unique identifier of the task to execute.

    The function fetches the task by its ID from the database. If the task is found, it proceeds
    to simulate execution. If the task is marked for recurrence, it calculates the next run
    time and creates a new task entry for it. If the task is not found, it logs a warning.

    Note: This function uses a context manager `get_db_session` to manage the database session
    lifecycle, ensuring the session is properly closed after use.

    Examples:
    - For a non-recurrent task, it simply updates the task's name post-execution.
    - For a recurrent task, it updates the task's name and creates a new task for the next occurrence.
    """
    with get_db_session() as db:
        task = get_task_by_id(db=db, task_id=task_id)
        if task:
            sleep_time = random.randint(1, 10)
            logger.info(f"Executing task {task.id} ('{task.name}'). Sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)

            executed_name = f"{task.name} (Executed at {datetime.now()})"
            update_task(db=db, task_id=task.id, new_name=executed_name)
            
            if task.recurrence and task.recurrence != RecurrenceFrequency.ONCE:
                next_run = calculate_next_run(task.scheduled_time, task.recurrence)
                if next_run:
                    new_task_name = f"Recurring: {task.name}"
                    create_task(db=db, task_name=new_task_name, scheduled_time=next_run, recurrence=task.recurrence)
                    logger.info(f"Scheduled next run for task {task.id} ('{task.name}') at {next_run}.")
        else:
            logger.warning(f"Task {task_id} not found.")
