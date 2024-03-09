from sqlalchemy.orm import Session
from fastapi import HTTPException
from .schemas import TaskCreate
from datetime import datetime
from . import models

def create_task(db: Session, task_name: str, scheduled_time: datetime, recurrence: models.RecurrenceFrequency = None) -> models.Task:
    """
    Creates a new task in the database with the specified details.

    Args:
    - db (Session): Database session for transaction management.
    - task_name (str): Name of the task to be created.
    - scheduled_time (datetime): The time when the task is scheduled to be executed.
    - recurrence (models.RecurrenceFrequency, optional): The recurrence pattern of the task. Defaults to None.

    Returns:
    - models.Task: The created task object.

    Raises:
    - Exception: If any database transaction fails, it rolls back the session and raises an exception.

    Example usage:
    ```python
    new_task = create_task(db, "Task Name", datetime.now(), models.RecurrenceFrequency.DAILY)
    ```
    """
    db_task = models.Task(name=task_name, scheduled_time=scheduled_time, recurrence=recurrence)
    db.add(db_task)
    try:
        db.commit()
        db.refresh(db_task)
    except Exception as e:
        db.rollback()
        raise e
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of tasks from the database with pagination.

    Args:
    - db (Session): Database session for fetching data.
    - skip (int): Number of records to skip (for pagination). Defaults to 0.
    - limit (int): Maximum number of records to return (for pagination). Defaults to 100.

    Returns:
    - List[models.Task]: A list of task objects.

    Example usage:
    ```python
    tasks = get_tasks(db, skip=10, limit=5)
    ```
    """
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_task_by_id(db: Session, task_id: int):
    """
    Retrieves a single task by its ID.

    Args:
    - db (Session): Database session for fetching data.
    - task_id (int): Unique identifier of the task to be retrieved.

    Returns:
    - models.Task or None: The task object if found, else None.

    Raises:
    - HTTPException: If the task with the specified ID does not exist, raises a 404 error.

    Example usage:
    ```python
    task = get_task_by_id(db, task_id=1)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    ```
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, new_name: str = None, new_scheduled_time: datetime = None, new_recurrence: models.RecurrenceFrequency = None) -> models.Task:
    """
    Updates an existing task in the database with new values provided.

    Args:
    - db (Session): Database session for transaction management.
    - task_id (int): ID of the task to be updated.
    - new_name (str, optional): New name for the task. Defaults to None.
    - new_scheduled_time (datetime, optional): New scheduled time for the task. Defaults to None.
    - new_recurrence (models.RecurrenceFrequency, optional): New recurrence frequency for the task. Defaults to None.

    Returns:
    - models.Task: The updated task object.

    Raises:
    - HTTPException: If the task with the specified ID does not exist or the update fails, it raises an appropriate HTTP error.

    Example usage:
    ```python
    updated_task = update_task(db, task_id=1, new_name="Updated Task Name")
    ```
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        # Example: raising an HTTPException for use in a FastAPI application
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    
    if new_name is not None:
        db_task.name = new_name
    if new_scheduled_time is not None:
        db_task.scheduled_time = new_scheduled_time
    if new_recurrence is not None:
        db_task.recurrence = new_recurrence
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        # Logging the exception might be beneficial here
        raise HTTPException(status_code=500, detail="Failed to update task")
    
    return db_task

def delete_task(db: Session, task_id: int):
    """
    Deletes a task by its ID from the database.

    Args:
    - db (Session): Database session for transaction management.
    - task_id (int): ID of the task to be deleted.

    Returns:
    - bool: True if the task was successfully deleted, False otherwise.

    Raises:
    - HTTPException: If the task with the specified ID does not exist.

    Example usage:
    ```python
    success = delete_task(db, task_id=1)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    ```
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
