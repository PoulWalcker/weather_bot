from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os


app = FastAPI()

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['weather_bot']
logs = db['logs']

max_limit = 1000

# Get all logs
@app.get('/logs')
def get_logs(skip: int = 0, limit: int = 10):
    if limit < 0:
        raise HTTPException(status_code=400, detail="Limit must be a non-negative integer.")
    if limit > max_limit:
        limit = max_limit

    logs_data = list(logs.find().limit(limit).skip(skip))
    for log in logs_data:
        log['_id'] = str(log['_id'])
        log['timestamp'] = log['timestamp'].isoformat()
    return logs_data


# Get logs for user_id
@app.get('/logs/{user_id}')
def get_logs_by_user(user_id: int, skip: int = 0, limit: int = 10):
    if limit < 0:
        raise HTTPException(status_code=400, detail="Limit must be a non-negative integer.")
    if limit > max_limit:
        limit = max_limit
    logs_data = list(logs.find({'user_id': int(user_id)}).limit(limit).skip(skip))
    for log in logs_data:
        log['_id'] = str(log['_id'])
        log['timestamp'] = log['timestamp'].isoformat()
    return logs_data


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
