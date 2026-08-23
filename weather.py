from flask import Flask, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

def get_db_connection():
    connect = sqlite3.connect("weather.db")
    connect.row_factory = sqlite3.Row
    return connect

def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS weather_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT,
            temperature REAL,
            humidity INTEGER,
            wind_speed REAL,
            searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

@app.route("/")
def home():
    return jsonify({
        "message": "Weather API is running",
        "example": "/weather?city=Jenin"
    })

@app.route("/weather")
def weather():

    city = request.args.get("city")

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(
        geo_url,
        params=geo_params
    )

    geo_data = geo_response.json()

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    city_name = location["name"]
    country = location.get("country")

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m"
        ]
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_data = weather_response.json()

    current = weather_data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind_speed = current["wind_speed_10m"]

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO weather_searches
        (
            city,
            country,
            temperature,
            humidity,
            wind_speed
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        city_name,
        country,
        temperature,
        humidity,
        wind_speed
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "city": city_name,
        "country": country,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed
    })

@app.route("/history")
def history():

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT *
        FROM weather_searches
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    result = []

    for row in rows:
        result.append(dict(row))

    return jsonify(result)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)

