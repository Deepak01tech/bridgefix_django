import requests
from django.shortcuts import render
from .models import Searchistory
from django.conf import settings

API_KEY = settings.WEATHER_API_KEY  # keep key in settings.py


def get_weather_data(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"]
        }

    except requests.exceptions.RequestException:
        return None


def index(request):
    weather_data = None
    error = None

    if request.method == "POST":
        city_name = request.POST.get("city")

        if city_name:
            weather_data = get_weather_data(city_name)

            if weather_data:
                Searchistory.objects.create(
                    city_name=city_name,
                    temperature=weather_data["temperature"],
                    humidity=weather_data["humidity"],
                    pressure=weather_data["pressure"],
                    description=weather_data["description"]
                )
            else:
                error = "City not found or API error"
        else:
            error = "Please enter a city name"

    return render(request, "index.html", {
        "weather": weather_data,
        "error": error
    })