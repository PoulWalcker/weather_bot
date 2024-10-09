import pytest
from fastapi.testclient import TestClient
from api import app
from pymongo import MongoClient
from datetime import datetime
import json
import os

client = TestClient(app)


@pytest.fixture(scope='module', autouse=True)
def setup_database():
    mongo_client = MongoClient('mongodb://localhost:27017/')
    db = mongo_client['weather_bot']
    logs = db['logs']

    # Clear data before tests
    logs.delete_many({})

    # Add mock data
    test_data_file = os.path.join(os.path.dirname(__file__), 'mock_test_data.json')
    with open(test_data_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    # Convert 'timestamp' -> datetime
    for log in test_data:
        log['timestamp'] = datetime.fromisoformat(log['timestamp'])

    logs.insert_many(test_data)

    # Jump to tests
    yield

    # Clear all data from db
    logs.delete_many({})


# Tests
def test_get_logs():
    response = client.get('/logs?skip=0&limit=0')
    assert response.status_code == 200
    print(response.json())
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0  # limit 0


def test_get_logs_with_time_filter():
    response = client.get("/logs?skip=0&limit=10&start_time=2024-10-09T14:45:25&end_time=2024-10-09T14:45:40")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for log in data:
        timestamp = datetime.fromisoformat(log['timestamp'])
        assert datetime.fromisoformat("2024-10-09T14:45:25") <= timestamp <= datetime.fromisoformat("2024-10-09T14:45:40")


def test_get_logs_by_user():
    user_id = 430450773
    response = client.get(f'/logs/{user_id}?skip=0&limit=0')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for log in data:
        assert log['user_id'] == user_id


def test_get_logs_by_user_with_time_filter():
    user_id = 430450773
    response = client.get(f"/logs/{user_id}?skip=0&limit=10&start_time=2024-10-09T14:45:25&end_time=2024-10-09T14:45:40")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for log in data:
        assert log['user_id'] == user_id
        timestamp = datetime.fromisoformat(log['timestamp'])
        assert datetime.fromisoformat("2024-10-09T14:45:25") <= timestamp <= datetime.fromisoformat("2024-10-09T14:45:40")


def test_get_logs_invalid_user():
    response = client.get("/logs/999999999")
    assert response.status_code == 200
    assert response.json() == []


def test_get_logs_invalid_time_format():
    response = client.get("/logs?start_time=invalid_time_format")
    assert response.status_code == 400
    assert "Invalid start_time format." in response.json()["detail"]


def test_limit_exceeds_max():
    response = client.get("/logs?limit=2000")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 1000


def test_negative_limit():
    response = client.get("/logs?limit=-1")
    assert response.status_code == 400
    assert "Limit must be a non-negative integer." in response.json()["detail"]
