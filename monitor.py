import requests
import time

from dotenv import dotenv_values

# Load variables from the .env file
config = dotenv_values()

# Access individual configuration variables
api_key = config['API_KEY']
location = config['LOCATION']

ALERT_A = 25  # Temperature threshold A
ALERT_A_PLUS = ALERT_A + 5  # Temperature threshold A+5
ALERT_B = 10  # Temperature threshold B
ALERT_B_MINUS = ALERT_B - 5  # Temperature threshold B-5
DELAY = 1500 # Wait for 15 minutes (900 seconds)

def get_temperature():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
    response = requests.get(url)
    data = response.json()
    print(url)
    print(data)
    temperature = data['main']['temp']
    return temperature

def get_forecast():
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=imperial'
    response = requests.get(url)
    data = response.json()
    print(data)
    forecast = data['list'][0]['main']['temp']
    return forecast

def play_alert_up():
    duration = 100
    frequency = 150
    winsound.Beep(frequency, duration)
    frequency = 200
    winsound.Beep(frequency, duration)
    frequency = 250
    winsound.Beep(frequency, duration)
    frequency = 300
    winsound.Beep(frequency, duration)

def play_alert_down():
    duration = 100
    frequency = 300
    winsound.Beep(frequency, duration)
    frequency = 250
    winsound.Beep(frequency, duration)
    frequency = 200
    winsound.Beep(frequency, duration)
    frequency = 150
    winsound.Beep(frequency, duration)

def monitor_temperature():
    alert_triggered = {'high': False, 'low': False}
    alert_counter = {'high': 0, 'low': 0}

    while True:
        temperature = get_temperature()
        forecast = get_forecast()

        if temperature > ALERT_A and forecast > ALERT_A_PLUS and not alert_triggered['high']:
            alert_counter['high'] += 1
            if alert_counter['high'] > 2:
                send_alert('high')
                play_alert_up()

        if temperature < ALERT_B and forecast < ALERT_B_MINUS and not alert_triggered['low']:
            alert_counter['low'] += 1
            if alert_counter['low'] > 2:
                play_alert_down()
                alert_triggered['low'] = True

        # Reset alerts counter and trigger status once per day
        if time.localtime().tm_hour == 0 and time.localtime().tm_min == 0:
            alert_counter = {'high': 0, 'low': 0}
            alert_triggered = {'high': False, 'low': False}

        time.sleep(DELAY)

monitor_temperature()
