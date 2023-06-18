import requests
import time

API_KEY = 'your_api_key'  # Replace with your OpenWeatherMap API key
LOCATION = 'your_location'  # Replace with your desired location

ALERT_A = 25  # Temperature threshold A
ALERT_A_PLUS = ALERT_A + 5  # Temperature threshold A+5
ALERT_B = 10  # Temperature threshold B
ALERT_B_MINUS = ALERT_B - 5  # Temperature threshold B-5

def get_temperature():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    return temperature

def get_forecast():
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    forecast = data['list'][0]['main']['temp']
    return forecast

def send_alert(alert_type):
    # Replace this with your preferred alert mechanism (e.g., email, SMS)
    print(f'Alert triggered: Temperature {alert_type}!')

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
                alert_triggered['high'] = True

        if temperature < ALERT_B and forecast < ALERT_B_MINUS and not alert_triggered['low']:
            alert_counter['low'] += 1
            if alert_counter['low'] > 2:
                send_alert('low')
                alert_triggered['low'] = True

        # Reset alerts counter and trigger status once per day
        if time.localtime().tm_hour == 0 and time.localtime().tm_min == 0:
            alert_counter = {'high': 0, 'low': 0}
            alert_triggered = {'high': False, 'low': False}

        time.sleep(900)  # Wait for 15 minutes (900 seconds)

monitor_temperature()
