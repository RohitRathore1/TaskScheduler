from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from .models import RecurrenceFrequency  # Ensure this import works as intended.

class TaskBase(BaseModel):
    """
    A base model for task data, shared properties used by models that interact with tasks.

    Attributes:
    - name (str): The name of the task. It should be a descriptive title of what the task involves.
    - scheduled_time (datetime): The time when the task is scheduled to be executed. It specifies when the task should start or be considered due.
    - recurrence (Optional[RecurrenceFrequency]): Specifies how often the task recurs. This can be daily, weekly, etc. If not specified, the task is considered non-recurring.
    """
    name: str = Field(..., description="The name of the task", example="Complete project report")
    scheduled_time: datetime = Field(..., description="The time when the task is scheduled to be executed", example="2023-01-01T12:00:00")
    recurrence: Optional[RecurrenceFrequency] = Field(None, description="How often the task recurs", example="daily")

class TaskCreate(TaskBase):
    """
    A model for creating a new task, inheriting shared properties from TaskBase with additional validation.

    Inherits:
    - TaskBase: Inherits the base properties like `name`, `scheduled_time`, and `recurrence` from the TaskBase model.

    Validators:
    - validate_scheduled_time: Ensures that the `scheduled_time` for a new task is in the future, raising a ValueError if not.
    """
    @validator('scheduled_time')
    def validate_scheduled_time(cls, v):
        """
        Validates that the scheduled time of a task is in the future.

        Args:
        - v (datetime): The scheduled time to be validated.

        Returns:
        - datetime: The validated scheduled time.

        Raises:
        - ValueError: If the scheduled time is not in the future.
        """
        if v < datetime.now():
            raise ValueError("scheduled_time must be in the future")
        return v

class TaskUpdate(BaseModel):
    """
    A model for updating an existing task, allowing partial updates.

    Attributes:
    - name (Optional[str]): Optional new name for the task. If provided, updates the task's current name.
    - scheduled_time (Optional[datetime]): Optional new scheduled time for the task. If provided, updates the task's current scheduled time.
    - recurrence (Optional[RecurrenceFrequency]): Optional new recurrence frequency for the task. If provided, updates the task's current recurrence pattern.
    """
    name: Optional[str] = Field(None, description="The new name of the task", example="Finalize project report")
    scheduled_time: Optional[datetime] = Field(None, description="The new scheduled time for the task execution", example="2023-01-02T12:00:00")
    recurrence: Optional[RecurrenceFrequency] = Field(None, description="The new recurrence frequency of the task", example="weekly")

class Task(TaskBase):
    """
    A model representing a task, including its ID, used for responses that include task data.

    Inherits:
    - TaskBase: Inherits the base properties and validation from the TaskBase model.

    Attributes:
    - id (int): The unique identifier of the task, automatically generated upon task creation.

    Configuration:
    - orm_mode (bool): Tells Pydantic to treat the SQLAlchemy models as dictionaries. This is required for data extraction from SQLAlchemy models into Pydantic models.
    """
    id: int = Field(..., description="The ID of the task")

    class Config:
        orm_mode = True
