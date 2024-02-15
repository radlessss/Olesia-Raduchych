import json
import requests

from flask import Flask, jsonify, request
from datetime import datetime

API_TOKEN = "olesia_hehe" 
RSA_KEY = "FVDMEW5EU3YFFBPM6CRWTQPEB"

app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv

def get_weather(location: str, date: str):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key={RSA_KEY}&date={date}&contentType=json"
    
    headers = {"X-Api-Key": RSA_KEY}
    
    response = requests.get(url, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        raise InvalidUsage(response.text, status_code=response.status_code)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/")
def home_page():
    return "<p><h2>KMA L2: python Saas.</h2></p>"

@app.route("/content/api/v1/integration/generate", methods=["POST"])
def weather_endpoint():
    json_data = request.get_json()

    requester_name = json_data.get("requester_name")
    location = json_data.get("location")
    date = json_data.get("date")

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    weather_data = get_weather(location, date)

    weather_info = {
        "temp_c": weather_data["currentConditions"]["temp"],
        "wind_kph": weather_data["currentConditions"]["windspeed"],
        "pressure_mb": weather_data["currentConditions"]["pressure"],
        "humidity": weather_data["currentConditions"]["humidity"],
        "sunset": weather_data["currentConditions"]["sunset"]
    }

    result = {
        "requester_name": requester_name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": location,
        "date": date,
        "weather": weather_info
    }

    return result

if __name__ == "__main__":
    app.run()
