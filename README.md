
# Weather Bot

#### This bot was created as a testing task for BobrAI.
## Description

**Weather Bot** is a Telegram app that provides weather data based on your request. It allows users to receive current weather information through a Telegram bot interface.

## Project Components

- `weather_tg_bot.py` — The code where the Telegram bot is run.
- `api.py` — Code for the REST API.
- `database` — Code to launch the MongoDB database.
- `test.py` — Tests for the application.
- `docker-compose.yml` — Configuration file for running the application in containers, both locally and remotely.

## Requirements

- **Python 3.8** or higher
- **MongoDB** installed and running locally or accessible via network
- **Docker** and **Docker Compose** (if you choose to run the application using Docker)
- **Dependencies** installed from `requirements.txt`

## Installation

### Running with Docker Compose

1. **Clone the repository**

   ```bash
   git clone https://github.com/PoulWalcker/weather_bot
   cd weather-bot
   ```
2. **Set up environment variables**

   Create a `.env` file in the root directory and specify the environment variables:

   ```env
   MONGO_URI=mongodb://localhost:27017/
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   WEATHER_API_KEY=your_openweathermap_api_key
   ```

   Replace `your_telegram_bot_token` with your actual Telegram bot token. 
   Replace `your_openweathermap_api_key` with your actual API KEY from [https://openweathermap.org/api](https://openweathermap.org/api)

3. **Run Docker Compose**

   ```bash
   docker-compose up -d
   ```

   This command will build and start the application along with the MongoDB database in Docker containers.

4. **Access the application**

   - The API will be available at `http://localhost:8000`.
   - The Telegram bot will be running, and you can interact with it through Telegram.

### Running Locally

If you prefer to run the application without Docker:

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**

   Create a `.env` file in the root directory and specify the environment variables:

   ```env
   MONGO_URI=mongodb://localhost:27017/
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   WEATHER_API_KEY=your_openweathermap_api_key
   ```

   Replace `your_telegram_bot_token` with your actual Telegram bot token. 
   Replace `your_openweathermap_api_key` with your actual API KEY from [https://openweathermap.org/api](https://openweathermap.org/api)

3. **Ensure MongoDB is running**

   Start your MongoDB database locally or ensure it is accessible at the `MONGO_URI`.

4. **Run the application**

   - **Start the API**

     ```bash
     uvicorn api:app --reload
     ```

     The API will be available at `http://localhost:8000`.

   - **Start the Telegram bot**

     ```bash
     python weather_tg_bot.py
     ```

## API Usage

### Overview

**Base URL**: `http://localhost:8000`

The API provides the following endpoints for working with logs:

### GET `/logs`

**Description**: Retrieve a list of all logs.

**Query Parameters**:

- `skip` (int, default `0`): The number of records to skip.
- `limit` (int, default `10`, max `1000`): The maximum number of records to return.
- `start_time` (string, optional): Start time for filtering logs in ISO 8601 format.
- `end_time` (string, optional): End time for filtering logs in ISO 8601 format.

**Example Requests**:

- Retrieve the first 10 logs:

  ```
  GET http://localhost:8000/logs
  ```

- Retrieve logs for a specific period:

  ```
  GET http://localhost:8000/logs?start_time=2024-10-01T00:00:00&end_time=2024-10-31T23:59:59
  ```

### GET `/logs/{user_id}`

**Description**: Retrieve logs for a specific user by `user_id`.

**Path Parameters**:

- `user_id` (int): The user's ID.

**Query Parameters**:

- Same as for `/logs`.

**Example Requests**:

- Retrieve logs for user with ID `430450773`:

  ```
  GET http://localhost:8000/logs/430450773
  ```

### Time Format

All time parameters should be in ISO 8601 format. Example: `2024-10-09T14:45:26.936000`

### Error Handling

- **400 Bad Request**: Incorrect query parameters.
- **422 Unprocessable Entity**: Validation error for query parameters.

## Testing

To run tests, follow these steps:

1. **Ensure MongoDB is running**

   Tests use the database to verify API functionality.

2. **Run tests using pytest**

   ```bash
   pytest test.py
   ```

   The output should show successful test execution like:

   ```
   ============================= test session starts =============================
   platform linux -- Python 3.9.1, pytest-6.2.1
   collected 7 items

   test.py .....                                                        [100%]

   ============================== 7 passed in 0.10s ==============================
   ```

## Project Structure

- `weather_tg_bot.py` — The code where the Telegram bot is run.
- `api.py` — Code for the REST API.
- `database` — Code to launch the MongoDB database.
- `test.py` — Tests for the application.
- `docker-compose.yml` — Configuration for Docker containers.
- `requirements.txt` — List of project dependencies.
- `README.md` — Project documentation.


## Contact

- **Email**: p.simanov.1999@gmail.com
- **GitHub**: [https://github.com/PoulWalcker/weather_bot](https://github.com/PoulWalcker/weather_bot)
