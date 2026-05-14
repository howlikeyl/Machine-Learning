import urllib.request
import urllib.parse
import urllib.error
import json
import sys

API_KEY = "42d33af17f6b86afac7997785f262b6c"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city: str) -> dict:
    """Fetch weather data for a given city from OpenWeatherMap API."""
    params = urllib.parse.urlencode({
        "q": city,
        "appid": API_KEY,
        "units": "imperial"  # Change to "metric" for Celsius
    })
    url = f"{BASE_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("Error: Invalid API key. Please check your API key.")
        elif e.code == 404:
            print(f"Error: City '{city}' not found. Please check the city name.")
        else:
            print(f"HTTP Error {e.code}: {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: Unable to reach the weather service.\nDetails: {e.reason}")
        sys.exit(1)


def parse_weather(data: dict) -> None:
    """Parse and display weather information from API response."""
    city        = data["name"]
    country     = data["sys"]["country"]
    temp        = data["main"]["temp"]
    feels_like  = data["main"]["feels_like"]
    humidity    = data["main"]["humidity"]
    condition   = data["weather"][0]["main"]
    description = data["weather"][0]["description"].capitalize()
    wind_speed  = data["wind"]["speed"]

    print("\n" + "=" * 40)
    print(f"  Weather for {city}, {country}")
    print("=" * 40)
    print(f"  Condition   : {condition} ({description})")
    print(f"  Temperature : {temp}°F  (feels like {feels_like}°F)")
    print(f"  Humidity    : {humidity}%")
    print(f"  Wind Speed  : {wind_speed} mph")
    print("=" * 40 + "\n")


def get_city_input() -> str:
    """Prompt the user for a city name with basic validation."""
    city = input("Enter city name: ").strip()
    if not city:
        print("Error: City name cannot be empty.")
        sys.exit(1)
    if any(char.isdigit() for char in city):
        print("Error: City name should not contain numbers.")
        sys.exit(1)
    return city


def main():
    print("=== Weather Data Fetcher ===")

    # Accept city as CLI argument or prompt interactively
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:]).strip()
    else:
        city = get_city_input()

    print(f"\nFetching weather for '{city}'...")
    data = fetch_weather(city)
    parse_weather(data)


if __name__ == "__main__":
    main()
