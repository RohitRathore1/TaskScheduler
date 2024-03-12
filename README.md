# TaskScheduler
Task scheduler in python that interacts with a SQL database. The service allow users to schedule tasks to 
be executed at a specified time and provide functionality to retrieve scheduled tasks. Packaged the 
implemented task scheduler in a container.

## Directory Structure

```table
/TaskScheduler
├── Dockerfile
├── README.md
├── alembic
│   └── <alembic files>
├── alembic.ini
├── app
│   └── <application code>
├── docker-compose.yml
├── k8s
│   ├── create-job.yaml
│   ├── db-credentials.yaml
│   └── deployment.yaml
├── mariadb-job
│   ├── Chart.lock
│   ├── Chart.yaml
│   ├── charts
│   ├── templates
│   │   └── <Helm templates>
│   └── values.yaml
├── poetry.lock
└── pyproject.toml
```

### File Descriptions
- `Dockerfile`: Contains instructions for building the Docker image for our application.
- `README.md`: Provides a detailed explanation of the project, including how to build and deploy the application, 
prerequisites, and how to run CRUD operations using the deployed resources.
- `alembic` and `alembic.ini`: Alembic for database migrations.
- `app`: Contains our application code.
- `docker-compose.yml`: Defines and runs multi-container Docker applications; useful for local development and testing.
- `k8s`: Directory containing Kubernetes YAML files for deploying our application, database, and any other required services.
    - `create-job.yaml`: Defines Kubernetes jobs for CRUD operations.
    - `db-credentials.yaml`: Stores database credentials as Kubernetes secrets.
    - `deployment.yaml`: Defines the deployment for our application and other required services.
- `mariadb-job`: Contains a Helm chart for deploying MariaDB and initializing it with required schema or data.
    - `templates`: Helm templates for defining Kubernetes resources.
    - `values.yaml`: Specifies default values for the Helm chart.
- `poetry.lock` and `pyproject.toml`: Poetry for dependency management.

## Running Locally

If running locally, ensure that you have Python 3.8 or higher installed on your machine.
Run using the following command:

```
poetry run uvicorn app.main:app --reload
```

Application will be running at the following ports:

- http://127.0.0.1:8000/

```json
{"message":"Welcome to the Task Scheduler API!"}
```

- http://127.0.0.1:8000/api/tasks/
It will parse the list of tasks from the database and return them in JSON format.

```json
[{"name":"Second Updated Task","scheduled_time":"2024-04-20T10:00:00","recurrence":"weekly","id":1},{"name":"Finish reading 'Atomic Habits'","scheduled_time":"2024-05-01T10:00:00","recurrence":"once","id":2},{"name":"Begin learning Spanish on Duolingo","scheduled_time":"2024-09-01T09:00:00","recurrence":"daily","id":3},{"name":"Start a daily meditation practice","scheduled_time":"2024-08-01T07:00:00","recurrence":"daily","id":4},{"name":"Run a half marathon","scheduled_time":"2024-07-01T06:00:00","recurrence":"once","id":5},{"name":"Complete the Python Advanced course","scheduled_time":"2024-06-01T10:00:00","recurrence":"once","id":6},{"name":"Task After Deletion","scheduled_time":"2024-10-01T10:00:00","recurrence":"once","id":7},{"name":"Play cricket","scheduled_time":"2024-03-15T15:00:00","recurrence":"weekly","id":8}]
```

- http://127.0.0.1:8000/api/tasks/2
It will parse the task with id 2 from the database and return it in JSON format.

```json
{"name":"Finish reading 'Atomic Habits'","scheduled_time":"2024-05-01T10:00:00","recurrence":"once","id":2}
```

!Note: Before running the application, ensure that the database is running and the database URL is correctly set in the environment variables.

## Documentation
After running the application locally we can access the documentation of API at the following URL:

