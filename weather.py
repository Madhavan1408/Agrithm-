import requests

API_KEY = "357cf98aa817c4ea8ce75a9f137ca7e3"

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url).json()

    weather = {
        "temperature": response["main"]["temp"],
        "humidity": response["main"]["humidity"],
        "condition": response["weather"][0]["description"]
    }

    return weather