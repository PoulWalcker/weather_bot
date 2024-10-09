FROM python:latest

WORKDIR /app

COPY requirements.txt .
COPY .env .
COPY api.py .
COPY database.py .
COPY weather_tg_bot.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]