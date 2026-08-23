# Weather API

A simple Flask API that allows users to search for the current weather by city name.

The application uses the Open-Meteo API to get location and weather data, stores search history in SQLite, and returns the result as JSON.

## Features

- Search weather by city name
- Get current temperature
- Get humidity
- Get wind speed
- Store search history in SQLite
- View previous searches
- JSON API responses

## Technologies

- Python
- Flask
- SQLite
- Requests
- Open-Meteo API

## Project Structure

```text
Weather/
├── weather.py
├── requirements.txt
├── .gitignore
└── weather.db
```

> `weather.db` is created automatically when the application runs.

## Installation

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

Git Bash:

```bash
source venv/Scripts/activate
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python weather.py
```

The API will run on:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Home

```http
GET /
```

Checks that the API is running.

### Search Weather

```http
GET /weather?city=Jenin
```

Example response:

```json
{
  "city": "Jenin",
  "country": "Palestine",
  "temperature": 30.5,
  "humidity": 45,
  "wind_speed": 8.2
}
```

You can replace `Jenin` with another city, for example:

```text
/weather?city=London
/weather?city=Tokyo
/weather?city=Dubai
```

### Search History

```http
GET /history
```

Returns the weather searches stored in the SQLite database.

## How It Works

```text
User enters city
      ↓
Flask receives the city
      ↓
Geocoding API gets latitude and longitude
      ↓
Weather API gets current weather
      ↓
Result is stored in SQLite
      ↓
Flask returns a JSON response
```

## Database

SQLite stores every successful weather search in the `weather_searches` table.

The table contains:

- `id`
- `city`
- `country`
- `temperature`
- `humidity`
- `wind_speed`
- `searched_at`

## Requirements

```text
Flask
requests
```
