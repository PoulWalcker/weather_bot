from pymongo import MongoClient
import os
from datetime import datetime

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)

db = client['weather_bot']
logs = db['logs']
user_settings = db['user_settings']


# Calls

def log_request(user_id, command, response):
    log_data = {
        'user_id': user_id,
        'command': command,
        'response': response,
        'timestamp': datetime.utcnow()
    }

    logs.insert_one(log_data)


def user_settings_request(user_id, city):
    try:
        user_settings.update_one(
            {'user_id': user_id},
            {'$set': {'city': city}},
            upsert=True
        )
    except Exception as e:
        print(f'Error during user_settings update: {e}')


def get_user_city(user_id):
    user_settings_data = user_settings.find_one({'user_id': user_id})

    if user_settings_data:
        return user_settings_data['city']
    else:
        return None
