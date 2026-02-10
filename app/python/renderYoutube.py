#!/usr/bin/python

import os
import requests
from jinja2 import Template
from dotenv import load_dotenv

basedir = "/home/lustyd/repos/BoatDisplay/app"
channelHandle = "@anamcarasailing"
# Load the .env file
load_dotenv(f"{basedir}/.env")
# Retrieve the key from environment variables
googleAPIKey = os.getenv("GOOGLE_KEY")

with open(f"{basedir}/jinjaTemplates/youtube.html.jinja") as f:
    tmpl = Template(f.read())
    URL = f"https://youtube.googleapis.com/youtube/v3/channels?part=statistics&forHandle={channelHandle}&key={googleAPIKey}"
    try:
        response = requests.get(URL)
        data = response.json()
        subscriberCount1 = data['items'][0]['statistics']['subscriberCount']
        viewCount1 = data['items'][0]['statistics']['viewCount']
        videoCount1 =  data['items'][0]['statistics']['videoCount']
        print(tmpl.render(
            channelName = "Anam Cara Sailing",
            subscriberCount = subscriberCount1,
            viewCount = viewCount1,
            videoCount = videoCount1
        ))
    except Exception as e:
        print(f"Error: {e}")
