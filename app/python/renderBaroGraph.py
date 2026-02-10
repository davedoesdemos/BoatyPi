#!/usr/bin/python

import os
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dotenv import load_dotenv

basedir = "/home/lustyd/repos/BoatDisplay/app"
filename = "baroGraph.svg"
# Load the .env file
load_dotenv(f"{basedir}/.env")
# Retrieve the key from environment variables
victronAPIKey = os.getenv("VICTRON_KEY")
victronSite = os.getenv("VICTRON_SITE")
outputFile = f"{basedir}/html/img/{filename}"
# Subtract a number hours from the current time for start time of graph
pastTime = datetime.now() - timedelta(hours=96)
# Convert to a Unix timestamp (float)
startTime = pastTime.timestamp()

#get baro graph
attributeID = "921"
attributeCodes = "tsB"
instanceID = "20"
URL = f"https://vrmapi.victronenergy.com/v2/installations/109115/widgets/Graph?attribute-ids[]={attributeID}&attributeCodes[]={attributeCodes}&instance={instanceID}&start={startTime}"
try:
    header = {"x-authorization": f"{victronAPIKey}"}
    response = requests.get(URL, headers=header)
    data = response.json()

    #sort the data
    graphData = data["records"]["data"]["921"]
    timestamps = [datetime.fromtimestamp(point[0]) for point in graphData]
    values = [point[1] for point in graphData]

    #draw the graph
    plt.figure(figsize=(7, 0.75), dpi=100)
    plt.plot (timestamps, values, linewidth=2.5)
    plt.tick_params(labelbottom=False, labelleft=True)
    plt.xticks([])
    plt.yticks(fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7, linewidth=1.2)
    plt.box(False)
    plt.savefig(outputFile)

except Exception as e:
    print(f"Error: {e}")
    print("Token may have expired")
