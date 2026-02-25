#!/usr/bin/python

import requests
from jinja2 import Template

basedir = "/home/lustyd/repos/BoatDisplay/app"
# Replace with your Cerbo's IP address
CerboIP = "192.168.1.2"
insideTemperature = 0
insideHumidity = 0
insidePressure = 0
outsideTemperature = 0
outsideHumidity = 0
outsidePressure = 0
fuelTankLevel = 0
fuelRemaining = 0
stateOfCharge = 0

URL = f"http://{CerboIP}:3000/signalk/v1/api/vessels/self/environment"
try:
    response = requests.get(URL)
    data = response.json()
    insideTemperature = f"{round(data['inside']['temperature']['value']-273.15, 1)}"
    insideHumidity = f"{round(data['inside']['relativeHumidity']['value'], 0):g}"
    insidePressure = f"{round(data['inside']['pressure']['value']/10, 0):g}"
    outsideTemperature = f"{round(data['outside']['temperature']['value']-273.15, 1)}"
    outsideHumidity = f"{round(data['outside']['relativeHumidity']['value'], 0):g}"
    outsidePressure = f"{round(data['outside']['pressure']['value']/10, 0):g}"

except Exception as e:
    print(f"Error: {e}")

URL = f"http://{CerboIP}:3000/signalk/v1/api/vessels/self/tanks/fuel"
try:
    response = requests.get(URL)
    data = response.json()
    fuelTankLevel = f"{data['20']['currentLevel']['value']}"
    fuelTankLevelpc = f"{round(data['20']['currentLevel']['value']*100, 0):g}"
    fuelRemaining = f"{round(data['20']['remaining']['value']*1000, 0):g}"

except Exception as e:
    print(f"Error: {e}")

URL = f"http://{CerboIP}:3000/signalk/v1/api/vessels/self/electrical/batteries"
try:
    response = requests.get(URL)
    data = response.json()
    stateOfCharge = F"{round(data['277']['capacity']['stateOfCharge']['value'], 1):g}"
    stateOfChargepc = F"{round(data['277']['capacity']['stateOfCharge']['value']*100, 1):g}"

except Exception as e:
    print(f"Error: {e}")


with open(f"{basedir}/jinjaTemplates/boatData.html.jinja") as f:
    tmpl = Template(f.read())
    try:
        print(tmpl.render(
            insideTemperature = insideTemperature,
            insideHumidity = insideHumidity,
            insidePressure = insidePressure,
            outsideTemperature = outsideTemperature,
            outsideHumidity = outsideHumidity,
            outsidePressure = outsidePressure,
            fuelTankLevel = fuelTankLevel,
            fuelTankLevelpc = fuelTankLevelpc,
            fuelRemaining = fuelRemaining,
            stateOfCharge = stateOfCharge,
            stateOfChargepc = stateOfChargepc
        ))
    except Exception as e:
        print(f"Error: {e}")
