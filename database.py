from pymongo import MongoClient
import os
from datetime import datetime

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)

db = client['weather_bot']
logs = db['logs']


# Calls

def log_request(user_id, command, response):
    log_data = {
        'user_id': user_id,
        'command': command,
        'response': response,
        'timestamp': datetime.utcnow()
    }

    logs.insert_one(log_data)
