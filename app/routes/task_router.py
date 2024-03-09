from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from typing import List
from ..database import SessionLocal
from fastapi.responses import Response
from .. import crud, models, task_executor, schemas
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
scheduler = BackgroundScheduler()
scheduler.start()

def get_db():
    """
    Dependency that creates and yields a database session from a SQLAlchemy SessionLocal instance, ensuring
    that the session is closed after request processing is complete.

    Yields:
    - A SQLAlchemy SessionLocal instance that can be used to execute database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def schedule_task_execution(task_id: int, run_date: datetime):
    """
    Schedules a task for execution using APScheduler at the specified run_date. If the run_date is in the past, 
    the task is executed immediately.

    Parameters:
    - task_id (int): The unique identifier of the task to be executed.
    - run_date (datetime): The scheduled datetime for the task to be executed.

    The task is scheduled with a job in APScheduler using a DateTrigger with the specified run_date. 
    A warning is logged if the run_date is in the past.
    """
    if run_date <= datetime.now():
        logger.warning(f"Task {task_id} scheduled time is in the past. Running immediately.")
    scheduler.add_job(task_executor.execute_task, trigger=DateTrigger(run_date=run_date), args=[task_id], misfire_grace_time=15)

@router.post("/tasks/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Creates a new task based on the provided details in the request body and schedules it for execution.

    Parameters:
    - task (schemas.TaskCreate): A Pydantic model representing the task to be created, including its name, 
      scheduled_time, and optional recurrence.
    - db (Session, Depends(get_db)): A database session dependency injected by FastAPI, used for database operations.

    Returns:
    - schemas.Task: The created task, including its generated ID and other details as specified in the request.

    The task is created in the database, and if it has a scheduled time, it is also scheduled for execution using 
    the `schedule_task_execution` function.
    """
    logger.info(f"Creating new task: {task.name}")
    new_task = crud.create_task(
        db=db, 
        task_name=task.name, 
        scheduled_time=task.scheduled_time, 
        recurrence=task.recurrence
    )
    schedule_task_execution(new_task.id, new_task.scheduled_time)
    return new_task

@router.get("/tasks/", response_model=List[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a paginated list of tasks from the database.

    Parameters:
    - skip (int, optional): The number of records to skip from the start. Useful for pagination. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Useful for pagination. Defaults to 100.
    - db (Session, Depends(get_db)): A database session dependency injected by FastAPI, used for database operations.

    Returns:
    - A list of task objects, each represented by the schemas.Task Pydantic model. This list may be empty if no tasks match the pagination criteria.
    """
    logger.info("Fetching list of tasks")
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=schemas.Task)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single task by its ID.

    This endpoint will search for a task in the database using the provided task ID. If the task is found,
    it returns the task details. If the task with the specified ID does not exist, a 404 error is returned.

    Parameters:
    - task_id (int): The unique identifier of the task. This is a path parameter.
    - db (Session, auto-injected): SQLAlchemy Session dependency that is automatically injected by FastAPI's 
      dependency injection system. It represents a database session that is used to query the database.

    Returns:
    - Task: A task object containing the details of the task, including its ID, name, scheduled time, and recurrence. 
      The structure of the returned task object is defined by the `schemas.Task` Pydantic model.

    Raises:
    - HTTPException: An exception with a 404 status code is raised if no task with the provided ID is found in the database.

    Example request:
    `GET /tasks/1`

    Successful response:
    ```json
    {
        "id": 1,
        "name": "Sample Task",
        "scheduled_time": "2023-01-01T10:00:00",
        "recurrence": "daily"
    }
    ```

    Response if task not found:
    ```json
    {
        "detail": "Task not found"
    }
    ```
    """
    logger.info(f"Fetching task with ID: {task_id}")
    task = crud.get_task_by_id(db=db, task_id=task_id)
    if not task:
        logger.error(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing task based on the provided task ID and update data.

    This endpoint allows partial updates to a task's details. Fields that can be updated include the task's name, 
    scheduled time, and recurrence frequency. Any combination of these fields can be provided in the request body.

    Parameters:
    - task_id (int): The unique identifier of the task to be updated. This is a path parameter.
    - task (schemas.TaskUpdate): A Pydantic model representing the fields to update, which may include `name`, 
      `scheduled_time`, and `recurrence`.
    - db (Session, auto-injected): SQLAlchemy Session dependency that is automatically injected by FastAPI's 
      dependency injection system. It represents a database session that is used to query and update the database.

    Returns:
    - Task: The updated task object containing the latest details. The structure of the returned task object 
      is defined by the `schemas.Task` Pydantic model.

    Raises:
    - HTTPException: An exception with a 404 status code is raised if no task with the provided ID is found in the database.

    Example request:
    `PUT /tasks/1`
    ```json
    {
        "name": "Updated Task Name",
        "scheduled_time": "2023-02-01T12:00:00",
        "recurrence": "weekly"
    }
    ```

    Successful response:
    ```json
    {
        "id": 1,
        "name": "Updated Task Name",
        "scheduled_time": "2023-02-01T12:00:00",
        "recurrence": "weekly"
    }
    ```
    """
    logger.info(f"Updating task: {task_id}")
    updated_task = crud.update_task(
        db=db, 
        task_id=task_id, 
        new_name=task.name, 
        new_scheduled_time=task.scheduled_time, 
        new_recurrence=task.recurrence
    )
    if not updated_task:
        logger.error(f"Failed to update task: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Deletes an existing task based on the provided task ID.

    This endpoint removes a task from the database. If the task with the specified ID does not exist, 
    a 404 error is returned. On successful deletion, no content is returned, and the status code is set to 204.

    Parameters:
    - task_id (int): The unique identifier of the task to be deleted. This is a path parameter.
    - db (Session, auto-injected): SQLAlchemy Session dependency that is automatically injected by FastAPI's 
      dependency injection system. It represents a database session that is used to query and update the database.

    Returns:
    - Response: An empty response with a 204 status code indicating successful deletion.

    Raises:
    - HTTPException: An exception with a 404 status code is raised if no task with the provided ID is found in the database.

    Example request:
    `DELETE /tasks/1`

    Successful response:
    ```http
    HTTP/1.1 204 No Content
    ```
    """
    logger.info(f"Deleting task: {task_id}")
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        logger.error(f"Failed to delete task: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
