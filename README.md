# TaskScheduler
Task scheduler in python that interacts with a SQL database. The service allow users to schedule tasks to 
be executed at a specified time and provide functionality to retrieve scheduled tasks. Packaged the 
implemented task scheduler in a container.

## Directory Structure

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

### File Descriptions
- `Dockerfile`: Contains instructions for building the Docker image for our application.
- `README.md`: Provides a detailed explanation of the project, including how to build and deploy the application, 
prerequisites, and how to run CRUD operations using the deployed resources.
- `alembic` and `alembic.ini`: Alembic for database migrations, include these files and directories for managing database schema changes.
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
docker build -t task-scheduler .
```

- Run the Docker container using the following command:
```
(taskscheduler-py3.11) (base) TeAmP0is0N@laas3-host:~/TaskScheduler$ docker compose up
[+] Running 2/0
 ✔ Container taskscheduler_db   Created                                                                                                                                                                           0.0s 
 ✔ Container taskscheduler_app  Created                                                                                                                                                                           0.0s 
Attaching to taskscheduler_app, taskscheduler_db
taskscheduler_db   | mariadb 07:02:47.44 INFO  ==> 
taskscheduler_db   | mariadb 07:02:47.44 INFO  ==> Welcome to the Bitnami mariadb container
taskscheduler_db   | mariadb 07:02:47.44 INFO  ==> Subscribe to project updates by watching https://github.com/bitnami/containers
taskscheduler_db   | mariadb 07:02:47.45 INFO  ==> Submit issues and feature requests at https://github.com/bitnami/containers/issues
taskscheduler_db   | mariadb 07:02:47.45 INFO  ==> 
taskscheduler_db   | mariadb 07:02:47.45 INFO  ==> ** Starting MariaDB setup **
taskscheduler_db   | mariadb 07:02:47.49 INFO  ==> Validating settings in MYSQL_*/MARIADB_* env vars
taskscheduler_db   | mariadb 07:02:47.49 INFO  ==> Initializing mariadb database
taskscheduler_db   | mariadb 07:02:47.51 INFO  ==> Updating 'my.cnf' with custom configuration
taskscheduler_db   | mariadb 07:02:47.52 INFO  ==> Setting user option
taskscheduler_db   | mariadb 07:02:47.53 INFO  ==> Setting slow_query_log option
taskscheduler_db   | mariadb 07:02:47.54 INFO  ==> Setting long_query_time option
taskscheduler_db   | mariadb 07:02:47.55 INFO  ==> Using persisted data
taskscheduler_db   | /opt/bitnami/mariadb/bin/mysql: Deprecated program name. It will be removed in a future release, use '/opt/bitnami/mariadb/bin/mariadb' instead
taskscheduler_db   | /opt/bitnami/mariadb/bin/mysql: Deprecated program name. It will be removed in a future release, use '/opt/bitnami/mariadb/bin/mariadb' instead
taskscheduler_db   | /opt/bitnami/mariadb/bin/mysql: Deprecated program name. It will be removed in a future release, use '/opt/bitnami/mariadb/bin/mariadb' instead
taskscheduler_db   | mariadb 07:02:47.60 INFO  ==> Running mysql_upgrade
taskscheduler_db   | mariadb 07:02:47.60 INFO  ==> Starting mariadb in background
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] Starting MariaDB 11.2.3-MariaDB source revision 79580f4f96fc2547711f674eb8dd514abd312b4a as process 65
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Compressed tables use zlib 1.2.13
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Using transactional memory
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Number of transaction pools: 1
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Using crc32 + pclmulqdq instructions
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] mysqld: O_TMPFILE is not supported on /opt/bitnami/mariadb/tmp (disabling future attempts)
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Using Linux native AIO
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Initializing buffer pool, total size = 128.000MiB, chunk size = 2.000MiB
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Completed initialization of buffer pool
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: File system buffers for log disabled (block size=512 bytes)
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: End of log at LSN=61545
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Opened 3 undo tablespaces
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: 128 rollback segments in 3 undo tablespaces are active.
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Removed temporary tablespace data file: "./ibtmp1"
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Setting file './ibtmp1' size to 12.000MiB. Physically writing the file full; Please wait ...
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: File './ibtmp1' size is now 12.000MiB.
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: log sequence number 61545; transaction id 43
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] Plugin 'FEEDBACK' is disabled.
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] Plugin 'wsrep-provider' is disabled.
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Loading buffer pool(s) from /bitnami/mariadb/data/ib_buffer_pool
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] Recovering after a crash using tc.log
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] Starting table crash recovery...
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] Crash table recovery finished.
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] Server socket created on IP: '127.0.0.1'.
taskscheduler_db   | 2024-03-12  7:02:47 0 [Warning] 'proxies_priv' entry '@% root@e38d78bd5050' ignored in --skip-name-resolve mode.
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] mysqld: Event Scheduler: Loaded 0 events
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] /opt/bitnami/mariadb/sbin/mysqld: ready for connections.
taskscheduler_db   | Version: '11.2.3-MariaDB'  socket: '/opt/bitnami/mariadb/tmp/mysql.sock'  port: 3306  Source distribution
taskscheduler_db   | 2024-03-12  7:02:47 0 [Note] InnoDB: Buffer pool(s) load completed at 240312  7:02:47
taskscheduler_app  | /usr/local/lib/python3.11/site-packages/pydantic/_internal/_config.py:322: UserWarning: Valid config keys have changed in V2:
taskscheduler_app  | * 'orm_mode' has been renamed to 'from_attributes'
taskscheduler_app  |   warnings.warn(message, UserWarning)
taskscheduler_app  | 2024-03-12 07:02:49,056 - INFO - Scheduler started
taskscheduler_app  | INFO:     Started server process [1]
taskscheduler_app  | INFO:     Waiting for application startup.
taskscheduler_app  | 2024-03-12 07:02:49,074 - INFO - Starting scheduler and loading tasks...
taskscheduler_app  | 2024-03-12 07:02:49,074 - INFO - Scheduler started
taskscheduler_app  | 2024-03-12 07:02:49,079 - ERROR - Error during scheduler startup: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on 'db' ([Errno 111] Connection refused)")
taskscheduler_app  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
taskscheduler_app  | INFO:     Application startup complete.
taskscheduler_app  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
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
    [{"name":"Second Updated Task","scheduled_time":"2024-04-20T10:00:00","recurrence":"weekly","id":1},{"name":"Finish reading 'Atomic Habits'","scheduled_time":"2024-05-01T10:00:00","recurrence":"once","id":2},{"name":"Begin learning Spanish on Duolingo","scheduled_time":"2024-09-01T09:00:00","recurrence":"daily","id":3},{"name":"Start a daily meditation practice","scheduled_time":"2024-08-01T07:00:00","recurrence":"daily","id":4},{"name":"Run a half marathon","scheduled_time":"2024-07-01T06:00:00","recurrence":"once","id":5},{"name":"Complete the Python Advanced course","scheduled_time":"2024-06-01T10:00:00","recurrence":"once","id":6},{"name":"Task After Deletion","scheduled_time":"2024-10-01T10:00:00","recurrence":"once","id":7},{"name":"Play cricket","scheduled_time":"2024-03-15T15:00:00","recurrence":"weekly","id":8}]
    ```

- Parse the task with id 2 from the database and return it in JSON format.
    - http://http://127.0.0.1:8000/api/tasks/2
    ```json
    {"name":"Finish reading 'Atomic Habits'","scheduled_time":"2024-05-01T10:00:00","recurrence":"once","id":2}
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

