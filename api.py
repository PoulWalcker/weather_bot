from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
import os
from datetime import datetime

app = FastAPI()

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['weather_bot']
logs = db['logs']

max_limit = 1000


def build_query(
        user_id: int = None,
        start_time: str = None,
        end_time: str = None
):
    query = {}

    if user_id:
        query['user_id'] = user_id

    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time)
            query['timestamp'] = {'$gte': start_dt}
        except ValueError:
            raise HTTPException(status_code=400, detail='Invalid start_time format. Use ISO format.')

    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time)
            if 'timestamp' in query:
                query['timestamp']['$lte'] = end_dt
            else:
                query['timestamp'] = {'$lte': end_dt}
        except ValueError:
            raise HTTPException(status_code=400, detail='Invalid end_time format. Use ISO format.')

    return query


# Get all logs
@app.get('/logs')
def get_logs(
        skip: int = Query(0, ge=0, description='Number of logs to skip'),
        limit: int = Query(10, ge=0, le=max_limit,description='Maximum number of logs to retrieve, max is 1000'),
        start_time: str = Query(None, description='Start time for filtering logs in ISO 8601 format (e.g., 2024-10-01T00:00:00)'),
        end_time: str = Query(None, description='End time for filtering logs in ISO 8601 format (e.g., 2024-10-31T23:59:59)')
):
    if limit == 0:
        return []
    if limit < 0:
        raise HTTPException(status_code=400, detail='Limit must be a non-negative integer.')
    if limit > max_limit:
        limit = max_limit

    query = build_query(start_time=start_time, end_time=end_time)

    logs_data = list(logs.find(query).skip(skip))
    for log in logs_data:
        log['_id'] = str(log['_id'])
        if isinstance(log['timestamp'],datetime):
            log['timestamp'] = log['timestamp'].isoformat()
    return logs_data


# Get logs for user_id
@app.get('/logs/{user_id}')
def get_logs_by_user(
        user_id: int,
        skip: int = Query(0, ge=0, description='Number of logs to skip'),
        limit: int = Query(10, ge=0, le=max_limit, description='Maximum number of logs to retrieve, max is 1000'),
        start_time: str = Query(None, description='Start time for filtering logs in ISO 8601 format (e.g., 2024-10-01T00:00:00)'),
        end_time: str = Query(None, description='End time for filtering logs in ISO 8601 format (e.g., 2024-10-31T23:59:59)')
):
    if limit < 0:
        raise HTTPException(status_code=400, detail='Limit must be a non-negative integer.')
    if limit > max_limit:
        limit = max_limit

    query = build_query(user_id, start_time, end_time)

    logs_data = list(logs.find(query).limit(limit).skip(skip))
    for log in logs_data:
        log['_id'] = str(log['_id'])
        if isinstance(log['timestamp'], datetime):
            log['timestamp'] = log['timestamp'].isoformat()
    return logs_data


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
