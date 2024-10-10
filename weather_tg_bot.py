from dotenv import load_dotenv
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from database import log_request

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
BASE_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'


# Telegram Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a weather bot. Enter the /weather <city> to get info.")


async def tg_weather_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    city = ' '.join(context.args).lower().strip()

    if len(context.args) == 0:
        await update.message.reply_text("Please provide a city name, e.g., /weather Moscow")
        log_request(user_id,f'/weather {city}', 'No city provided')
        return
    if not city.isalpha():
        await update.message.reply_text('Please enter the correct city name.')
        log_request(user_id, f'/weather{city}', f'Incorrect city value: {city}')
        return

    weather_data_json, err = await fetch_weather_data(city)
    if not weather_data_json:
        await update.message.reply_text("Sorry, I couldn't get the weather information. Please try again later.")
        log_request(user_id, f'/weather {city}', f'Failed to fetch weather data. Error: {err}')
        return
    weather_data_parsed = parse_weather_data(weather_data_json)

    # Logging user request
    log_request(user_id, f'/weather {city}', weather_data_parsed)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=weather_data_parsed)


# API Calls
async def fetch_weather_data(city):
    url = f'{BASE_WEATHER_URL}?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=en'

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError:
        error_message = "Error: Could not connect to the weather service."
    except requests.exceptions.Timeout:
        error_message = "Error: Request to weather service timed out."
    except requests.exceptions.RequestException as err:
        error_message = f"An error occurred: {err}"
    print(error_message)
    return None, error_message

# General Calls


def parse_weather_data(weather_data):
    try:
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        weather_description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        return (
            f'Temperature: {temp} cels.\n'
            f'Feels like: {feels_like} cels. \n'
            f'Description: {weather_description}. \n'
            f'Humidity: {humidity}%.\n'
            f'Wind Speed: {wind_speed} m/s'
        )

    except KeyError as e:
        print(f'Missing key in response data: {e}')
        return 'Error: Could not parse weather data.'



if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    start_handler = CommandHandler('start', start)
    weather_handler = CommandHandler('weather', tg_weather_input)
    application.add_handler(start_handler)
    application.add_handler(weather_handler)

    application.run_polling()