- Check the newly created task using the following command:
```bash
(taskscheduler-py3.11) (base) TeAmP0is0N@laas3-host:~/TaskScheduler$ docker exec -it taskscheduler_db bash
I have no name!@298f0f90c4f8:/$ mariadb -u root -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 4
Server version: 11.2.3-MariaDB Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| taskscheduler      |
| test               |
+--------------------+
6 rows in set (0.001 sec)

MariaDB [(none)]> USE taskscheduler;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [taskscheduler]> SHOW TABLES;
+-------------------------+
| Tables_in_taskscheduler |
+-------------------------+
| tasks                   |
+-------------------------+
1 row in set (0.001 sec)

MariaDB [taskscheduler]> SELECT * FROM tasks;
+----+-------------------------------------+---------------------+------------+
| id | name                                | scheduled_time      | recurrence |
+----+-------------------------------------+---------------------+------------+
|  1 | Second Updated Task                 | 2024-04-20 10:00:00 | WEEKLY     |
|  2 | Finish reading 'Atomic Habits'      | 2024-05-01 10:00:00 | ONCE       |
|  3 | Begin learning Spanish on Duolingo  | 2024-09-01 09:00:00 | DAILY      |
|  4 | Start a daily meditation practice   | 2024-08-01 07:00:00 | DAILY      |
|  5 | Run a half marathon                 | 2024-07-01 06:00:00 | ONCE       |
|  6 | Complete the Python Advanced course | 2024-06-01 10:00:00 | ONCE       |
|  7 | Task After Deletion                 | 2024-10-01 10:00:00 | ONCE       |
|  8 | Play cricket                        | 2024-03-15 15:00:00 | WEEKLY     |
|  9 | Attend coding webinar               | 2024-04-10 18:00:00 | ONCE       |
+----+-------------------------------------+---------------------+------------+
9 rows in set (0.001 sec)

MariaDB [taskscheduler]> 
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