import os
from datetime import datetime
from collections import defaultdict

from flask import Flask , render_template , url_for , request , redirect , flash
import requests
from dotenv import load_dotenv

# Loading environmenmt variables
load_dotenv()
API_KEY = os.getenv(".env", "b1b434f71785ce0e39fcc8e6c7c2a72d")

if not API_KEY:
    raise RuntimeError("API KEY not found")

# API endpoints
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("Flask-Secret" ,"change me for pord")

# Converts Kelvin to Celcius
def kelvinToCelcius(k):
    return k - 273.15

# Formats current weather into readable format
def formatCurrentWeather(data):
    '''Returns a simplified dict format for current weather card'''

    weather = {
        "city" : f"{data.get('name')} , {data.get('sys' , {}).get('country')}",
        "tempC" : round(kelvinToCelcius(data["main"]["temp"]) , 1),
        "feelsLikeC" : round(kelvinToCelcius(data["main"]["feels_like"])),
        "humidity" : data["main"]["humidity"],
        "windSpeed" : data["wind"]["speed"],
        "description" : data["weather"][0]["description"].title(),
        "icon" : data["weather"][0]["icon"],

    }

    return weather

# Aggregates forecast data
def aggregateForecast(data):
    """
    Accepts the 5-day / 3-hour forecast JSON and aggregates per-day: 
    returns list of days with date, min/max temp, weather (most frequent), icon.

    """
    byDate= defaultdict(list)
    for item in data.get("list" , []):
        dtTxt = item.get("dt_txt")
        dateStr = dtTxt.split()[0]
        byDate[dateStr].append(item)

    days = []
    for dateStr, entries in sorted(byDate.items()):
        temps = [e["main"]["temp"] for e in entries]

        tempC = [kelvinToCelcius(t) for t in temps]

        minTemp = round(min(tempC) , 1)
        maxTemp = round(max(tempC) , 1)

        freq = defaultdict(int)
        for e in entries:
            desc = e["weather"][0]["description"]
            icon = e["weather"][0]["icon"]
            freq[(desc , icon)] += 1 

        (desc , icon) , _ = max(freq.items() , key = lambda x: x[1])

        days.append({
            "date" : datetime.strptime(dateStr , "%Y-%m-%d").strftime("%a , %d %b"),
            "minTemp" : minTemp ,
            "maxTemp" : maxTemp , 
            "description" : desc.title() , 
            "icon" : icon

        })

        return days

# Homepage route
@app.route("/" , methods=["GET" , "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city" , "").strip()

        if not city:
            flash("Please enter a city name" ,"Warning")
            return redirect(url_for("index"))
        
        return redirect(url_for("forecast" , city=city))
    return render_template("index.html")

# Forecast route
@app.route("/forecast")
def forecast():
    city = request.args.get("city")
    if not city:
        flash("City not provided" , "warning")
        return redirect(url_for("index"))

    # Fetch current weather
    params= {"q" : city , "appid" : API_KEY}
    response = requests.get(BASE_WEATHER_URL , params=params , timeout = 10)

    if response.status_code != 200:
        flash(f"Could not fetch data for {city}. Please check the city name." , "danger")

        return redirect(url_for("index"))

    currentData = response.json()
    current = formatCurrentWeather(currentData)

    # Forecast (5 day / 3 hour)
    paramsF = {"q" : city , "appid" : API_KEY}
    response2 = requests.get(BASE_FORECAST_URL , params=paramsF , timeout = 10)

    days = []
    if response2.status_code == 200:
        forecastData = response2.json()
        days = aggregateForecast(forecastData)

    return render_template("forecast.html" , current = current , days= days)    


if __name__ == "__main__":
    app.run(debug=True)


