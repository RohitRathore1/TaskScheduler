# TaskScheduler

Run using the following command:

```
poetry run uvicorn app.main:app --reload
```


http://127.0.0.1:8000/

http://127.0.0.1:8000/api/tasks/

http://127.0.0.1:8000/api/tasks/7

# Documentation

- [Redoc](http://127.0.0.1:8000/redoc)

# Docker 

## Run

```
docker run -d -p 8000:8000 \
-e DATABASE_URL="mysql+pymysql://admin:admin@127.0.0.1/taskscheduler?charset=utf8mb4" \
--network="host" \
task-scheduler
```


```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Play cricket",
  "scheduled_time": "2024-03-15T15:00:00",
  "recurrence": "weekly"
}'
```
