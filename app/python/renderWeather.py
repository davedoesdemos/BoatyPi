#!/usr/bin/python

import os
import requests
from datetime import datetime
from jinja2 import Template
from dotenv import load_dotenv

basedir = "/home/lustyd/repos/BoatDisplay/app"
longitude = ""
latitude = ""
CerboIP = "192.168.1.2"
# Load the .env file
load_dotenv(f"{basedir}/.env")
# Retrieve the key from environment variables
weatherAPIKEY = os.getenv("WEATHER_KEY")

def get_moon_phase_name(phase_age: float) -> str:
    """Determines the name of the lunar phase based on the age of the moon."""
    PHASES_THRESHOLDS = [
        (1.0, "newmoon"),
        (7.0, "waxingcrescent"),
        (8.5, "firstquarter"),
        (14.0, "waxinggibbous"),
        (15.5, "fullmoon"),
        (22.0, "waninggibbous"),
        (23.5, "lastquarter"),
        (29.0, "waningcrescent"),
    ]

    for threshold, phase_name in PHASES_THRESHOLDS:
        if phase_age <= threshold:
            return phase_name  
    return "newmoon"

URL = f"http://{CerboIP}:3000/signalk/v1/api/vessels/self/navigation/position/values/n2k-on-ve.can-socket.11"
try:
    response = requests.get(URL)
    data = response.json()
    longitude = data['value']['longitude']
    latitude = data['value']['latitude']

except Exception as e:
    print(f"Error: {e}")

with open(f"{basedir}/jinjaTemplates/weather.html.jinja") as f:
    tmpl = Template(f.read())
    URL2 = f"https://api.openweathermap.org/data/3.0/onecall?exclude=minutely,hourly&lat={latitude}&lon={longitude}&units=metric&appid={weatherAPIKEY}"
    URL3 = f"http://api.openweathermap.org/geo/1.0/reverse?&lat={latitude}&lon={longitude}&appid={weatherAPIKEY}"
    try:
        response2 = requests.get(URL2)
        response3 = requests.get(URL3)
        data = response2.json()
        location = response3.json()
        city = location[0]["name"]
        currentDate = datetime.fromtimestamp(data["current"]["dt"]).strftime("%A, %-d %B %Y")
        sunrise = datetime.fromtimestamp(data["current"]["sunrise"]).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["current"]["sunset"]).strftime("%H:%M")
        moonPhase = get_moon_phase_name(data["daily"][0]["moon_phase"])
        for day in data["daily"]:
            day["dt"] = datetime.fromtimestamp(day["dt"]).strftime('%a')
            day["temp"]["max"] = f"{round(day["temp"]["max"]):g}"
            day["temp"]["min"] = f"{round(day["temp"]["min"]):g}"
        data["current"]["temp"] = f"{round(data["current"]["temp"], 0):g}"
        data["current"]["feels_like"] = f"{round(data["current"]["feels_like"], 0):g}"
        print(tmpl.render(
            city = city,
            currentDate = currentDate,
            sunrise = sunrise,
            sunset = sunset,
            moonPhase = moonPhase,
            weather_data = data
        ))
    except Exception as e:
        print(f"Error: {e}")