- [Redoc](http://127.0.0.1:8000/redoc)

# Run Image Using Docker 
Make sure you have `Docker` & `docker-compose` installed on your machine.

- Clone the reository and navigate to the root directory of the project.

```
git clone git@github.com:RohitRathore1/TaskScheduler.git
```

- Build the Docker image using the following command:
```
$ docker build -t task-scheduler .
```

- Run the Docker container using the following command:
```
$ docker compose up
```

- Create a new task using the following command:
```bash
(base) TeAmP0is0N@laas3-host:~/TaskScheduler$ . /home/TeAmP0is0N/.cache/pypoetry/virtualenvs/taskscheduler-psVrb7oN-py3.11/bin/activate
(taskscheduler-py3.11) (base) TeAmP0is0N@laas3-host:~/TaskScheduler$ curl -X 'POST' \
>   'http://127.0.0.1:8000/api/tasks/' \
>   -H 'accept: application/json' \
>   -H 'Content-Type: application/json' \
>   -d '{
>   "name": "Attend coding webinar",
>   "scheduled_time": "2024-04-10T18:00:00",
>   "recurrence": "once"
> }'
{"name":"Attend coding webinar","scheduled_time":"2024-04-10T18:00:00","recurrence":"once","id":9}(taskscheduler-py3.11) (base)
```

- Access the application at the following URL:
    - http://127.0.0.1:8000/
    ```json
    {"message":"Welcome to the Task Scheduler API!"}
    ```
- Access the documentation of API at the following URL:
    - [Redoc]([http://](http://127.0.0.1:8000/redoc)

- Fetch the list of tasks from the database and return them in JSON format.
    - http://127.0.0.1:8000/api/tasks/
    ```json
    [{"name":"Attend coding webinar","scheduled_time":"2024-04-10T18:00:00","recurrence":"once","id":1},{"name":"Weekly Grocery Shopping","scheduled_time":"2024-03-20T10:00:00","recurrence":"weekly","id":2},{"name":"Monthly Subscription Renewal","scheduled_time":"2024-04-01T12:00:00","recurrence":"monthly","id":3},{"name":"Annual Health Checkup","scheduled_time":"2024-05-15T09:00:00","recurrence":"yearly","id":4},{"name":"Daily Morning Yoga","scheduled_time":"2024-03-25T07:30:00","recurrence":"daily","id":5},{"name":"Biweekly Project Meeting","scheduled_time":"2024-03-28T14:00:00","recurrence":"biweekly","id":6}]
    ```

- Parse the task with id 2 from the database and return it in JSON format.
    - http://http://127.0.0.1:8000/api/tasks/2
    ```json
    {"name":"Weekly Grocery Shopping","scheduled_time":"2024-03-20T10:00:00","recurrence":"weekly","id":2}
    ```

More tasks to add:

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Weekly Grocery Shopping",
  "scheduled_time": "2024-03-20T10:00:00",
  "recurrence": "weekly"
}'
```

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Monthly Subscription Renewal",
  "scheduled_time": "2024-04-01T12:00:00",
  "recurrence": "monthly"
}'
```

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Annual Health Checkup",
  "scheduled_time": "2024-05-15T09:00:00",
  "recurrence": "yearly"
}'
```

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Daily Morning Yoga",
  "scheduled_time": "2024-03-25T07:30:00",
  "recurrence": "daily"
}'
```

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Biweekly Project Meeting",
  "scheduled_time": "2024-03-28T14:00:00",
  "recurrence": "biweekly"
}'
```
As per your needs you can add more tasks like this. The DB will look like this:

```sql
MariaDB [taskscheduler]> SELECT * FROM tasks;
+----+------------------------------+---------------------+------------+
| id | name                         | scheduled_time      | recurrence |
+----+------------------------------+---------------------+------------+
|  1 | Attend coding webinar        | 2024-04-10 18:00:00 | ONCE       |
|  2 | Weekly Grocery Shopping      | 2024-03-20 10:00:00 | WEEKLY     |
|  3 | Monthly Subscription Renewal | 2024-04-01 12:00:00 | MONTHLY    |
|  4 | Annual Health Checkup        | 2024-05-15 09:00:00 | YEARLY     |
|  5 | Daily Morning Yoga           | 2024-03-25 07:30:00 | DAILY      |
|  6 | Biweekly Project Meeting     | 2024-03-28 14:00:00 | BIWEEKLY   |
+----+------------------------------+---------------------+------------+
6 rows in set (0.001 sec)
```

- Check the newly created task using the following command:
```bash
MariaDB [taskscheduler]> SHOW TABLES;
+-------------------------+
| Tables_in_taskscheduler |
+-------------------------+
| tasks                   |
+-------------------------+
1 row in set (0.001 sec)

MariaDB [taskscheduler]> SELECT * FROM tasks;
+----+------------------------------+---------------------+------------+
| id | name                         | scheduled_time      | recurrence |
+----+------------------------------+---------------------+------------+
|  1 | Attend coding webinar        | 2024-04-10 18:00:00 | ONCE       |
|  2 | Weekly Grocery Shopping      | 2024-03-20 10:00:00 | WEEKLY     |
|  3 | Monthly Subscription Renewal | 2024-04-01 12:00:00 | MONTHLY    |
|  4 | Annual Health Checkup        | 2024-05-15 09:00:00 | YEARLY     |
|  5 | Daily Morning Yoga           | 2024-03-25 07:30:00 | DAILY      |
|  6 | Biweekly Project Meeting     | 2024-03-28 14:00:00 | BIWEEKLY   |
+----+------------------------------+---------------------+------------+
6 rows in set (0.001 sec)
```

In the same way we can perform other CRUD operations using the API.

# Run Image Using Kubernetes

Make sure you have `kubectl` and `minikube` installed on your machine.

- Start the minikube cluster using the following command:
```bash
minikube start
```

- Deploy the application using the following command:
```bash
kubectl apply -f k8s/
```

- Check the status of the pods using the following command:
```bash
kubectl get pods
```

- Access the application using the following command:
```bash
minikube service taskscheduler-app
```

# Database Schema

The application uses a MariaDB database to manage tasks. The database schema is designed to store tasks with their 
details. Below is the documentation of the database schema, including the table structure and the relationships 
between them.

- Tables

`tasks`
This table stores the main information about tasks. Each task has an ID, a name, a scheduled time, and a recurrence pattern.

- `id (INT, auto-increment, primary key)`: Unique identifier for each task.
- `name (VARCHAR(255), not null, unique)`: The name of the task. Each task must have a unique name.
- `scheduled_time (DATETIME, not null)`: The date and time when the task is scheduled to be executed.
- `recurrence (ENUM('ONCE', 'DAILY', 'WEEKLY', 'BIWEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY'), null)`: The recurrence pattern 
of the task. This field can be null if the task is a one-time task.

- Schema Definition

```sql
CREATE TABLE IF NOT EXISTS tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  scheduled_time DATETIME NOT NULL,
  recurrence ENUM('ONCE', 'DAILY', 'WEEKLY', 'BIWEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY') NULL
);
```

- Relationships

The current schema is simple and does not have relationships between tables. However, if the application grows and more tables 
are added, relationships may be established using foreign keys to connect related data across different tables.
