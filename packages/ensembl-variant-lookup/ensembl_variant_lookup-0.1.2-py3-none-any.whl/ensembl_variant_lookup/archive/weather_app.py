# weather_app_package/weather_app.py
import requests

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # Use 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        return weather_data['main']
    else:
        return None

def main():
    print("Welcome to the Python Weather App!")

    # Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
    api_key = 'YOUR_API_KEY'

    city = input("Enter the city name: ")
    weather_info = get_weather(api_key, city)

    if weather_info:
        print(f"Weather in {city}:")
        print(f"Temperature: {weather_info['temp']}°C")
        print(f"Feels Like: {weather_info['feels_like']}°C")
        print(f"Min Temperature: {weather_info['temp_min']}°C")
        print(f"Max Temperature: {weather_info['temp_max']}°C")
        print(f"Humidity: {weather_info['humidity']}%")
    else:
        print(f"Unable to fetch weather information for {city}.")

if __name__ == "__main__":
    main()
