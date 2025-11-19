# Smart Forecast — Weather App (Glass UI)

A modern Flask web app that fetches real-time weather and a 5-day forecast using the OpenWeatherMap API. Features a polished Glassmorphism UI (blue/purple theme)

## Features
- Current weather (temp, feels-like, humidity, wind)
- 5-day aggregated forecast
- Clean glass UI (A1 Blue/Purple)
- Responsive design
- Uses OpenWeatherMap API

## Setup

# 1. Clone the repo:

git clone https://github.com/FlappyBird1296/weather-app.git
cd weather-app

# 2. Create and edit .env from .env.example:
API_KEY=your_openweathermap_api_key

# 3. Install dependencies:
python -m pip install -r requirements.txt

# 4. Run the app:
python app.py
Open http://127.0.0.1:5000 in your browser.

## 📦 Requirements

Flask==2.2.5
python-dotenv==1.0.0
requests==2.31.0

## 🔮 Future Improvements

- Add geolocation (browser) to auto-suggest city.
- Cache API responses to avoid rate limits.  

## 👨‍💻 Author
**Manoranjan Gope**  
B.Tech CSE (AI & ML)
First year

## ⭐ Contribute
Pull requests are welcome!  
If you like this project, please ⭐ the repo.
 