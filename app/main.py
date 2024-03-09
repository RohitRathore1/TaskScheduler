from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, models, task_executor, schemas
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from app.routes.task_router import router as task_router
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task Scheduler API!", version="0.1")
scheduler = BackgroundScheduler()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def schedule_task_execution(task_id: int, run_date: datetime):
    if run_date <= datetime.now():
        logger.warning(f"Task {task_id} scheduled time is in the past. Running immediately.")
    scheduler.add_job(task_executor.execute_task, trigger=DateTrigger(run_date=run_date), args=[task_id], misfire_grace_time=15)

@app.on_event("startup")
def start_scheduler():
    logger.info("Starting scheduler and loading tasks...")
    try:
        scheduler.start()
        db = next(get_db())
        tasks = crud.get_tasks(db=db)
        for task in tasks:
            if task.scheduled_time >= datetime.now():
                schedule_task_execution(task.id, task.scheduled_time)
        db.close()
        logger.info(f"Scheduled tasks for execution: {len(tasks)}")
    except Exception as e:
        logger.error(f"Error during scheduler startup: {e}")

@app.on_event("shutdown")
def shutdown_scheduler():
    logger.info("Shutting down scheduler...")
    try:
        scheduler.shutdown()
    except Exception as e:
        logger.error(f"Error during scheduler shutdown: {e}")

app.include_router(task_router, prefix="/api", tags=["Tasks"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Task Scheduler API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
