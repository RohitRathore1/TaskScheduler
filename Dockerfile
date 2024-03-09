# Use an official Python runtime as a parent image
FROM python:3.11-slim as requirements-stage

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the necessary files for dependency installation to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Export the dependencies to a requirements.txt file
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Start a new stage from a slim version of the Python 3.11 image
FROM python:3.11-slim

# Copy the requirements file from the previous stage
COPY --from=requirements-stage /app/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
